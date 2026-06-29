# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from drivers import PanelDriver

from ocioview.items.display_view_edit import DisplayViewEdit
from ocioview.items.shared_view_model import SharedViewModel
from ocioview.items.utils import ViewType


def _add_view_transform():
    ocio.GetCurrentConfig().addViewTransform(
        ocio.ViewTransform(
            ocio.REFERENCE_SPACE_SCENE,
            "vt1",
            toReference=ocio.GroupTransform(),
            fromReference=ocio.GroupTransform(),
        )
    )


def test_shared_view_panel_add_edit_remove(qapp):
    _add_view_transform()
    display_view_edit = DisplayViewEdit()
    driver = PanelDriver(display_view_edit.shared_view_edit)

    driver.add()
    driver.select("SharedView_1")
    driver.set_field(SharedViewModel.DESCRIPTION, "desc")
    assert (
        ocio.GetCurrentConfig().getDisplayViewDescription("", "SharedView_1")
        == "desc"
    )

    driver.select("SharedView_1")
    driver.remove()
    assert "SharedView_1" not in list(ocio.GetCurrentConfig().getSharedViews())


def test_view_panel_add_remove(qapp):
    display_view_edit = DisplayViewEdit()
    view_edit = display_view_edit.view_edit
    view_edit.display_list.set_current_item("sRGB")

    driver = PanelDriver(view_edit)
    driver.add(ViewType.VIEW_SCENE.value)

    view_name = next(
        n for n in view_edit.model.get_item_names() if n.startswith("View_")
    )

    driver.select(view_name)
    driver.remove()
    assert view_name not in view_edit.model.get_item_names()
