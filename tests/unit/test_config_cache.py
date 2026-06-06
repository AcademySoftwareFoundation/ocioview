# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from ocioview.config_cache import ConfigCache


def test_color_space_names_include_raw():
    assert "raw" in ConfigCache.get_color_space_names()


def test_cache_invalidates_when_config_changes():
    assert ocio.GetCurrentConfig().getColorSpace("probe_cs") is None
    assert "probe_cs" not in ConfigCache.get_color_space_names()

    ocio.GetCurrentConfig().addColorSpace(
        ocio.ColorSpace(ocio.REFERENCE_SPACE_SCENE, "probe_cs")
    )

    # New cache ID -> cache rebuilt on next query
    assert "probe_cs" in ConfigCache.get_color_space_names()


def test_get_color_spaces_returns_list():
    spaces = ConfigCache.get_color_spaces()
    assert isinstance(spaces, list)
    assert any(cs.getName() == "raw" for cs in spaces)
