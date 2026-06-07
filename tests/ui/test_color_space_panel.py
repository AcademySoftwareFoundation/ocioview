# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from drivers import PanelDriver

from ocioview.items.color_space_edit import ColorSpaceEdit
from ocioview.items.color_space_model import ColorSpaceModel
from ocioview.undo import undo_stack


def test_add_and_edit_fields(qapp):
    panel = ColorSpaceEdit()
    driver = PanelDriver(panel)

    driver.add()
    driver.select("ColorSpace_1")
    driver.set_field(ColorSpaceModel.NAME, "foo")
    driver.set_field(ColorSpaceModel.FAMILY, "test/family")
    driver.set_field(ColorSpaceModel.IS_DATA, True)

    color_space = ocio.GetCurrentConfig().getColorSpace("foo")
    assert color_space is not None
    assert color_space.getFamily() == "test/family"
    assert color_space.isData() is True


def test_remove(qapp):
    panel = ColorSpaceEdit()
    driver = PanelDriver(panel)

    driver.add()
    assert ocio.GetCurrentConfig().getColorSpace("ColorSpace_1") is not None

    driver.select("ColorSpace_1")
    driver.remove()
    assert ocio.GetCurrentConfig().getColorSpace("ColorSpace_1") is None


def test_edit_undo(qapp):
    panel = ColorSpaceEdit()
    driver = PanelDriver(panel)

    driver.add()
    driver.select("ColorSpace_1")
    before = ocio.GetCurrentConfig().serialize()

    driver.set_field(ColorSpaceModel.FAMILY, "fam")
    assert (
        ocio.GetCurrentConfig().getColorSpace("ColorSpace_1").getFamily() == "fam"
    )

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
