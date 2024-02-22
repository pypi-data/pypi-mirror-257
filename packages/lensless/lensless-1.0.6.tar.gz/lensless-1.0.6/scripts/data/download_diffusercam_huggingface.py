from datasets import load_dataset
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import torch
from lensless.utils.image import resize
from lensless.utils.io import save_image
from huggingface_hub import hf_hub_download
from lensless.utils.io import load_psf
from torchvision import transforms


def get_image_url(file_name, repo_path):
    return (
        f"https://huggingface.co/datasets/{repo_path}/resolve/main/"
        + file_name
        + "?download=true"
    )

def load_url_image(url=None,):
    r"""

    Load an image from a URL and return a torch.Tensor.

    :param str url: URL of the image file.
    :param int, tuple[int] img_size: Size of the image to return.
    :param float downsample: Factor to downsample the image on each axis.
    :param bool grayscale: Whether to convert the image to grayscale.
    :param str resize_mode: If ``img_size`` is not None, options are ``"crop"`` or ``"resize"``.
    :param str device: Device on which to load the image (gpu or cpu).
    :return: :class:`torch.Tensor` containing the image.
    """

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    x = np.array(img)
    return x



repo_id = "bezzam/DiffuserCam-Lensless-Mirflickr-Dataset"
downsample = 2

# load one example
dataset = load_dataset(repo_id, split="test")
h = dataset[0]["lensless"]
lensless_np = np.array(h)

# load PSF
# psf_url = get_image_url("psf.png", repo_id)
# # psf = load_url_image(psf_url)
# psf = psf / np.linalg.norm(psf.ravel())
# if downsample != 1:
#     psf = resize(psf, factor=1 / (downsample * 4))
# # add extra dimension to PSF
# psf = psf[np.newaxis, :]
# background subtraction
# bg = []
# bg_pix = (5, 25)
# for i in range(psf.shape[3]):
#     bg_i = np.mean(psf[:, bg_pix[0] : bg_pix[1], bg_pix[0] : bg_pix[1], i])
#     psf[:, :, :, i] -= bg_i
#     bg.append(bg_i)

# psf = np.clip(psf, a_min=0, a_max=psf.max())
# bg = np.array(bg)
# psf = torch.from_numpy(psf)

psf_fp = hf_hub_download(repo_id=repo_id, filename="psf.png", repo_type="dataset")
# psf_fp = hf_hub_download(repo_id=repo_id, filename="psf.tiff", repo_type="dataset")

psf, bg = load_psf(
    psf_fp,
    downsample=downsample * 4,  # PSF is 4x the resolution of the images
    return_float=True,
    return_bg=True,
    bg_pix=(0, 15),
)
transform_BRG2RGB = transforms.Lambda(lambda x: x[..., [2, 1, 0]])
psf = torch.from_numpy(psf)
# psf = transform_BRG2RGB(psf)



# prepare data
img = lensless_np / lensless_np.max()
if downsample != 1:
    img = resize(img, factor=1 / downsample)

img = img - bg
img = np.clip(img, a_min=0, a_max=img.max())
img = torch.from_numpy(img)
    
# perform reconstruction
from lensless import ADMM

recon = ADMM(psf, n_iter=100)
recon.set_data(img)
res = recon.apply(plot=False)

# save result
res = res.cpu().numpy()
save_image(res[0], "reconstruction_hf.png")

# ## same reconstruction with original dataset
# from lensless.utils.io import load_psf
# import torch
# from torchvision import transforms

# lensless_fp = "/scratch/bezzam/DiffuserCam_mirflickr/dataset/diffuser_images/im2.npy"
# psf_fp = "/home/bezzam/LenslessPiCam/data/psf/diffusercam_psf.tiff"
# psf, background = load_psf(
#     psf_fp,
#     downsample=downsample * 4,  # PSF is 4x the resolution of the images
#     return_float=True,
#     return_bg=True,
#     bg_pix=(0, 15),
# )
# transform_BRG2RGB = transforms.Lambda(lambda x: x[..., [2, 1, 0]])
# psf = transform_BRG2RGB(torch.from_numpy(psf))

# lensless = np.load(lensless_fp)
# if downsample != 1.0:
#     lensless = resize(lensless, factor=1 / downsample)
# lensless = torch.from_numpy(lensless)
# lensless = lensless.unsqueeze(0)
# lensless = transform_BRG2RGB(lensless)

# from lensless import ADMM
# recon = ADMM(psf, n_iter=100)
# recon.set_data(lensless)
# res = recon.apply(plot=False)

# # save result
# res = res.cpu().numpy()
# save_image(res[0], "reconstruction_original.png")


# import pudb; pudb.set_trace()