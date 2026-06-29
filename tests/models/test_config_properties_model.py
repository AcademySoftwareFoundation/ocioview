# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from ocioview.items.config_properties_model import ConfigPropertiesModel
from ocioview.undo import undo_stack


def test_edit_name_and_undo_restores():
    before = ocio.GetCurrentConfig().serialize()

    model = ConfigPropertiesModel()
    model.setData(model.index(0, model.NAME.column), "MyConfig")
    assert ocio.GetCurrentConfig().getName() == "MyConfig"

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before


def test_edit_description_and_undo_restores():
    before = ocio.GetCurrentConfig().serialize()

    model = ConfigPropertiesModel()
    model.setData(model.index(0, model.DESCRIPTION.column), "my desc")
    assert ocio.GetCurrentConfig().getDescription() == "my desc"

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before


def test_edit_family_separator_and_undo_restores():
    before = ocio.GetCurrentConfig().serialize()

    model = ConfigPropertiesModel()
    model.setData(model.index(0, model.FAMILY_SEPARATOR.column), "|")
    assert ocio.GetCurrentConfig().getFamilySeparator() == "|"

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before


def test_edit_search_path_and_undo_restores():
    before = ocio.GetCurrentConfig().serialize()

    model = ConfigPropertiesModel()
    model.setData(model.index(0, model.SEARCH_PATH.column), ["luts"])
    assert "luts" in list(ocio.GetCurrentConfig().getSearchPaths())

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
