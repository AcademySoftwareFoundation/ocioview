# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from ocioview.items.look_model import LookModel
from ocioview.undo import undo_stack


def test_create_item_adds_look_and_undo_restores():
    before = ocio.GetCurrentConfig().serialize()

    model = LookModel()
    model.create_item("foo")
    assert ocio.GetCurrentConfig().getLook("foo") is not None

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert ocio.GetCurrentConfig().getLook("foo") is None


def test_rename_via_set_data_and_undo_restores():
    model = LookModel()
    model.create_item("foo")
    before = ocio.GetCurrentConfig().serialize()

    index = model.get_index_from_item_name("foo")
    name_index = index.sibling(index.row(), model.NAME.column)
    model.setData(name_index, "bar")

    assert ocio.GetCurrentConfig().getLook("bar") is not None
    assert ocio.GetCurrentConfig().getLook("foo") is None

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert ocio.GetCurrentConfig().getLook("foo") is not None


def test_edit_description_and_undo_restores():
    model = LookModel()
    model.create_item("foo")
    before = ocio.GetCurrentConfig().serialize()

    index = model.get_index_from_item_name("foo")
    desc_index = index.sibling(index.row(), model.DESCRIPTION.column)
    model.setData(desc_index, "desc")

    assert ocio.GetCurrentConfig().getLook("foo").getDescription() == "desc"

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before


def test_remove_look():
    model = LookModel()
    model.create_item("foo")

    row = model.get_index_from_item_name("foo").row()
    model.removeRows(row, 1)

    assert ocio.GetCurrentConfig().getLook("foo") is None
