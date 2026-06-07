# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio
import pytest

from ocioview.transforms.transform_edit_stack import TransformEditStack


def _round_trip(transform):
    """Load a transform into the edit stack and read it back out."""
    stack = TransformEditStack()
    group = ocio.GroupTransform()
    group.appendTransform(transform)
    stack.set_transform(group)
    return stack.transform()


def _matrix():
    transform = ocio.MatrixTransform()
    transform.setMatrix([2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1])
    return transform


def _exponent():
    return ocio.ExponentTransform(value=[2.2, 2.2, 2.2, 1.0])


def _exponent_with_linear():
    return ocio.ExponentWithLinearTransform(
        gamma=[2.4, 2.4, 2.4, 1.0], offset=[0.055, 0.055, 0.055, 0.0]
    )


def _log():
    transform = ocio.LogTransform()
    transform.setBase(10.0)
    return transform


def _log_affine():
    transform = ocio.LogAffineTransform()
    transform.setLogSideSlopeValue([0.3, 0.3, 0.3])
    return transform


def _log_camera():
    transform = ocio.LogCameraTransform(linSideBreak=[0.1, 0.1, 0.1])
    transform.setBase(10.0)
    return transform


def _range():
    transform = ocio.RangeTransform()
    transform.setMinInValue(0.25)
    transform.setMaxInValue(0.75)
    return transform


def _cdl():
    transform = ocio.CDLTransform()
    transform.setSlope([1.1, 1.2, 1.3])
    return transform


def _exposure_contrast():
    transform = ocio.ExposureContrastTransform()
    transform.setExposure(0.5)
    return transform


def _fixed_function():
    return ocio.FixedFunctionTransform(
        style=ocio.FIXED_FUNCTION_ACES_RED_MOD_03
    )


def _allocation():
    return ocio.AllocationTransform(
        allocation=ocio.ALLOCATION_LG2, vars=[-8.0, 8.0, 0.0058]
    )


def _file():
    return ocio.FileTransform(src="test.cube")


# (name, builder, read) — ``read`` returns a comparable representation of the
# editor-modeled parameter that should survive a load/read round-trip.
CASES = [
    ("matrix", _matrix, lambda t: list(t.getMatrix())),
    ("exponent", _exponent, lambda t: list(t.getValue())),
    ("exponent_with_linear", _exponent_with_linear, lambda t: list(t.getGamma())),
    ("log", _log, lambda t: t.getBase()),
    ("log_affine", _log_affine, lambda t: list(t.getLogSideSlopeValue())),
    ("log_camera", _log_camera, lambda t: t.getBase()),
    ("range", _range, lambda t: t.getMinInValue()),
    ("cdl", _cdl, lambda t: list(t.getSlope())),
    ("exposure_contrast", _exposure_contrast, lambda t: t.getExposure()),
    ("fixed_function", _fixed_function, lambda t: t.getStyle()),
    ("allocation", _allocation, lambda t: t.getAllocation()),
    ("file", _file, lambda t: t.getSrc()),
]


@pytest.mark.parametrize(
    "name,builder,read", CASES, ids=[case[0] for case in CASES]
)
def test_transform_edit_round_trip(qapp, name, builder, read):
    """Loading a transform into its editor and reading it back preserves the
    editor-modeled parameter."""
    transform = builder()
    expected = read(transform)

    out = _round_trip(transform)

    assert read(out) == expected
