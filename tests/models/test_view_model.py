# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from ocioview.items.utils import ViewType
from ocioview.items.view_model import ViewModel
from ocioview.undo import undo_stack


def _setup_display(display="disp1"):
    ocio.GetCurrentConfig().addDisplayView(display, "view1", "display_reference")


def test_add_scene_view_and_undo_restores():
    _setup_display()
    before = ocio.GetCurrentConfig().serialize()

    model = ViewModel()
    model.set_display("disp1")
    model.add_preset(ViewType.VIEW_SCENE.value)

    new_views = [n for n in model.get_item_names() if n.startswith("View_")]
    assert new_views

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before


def test_edit_view_color_space_and_undo_restores():
    _setup_display()
    model = ViewModel()
    model.set_display("disp1")
    model.add_preset(ViewType.VIEW_SCENE.value)
    name = [n for n in model.get_item_names() if n.startswith("View_")][0]
    before = ocio.GetCurrentConfig().serialize()

    index = model.get_index_from_item_name(name)
    cs_index = index.sibling(index.row(), model.COLOR_SPACE.column)
    model.setData(cs_index, "scene_reference")

    assert (
        ocio.GetCurrentConfig().getDisplayViewColorSpaceName("disp1", name)
        == "scene_reference"
    )

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before


def test_remove_view():
    _setup_display()
    model = ViewModel()
    model.set_display("disp1")
    model.add_preset(ViewType.VIEW_SCENE.value)
    name = [n for n in model.get_item_names() if n.startswith("View_")][0]

    row = model.get_index_from_item_name(name).row()
    model.removeRows(row, 1)

    assert name not in model.get_item_names()
