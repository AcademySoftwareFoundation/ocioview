# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio
import pytest

from ocioview.config_cache import ConfigCache
from ocioview.items.active_display_view_model import (
    ActiveDisplayModel,
    ActiveViewModel,
)
from ocioview.items.color_space_model import ColorSpaceModel
from ocioview.items.config_properties_model import ConfigPropertiesModel
from ocioview.items.display_model import DisplayModel
from ocioview.items.file_rule_model import FileRuleModel
from ocioview.items.look_model import LookModel
from ocioview.items.named_transform_model import NamedTransformModel
from ocioview.items.role_model import RoleModel
from ocioview.items.shared_view_model import SharedViewModel
from ocioview.items.view_model import ViewModel
from ocioview.items.view_transform_model import ViewTransformModel
from ocioview.items.viewing_rule_model import ViewingRuleModel
from ocioview.ref_space_manager import ReferenceSpaceManager
from ocioview.undo import undo_stack


# Immutable built-in config registry names (pinned for stability).
BUILTIN_CONFIGS = [
    "cg-config-v2.1.0_aces-v1.3_ocio-v2.3",
    "studio-config-v2.1.0_aces-v1.3_ocio-v2.3",
]


def test_operation_sequence_undo_redo_invariant():
    """A multi-model edit sequence fully undoes and redoes byte-identically."""
    start = ocio.GetCurrentConfig().serialize()

    ColorSpaceModel().create_item("cs_a")
    RoleModel().create_item("role_a")
    LookModel().create_item("look_a")
    ViewTransformModel().create_item("vt_a")
    DisplayModel().create_item("disp_a")
    NamedTransformModel().create_item("nt_a")

    end = ocio.GetCurrentConfig().serialize()
    assert end != start

    op_count = undo_stack.count()
    assert op_count == 6

    for _ in range(op_count):
        undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == start

    for _ in range(op_count):
        undo_stack.redo()
    assert ocio.GetCurrentConfig().serialize() == end


@pytest.mark.parametrize("builtin_name", BUILTIN_CONFIGS)
def test_builtin_config_model_read_smoke(builtin_name):
    """Every model can read a rich real config without mutating it."""
    ocio.SetCurrentConfig(ocio.Config.CreateFromBuiltinConfig(builtin_name))
    ReferenceSpaceManager._ref_scene_name = None
    ReferenceSpaceManager._ref_display_name = None
    ReferenceSpaceManager.init_reference_spaces()
    ConfigCache._callbacks.clear()

    before = ocio.GetCurrentConfig().serialize()

    models = [
        ColorSpaceModel(),
        RoleModel(),
        LookModel(),
        ViewTransformModel(),
        NamedTransformModel(),
        FileRuleModel(),
        ViewingRuleModel(),
        DisplayModel(),
        SharedViewModel(),
        ActiveDisplayModel(),
        ActiveViewModel(),
        ConfigPropertiesModel(),
    ]
    for model in models:
        # Exercise the read paths.
        model.get_item_names()
        model.rowCount()

    # ViewModel is display-contextual.
    displays = list(ocio.GetCurrentConfig().getDisplays())
    if displays:
        view_model = ViewModel()
        view_model.set_display(displays[0])
        assert view_model.get_item_names()  # the first display has views

    assert ocio.GetCurrentConfig().serialize() == before
