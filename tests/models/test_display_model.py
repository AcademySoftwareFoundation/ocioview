# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from ocioview.items.display_model import DisplayModel
from ocioview.undo import undo_stack


def _displays():
    return list(ocio.GetCurrentConfig().getDisplays())


def test_create_display_and_undo_restores():
    before = ocio.GetCurrentConfig().serialize()

    model = DisplayModel()
    model.create_item("foo")
    assert "foo" in _displays()

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert "foo" not in _displays()


def test_rename_display_and_undo_restores():
    model = DisplayModel()
    model.create_item("foo")
    before = ocio.GetCurrentConfig().serialize()

    index = model.get_index_from_item_name("foo")
    name_index = index.sibling(index.row(), model.NAME.column)
    model.setData(name_index, "bar")

    assert "bar" in _displays()
    assert "foo" not in _displays()

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert "foo" in _displays()


def test_remove_display():
    model = DisplayModel()
    model.create_item("foo")

    row = model.get_index_from_item_name("foo").row()
    model.removeRows(row, 1)

    assert "foo" not in _displays()
