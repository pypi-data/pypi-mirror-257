import pytest
import numpy as np
from scipy.ndimage import gaussian_filter
from nabu.utils import subdivide_into_overlapping_segment

try:
    import astra

    __has_astra__ = True
except ImportError:
    __has_astra__ = False
from nabu.cuda.utils import __has_pycuda__, get_cuda_context

if __has_pycuda__:
    from nabu.reconstruction.cone import ConebeamReconstructor
if __has_astra__:
    from astra.extrautils import clipCircle


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.vol_shape = (128, 126, 126)
    cls.n_angles = 180
    cls.prj_width = 192  # detector larger than the sample
    cls.src_orig_dist = 1000
    cls.orig_det_dist = 100
    cls.volume, cls.cone_data = generate_hollow_cube_cone_sinograms(
        cls.vol_shape, cls.n_angles, cls.src_orig_dist, cls.orig_det_dist, prj_width=cls.prj_width
    )
    if __has_pycuda__:
        cls.ctx = get_cuda_context()


@pytest.mark.skipif(not (__has_pycuda__ and __has_astra__), reason="Need pycuda and astra for this test")
@pytest.mark.usefixtures("bootstrap")
class TestCone:
    def _create_cone_reconstructor(self, relative_z_position=None):
        return ConebeamReconstructor(
            self.cone_data.shape,
            self.src_orig_dist,
            self.orig_det_dist,
            relative_z_position=relative_z_position,
            volume_shape=self.volume.shape,
            cuda_options={"ctx": self.ctx},
        )

    def test_simple_cone_reconstruction(self):
        C = self._create_cone_reconstructor()
        res = C.reconstruct(self.cone_data)
        delta = np.abs(res - self.volume)

        # Can we do better ? We already had to lowpass-filter the volume!
        # First/last slices are OK
        assert np.max(delta[:8]) < 1e-5
        assert np.max(delta[-8:]) < 1e-5
        # Middle region has a relatively low error
        assert np.max(delta[40:-40]) < 0.11
        # Transition zones between "zero" and "cube" has a large error
        assert np.max(delta[10:25]) < 0.2
        assert np.max(delta[-25:-10]) < 0.2
        # End of transition zones have a smaller error
        assert np.max(delta[25:40]) < 0.125
        assert np.max(delta[-40:-25]) < 0.125

    def test_against_explicit_astra_calls(self):
        C = self._create_cone_reconstructor()

        res = C.reconstruct(self.cone_data)
        #
        # Check that ConebeamReconstructor is consistent with these calls to astra
        #
        # "vol_geom" shape layout is (y, x, z). But here this geometry is used for the reconstruction
        # (i.e sinogram -> volume)and not for projection (volume -> sinograms).
        # So we assume a square slice. Mind that this is a particular case.
        vol_geom = astra.create_vol_geom(self.vol_shape[2], self.vol_shape[2], self.vol_shape[0])

        angles = np.linspace(0, 2 * np.pi, self.n_angles, True)
        proj_geom = astra.create_proj_geom(
            "cone",
            1.0,
            1.0,
            self.cone_data.shape[0],
            self.prj_width,
            angles,
            self.src_orig_dist,
            self.orig_det_dist,
        )
        sino_id = astra.data3d.create("-sino", proj_geom, data=self.cone_data)
        rec_id = astra.data3d.create("-vol", vol_geom)

        cfg = astra.astra_dict("FDK_CUDA")
        cfg["ReconstructionDataId"] = rec_id
        cfg["ProjectionDataId"] = sino_id
        alg_id = astra.algorithm.create(cfg)
        astra.algorithm.run(alg_id)

        res_astra = astra.data3d.get(rec_id)

        # housekeeping
        astra.algorithm.delete(alg_id)
        astra.data3d.delete(rec_id)
        astra.data3d.delete(sino_id)

        assert (
            np.max(np.abs(res - res_astra)) < 5e-4
        ), "ConebeamReconstructor results are inconsistent with plain calls to astra"

    def test_projection_full_vs_partial(self):
        """
        In the ideal case, all the data volume (and reconstruction) fits in memory.
        In practice this is rarely the case, so we have to reconstruct the volume slabs by slabs.
        The slabs should be slightly overlapping to avoid "stitching" artefacts at the edges.
        """
        # Astra seems to duplicate the projection data, even if all GPU memory is handled externally
        # Let's try with (n_z * n_y * n_x + 2 * n_a * n_z * n_x) * 4  <  mem_limit
        # 256^3 seems OK with n_a = 200 (180 MB)
        n_z = n_y = n_x = 256
        n_a = 200
        src_orig_dist = 1000
        orig_det_dist = 100

        volume, cone_data = generate_hollow_cube_cone_sinograms(
            vol_shape=(n_z, n_y, n_x), n_angles=n_a, src_orig_dist=src_orig_dist, orig_det_dist=orig_det_dist
        )
        C_full = ConebeamReconstructor(cone_data.shape, src_orig_dist, orig_det_dist, cuda_options={"ctx": self.ctx})

        vol_geom = astra.create_vol_geom(n_y, n_x, n_z)

        proj_geom = astra.create_proj_geom("cone", 1.0, 1.0, n_z, n_x, C_full.angles, src_orig_dist, orig_det_dist)
        proj_id, projs_full_geom = astra.create_sino3d_gpu(volume, proj_geom, vol_geom)
        astra.data3d.delete(proj_id)

        # Do the same slab-by-slab
        inner_slab_size = 64
        overlap = 16
        slab_size = inner_slab_size + overlap * 2
        slabs = subdivide_into_overlapping_segment(n_z, slab_size, overlap)

        projs_partial_geom = np.zeros_like(projs_full_geom)
        for slab in slabs:
            z_min, z_inner_min, z_inner_max, z_max = slab
            rel_z_pos = (z_min + z_max) / 2 - n_z / 2
            subvolume = volume[z_min:z_max, :, :]
            C = ConebeamReconstructor(
                (z_max - z_min, n_a, n_x),
                src_orig_dist,
                orig_det_dist,
                relative_z_position=rel_z_pos,
                cuda_options={"ctx": self.ctx},
            )
            proj_id, projs = astra.create_sino3d_gpu(subvolume, C.proj_geom, C.vol_geom)
            astra.data3d.delete(proj_id)

            projs_partial_geom[z_inner_min:z_inner_max] = projs[z_inner_min - z_min : z_inner_max - z_min]

        error_profile = [
            np.max(np.abs(proj_partial - proj_full))
            for proj_partial, proj_full in zip(projs_partial_geom, projs_full_geom)
        ]
        assert np.all(np.isclose(error_profile, 0.0, atol=0.0375)), "Mismatch between full-cone and slab geometries"

    def test_cone_reconstruction_magnified_vs_demagnified(self):
        """
        This will only test the astra toolbox.
        When reconstructing a volume from cone-beam data, the volume "should" have a smaller shape than the projection
        data shape (because of cone magnification).
        But astra provides the same results when backprojecting on a "de-magnified grid" and the original grid shape.
        """
        n_z = n_y = n_x = 256
        n_a = 500
        src_orig_dist = 1000
        orig_det_dist = 100
        magnification = 1 + orig_det_dist / src_orig_dist
        angles = np.linspace(0, 2 * np.pi, n_a, True)

        volume, cone_data = generate_hollow_cube_cone_sinograms(
            vol_shape=(n_z, n_y, n_x),
            n_angles=n_a,
            src_orig_dist=src_orig_dist,
            orig_det_dist=orig_det_dist,
            apply_filter=False,
        )
        rec_original_grid = astra_cone_beam_reconstruction(
            cone_data, angles, src_orig_dist, orig_det_dist, demagnify_volume=False
        )
        rec_reduced_grid = astra_cone_beam_reconstruction(
            cone_data, angles, src_orig_dist, orig_det_dist, demagnify_volume=True
        )

        m_z = (n_z - int(n_z / magnification)) // 2
        m_y = (n_y - int(n_y / magnification)) // 2
        m_x = (n_x - int(n_x / magnification)) // 2

        assert np.allclose(rec_original_grid[m_z:-m_z, m_y:-m_y, m_x:-m_x], rec_reduced_grid)

    def test_reconstruction_full_vs_partial(self):
        n_z = n_y = n_x = 256
        n_a = 500
        src_orig_dist = 1000
        orig_det_dist = 100
        angles = np.linspace(0, 2 * np.pi, n_a, True)

        volume, cone_data = generate_hollow_cube_cone_sinograms(
            vol_shape=(n_z, n_y, n_x),
            n_angles=n_a,
            src_orig_dist=src_orig_dist,
            orig_det_dist=orig_det_dist,
            apply_filter=False,
        )

        rec_full_volume = astra_cone_beam_reconstruction(cone_data, angles, src_orig_dist, orig_det_dist)

        rec_partial = np.zeros_like(rec_full_volume)
        inner_slab_size = 64
        overlap = 18
        slab_size = inner_slab_size + overlap * 2
        slabs = subdivide_into_overlapping_segment(n_z, slab_size, overlap)
        for slab in slabs:
            z_min, z_inner_min, z_inner_max, z_max = slab
            m1, m2 = z_inner_min - z_min, z_max - z_inner_max
            C = ConebeamReconstructor((z_max - z_min, n_a, n_x), src_orig_dist, orig_det_dist)
            rec = C.reconstruct(
                cone_data[z_min:z_max],
                relative_z_position=((z_min + z_max) / 2) - n_z / 2,  #  (z_min + z_max)/2.
            )
            rec_partial[z_inner_min:z_inner_max] = rec[m1 : (-m2) or None]

        # Compare volumes in inner circle
        for i in range(n_z):
            clipCircle(rec_partial[i])
            clipCircle(rec_full_volume[i])

        diff = np.abs(rec_partial - rec_full_volume)
        err_max_profile = np.max(diff, axis=(-1, -2))
        err_median_profile = np.median(diff, axis=(-1, -2))

        assert np.max(err_max_profile) < 2e-3
        assert np.max(err_median_profile) < 5e-6


