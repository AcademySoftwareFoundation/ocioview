# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import pytest

pytestmark = pytest.mark.slow

import PyOpenColorIO as ocio

from ocioview.mode import OCIOViewMode


def test_app_builds_with_docks(ocio_view):
    """The main window constructs with its three docks."""
    assert ocio_view.config_dock is not None
    assert ocio_view.viewer_dock is not None
    assert ocio_view.inspect_dock is not None


def test_mode_switch(ocio_view):
    """Switching application mode updates the current mode."""
    OCIOViewMode.set_current_mode(OCIOViewMode.Preview)
    assert OCIOViewMode.current_mode() is OCIOViewMode.Preview
    OCIOViewMode.set_current_mode(OCIOViewMode.Edit)
    assert OCIOViewMode.current_mode() is OCIOViewMode.Edit


def test_load_config_roundtrip(ocio_view, tmp_path):
    """Loading a config file through the app populates the current config."""
    builtin = ocio.Config.CreateFromBuiltinConfig(
        "cg-config-v2.1.0_aces-v1.3_ocio-v2.3"
    )
    expected = len(list(builtin.getColorSpaces()))

    path = tmp_path / "test.ocio"
    builtin.serialize(str(path))

    ocio_view.load_config(path)

    loaded = len(list(ocio.GetCurrentConfig().getColorSpaces()))
    assert loaded == expected
