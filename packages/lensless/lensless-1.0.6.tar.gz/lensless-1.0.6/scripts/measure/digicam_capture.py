"""

Set DigiCam mask and take picture.

"""

from lensless.hardware.utils import display
import warnings
import hydra
from datetime import datetime
import numpy as np
from slm_controller import slm
from slm_controller.hardware import SLMParam, slm_devices
import matplotlib.pyplot as plt

from lensless.hardware.slm import set_programmable_mask, adafruit_sub2full
from lensless.hardware.aperture import rect_aperture, circ_aperture
from lensless.hardware.utils import set_mask_sensor_distance

import os
from lensless.utils.plot import plot_image, pixel_histogram
from lensless.utils.io import save_image
from lensless.hardware.utils import capture


@hydra.main(version_base=None, config_path="../../configs", config_name="digicam_capture")
def digicam_capture(config):

    rpi_username = config.rpi.username
    rpi_hostname = config.rpi.hostname

    """
    1) Set display image.
    """

    display_config = config.display
    if display_config is not None:
        display(rpi_username=rpi_username, rpi_hostname=rpi_hostname, **display_config)

    """
    2) Set digicam mask.
    """
    digicam_config = config.digicam
    if digicam_config is not None:
        device = digicam_config.device

        shape = slm_devices[device][SLMParam.SLM_SHAPE]
        if not slm_devices[device][SLMParam.MONOCHROME]:
            shape = (3, *shape)
        pixel_pitch = slm_devices[device][SLMParam.PIXEL_PITCH]

        # set mask to sensor distance
        if digicam_config.z is not None:
            set_mask_sensor_distance(digicam_config.z, rpi_username, rpi_hostname)

        center = np.array(digicam_config.center) * pixel_pitch

        # create random pattern
        pattern = None
        if digicam_config.pattern.endswith(".npy"):
            if digicam_config.subpattern:
                assert digicam_config.aperture is not None
                subpattern = np.load(digicam_config.pattern)
                pattern = adafruit_sub2full(subpattern, digicam_config.aperture.center)
            else:
                pattern = np.load(digicam_config.pattern)
        elif digicam_config.pattern == "random":
            rng = np.random.RandomState(config.seed)
            pattern = rng.uniform(low=digicam_config.min_val, high=1, size=shape)
            pattern = (pattern * np.iinfo(np.uint8).max).astype(np.uint8)

        elif digicam_config.pattern == "rect":
            rect_shape = digicam_config.rect_shape
            apert_dim = rect_shape[0] * pixel_pitch[0], rect_shape[1] * pixel_pitch[1]
            ap = rect_aperture(
                apert_dim=apert_dim,
                slm_shape=slm_devices[device][SLMParam.SLM_SHAPE],
                pixel_pitch=pixel_pitch,
                center=center,
            )
            pattern = ap.values
        elif digicam_config.pattern == "circ":
            ap = circ_aperture(
                radius=config.radius * pixel_pitch[0],
                slm_shape=slm_devices[device][SLMParam.SLM_SHAPE],
                pixel_pitch=pixel_pitch,
                center=center,
            )
            pattern = ap.values
        else:
            raise ValueError(f"Pattern {digicam_config.pattern} not supported")

        # apply aperture
        if digicam_config.aperture is not None and digicam_config.aperture.shape is not None:

            apert_dim = np.array(digicam_config.aperture.shape) * np.array(pixel_pitch)
            ap = rect_aperture(
                apert_dim=apert_dim,
                slm_shape=slm_devices[device][SLMParam.SLM_SHAPE],
                pixel_pitch=pixel_pitch,
                center=np.array(digicam_config.aperture.center) * pixel_pitch,
            )
            aperture = ap.values
            aperture[aperture > 0] = 1
            pattern = pattern * aperture

        # save pattern
        if not digicam_config.pattern.endswith(".npy") and config.save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pattern_fn = f"{device}_{digicam_config.pattern}_pattern_{timestamp}.npy"
            np.save(pattern_fn, pattern)
            if config.verbose:
                print(f"Saved pattern to {pattern_fn}")

        if config.verbose:
            print("Pattern shape : ", pattern.shape)
            print("Pattern dtype : ", pattern.dtype)
            print("Pattern min   : ", pattern.min())
            print("Pattern max   : ", pattern.max())

        assert pattern is not None

        if config.verbose:
            n_nonzero = np.count_nonzero(pattern)
            print(f"Nonzero pixels: {n_nonzero}")

        set_programmable_mask(pattern, device, rpi_username, rpi_hostname, verbose=config.verbose)

        # preview mask
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s = slm.create(device)
            s._show_preview(pattern)
            plt.savefig("preview.png")

    """
    3) Take picture with Raspberry Pi camera.
    """

    plot = config.plot
    if config.save:
        if config.output is not None:
            # make sure output directory exists
            os.makedirs(config.output, exist_ok=True)
            save = config.output
        else:
            save = os.getcwd()
    else:
        save = False

    fn = config.capture.raw_data_fn
    localfile, img = capture(
        fn=fn,
        rpi_username=rpi_username,
        rpi_hostname=rpi_hostname,
        verbose=config.verbose,
        output_dir=save,
        **config.capture,
    )

    # save image as viewable 8 bit
    if config.capture.nbits_out != 8:
        fp = os.path.join(save, f"{fn}_8bit.png")
        save_image(img, fp)

    # plot RGB
    if plot:
        plot_image(img, gamma=config.gamma)
        if save:
            plt.savefig(os.path.join(save, f"{fn}_plot.png"))
        pixel_histogram(img)
        if save:
            plt.savefig(os.path.join(save, f"{fn}_hist.png"))

        plt.show()

    if save:
        print(f"\nSaved plots to: {save}")


if __name__ == "__main__":
    digicam_capture()
