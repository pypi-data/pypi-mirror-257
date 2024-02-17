import numpy as np
import pytest
from nabu.testutils import get_data, generate_tests_scenarios, compare_shifted_images
from nabu.cuda.utils import get_cuda_context, __has_pycuda__, __has_cufft__
from nabu.opencl.utils import get_opencl_context, __has_pyopencl__
from nabu.thirdparty.algotom_convert_sino import extend_sinogram

__has_pycuda__ = __has_pycuda__ and __has_cufft__  # need both for using Cuda backprojector


if __has_pycuda__:
    from nabu.reconstruction.fbp import CudaBackprojector
if __has_pyopencl__:
    from nabu.reconstruction.fbp_opencl import OpenCLBackprojector


scenarios = generate_tests_scenarios({"backend": ["cuda", "opencl"]})


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    file_desc = get_data("sino_halftomo.npz")
    cls.sino = file_desc["sinogram"] * 1e4
    cls.rot_center = file_desc["rot_center"]
    cls.tol = 5e-3
    if __has_pycuda__:
        cls.cuda_ctx = get_cuda_context()
    if __has_pyopencl__:
        cls.opencl_ctx = get_opencl_context("all")


@pytest.mark.usefixtures("bootstrap")
@pytest.mark.parametrize("config", scenarios)
class TestHalftomo:
    def _get_backprojector(self, config, *bp_args, **bp_kwargs):
        if config["backend"] == "cuda":
            if not (__has_pycuda__):
                pytest.skip("Need pycuda + scikit-cuda")
            Backprojector = CudaBackprojector
            ctx = self.cuda_ctx
        else:
            if not (__has_pyopencl__):
                pytest.skip("Need pyopencl")
            Backprojector = OpenCLBackprojector
            ctx = self.opencl_ctx
            if config.get("opencl_use_textures", True) is False:
                # patch "extra_options"
                extra_options = bp_kwargs.pop("extra_options", {})
                extra_options["use_textures"] = False
                bp_kwargs["extra_options"] = extra_options
        return Backprojector(*bp_args, **bp_kwargs, backend_options={"ctx": ctx})

    def test_halftomo_right_side(self, config, sino=None, rot_center=None):
        if sino is None:
            sino = self.sino
        if rot_center is None:
            rot_center = self.rot_center

        sino_extended, rot_center_ext = extend_sinogram(sino, rot_center, apply_log=False)
        sino_extended *= 2  # compat. with nabu normalization

        backprojector_extended = self._get_backprojector(
            config,
            sino_extended.shape,
            rot_center=rot_center_ext,
            halftomo=False,
            padding_mode="edges",
            angles=np.linspace(0, 2 * np.pi, sino.shape[0], True),
            extra_options={"centered_axis": True},
        )
        ref = backprojector_extended.fbp(sino_extended)

        backprojector = self._get_backprojector(
            config,
            sino.shape,
            rot_center=rot_center,
            halftomo=True,
            padding_mode="edges",
            extra_options={"centered_axis": True},
        )
        res = backprojector.fbp(sino)

        # The approach in algotom (used as reference) slightly differers:
        #   - altogom extends the sinogram with padding, so that it's ready-to-use for FBP
        #   - nabu filters the sinogram first, and then does the "half-tomo preparation".
        #     Filtering the sinogram first is better to avoid artefacts due to sharp transition in the borders
        metric, upper_bound = compare_shifted_images(res, ref, return_upper_bound=True)
        assert metric < 5, "Something wrong for halftomo with backend %s" % (config["backend"])

    def test_halftomo_left_side(self, config):
        sino = np.ascontiguousarray(self.sino[:, ::-1])
        rot_center = sino.shape[-1] - 1 - self.rot_center
        return self.test_halftomo_right_side(config, sino=sino, rot_center=rot_center)

    def test_halftomo_cor_outside_fov(self, config):
        sino = np.ascontiguousarray(self.sino[:, : self.sino.shape[-1] // 2])
        backprojector = self._get_backprojector(config, sino.shape, rot_center=self.rot_center, halftomo=True)
        res = backprojector.fbp(sino)
        # Just check that it runs, but no reference results. Who does this anyway ?!
