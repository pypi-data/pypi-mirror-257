import numpy as np
from lensless.recon import ReconstructionAlgorithm
from scipy import fft

try:
    import torch

    torch_available = True
except ImportError:
    torch_available = False


class ADMM_PnP(ReconstructionAlgorithm):
    """
    Object for applying ADMM (Alternating Direction Method of Multipliers) with
    a non-negativity constraint and a total variation (TV) prior.

    Paper about ADMM: https://web.stanford.edu/~boyd/papers/pdf/admm_distr_stats.pdf

    Slides about ADMM: https://web.stanford.edu/class/ee364b/lectures/admm_slides.pdf

    """

    def __init__(
        self,
        psf,
        proj,
        dtype=None,
        mu1=1e-6,
        mu2=1e-5,
        mu3=4e-5,
        tau=0.0001,
        pad=False,
        norm="backward",
        use_projection_dual=False,
        **kwargs,
    ):
        """

        Parameters
        ----------
        psf : :py:class:`~numpy.ndarray` or :py:class:`~torch.Tensor`
            Point spread function (PSF) that models forward propagation.
            Must be of shape (depth, height, width, channels) even if
            depth = 1 and channels = 1. You can use :py:func:`~lensless.io.load_psf`
            to load a PSF from a file such that it is in the correct format.
        proj : :py:class:`function`
            Projection function to apply at each iteration.
        dtype : float32 or float64
            Data type to use for optimization. Default is float32.
        mu1 : float
            Step size for updating primal/dual variables.
        mu2 : float
            Step size for updating primal/dual variables.
        mu3 : float
            Step size for updating primal/dual variables.
        tau : float
            Weight for L1 norm of `psi` applied to the image estimate.
        pad : bool
            Whether to pad the image with zeros before applying the PSF. Default
            is False, as optimized data is already padded.
        norm : str
            Normalization to use for the convolution. Options are "forward",
            "backward", and "ortho". Default is "backward".
        use_projection_dual : bool
            Whether to use dual update for the user specify projection. This result in an algorithm closer to ADMM.
            During our testing, it seems to give better result with few iteration (<20) but worst otherwise.  Default is False.
        """
        self._mu1 = mu1
        self._mu2 = mu2
        self._mu3 = mu3
        self._tau = tau

        # TODO add check for proj
        self._proj = proj
        self._use_projection_dual = use_projection_dual

        # 3D ADMM is not supported yet
        assert len(psf.shape) == 4, "PSF must be 4D: (depth, height, width, channels)."
        if psf.shape[0] > 1:
            raise NotImplementedError(
                "3D ADMM is not supported yet, use gradient descent or APGD instead."
            )

        # call reset() to initialize matrices
        super(ADMM_PnP, self).__init__(psf, dtype, pad=pad, norm=norm, **kwargs)

        # precompute_R_divmat (self._H computed by constructor with reset())
        if self.is_torch:
            self._R_divmat = 1.0 / (
                self._mu1 * (torch.abs(self._convolver._Hadj * self._convolver._H))
                + self._mu2
                + self._mu3
            ).type(self._complex_dtype)
        else:
            self._R_divmat = 1.0 / (
                self._mu1 * (np.abs(self._convolver._Hadj * self._convolver._H))
                + self._mu2 * np.abs(self._PsiTPsi)
                + self._mu3
            ).astype(self._complex_dtype)

    def reset(self):
        if self.is_torch:
            # TODO initialize without padding
            # initialize image estimate as [Batch, Depth, Height, Width, Channels]
            if self._initial_est is not None:
                self._image_est = self._initial_est
            else:
                self._image_est = torch.zeros([1] + self._padded_shape, dtype=self._dtype).to(
                    self._psf.device
                )

            # self._image_est = torch.zeros_like(self._psf)
            self._X = torch.zeros_like(self._image_est)
            self._U = torch.zeros_like(self._proj(self._image_est))
            self._W = torch.zeros_like(self._X)
            if self._image_est.max():
                # if non-zero
                # self._forward_out = self._forward()
                self._forward_out = self._convolver.convolve(self._image_est)
            else:
                self._forward_out = torch.zeros_like(self._X)

            self._xi = torch.zeros_like(self._image_est)
            self._eta = torch.zeros_like(self._U)
            self._rho = torch.zeros_like(self._X)

            # precompute_X_divmat
            self._X_divmat = 1.0 / (self._convolver._pad(torch.ones_like(self._psf)) + self._mu1)
            # self._X_divmat = 1.0 / (torch.ones_like(self._psf) + self._mu1)

        else:
            if self._initial_est is not None:
                self._image_est = self._initial_est
            else:
                self._image_est = np.zeros([1] + self._padded_shape, dtype=self._dtype)

            # self._U = np.zeros(np.r_[self._padded_shape, [2]], dtype=self._dtype)
            self._X = np.zeros_like(self._image_est)
            self._U = np.zeros_like(self._proj(self._image_est))
            self._W = np.zeros_like(self._X)
            if self._image_est.max():
                # if non-zero
                # self._forward_out = self._forward()
                self._forward_out = self._convolver.convolve(self._image_est)
            else:
                self._forward_out = np.zeros_like(self._X)

            self._xi = np.zeros_like(self._image_est)
            self._eta = np.zeros_like(self._U)
            self._rho = np.zeros_like(self._X)

            # precompute_X_divmat
            self._X_divmat = 1.0 / (
                self._convolver._pad(np.ones(self._psf_shape, dtype=self._dtype)) + self._mu1
            )

    def _U_update(self):
        """Total variation update."""
        # to avoid computing sparse operator twice
        if self._use_projection_dual:
            self._U = self._proj(self._U + self._eta / self._mu2)
        else:
            self._U = self._proj(self._image_est)

    def _X_update(self):
        # to avoid computing forward model twice
        # self._X = self._X_divmat * (self._xi + self._mu1 * self._forward_out + self._data)
        self._X = self._X_divmat * (
            self._xi + self._mu1 * self._forward_out + self._convolver._pad(self._data)
        )

    def _W_update(self):
        """Non-negativity update"""
        if self.is_torch:
            self._W = torch.maximum(
                self._rho / self._mu3 + self._image_est, torch.zeros_like(self._image_est)
            )
        else:
            self._W = np.maximum(self._rho / self._mu3 + self._image_est, 0)

    def _image_update(self):
        rk = (
            (self._mu3 * self._W - self._rho)
            + self._mu2 * self._U
            + self._convolver.deconvolve(self._mu1 * self._X - self._xi)
        )

        # rk = self._convolver._pad(rk)

        if self.is_torch:
            freq_space_result = self._R_divmat * torch.fft.rfft2(rk, dim=(-3, -2))
            self._image_est = torch.fft.irfft2(freq_space_result, dim=(-3, -2))
        else:
            freq_space_result = self._R_divmat * fft.rfft2(rk, axes=(-3, -2))
            self._image_est = fft.irfft2(freq_space_result, axes=(-3, -2))

        # self._image_est = self._convolver._crop(res)

    def _xi_update(self):
        # to avoid computing forward model twice
        self._xi += self._mu1 * (self._forward_out - self._X)

    def _eta_update(self):
        # to avoid finite difference operataion again?
        self._eta += self._mu2 * (self._image_est - self._U)

    def _rho_update(self):
        self._rho += self._mu3 * (self._image_est - self._W)

    def _update(self, iter):
        self._U_update()
        if torch.isnan(self._U).any():
            raise RuntimeError("NaN encountered in U update.")
        self._X_update()
        if torch.isnan(self._X).any():
            raise RuntimeError("NaN encountered in X update.")
        self._W_update()
        if torch.isnan(self._W).any():
            raise RuntimeError("NaN encountered in W update.")
        self._image_update()
        if torch.isnan(self._image_est).any():
            raise RuntimeError("NaN encountered in image update.")

        # update forward and sparse operators
        self._forward_out = self._convolver.convolve(self._image_est)

        self._xi_update()
        if self._use_projection_dual:
            self._eta_update()
        self._rho_update()

    def _form_image(self):
        image = self._convolver._crop(self._image_est)

        # # TODO without cropping
        # image = self._image_est

        image[image < 0] = 0
        return image