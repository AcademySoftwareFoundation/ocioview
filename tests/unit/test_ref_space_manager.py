# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from ocioview.ref_space_manager import ReferenceSpaceManager


def test_scene_reference_space_found_on_raw_config():
    cs = ReferenceSpaceManager.scene_reference_space()
    assert cs is not None
    assert cs.getReferenceSpaceType() == ocio.REFERENCE_SPACE_SCENE
    assert not cs.isData()


def test_display_reference_space_found_on_raw_config():
    cs = ReferenceSpaceManager.display_reference_space()
    assert cs is not None
    assert cs.getReferenceSpaceType() == ocio.REFERENCE_SPACE_DISPLAY


def test_scene_reference_space_created_when_missing():
    # Empty config with no color spaces, and cleared tracking
    ocio.SetCurrentConfig(ocio.Config())
    ReferenceSpaceManager._ref_scene_name = None

    cs = ReferenceSpaceManager.scene_reference_space()
    assert cs is not None
    assert cs.getName() == "scene_reference"
    assert ocio.GetCurrentConfig().getColorSpace("scene_reference") is not None
