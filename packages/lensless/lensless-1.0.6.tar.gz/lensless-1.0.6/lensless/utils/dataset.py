# #############################################################################
# dataset.py
# =================
# Authors :
# Yohann PERRON [yohann.perron@gmail.com]
# Eric BEZZAM [ebezzam@gmail.com]
# #############################################################################

import numpy as np
import glob
import os
import torch
from abc import abstractmethod
from torch.utils.data import Dataset
from torchvision import transforms
from lensless.utils.simulation import FarFieldSimulator
from lensless.utils.io import load_image, load_psf
from lensless.utils.image import resize
import re
from lensless.hardware.utils import capture
from lensless.hardware.utils import display
from lensless.hardware.slm import set_programmable_mask, adafruit_sub2full


def convert(text):
    return int(text) if text.isdigit() else text.lower()


def alphanum_key(key):
    return [convert(c) for c in re.split("([0-9]+)", key)]


def natural_sort(arr):
    return sorted(arr, key=alphanum_key)


class DualDataset(Dataset):
    """
    Abstract class for defining a dataset of paired lensed and lensless images.
    """

    def __init__(
        self,
        indices=None,
        # psf_path=None,
        background=None,
        # background_pix=(0, 15),
        downsample=1,
        flip=False,
        flip_ud=False,
        flip_lr=False,
        transform_lensless=None,
        transform_lensed=None,
        input_snr=None,
        **kwargs,
    ):
        """
        Dataset consisting of lensless and corresponding lensed image.

        Parameters
        ----------
        indices : range or int or None
            Indices of the images to use in the dataset (if integer, it should be interpreted as range(indices)), by default None.
        psf_path : str
            Path to the PSF of the imaging system, by default None.
        background : :py:class:`~torch.Tensor` or None, optional
            If not ``None``, background is removed from lensless images, by default ``None``. If PSF is provided, background is estimated from the PSF.
        background_pix : tuple, optional
            Pixels to use for background estimation, by default (0, 15).
        downsample : int, optional
            Downsample factor of the lensless images, by default 1.
        flip : bool, optional
            If ``True``, lensless images are flipped, by default ``False``.
        transform_lensless : PyTorch Transform or None, optional
            Transform to apply to the lensless images, by default ``None``. Note that this transform is applied on HWC images (different from torchvision).
        transform_lensed : PyTorch Transform or None, optional
            Transform to apply to the lensed images, by default ``None``. Note that this transform is applied on HWC images (different from torchvision).
        input_snr : float, optional
            If not ``None``, Poisson noise is added to the lensless images to match the given SNR.
        """
        if isinstance(indices, int):
            indices = range(indices)
        self.indices = indices
        self.background = background
        self.input_snr = input_snr
        self.downsample = downsample
        self.flip = flip
        self.flip_ud = flip_ud
        self.flip_lr = flip_lr
        self.transform_lensless = transform_lensless
        self.transform_lensed = transform_lensed

        # self.psf = None
        # if psf_path is not None:
        #     psf, background = load_psf(
        #         psf_path,
        #         downsample=downsample,
        #         return_float=True,
        #         return_bg=True,
        #         bg_pix=background_pix,
        #     )
        #     if self.background is None:
        #         self.background = background
        #     self.psf = torch.from_numpy(psf)
        #     if self.transform_lensless is not None:
        #         self.psf = self.transform_lensless(self.psf)

    @abstractmethod
    def __len__(self):
        """
        Abstract method to get the length of the dataset. It should take into account the indices parameter.
        """
        raise NotImplementedError

    @abstractmethod
    def _get_images_pair(self, idx):
        """
        Abstract method to get the lensed and lensless images. Should return a pair (lensless, lensed) of numpy arrays with values in [0,1].

        Parameters
        ----------
        idx : int
            images index
        """
        raise NotImplementedError

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.item()

        if self.indices is not None:
            idx = self.indices[idx]
        lensless, lensed = self._get_images_pair(idx)

        if isinstance(lensless, np.ndarray):
            # expected case
            if self.downsample != 1.0:
                lensless = resize(lensless, factor=1 / self.downsample)
                lensed = resize(lensed, factor=1 / self.downsample)

            lensless = torch.from_numpy(lensless)
            lensed = torch.from_numpy(lensed)
        else:
            # torch tensor
            # This mean get_images_pair returned a torch tensor. This isn't recommended, if possible get_images_pair should return a numpy array
            # In this case it should also have applied the downsampling
            pass

        # If [H, W, C] -> [D, H, W, C]
        if len(lensless.shape) == 3:
            lensless = lensless.unsqueeze(0)
        if len(lensed.shape) == 3:
            lensed = lensed.unsqueeze(0)

        if self.background is not None:
            lensless = lensless - self.background

        # add noise
        if self.input_snr is not None:
            from waveprop.noise import add_shot_noise

            lensless = add_shot_noise(lensless, self.input_snr)

        # flip image x and y if needed
        if self.flip:
            lensless = torch.rot90(lensless, dims=(-3, -2), k=2)
            lensed = torch.rot90(lensed, dims=(-3, -2), k=2)
        if self.flip_ud:
            lensless = torch.flip(lensless, dims=(-4, -3))
            lensed = torch.flip(lensed, dims=(-4, -3))
        if self.flip_lr:
            lensless = torch.flip(lensless, dims=(-4, -2))
            lensed = torch.flip(lensed, dims=(-4, -2))
        if self.transform_lensless:
            lensless = self.transform_lensless(lensless)
        if self.transform_lensed:
            lensed = self.transform_lensed(lensed)

        return lensless, lensed


