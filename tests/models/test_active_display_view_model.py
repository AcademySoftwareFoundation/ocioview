# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio
from PySide6 import QtCore

from ocioview.items.active_display_view_model import (
    ActiveDisplayModel,
    ActiveViewModel,
)
from ocioview.undo import undo_stack


def _active_displays():
    return list(ocio.GetCurrentConfig().getActiveDisplays())


def _active_views():
    return list(ocio.GetCurrentConfig().getActiveViews())


def test_toggle_active_display_and_undo_restores():
    ocio.GetCurrentConfig().addDisplayView("disp2", "view1", "display_reference")
    before = ocio.GetCurrentConfig().serialize()

    model = ActiveDisplayModel()
    index = model.get_index_from_item_name("disp2")
    active_index = index.sibling(index.row(), model.ACTIVE.column)
    model.setData(active_index, QtCore.Qt.Checked.value, QtCore.Qt.CheckStateRole)

    assert "disp2" in _active_displays()

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before


def test_toggle_active_view_and_undo_restores():
    config = ocio.GetCurrentConfig()
    config.addDisplayView("disp1", "viewA", "display_reference")
    config.addDisplayView("disp1", "viewB", "display_reference")
    before = ocio.GetCurrentConfig().serialize()

    model = ActiveViewModel()
    index = model.get_index_from_item_name("viewA")
    active_index = index.sibling(index.row(), model.ACTIVE.column)
    model.setData(active_index, QtCore.Qt.Checked.value, QtCore.Qt.CheckStateRole)

    assert "viewA" in _active_views()

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
