# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from ocioview.items.viewing_rule_model import ViewingRuleModel, ViewingRuleType
from ocioview.undo import undo_stack


def _rule_names():
    viewing_rules = ocio.GetCurrentConfig().getViewingRules()
    return [
        viewing_rules.getName(i)
        for i in range(viewing_rules.getNumEntries())
    ]


def test_add_color_space_rule_and_undo_restores():
    before = ocio.GetCurrentConfig().serialize()
    assert _rule_names() == []

    model = ViewingRuleModel()
    model.add_preset(ViewingRuleType.RULE_COLOR_SPACE.value)
    assert "ColorSpaceRule_1" in _rule_names()

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert _rule_names() == []


def test_rename_rule_and_undo_restores():
    model = ViewingRuleModel()
    model.add_preset(ViewingRuleType.RULE_COLOR_SPACE.value)
    before = ocio.GetCurrentConfig().serialize()

    index = model.get_index_from_item_name("ColorSpaceRule_1")
    name_index = index.sibling(index.row(), model.NAME.column)
    model.setData(name_index, "bar")

    assert "bar" in _rule_names()
    assert "ColorSpaceRule_1" not in _rule_names()

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert "ColorSpaceRule_1" in _rule_names()


def test_edit_color_spaces_and_undo_restores():
    model = ViewingRuleModel()
    model.add_preset(ViewingRuleType.RULE_COLOR_SPACE.value)
    before = ocio.GetCurrentConfig().serialize()

    index = model.get_index_from_item_name("ColorSpaceRule_1")
    cs_index = index.sibling(index.row(), model.COLOR_SPACES.column)
    model.setData(cs_index, ["scene_reference"])

    viewing_rules = ocio.GetCurrentConfig().getViewingRules()
    i = viewing_rules.getIndexForRule("ColorSpaceRule_1")
    assert list(viewing_rules.getColorSpaces(i)) == ["scene_reference"]

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before


def test_remove_rule():
    model = ViewingRuleModel()
    model.add_preset(ViewingRuleType.RULE_COLOR_SPACE.value)

    row = model.get_index_from_item_name("ColorSpaceRule_1").row()
    model.removeRows(row, 1)

    assert "ColorSpaceRule_1" not in _rule_names()
