from math import pi
import numpy as np
from scipy.fft import rfft, irfft
from silx.image.tomography import compute_fourier_filter, get_next_power
from ..processing.padding_base import PaddingBase
from ..utils import check_supported, get_num_threads

# # COMPAT.
# from .filtering_cuda import CudaSinoFilter

# SinoFilter = deprecated_class(
#     "From version 2023.1, 'filtering_cuda.CudaSinoFilter' should be used instead of 'filtering.SinoFilter'. In the future, 'filtering.SinoFilter' will be a numpy-only class.",
#     do_print=True,
# )(CudaSinoFilter)
# #


class SinoFilter:
    available_filters = [
        "ramlak",
        "shepp-logan",
        "cosine",
        "hamming",
        "hann",
        "tukey",
        "lanczos",
        "hilbert",
    ]

    """
    A class for sinogram filtering.
    It does the following:
      - pad input array
      - Fourier transform each row
      - multiply with a 1D or 2D filter
      - inverse Fourier transform
    """

    available_padding_modes = PaddingBase.supported_modes
    default_extra_options = {"cutoff": 1.0, "fft_threads": 0}  # use all threads by default

    def __init__(
        self,
        sino_shape,
        filter_name=None,
        padding_mode="zeros",
        extra_options=None,
    ):
        self._init_extra_options(extra_options)
        self._set_padding_mode(padding_mode)
        self._calculate_shapes(sino_shape)
        self._init_fft()
        self._allocate_memory()
        self._compute_filter(filter_name)

    def _init_extra_options(self, extra_options):
        self.extra_options = self.default_extra_options.copy()
        self.extra_options.update(extra_options or {})

    def _set_padding_mode(self, padding_mode):
        # Compat.
        if padding_mode == "edges":
            padding_mode = "edge"
        if padding_mode == "zeros":
            padding_mode = "constant"
        #
        check_supported(padding_mode, self.available_padding_modes, "padding mode")
        self.padding_mode = padding_mode

    def _calculate_shapes(self, sino_shape):
        self.ndim = len(sino_shape)
        if self.ndim == 2:
            n_angles, dwidth = sino_shape
            n_sinos = 1
        elif self.ndim == 3:
            n_sinos, n_angles, dwidth = sino_shape
        else:
            raise ValueError("Invalid sinogram number of dimensions")
        self.sino_shape = sino_shape
        self.n_angles = n_angles
        self.dwidth = dwidth
        # Make sure to use int() here, otherwise pycuda/pyopencl will crash in some cases
        self.dwidth_padded = int(get_next_power(2 * self.dwidth))
        self.sino_padded_shape = (n_angles, self.dwidth_padded)
        if self.ndim == 3:
            self.sino_padded_shape = (n_sinos,) + self.sino_padded_shape
        sino_f_shape = list(self.sino_padded_shape)
        sino_f_shape[-1] = sino_f_shape[-1] // 2 + 1
        self.sino_f_shape = tuple(sino_f_shape)
        self.pad_left = (self.dwidth_padded - self.dwidth) // 2
        self.pad_right = self.dwidth_padded - self.dwidth - self.pad_left

    def _init_fft(self):
        pass

    def _allocate_memory(self):
        pass

    def set_filter(self, h_filt, normalize=True):
        """
        Set a filter for sinogram filtering.

        Parameters
        ----------
        h_filt: numpy.ndarray
            Array containing the filter. Each line of the sinogram will be filtered with
            this filter. It has to be the Real-to-Complex Fourier Transform
            of some real filter, padded to 2*sinogram_width.
        normalize: bool or float, optional
            Whether to normalize (multiply) the filter with pi/num_angles.
        """
        if h_filt.size != self.sino_f_shape[-1]:
            raise ValueError(
                """
                Invalid filter size: expected %d, got %d.
                Please check that the filter is the Fourier R2C transform of
                some real 1D filter.
                """
                % (self.sino_f_shape[-1], h_filt.size)
            )
        if not (np.iscomplexobj(h_filt)):
            print("Warning: expected a complex Fourier filter")
        self.filter_f = h_filt.copy()
        if normalize:
            self.filter_f *= pi / self.n_angles
        self.filter_f = self.filter_f.astype(np.complex64)

    def _compute_filter(self, filter_name):
        self.filter_name = filter_name or "ram-lak"
        # TODO add this one into silx
        if self.filter_name == "hilbert":
            freqs = np.fft.fftfreq(self.dwidth_padded)
            filter_f = 1.0 / (2 * pi * 1j) * np.sign(freqs)
        #
        else:
            filter_f = compute_fourier_filter(
                self.dwidth_padded,
                self.filter_name,
                cutoff=self.extra_options["cutoff"],
            )
        filter_f = filter_f[: self.dwidth_padded // 2 + 1]  # R2C
        self.set_filter(filter_f, normalize=True)

    def _check_array(self, arr):
        if arr.dtype != np.float32:
            raise ValueError("Expected data type = numpy.float32")
        if arr.shape != self.sino_shape:
            raise ValueError("Expected sinogram shape %s, got %s" % (self.sino_shape, arr.shape))

    def filter_sino(self, sino, output=None, no_output=False):
        """
        Perform the sinogram siltering.

        Parameters
        ----------
        sino: numpy.ndarray or pycuda.gpuarray.GPUArray
            Input sinogram (2D or 3D)
        output: numpy.ndarray or pycuda.gpuarray.GPUArray, optional
            Output array.
        no_output: bool, optional
            If set to True, no copy is be done. The resulting data lies
            in self.d_sino_padded.
        """
        self._check_array(sino)
        sino_padded = np.pad(
            sino, ((0, 0), (0, self.dwidth_padded - self.dwidth)), mode=self.padding_mode
        )  # pad with a FFT-friendly layout
        sino_padded_f = rfft(sino_padded, axis=1, workers=get_num_threads(self.extra_options["fft_threads"]))
        sino_padded_f *= self.filter_f
        sino_filtered = irfft(sino_padded_f, axis=1, workers=get_num_threads(self.extra_options["fft_threads"]))
        if output is None:
            res = np.zeros(self.sino_shape, dtype=np.float32)
        else:
            res = output
        if self.ndim == 2:
            res[:] = sino_filtered[:, : self.dwidth]  # pylint: disable=E1126 # ?!
        else:
            res[:] = sino_filtered[:, :, : self.dwidth]  # pylint: disable=E1126 # ?!
        return res

    __call__ = filter_sino


def filter_sinogram(
    sinogram,
    padded_width,
    filter_name="ramlak",
    padding_mode="constant",
    normalize=True,
    filter_cutoff=1.0,
    **padding_kwargs,
):
    """
    Simple function to filter sinogram.

    Parameters
    ----------
    sinogram: numpy.ndarray
        Sinogram, two dimensional array with shape (n_angles, sino_width)
    padded_width: int
        Width to use for padding. Must be greater than sinogram width (i.e than sinogram.shape[-1])
    filter_name: str, optional
        Which filter to use. Default is ramlak (roughly equivalent to abs(nu) in frequency domain)
    padding_mode: str, optional
        Which padding mode to use. Default is zero-padding.
    normalize: bool, optional
        Whether to multiply the filtered sinogram with pi/n_angles
    filter_cutoff: float, optional
        frequency cutoff for filter
    """
    n_angles, width = sinogram.shape
    sinogram_padded = np.pad(sinogram, ((0, 0), (0, padded_width - width)), mode=padding_mode, **padding_kwargs)
    fourier_filter = compute_fourier_filter(padded_width, filter_name, cutoff=filter_cutoff)
    if normalize:
        fourier_filter *= np.pi / n_angles
    fourier_filter = fourier_filter[: padded_width // 2 + 1]  # R2C
    sino_f = rfft(sinogram_padded, axis=1)
    sino_f *= fourier_filter
    sino_filtered = irfft(sino_f, axis=1)[:, :width]  # pylint: disable=E1126 # ?!
    return sino_filtered
