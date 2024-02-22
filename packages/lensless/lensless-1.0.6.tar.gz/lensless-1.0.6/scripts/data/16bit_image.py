import os
import glob
import numpy as np
from PIL import Image

def save_u16_to_tiff(u16in, size, tiff_filename):
    """
    Since Pillow has poor support for 16-bit TIFF, we make our own
    save function to properly save a 16-bit TIFF.
    """
    # write 16-bit TIFF image

    # PIL interprets mode 'I;16' as "uint16, little-endian"
    img_out = Image.new('I;16', size)

    if HAS_NUMPY:
        # make sure u16in little-endian, output bytes
        outpil = u16in.astype(u16in.dtype.newbyteorder("<")).tobytes()
    else:
        # little-endian u16 format
        outpil = struct.pack(
                "<%dH"%(len(u16in)),
                *u16in
                )
    img_out.frombytes(outpil)
    img_out.save(tiff_filename)


dir_diffuser = "/scratch/bezzam/DiffuserCam_mirflickr/dataset/diffuser_images"
files_diffuser = glob.glob(os.path.join(dir_diffuser, "*.npy"))

# load a single file
diffuser_np = np.load(files_diffuser[0])

# conver to 16-bit
diffuser_np = (diffuser_np * 65535).astype(np.uint16)

# import pudb; pudb.set_trace()  # XXX BREAKPOINT

# save as 16-bit image

img = Image.fromarray(diffuser_np)
img.save("diffuser.tiff")

# load the 16-bit image
img = Image.open("diffuser.tiff")
diffuser_img = np.array(img)

import pudb; pudb.set_trace()  # XXX BREAKPOINT