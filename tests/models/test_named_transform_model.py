# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from ocioview.items.named_transform_model import NamedTransformModel
from ocioview.undo import undo_stack


def test_create_item_adds_named_transform_and_undo_restores():
    before = ocio.GetCurrentConfig().serialize()

    model = NamedTransformModel()
    model.create_item("foo")
    assert ocio.GetCurrentConfig().getNamedTransform("foo") is not None

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert ocio.GetCurrentConfig().getNamedTransform("foo") is None


def test_rename_via_set_data_and_undo_restores():
    model = NamedTransformModel()
    model.create_item("foo")
    before = ocio.GetCurrentConfig().serialize()

    index = model.get_index_from_item_name("foo")
    name_index = index.sibling(index.row(), model.NAME.column)
    model.setData(name_index, "bar")

    assert ocio.GetCurrentConfig().getNamedTransform("bar") is not None
    assert ocio.GetCurrentConfig().getNamedTransform("foo") is None

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert ocio.GetCurrentConfig().getNamedTransform("foo") is not None


def test_edit_description_and_undo_restores():
    model = NamedTransformModel()
    model.create_item("foo")
    before = ocio.GetCurrentConfig().serialize()

    index = model.get_index_from_item_name("foo")
    desc_index = index.sibling(index.row(), model.DESCRIPTION.column)
    model.setData(desc_index, "desc")

    assert ocio.GetCurrentConfig().getNamedTransform("foo").getDescription() == "desc"

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before


def test_remove_named_transform():
    model = NamedTransformModel()
    model.create_item("foo")

    row = model.get_index_from_item_name("foo").row()
    model.removeRows(row, 1)

    assert ocio.GetCurrentConfig().getNamedTransform("foo") is None
