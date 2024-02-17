# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "17/05/2022"


import pytest
from nabu.stitching.frame_composition import ZFrameComposition
import numpy

from nabu.stitching.overlap import OverlapStitchingStrategy, ZStichOverlapKernel


def test_frame_composition():
    """
    Test _ZFrameComposition
    """
    frame_0 = numpy.zeros((100, 1))
    frame_1 = numpy.ones((98, 1))
    frame_2 = numpy.ones((205, 1)) * 2.0

    frames = (frame_0, frame_1, frame_2)

    y_shifts = -20, -10

    kernels = [
        ZStichOverlapKernel(
            frame_width=1,
            stitching_strategy=OverlapStitchingStrategy.LINEAR_WEIGHTS,
            overlap_size=4,
        ),
        ZStichOverlapKernel(
            frame_width=1,
            stitching_strategy=OverlapStitchingStrategy.MEAN,
            overlap_size=8,
        ),
    ]
    # check raw composition
    raw_composition = ZFrameComposition.compute_raw_frame_compositions(
        frames=frames,
        key_lines=(
            (90, 10),
            (98 - 5, 5),
        ),
        overlap_kernels=kernels,
        stitching_axis=0,
    )
    assert isinstance(raw_composition, ZFrameComposition)

    assert raw_composition.local_start_y == (0, 12, 9)
    assert raw_composition.local_end_y == (88, 89, 205)
    assert raw_composition.global_start_y == (0, 92, 177)
    assert raw_composition.global_end_y == (88, 169, 373)

    stitched_data = numpy.empty((100 + 98 + 205 - 30, 1))
    raw_composition.compose(output_frame=stitched_data, input_frames=frames)
    assert stitched_data[0, 0] == 0
    assert stitched_data[150, 0] == 1.0
    assert stitched_data[-1, 0] == 2.0

    # check stitch composition
    stitch_composition = ZFrameComposition.compute_stitch_frame_composition(
        frames=frames,
        key_lines=(
            (90, 10),
            (98 - 5, 5),
        ),
        overlap_kernels=kernels,
        stitching_axis=0,
    )

    ZFrameComposition.pprint_z_stitching(raw_composition, stitch_composition)

    assert stitch_composition.local_start_y == (0, 0)
    assert stitch_composition.local_end_y == (4, 8)
    assert stitch_composition.global_start_y == (88, 169)
    assert stitch_composition.global_end_y == (92, 177)

    stitched_frames = []
    for frame_0, frame_1, kernel, y_shift in zip(frames[:-1], frames[1:], kernels, y_shifts):
        # take frames once shifted
        frame_0_overlap = frame_0[y_shift:]
        frame_1_overlap = frame_1[:-y_shift]
        # select the overlap area
        frame_0_overlap = frame_0[-kernel.overlap_size :]
        frame_1_overlap = frame_1[: kernel.overlap_size]

        stitched_frames.append(kernel.stitch(frame_0_overlap, frame_1_overlap)[0])

    stitch_composition.compose(
        output_frame=stitched_data,
        input_frames=stitched_frames,
    )
    assert 0.0 < stitched_data[90, 0] < 1.0
    assert 1.0 < stitched_data[172, 0] < 2.0


_raw_comp_config = (
    {
        "key_lines": (
            (17, 2),
            (36, 3),
        ),
        "raw_global_start": (0, 19, 53),
        "raw_global_end": (16, 49, 68),
        "raw_local_start": (0, 4, 5),
        "raw_local_end": (16, 34, 20),
        "kernels": (
            ZStichOverlapKernel(
                frame_width=1,
                stitching_strategy=OverlapStitchingStrategy.LINEAR_WEIGHTS,
                overlap_size=3,
            ),
            ZStichOverlapKernel(
                frame_width=1,
                stitching_strategy=OverlapStitchingStrategy.MEAN,
                overlap_size=4,
            ),
        ),
    },
)


@pytest.mark.parametrize("configuration", _raw_comp_config)
def test_raw_frame_composition_exotic_config(configuration):
    """
    Test some
    """
    frame_0 = numpy.zeros((20, 1))
    frame_1 = numpy.ones((40, 1))
    frame_2 = numpy.ones((20, 1)) * 2.0

    frames = (frame_0, frame_1, frame_2)

    key_lines = configuration.get("key_lines")
    kernels = configuration.get("kernels")
    # check raw composition
    raw_composition = ZFrameComposition.compute_raw_frame_compositions(
        frames=frames,
        overlap_kernels=kernels,
        key_lines=key_lines,
        stitching_axis=0,
    )

    assert raw_composition.global_start_y == configuration.get("raw_global_start")
    assert raw_composition.global_end_y == configuration.get("raw_global_end")
    assert raw_composition.local_start_y == configuration.get("raw_local_start")
    assert raw_composition.local_end_y == configuration.get("raw_local_end")

    stitched_data = numpy.empty(
        (
            (raw_composition.global_end_y[-1] - raw_composition.global_start_y[0]),
            1,
        )
    )
    raw_composition.compose(output_frame=stitched_data, input_frames=frames)
