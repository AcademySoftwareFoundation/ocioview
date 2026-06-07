# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from drivers import PanelDriver

from ocioview.items.file_rule_model import FileRuleModel, FileRuleType
from ocioview.items.rule_edit import RuleEdit
from ocioview.items.viewing_rule_model import ViewingRuleModel, ViewingRuleType


def _file_rule_names():
    file_rules = ocio.GetCurrentConfig().getFileRules()
    return [file_rules.getName(i) for i in range(file_rules.getNumEntries())]


def _viewing_rule_names():
    viewing_rules = ocio.GetCurrentConfig().getViewingRules()
    return [
        viewing_rules.getName(i)
        for i in range(viewing_rules.getNumEntries())
    ]


def test_file_rule_panel_add_edit_remove(qapp):
    rule_edit = RuleEdit()
    driver = PanelDriver(rule_edit.file_rule_edit)

    driver.add(FileRuleType.RULE_BASIC.value)
    driver.select("BasicRule_1")
    driver.set_field(FileRuleModel.PATTERN, "foo*")

    file_rules = ocio.GetCurrentConfig().getFileRules()
    i = file_rules.getIndexForRule("BasicRule_1")
    assert file_rules.getPattern(i) == "foo*"

    driver.remove()
    assert "BasicRule_1" not in _file_rule_names()


def test_viewing_rule_panel_add_rename_remove(qapp):
    rule_edit = RuleEdit()
    driver = PanelDriver(rule_edit.viewing_rule_edit)

    driver.add(ViewingRuleType.RULE_COLOR_SPACE.value)
    driver.select("ColorSpaceRule_1")
    driver.set_field(ViewingRuleModel.NAME, "myrule")
    assert "myrule" in _viewing_rule_names()

    driver.select("myrule")
    driver.remove()
    assert "myrule" not in _viewing_rule_names()
