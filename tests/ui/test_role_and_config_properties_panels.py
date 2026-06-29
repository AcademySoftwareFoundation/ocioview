# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from drivers import PanelDriver

from ocioview.items.config_properties_edit import ConfigPropertiesEdit
from ocioview.items.config_properties_model import ConfigPropertiesModel
from ocioview.items.role_edit import RoleEdit


def _role_names():
    return list(ocio.GetCurrentConfig().getRoleNames())


def test_role_panel_add_remove(qapp):
    panel = RoleEdit()
    driver = PanelDriver(panel)

    driver.add()
    assert "role_1" in _role_names()

    driver.select("role_1")
    driver.remove()
    assert "role_1" not in _role_names()


def test_config_properties_panel_edit_description(qapp):
    panel = ConfigPropertiesEdit()
    driver = PanelDriver(panel)

    driver.set_field(ConfigPropertiesModel.DESCRIPTION, "my desc")

    assert ocio.GetCurrentConfig().getDescription() == "my desc"
