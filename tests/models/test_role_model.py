# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import pytest
import PyOpenColorIO as ocio

from ocioview.items.role_model import RoleModel
from ocioview.undo import undo_stack


def _role_names():
    return list(ocio.GetCurrentConfig().getRoleNames())


def test_create_item_adds_role_and_undo_restores():
    before = ocio.GetCurrentConfig().serialize()

    model = RoleModel()
    model.create_item("foo")
    assert "foo" in _role_names()

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert "foo" not in _role_names()


def test_rename_via_set_data():
    model = RoleModel()
    model.create_item("foo")

    index = model.get_index_from_item_name("foo")
    name_index = index.sibling(index.row(), model.NAME.column)
    model.setData(name_index, "bar")

    assert "bar" in _role_names()
    assert "foo" not in _role_names()


@pytest.mark.xfail(
    strict=True,
    reason=(
        "RoleModel rename+undo corrupts roles: OCIO serializes roles sorted, "
        "but ItemModelUndoCommand replays on a stale QPersistentModelIndex "
        "because _set_value emits no row-move signal on the sort reorder."
    ),
)
def test_rename_undo_restores():
    model = RoleModel()
    model.create_item("foo")
    before = ocio.GetCurrentConfig().serialize()

    index = model.get_index_from_item_name("foo")
    name_index = index.sibling(index.row(), model.NAME.column)
    model.setData(name_index, "bar")

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before


def test_edit_color_space_and_undo_restores():
    model = RoleModel()
    model.create_item("foo")
    before = ocio.GetCurrentConfig().serialize()

    index = model.get_index_from_item_name("foo")
    cs_index = index.sibling(index.row(), model.COLOR_SPACE.column)
    model.setData(cs_index, "scene_reference")

    assert ocio.GetCurrentConfig().getRoleColorSpace("foo") == "scene_reference"

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before


def test_remove_role():
    model = RoleModel()
    model.create_item("foo")

    row = model.get_index_from_item_name("foo").row()
    model.removeRows(row, 1)

    assert "foo" not in _role_names()
