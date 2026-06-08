# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio
import pytest

from ocioview.transforms.transform_edit_stack import TransformEditStack


def _round_trip(transform):
    stack = TransformEditStack()
    group = ocio.GroupTransform()
    group.appendTransform(transform)
    stack.set_transform(group)
    return stack.transform()


# (name, style, params) — styles requiring parameters previously crashed the
# editor (it constructed the transform with no params before setting them).
# "lin_to_double_log" has no dedicated editor widget, exercising the
# loaded-param preservation path.
FF_CASES = [
    ("rec2100_surround", ocio.FIXED_FUNCTION_REC2100_SURROUND, [0.8]),
    (
        "aces_gamut_comp_13",
        ocio.FIXED_FUNCTION_ACES_GAMUT_COMP_13,
        [1.147, 1.264, 1.312, 0.815, 0.803, 0.880, 1.2],
    ),
    (
        "lin_to_double_log",
        ocio.FIXED_FUNCTION_LIN_TO_DOUBLE_LOG,
        [2.0, 0.5, 0.5, 1.0, 0.0, 1.0, 0.0, 0.18, 0.0, 0.18, 0.0, 1.0, 1.0],
    ),
    ("rgb_to_hsv", ocio.FIXED_FUNCTION_RGB_TO_HSV, []),
]


@pytest.mark.parametrize(
    "name,style,params", FF_CASES, ids=[case[0] for case in FF_CASES]
)
def test_fixed_function_round_trip(qapp, name, style, params):
    """A FixedFunctionTransform round-trips through its editor preserving the
    style and parameters."""
    transform = ocio.FixedFunctionTransform(style=style, params=params)

    out = _round_trip(transform)

    assert out.getStyle() == style
    assert list(out.getParams()) == list(params)
