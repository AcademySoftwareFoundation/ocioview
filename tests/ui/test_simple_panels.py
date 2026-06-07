# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from drivers import PanelDriver

from ocioview.items.look_edit import LookEdit
from ocioview.items.look_model import LookModel
from ocioview.items.named_transform_edit import NamedTransformEdit
from ocioview.items.named_transform_model import NamedTransformModel
from ocioview.items.view_transform_edit import ViewTransformEdit
from ocioview.items.view_transform_model import ViewTransformModel


def test_look_panel_add_edit_remove(qapp):
    panel = LookEdit()
    driver = PanelDriver(panel)

    driver.add()
    driver.select("Look_1")
    driver.set_field(LookModel.DESCRIPTION, "desc")
    assert ocio.GetCurrentConfig().getLook("Look_1").getDescription() == "desc"

    driver.remove()
    assert ocio.GetCurrentConfig().getLook("Look_1") is None


def test_view_transform_panel_add_edit_remove(qapp):
    panel = ViewTransformEdit()
    driver = PanelDriver(panel)

    driver.add()
    driver.select("ViewTransform_1")
    driver.set_field(ViewTransformModel.DESCRIPTION, "desc")
    assert (
        ocio.GetCurrentConfig().getViewTransform("ViewTransform_1").getDescription()
        == "desc"
    )

    driver.remove()
    assert ocio.GetCurrentConfig().getViewTransform("ViewTransform_1") is None


def test_named_transform_panel_add_edit_remove(qapp):
    panel = NamedTransformEdit()
    driver = PanelDriver(panel)

    driver.add()
    driver.select("NamedTransform_1")
    driver.set_field(NamedTransformModel.DESCRIPTION, "desc")
    assert (
        ocio.GetCurrentConfig().getNamedTransform("NamedTransform_1").getDescription()
        == "desc"
    )

    driver.remove()
    assert ocio.GetCurrentConfig().getNamedTransform("NamedTransform_1") is None