class SimulatedFarFieldDataset(DualDataset):
    """
    Dataset of propagated images (through simulation) from a Torch Dataset. :py:class:`lensless.utils.simulation.FarFieldSimulator` is used for simulation,
    assuming a far-field propagation and a shift-invariant system with a single point spread function (PSF).

    """

    def __init__(
        self,
        dataset,
        simulator,
        pre_transform=None,
        dataset_is_CHW=False,
        flip=False,
        vertical_shift=None,
        horizontal_shift=None,
        crop=None,
        downsample=1,
        **kwargs,
    ):
        """
        Parameters
        ----------

        dataset : :py:class:`torch.utils.data.Dataset`
            Dataset to propagate. Should output images with shape [H, W, C] unless ``dataset_is_CHW`` is ``True`` (and therefore images have the dimension ordering of [C, H, W]).
        simulator : :py:class:`lensless.utils.simulation.FarFieldSimulator`
            Simulator object used on images from ``dataset``. Waveprop simulator to use for the simulation. It is expected to have ``is_torch = True``.
        pre_transform : PyTorch Transform or None, optional
            Transform to apply to the images before simulation, by default ``None``. Note that this transform is applied on HCW images (different from torchvision).
        dataset_is_CHW : bool, optional
            If True, the input dataset is expected to output images with shape [C, H, W], by default ``False``.
        flip : bool, optional
            If True, images are flipped beffore the simulation, by default ``False``.
        """

        # we do the flipping before the simualtion
        super(SimulatedFarFieldDataset, self).__init__(flip=False, **kwargs)

        assert isinstance(dataset, Dataset)
        self.dataset = dataset
        self.n_files = len(dataset)
        self.dataset_is_CHW = dataset_is_CHW
        self._pre_transform = pre_transform
        self.flip_pre_sim = flip

        self.vertical_shift = vertical_shift
        self.horizontal_shift = horizontal_shift
        self.crop = crop.copy() if crop is not None else None
        if downsample != 1:
            if self.vertical_shift is not None:
                self.vertical_shift = int(self.vertical_shift // downsample)
            if self.horizontal_shift is not None:
                self.horizontal_shift = int(self.horizontal_shift // downsample)

            if crop is not None:
                self.crop["vertical"][0] = int(self.crop["vertical"][0] // downsample)
                self.crop["vertical"][1] = int(self.crop["vertical"][1] // downsample)
                self.crop["horizontal"][0] = int(self.crop["horizontal"][0] // downsample)
                self.crop["horizontal"][1] = int(self.crop["horizontal"][1] // downsample)

        # check simulator
        assert isinstance(simulator, FarFieldSimulator), "Simulator should be a FarFieldSimulator"
        assert simulator.is_torch, "Simulator should be a pytorch simulator"
        assert simulator.fft_shape is not None, "Simulator should have a psf"
        self.sim = simulator

    @property
    def psf(self):
        return self.sim.get_psf()

    def get_image(self, index):
        return self.dataset[index]

    def _get_images_pair(self, index):
        # load image
        img, _ = self.get_image(index)
        # convert to HWC for simulator and transform
        if self.dataset_is_CHW:
            img = img.moveaxis(-3, -1)
        if self.flip_pre_sim:
            img = torch.rot90(img, dims=(-3, -2))
        if self._pre_transform is not None:
            img = self._pre_transform(img)

        lensless, lensed = self.sim.propagate_image(img, return_object_plane=True)

        if self.vertical_shift is not None:
            lensed = torch.roll(lensed, self.vertical_shift, dims=-3)
        if self.horizontal_shift is not None:
            lensed = torch.roll(lensed, self.horizontal_shift, dims=-2)

        if lensed.shape[-1] == 1 and lensless.shape[-1] == 3:
            # copy to 3 channels
            lensed = lensed.repeat(1, 1, 3)
        assert (
            lensed.shape[-1] == lensless.shape[-1]
        ), "Lensed and lensless should have same number of channels"

        return lensless, lensed

    def __len__(self):
        if self.indices is None:
            return self.n_files
        else:
            return len([x for x in self.indices if x < self.n_files])


class MeasuredDatasetSimulatedOriginal(DualDataset):
    """
    Abstract class for defining a dataset of paired lensed and lensless images.

    Dataset consisting of lensless image captured from a screen and the corresponding image shown on the screen.
    Unlike :py:class:`lensless.utils.dataset.MeasuredDataset`, the ground-truth lensed image is simulated using a :py:class:`lensless.utils.simulation.FarFieldSimulator`
    object rather than measured with a lensed camera.

    The class assumes that the ``measured_dir`` and ``original_dir`` have file names that match.

    The method ``_get_images_pair`` must be defined.
    """

    def __init__(
        self,
        measured_dir,
        original_dir,
        simulator,
        measurement_ext="png",
        original_ext="jpg",
        downsample=1,
        background=None,
        flip=False,
        **kwargs,
    ):
        """
        Dataset consisting of lensless image captured from a screen and the corresponding image shown on screen.

        Parameters
        ----------
        """
        super(MeasuredDatasetSimulatedOriginal, self).__init__(
            downsample=1, background=background, flip=flip, **kwargs
        )
        self.pre_downsample = downsample

        self.measured_dir = measured_dir
        self.original_dir = original_dir
        assert os.path.isdir(self.measured_dir)
        assert os.path.isdir(self.original_dir)

        self.measurement_ext = measurement_ext.lower()
        self.original_ext = original_ext.lower()

        files = natural_sort(glob.glob(os.path.join(self.measured_dir, "*." + measurement_ext)))

        self.files = [os.path.basename(fn) for fn in files]

        if len(self.files) == 0:
            raise FileNotFoundError(
                f"No files found in {self.measured_dir} with extension {self.measurement_ext }"
            )

        # check that corresponding files exist
        for fn in self.files:
            original_fp = os.path.join(self.original_dir, fn[:-3] + self.original_ext)
            assert os.path.exists(original_fp), f"File {original_fp} does not exist"

        # check simulator
        assert isinstance(simulator, FarFieldSimulator), "Simulator should be a FarFieldSimulator"
        assert simulator.is_torch, "Simulator should be a pytorch simulator"
        assert simulator.fft_shape is None, "Simulator should not have a psf"
        self.sim = simulator

    def __len__(self):
        if self.indices is None:
            return len(self.files)
        else:
            return len([i for i in self.indices if i < len(self.files)])

    # def _get_images_pair(self, idx):
    #     if self.image_ext == "npy" or self.image_ext == "npz":
    #         lensless_fp = os.path.join(self.lensless_dir, self.files[idx])
    #         original_fp = os.path.join(self.original_dir, self.files[idx])
    #         lensless = np.load(lensless_fp)
    #         lensless = resize(lensless, factor=1 / self.downsample)
    #         original = np.load(original_fp[:-3] + self.original_ext)
    #     else:
    #         # more standard image formats: png, jpg, tiff, etc.
    #         lensless_fp = os.path.join(self.lensless_dir, self.files[idx])
    #         original_fp = os.path.join(self.original_dir, self.files[idx])
    #         lensless = load_image(lensless_fp, downsample=self.pre_downsample)
    #         original = load_image(
    #             original_fp[:-3] + self.original_ext, downsample=self.pre_downsample
    #         )

    #         # convert to float
    #         if lensless.dtype == np.uint8:
    #             lensless = lensless.astype(np.float32) / 255
    #             original = original.astype(np.float32) / 255
    #         else:
    #             # 16 bit
    #             lensless = lensless.astype(np.float32) / 65535
    #             original = original.astype(np.float32) / 65535

    #     # convert to torch
    #     lensless = torch.from_numpy(lensless)
    #     original = torch.from_numpy(original)

    #     # project original image to lensed space
    #     with torch.no_grad():
    #         lensed = self.sim.propagate_image()

    #     return lensless, lensed


class DigiCamCelebA(MeasuredDatasetSimulatedOriginal):
    def __init__(
        self,
        celeba_root,
        data_dir=None,
        psf_path=None,
        downsample=1,
        flip=True,
        vertical_shift=None,
        horizontal_shift=None,
        crop=None,
        simulation_config=None,
        **kwargs,
    ):
        """

        Some parameters default to work for the ``celeba_adafruit_random_2mm_20230720_10K`` dataset,
        namely: flip, vertical_shift, horizontal_shift, crop, simulation_config.

        Parameters
        ----------
        celeba_root : str
            Path to the CelebA dataset.
        data_dir : str, optional
            Path to the lensless images, by default looks inside the ``data`` folder. Can download if not available.
        psf_path : str, optional
            Path to the PSF of the imaging system, by default looks inside the ``data/psf`` folder. Can download if not available.
        downsample : int, optional
            Downsample factor of the lensless images, by default 1.
        flip : bool, optional
            If True, measurements are flipped, by default ``True``. Does not get applied to the original images.
        vertical_shift : int, optional
            Vertical shift (in pixels) of the lensed images to align.
        horizontal_shift : int, optional
            Horizontal shift (in pixels) of the lensed images to align.
        crop : dict, optional
            Dictionary of crop parameters (vertical: [start, end], horizontal: [start, end]) to select region of interest.
        """

        if vertical_shift is None:
            # default to (no downsampling) of celeba_adafruit_random_2mm_20230720_10K
            vertical_shift = -85
            horizontal_shift = -5

        if crop is None:
            crop = {"vertical": [30, 560], "horizontal": [285, 720]}
        self.crop = crop

        self.vertical_shift = vertical_shift
        self.horizontal_shift = horizontal_shift
        if downsample != 1:
            self.vertical_shift = int(self.vertical_shift // downsample)
            self.horizontal_shift = int(self.horizontal_shift // downsample)

            self.crop["vertical"][0] = int(self.crop["vertical"][0] // downsample)
            self.crop["vertical"][1] = int(self.crop["vertical"][1] // downsample)
            self.crop["horizontal"][0] = int(self.crop["horizontal"][0] // downsample)
            self.crop["horizontal"][1] = int(self.crop["horizontal"][1] // downsample)

        # download dataset if necessary
        if data_dir is None:
            data_dir = os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "data",
                "celeba_adafruit_random_2mm_20230720_10K",
            )
        if not os.path.isdir(data_dir):
            main_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")
            print("DigiCam CelebA dataset not found.")
            try:
                from torchvision.datasets.utils import download_and_extract_archive
            except ImportError:
                exit()
            msg = "Do you want to download this dataset of 10K examples (12.2GB)?"

            # default to yes if no input is given
            valid = input("%s (Y/n) " % msg).lower() != "n"
            if valid:
                url = "https://drive.switch.ch/index.php/s/9NNGCJs3DoBDGlY/download"
                filename = "celeba_adafruit_random_2mm_20230720_10K.zip"
                download_and_extract_archive(url, main_dir, filename=filename, remove_finished=True)

        # download PSF if necessary
        if psf_path is None:
            psf_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "data",
                "psf",
                "adafruit_random_2mm_20231907.png",
            )
        if not os.path.exists(psf_path):
            try:
                from torchvision.datasets.utils import download_url
            except ImportError:
                exit()
            msg = "Do you want to download the PSF (38.8MB)?"

            # default to yes if no input is given
            valid = input("%s (Y/n) " % msg).lower() != "n"
            output_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "psf")
            if valid:
                url = "https://drive.switch.ch/index.php/s/kfN5vOqvVkNyHmc/download"
                filename = "adafruit_random_2mm_20231907.png"
                download_url(url, output_path, filename=filename)

        # load PSF
        self.flip_measurement = flip
        psf, background = load_psf(
            psf_path,
            downsample=downsample * 4,  # PSF is 4x the resolution of the images
            return_float=True,
            return_bg=True,
            flip=flip,
            bg_pix=(0, 15),
        )
        self.psf = torch.from_numpy(psf)

        # create simulator
        simulation_config["output_dim"] = tuple(self.psf.shape[-3:-1])
        simulator = FarFieldSimulator(
            is_torch=True,
            **simulation_config,
        )

        super().__init__(
            measured_dir=data_dir,
            original_dir=os.path.join(celeba_root, "celeba", "img_align_celeba"),
            simulator=simulator,
            measurement_ext="png",
            original_ext="jpg",
            downsample=downsample,
            background=background,
            flip=False,  # will do flipping only on measurement
            **kwargs,
        )

    def _get_images_pair(self, idx):

        # more standard image formats: png, jpg, tiff, etc.
        lensless_fp = os.path.join(self.measured_dir, self.files[idx])
        original_fp = os.path.join(self.original_dir, self.files[idx][:-3] + self.original_ext)
        lensless = load_image(
            lensless_fp, downsample=self.pre_downsample, flip=self.flip_measurement
        )
        original = load_image(original_fp[:-3] + self.original_ext)

        # convert to float
        if lensless.dtype == np.uint8:
            lensless = lensless.astype(np.float32) / 255
            original = original.astype(np.float32) / 255
        else:
            # 16 bit
            lensless = lensless.astype(np.float32) / 65535
            original = original.astype(np.float32) / 65535

        # convert to torch
        lensless = torch.from_numpy(lensless)
        original = torch.from_numpy(original)

        # project original image to lensed space
        with torch.no_grad():
            lensed = self.sim.propagate_image(original, return_object_plane=True)

        if self.vertical_shift is not None:
            lensed = torch.roll(lensed, self.vertical_shift, dims=-3)
        if self.horizontal_shift is not None:
            lensed = torch.roll(lensed, self.horizontal_shift, dims=-2)

        return lensless, lensed


class MeasuredDataset(DualDataset):
    """
    Dataset consisting of lensless and corresponding lensed image.
    It can be used with a PyTorch DataLoader to load a batch of lensless and corresponding lensed images.
    Unless the setup is perfectly calibrated, one should expect to have to use ``transform_lensed`` to adjust the alignment and rotation.
    """

    def __init__(
        self,
        root_dir,
        lensless_fn="diffuser",
        lensed_fn="lensed",
        image_ext="npy",
        **kwargs,
    ):
        """
        Dataset consisting of lensless and corresponding lensed image. Default parameters are for the
        `DiffuserCam Lensless Mirflickr Dataset (DLMD) <https://waller-lab.github.io/LenslessLearning/dataset.html>`_.

        Parameters
        ----------
        root_dir : str
            Path to the test dataset. It is expected to contain two folders: ones of lensless images and one of lensed images.
        lensless_fn : str, optional
            Name of the folder containing the lensless images, by default "diffuser".
        lensed_fn : str, optional
            Name of the folder containing the lensed images, by default "lensed".
        image_ext : str, optional
            Extension of the images, by default "npy".
        """

        super(MeasuredDataset, self).__init__(**kwargs)

        self.root_dir = root_dir
        self.lensless_dir = os.path.join(root_dir, lensless_fn)
        self.lensed_dir = os.path.join(root_dir, lensed_fn)
        assert os.path.isdir(self.lensless_dir)
        assert os.path.isdir(self.lensed_dir)

        self.image_ext = image_ext.lower()

        files = natural_sort(glob.glob(os.path.join(self.lensless_dir, "*." + image_ext)))
        self.files = [os.path.basename(fn) for fn in files]

        if len(self.files) == 0:
            raise FileNotFoundError(
                f"No files found in {self.lensless_dir} with extension {image_ext}"
            )

    def __len__(self):
        if self.indices is None:
            return len(self.files)
        else:
            return len([i for i in self.indices if i < len(self.files)])

    def _get_images_pair(self, idx):
        if self.image_ext == "npy" or self.image_ext == "npz":
            lensless_fp = os.path.join(self.lensless_dir, self.files[idx])
            lensed_fp = os.path.join(self.lensed_dir, self.files[idx])
            lensless = np.load(lensless_fp)
            lensed = np.load(lensed_fp)

        else:
            # more standard image formats: png, jpg, tiff, etc.
            lensless_fp = os.path.join(self.lensless_dir, self.files[idx])
            lensed_fp = os.path.join(self.lensed_dir, self.files[idx])
            lensless = load_image(lensless_fp)
            lensed = load_image(lensed_fp)

            # convert to float
            if lensless.dtype == np.uint8:
                lensless = lensless.astype(np.float32) / 255
                lensed = lensed.astype(np.float32) / 255
            else:
                # 16 bit
                lensless = lensless.astype(np.float32) / 65535
                lensed = lensed.astype(np.float32) / 65535

        return lensless, lensed


class DiffuserCamMirflickr(MeasuredDataset):
    """
    Helper class for DiffuserCam Mirflickr dataset.

    Note that image colors are in BGR format: https://github.com/Waller-Lab/LenslessLearning/blob/master/utils.py#L432
    """

    def __init__(
        self,
        dataset_dir,
        psf_path,
        downsample=2,
        **kwargs,
    ):

        # check psf path exist
        if not os.path.exists(psf_path):
            psf_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "data", "psf", "diffusercam_psf.tiff"
            )

            try:
                from torchvision.datasets.utils import download_url
            except ImportError:
                exit()
            msg = "Do you want to download the DiffuserCam PSF (5.9MB)?"

            # default to yes if no input is given
            valid = input("%s (Y/n) " % msg).lower() != "n"
            output_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "psf")
            if valid:
                url = "https://drive.switch.ch/index.php/s/BteiuEcONmhmDSn/download"
                filename = "diffusercam_psf.tiff"
                download_url(url, output_path, filename=filename)

        psf, background = load_psf(
            psf_path,
            downsample=downsample * 4,  # PSF is 4x the resolution of the images
            return_float=True,
            return_bg=True,
            bg_pix=(0, 15),
        )
        transform_BRG2RGB = transforms.Lambda(lambda x: x[..., [2, 1, 0]])
        self.psf = transform_BRG2RGB(torch.from_numpy(psf))
        self.allowed_idx = np.arange(2, 25001)

        assert os.path.isdir(os.path.join(dataset_dir, "diffuser_images")) and os.path.isdir(
            os.path.join(dataset_dir, "ground_truth_lensed")
        ), "Dataset should contain 'diffuser_images' and 'ground_truth_lensed' folders. It can be downloaded from https://waller-lab.github.io/LenslessLearning/dataset.html"

        super().__init__(
            root_dir=dataset_dir,
            background=background,
            downsample=downsample,
            flip=False,
            transform_lensless=transform_BRG2RGB,
            transform_lensed=transform_BRG2RGB,
            lensless_fn="diffuser_images",
            lensed_fn="ground_truth_lensed",
            image_ext="npy",
            **kwargs,
        )

    def _get_images_pair(self, idx):

        assert idx >= self.allowed_idx.min(), f"idx should be >= {self.allowed_idx.min()}"
        assert idx <= self.allowed_idx.max(), f"idx should be <= {self.allowed_idx.max()}"

        fn = f"im{idx}.npy"
        lensless_fp = os.path.join(self.lensless_dir, fn)
        lensed_fp = os.path.join(self.lensed_dir, fn)
        lensless = np.load(lensless_fp)
        lensed = np.load(lensed_fp)

        return lensless, lensed


class DiffuserCamTestDataset(MeasuredDataset):
    """
    Dataset consisting of lensless and corresponding lensed image. This is the standard dataset used for benchmarking.
    """

    def __init__(
        self,
        data_dir=None,
        n_files=None,
        downsample=2,
    ):
        """
        Dataset consisting of lensless and corresponding lensed image. Default parameters are for the test set of
        `DiffuserCam Lensless Mirflickr Dataset (DLMD) <https://waller-lab.github.io/LenslessLearning/dataset.html>`_.

        Parameters
        ----------
        data_dir : str, optional
            The path to ``DiffuserCam_Test`` dataset, by default looks inside the ``data`` folder.
        n_files : int, optional
            Number of image pairs to load in the dataset , by default use all.
        downsample : int, optional
            Downsample factor of the lensless images, by default 2. Note that the PSF has a resolution of 4x of the images.
        """

        # download dataset if necessary
        if data_dir is None:
            data_dir = os.path.join(
                os.path.dirname(__file__), "..", "..", "data", "DiffuserCam_Test"
            )
        if not os.path.isdir(data_dir):
            main_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")
            print("DiffuserCam test set not found for benchmarking.")
            try:
                from torchvision.datasets.utils import download_and_extract_archive
            except ImportError:
                exit()
            msg = "Do you want to download the dataset (3.5GB)?"

            # default to yes if no input is given
            valid = input("%s (Y/n) " % msg).lower() != "n"
            if valid:
                url = "https://drive.switch.ch/index.php/s/D3eRJ6PRljfHoH8/download"
                filename = "DiffuserCam_Test.zip"
                download_and_extract_archive(url, main_dir, filename=filename, remove_finished=True)

        psf_fp = os.path.join(data_dir, "psf.tiff")
        psf, background = load_psf(
            psf_fp,
            downsample=downsample * 4,  # PSF is 4x the resolution of the images
            return_float=True,
            return_bg=True,
            bg_pix=(0, 15),
            flip_ud=True,
            flip_lr=False,
        )

        # transform from BGR to RGB
        transform_BRG2RGB = transforms.Lambda(lambda x: x[..., [2, 1, 0]])

        self.psf = transform_BRG2RGB(torch.from_numpy(psf))

        if n_files is None:
            indices = None
        else:
            indices = range(n_files)

        super().__init__(
            root_dir=data_dir,
            indices=indices,
            background=background,
            downsample=downsample,
            flip=False,
            flip_ud=True,
            flip_lr=False,
            transform_lensless=transform_BRG2RGB,
            transform_lensed=transform_BRG2RGB,
            lensless_fn="diffuser",
            lensed_fn="lensed",
            image_ext="npy",
        )


class SimulatedDatasetTrainableMask(SimulatedFarFieldDataset):
    """
    Dataset of propagated images (through simulation) from a Torch Dataset with learnable mask.
    The `waveprop <https://github.com/ebezzam/waveprop/blob/master/waveprop/simulation.py>`_ package is used for the simulation,
    assuming a far-field propagation and a shift-invariant system with a single point spread function (PSF).
    To ensure autograd compatibility, the dataloader should have ``num_workers=0``.
    """

    def __init__(
        self,
        mask,
        dataset,
        simulator,
        **kwargs,
    ):
        """
        Parameters
        ----------

        mask : :py:class:`lensless.hardware.trainable_mask.TrainableMask`
            Mask to use for simulation. Should be a 4D tensor with shape [1, H, W, C]. Simulation of multi-depth data is not supported yet.
        dataset : :py:class:`torch.utils.data.Dataset`
            Dataset to propagate. Should output images with shape [H, W, C] unless ``dataset_is_CHW`` is ``True`` (and therefore images have the dimension ordering of [C, H, W]).
        simulator : :py:class:`lensless.utils.simulation.FarFieldSimulator`
            Simulator object used on images from ``dataset``. Waveprop simulator to use for the simulation. It is expected to have ``is_torch = True``.
        """

        self._mask = mask

        temp_psf = self._mask.get_psf()
        test_sim = FarFieldSimulator(psf=temp_psf, **simulator.params)
        assert (
            test_sim.conv_dim == simulator.conv_dim
        ).all(), "PSF shape should match simulator shape"
        assert (
            not simulator.quantize
        ), "Simulator should not perform quantization to maintain differentiability. Please set quantize=False"

        super(SimulatedDatasetTrainableMask, self).__init__(dataset, simulator, **kwargs)

    def _get_images_pair(self, index):
        # update psf
        psf = self._mask.get_psf()
        self.sim.set_point_spread_function(psf)

        # return simulated images
        return super()._get_images_pair(index)


class HITLDatasetTrainableMask(SimulatedDatasetTrainableMask):
    """
    Dataset of on-the-fly measurements and simulated ground-truth.
    """

    def __init__(
        self,
        rpi_username,
        rpi_hostname,
        celeba_root,
        display_config,
        capture_config,
        mask_center,
        **kwargs,
    ):
        self.rpi_username = rpi_username
        self.rpi_hostname = rpi_hostname
        self.celeba_root = celeba_root
        assert os.path.isdir(self.celeba_root)

        self.display_config = display_config
        self.capture_config = capture_config
        self.mask_center = mask_center

        super(HITLDatasetTrainableMask, self).__init__(**kwargs)

    def __getitem__(self, index):

        # propagate through mask in digital model
        _, lensed = super().__getitem__(index)

        ## measure lensless image
        # get image file path
        idx = self.dataset.indices[index]

        # twice nested as we do train-test split of subset of CelebA
        fn = self.dataset.dataset.dataset.filename[idx]
        fp = os.path.join(self.celeba_root, "celeba", "img_align_celeba", fn)

        # display on screen
        display(
            fp=fp,
            rpi_username=self.rpi_username,
            rpi_hostname=self.rpi_hostname,
            **self.display_config,
        )

        # set mask
        with torch.no_grad():
            subpattern = self._mask.get_vals()
            subpattern_np = subpattern.detach().cpu().numpy().copy()
            pattern = adafruit_sub2full(
                subpattern_np,
                center=self.mask_center,
            )
        set_programmable_mask(
            pattern,
            self._mask.device,
            self.rpi_username,
            self.rpi_hostname,
        )

        # take picture
        _, img = capture(
            rpi_username=self.rpi_username,
            rpi_hostname=self.rpi_hostname,
            verbose=False,
            **self.capture_config,
        )

        # -- normalize
        img = img.astype(np.float32) / img.max()

        # prep
        img = torch.from_numpy(img)
        # -- if [H, W, C] -> [D, H, W, C]
        if len(img.shape) == 3:
            img = img.unsqueeze(0)

        if self.background is not None:
            img = img - self.background

        # flip image x and y if needed
        if self.capture_config.flip:
            img = torch.rot90(img, dims=(-3, -2), k=2)

        # return simulated images (replace simulated with measured)
        return img, lensed
