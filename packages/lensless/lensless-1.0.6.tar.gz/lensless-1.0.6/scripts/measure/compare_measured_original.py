from lensless.utils.io import load_psf, load_image, save_image
from lensless import ADMM
import numpy as np
from lensless.utils.simulation import FarFieldSimulator
import torch
import matplotlib.pyplot as plt


# lensless_fp = "000001.png"
lensless_fp = "/scratch/bezzam/celeba/celeba_adafruit_random_30cm_2mm_20231004_26K/000001.png"
original_fp = "/scratch/bezzam/celeba/img_align_celeba/000001.jpg"
psf_fp = "rpi_hq_adafruit_psf_2mm/raw_data_rgb.png"
downsample = 1
flip = True
scene2mask = 0.25
mask2sensor = 0.002
object_height = 0.33
sensor = "rpi_hq"
torch_device = "cuda"
vertical_shift = -117
# vertical_shift = 0
# horizontal_shift = -80
horizontal_shift = -25

crop = {
    "vertical": [30, 560],
    "horizontal": [285, 720],
}


psf, background = load_psf(
    psf_fp,
    downsample=downsample * 4,  # PSF is 4x the resolution of the images
    return_float=True,
    return_bg=True,
    flip=flip,
    bg_pix=(0, 15),
)
psf = torch.from_numpy(psf).type(torch.float32).to(torch_device)


print(f"PSF shape : {psf.shape}")
print(f"PSF min : {psf.min()}")
print(f"PSF max : {psf.max()}")
print(f"PSF dtype : {psf.dtype}")
print(f"PSF norm : {psf.norm()}")


lensless = load_image(lensless_fp, downsample=downsample, flip=flip)
original = load_image(original_fp)


# convert to torch
lensless = torch.from_numpy(lensless)
original = torch.from_numpy(original)


simulator = FarFieldSimulator(
    is_torch=True,
    output_dim=tuple(psf.shape[-3:-1]),
    scene2mask=scene2mask,
    mask2sensor=mask2sensor,
    object_height=object_height,
    sensor=sensor,
)
lensed = simulator.propagate_image(original, return_object_plane=True)
if vertical_shift is not None:
    lensed = torch.roll(lensed, vertical_shift, dims=-3)
if horizontal_shift is not None:
    lensed = torch.roll(lensed, horizontal_shift, dims=-2)


print(f"Lensless shape : {lensless.shape}")
print(f"Lensed shape : {lensed.shape}")


recon = ADMM(psf)
recon.set_data(lensless.to(torch_device))
res = recon.apply(disp_iter=None, plot=False, n_iter=10)
res_np = res[0].cpu().numpy()
res_np = res_np / res_np.max()
save_image(res_np, f"lensless_recon.png")
lensed_np = lensed.cpu().numpy()
save_image(lensed_np, f"lensed.png")

plt.figure()
plt.imshow(lensed_np, alpha=0.4)
plt.imshow(res_np, alpha=0.7)
plt.savefig("overlay_lensed_recon.png")