def generate_hollow_cube_cone_sinograms(
    vol_shape, n_angles, src_orig_dist, orig_det_dist, prj_width=None, apply_filter=True
):
    # Adapted from Astra toolbox python samples

    n_z, n_y, n_x = vol_shape
    vol_geom = astra.create_vol_geom(n_y, n_x, n_z)

    prj_width = prj_width or n_x
    prj_height = n_z
    angles = np.linspace(0, 2 * np.pi, n_angles, True)

    proj_geom = astra.create_proj_geom("cone", 1.0, 1.0, prj_width, prj_width, angles, src_orig_dist, orig_det_dist)
    magnification = 1 + orig_det_dist / src_orig_dist

    # hollow cube
    cube = np.zeros(astra.geom_size(vol_geom), dtype="f")

    d = int(min(n_x, n_y) / 2 * (1 - np.sqrt(2) / 2))
    cube[20:-20, d:-d, d:-d] = 1
    cube[40:-40, d + 20 : -(d + 20), d + 20 : -(d + 20)] = 0

    # d = int(min(n_x, n_y) / 2 * (1 - np.sqrt(2) / 2) * magnification)
    # d1 = d + 10
    # d2 = d + 20
    # cube[40:-40, d1:-d1, d1:-d1] = 1
    # cube[60:-60, d2 : -d2, d2 : -d2] = 0

    # High-frequencies yield cannot be accurately retrieved
    if apply_filter:
        cube = gaussian_filter(cube, (1.0, 1.0, 1.0))

    proj_id, proj_data = astra.create_sino3d_gpu(cube, proj_geom, vol_geom)
    astra.data3d.delete(proj_id)  # (n_z, n_angles, n_x)

    return cube, proj_data


