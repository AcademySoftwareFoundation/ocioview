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


def _color_space():
    # raw config provides the "raw" and "scene_reference" color spaces.
    return ocio.ColorSpaceTransform(src="raw", dst="scene_reference")


def _display_view():
    # raw config provides the "sRGB" display with a "Raw" view.
    return ocio.DisplayViewTransform(src="raw", display="sRGB", view="Raw")


def _look():
    ocio.GetCurrentConfig().addLook(
        ocio.Look(name="mylook", processSpace="raw")
    )
    return ocio.LookTransform(src="raw", dst="scene_reference", looks="mylook")


def _builtin():
    return ocio.BuiltinTransform(style="IDENTITY")


CASES = [
    ("color_space", _color_space, lambda t: (t.getSrc(), t.getDst())),
    (
        "display_view",
        _display_view,
        lambda t: (t.getSrc(), t.getDisplay(), t.getView()),
    ),
    ("look", _look, lambda t: (t.getSrc(), t.getDst(), t.getLooks())),
    ("builtin", _builtin, lambda t: t.getStyle()),
]


@pytest.mark.parametrize(
    "name,builder,read", CASES, ids=[case[0] for case in CASES]
)
def test_config_transform_edit_round_trip(qapp, name, builder, read):
    """A config-referencing transform round-trips through its editor."""
    transform = builder()
    expected = read(transform)

    out = _round_trip(transform)

    assert read(out) == expected
