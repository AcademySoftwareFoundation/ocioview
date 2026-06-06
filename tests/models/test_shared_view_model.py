# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from ocioview.items.shared_view_model import SharedViewModel
from ocioview.undo import undo_stack


def _add_view_transform():
    ocio.GetCurrentConfig().addViewTransform(
        ocio.ViewTransform(
            ocio.REFERENCE_SPACE_SCENE,
            "vt1",
            toReference=ocio.GroupTransform(),
            fromReference=ocio.GroupTransform(),
        )
    )


def _shared_views():
    return list(ocio.GetCurrentConfig().getSharedViews())


def test_create_shared_view_and_undo_restores():
    _add_view_transform()
    before = ocio.GetCurrentConfig().serialize()

    model = SharedViewModel()
    model.create_item("sv1")
    assert "sv1" in _shared_views()

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert "sv1" not in _shared_views()


def test_rename_shared_view_and_undo_restores():
    _add_view_transform()
    model = SharedViewModel()
    model.create_item("sv1")
    before = ocio.GetCurrentConfig().serialize()

    index = model.get_index_from_item_name("sv1")
    name_index = index.sibling(index.row(), model.NAME.column)
    model.setData(name_index, "sv2")

    assert "sv2" in _shared_views()
    assert "sv1" not in _shared_views()

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert "sv1" in _shared_views()


def test_remove_shared_view():
    _add_view_transform()
    model = SharedViewModel()
    model.create_item("sv1")

    row = model.get_index_from_item_name("sv1").row()
    model.removeRows(row, 1)

    assert "sv1" not in _shared_views()
