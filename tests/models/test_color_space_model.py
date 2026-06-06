# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from ocioview.items.color_space_model import ColorSpaceModel
from ocioview.undo import undo_stack


# NOTE: Always access the config via ``ocio.GetCurrentConfig()`` rather than
#       caching the reference. Undo/redo restores state by calling
#       ``ocio.SetCurrentConfig()``, which swaps in a new config object, so a
#       cached reference goes stale after any undo.


def test_create_item_adds_color_space_and_undo_restores():
    before = ocio.GetCurrentConfig().serialize()

    model = ColorSpaceModel()
    model.create_item("foo")
    assert ocio.GetCurrentConfig().getColorSpace("foo") is not None

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert ocio.GetCurrentConfig().getColorSpace("foo") is None


def test_rename_via_set_data_and_undo_restores():
    model = ColorSpaceModel()
    model.create_item("foo")
    before = ocio.GetCurrentConfig().serialize()

    index = model.get_index_from_item_name("foo")
    name_index = index.sibling(index.row(), model.NAME.column)
    model.setData(name_index, "bar")

    assert ocio.GetCurrentConfig().getColorSpace("bar") is not None
    assert ocio.GetCurrentConfig().getColorSpace("foo") is None

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert ocio.GetCurrentConfig().getColorSpace("foo") is not None
    assert ocio.GetCurrentConfig().getColorSpace("bar") is None


def test_remove_unused_color_space():
    model = ColorSpaceModel()
    model.create_item("foo")

    row = model.get_index_from_item_name("foo").row()
    model.removeRows(row, 1)

    assert ocio.GetCurrentConfig().getColorSpace("foo") is None


def test_removal_guard_refuses_referenced_color_space():
    model = ColorSpaceModel()
    model.create_item("foo")
    ocio.GetCurrentConfig().setRole("my_role", "foo")

    warnings = []
    model.warning_raised.connect(warnings.append)

    row = model.get_index_from_item_name("foo").row()
    model.removeRows(row, 1)

    assert ocio.GetCurrentConfig().getColorSpace("foo") is not None  # not removed
    assert warnings  # a refusal warning was raised
