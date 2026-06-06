# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from ocioview.items.file_rule_model import FileRuleModel, FileRuleType
from ocioview.undo import undo_stack


def _rule_names():
    file_rules = ocio.GetCurrentConfig().getFileRules()
    return [file_rules.getName(i) for i in range(file_rules.getNumEntries())]


def test_add_basic_rule_and_undo_restores():
    before = ocio.GetCurrentConfig().serialize()
    assert _rule_names() == ["Default"]

    model = FileRuleModel()
    model.add_preset(FileRuleType.RULE_BASIC.value)
    assert "BasicRule_1" in _rule_names()

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert _rule_names() == ["Default"]


def test_rename_basic_rule_and_undo_restores():
    model = FileRuleModel()
    model.add_preset(FileRuleType.RULE_BASIC.value)
    before = ocio.GetCurrentConfig().serialize()

    index = model.get_index_from_item_name("BasicRule_1")
    name_index = index.sibling(index.row(), model.NAME.column)
    model.setData(name_index, "bar")

    assert "bar" in _rule_names()
    assert "BasicRule_1" not in _rule_names()

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert "BasicRule_1" in _rule_names()


def test_edit_pattern_and_undo_restores():
    model = FileRuleModel()
    model.add_preset(FileRuleType.RULE_BASIC.value)
    before = ocio.GetCurrentConfig().serialize()

    index = model.get_index_from_item_name("BasicRule_1")
    pattern_index = index.sibling(index.row(), model.PATTERN.column)
    model.setData(pattern_index, "foo*")

    file_rules = ocio.GetCurrentConfig().getFileRules()
    i = file_rules.getIndexForRule("BasicRule_1")
    assert file_rules.getPattern(i) == "foo*"

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before


def test_remove_basic_rule_keeps_default():
    model = FileRuleModel()
    model.add_preset(FileRuleType.RULE_BASIC.value)

    row = model.get_index_from_item_name("BasicRule_1").row()
    model.removeRows(row, 1)

    assert "BasicRule_1" not in _rule_names()
    assert "Default" in _rule_names()