def astra_cone_beam_reconstruction(cone_data, angles, src_orig_dist, orig_det_dist, demagnify_volume=False):
    """
    Handy (but data-inefficient) function to reconstruct data from cone-beam geometry
    """

    n_z, n_a, n_x = cone_data.shape

    proj_geom = astra.create_proj_geom("cone", 1.0, 1.0, n_z, n_x, angles, src_orig_dist, orig_det_dist)
    sino_id = astra.data3d.create("-sino", proj_geom, data=cone_data)

    m = 1 + orig_det_dist / src_orig_dist if demagnify_volume else 1.0
    n_z_vol, n_y_vol, n_x_vol = int(n_z / m), int(n_x / m), int(n_x / m)
    vol_geom = astra.create_vol_geom(n_y_vol, n_x_vol, n_z_vol)
    rec_id = astra.data3d.create("-vol", vol_geom)

    cfg = astra.astra_dict("FDK_CUDA")
    cfg["ReconstructionDataId"] = rec_id
    cfg["ProjectionDataId"] = sino_id
    alg_id = astra.algorithm.create(cfg)

    astra.algorithm.run(alg_id)

    rec = astra.data3d.get(rec_id)

    astra.data3d.delete(sino_id)
    astra.data3d.delete(rec_id)
    astra.algorithm.delete(alg_id)

    return rec
