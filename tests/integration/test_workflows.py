# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import pytest

pytestmark = pytest.mark.slow

import PyOpenColorIO as ocio
from PySide6 import QtCore, QtWidgets

import ocioview.main_window
from ocioview.main_window import OCIOView
from ocioview.mode import OCIOViewMode
from ocioview.signal_router import SignalRouter
from ocioview.transform_manager import TransformManager


def test_save_and_reload_round_trip(qtbot, tmp_path, monkeypatch):
    """Build a config in the app, save it to disk, and reload it intact."""
    # Isolate QSettings so the non-transient app never touches real settings,
    # and auto-discard the unsaved-changes prompt on teardown.
    temp_settings = QtCore.QSettings(
        str(tmp_path / "settings.ini"), QtCore.QSettings.IniFormat
    )
    monkeypatch.setattr(ocioview.main_window, "settings", temp_settings)
    monkeypatch.setattr(
        QtWidgets.QMessageBox,
        "warning",
        staticmethod(lambda *args, **kwargs: QtWidgets.QMessageBox.Discard),
    )

    ocio_view = OCIOView(transient=False)
    qtbot.addWidget(ocio_view)

    ocio_view.config_dock.color_space_edit.list.add_button.click()
    assert ocio.GetCurrentConfig().getColorSpace("ColorSpace_1") is not None

    config_path = tmp_path / "test.ocio"
    monkeypatch.setattr(
        QtWidgets.QFileDialog,
        "getSaveFileName",
        staticmethod(
            lambda *args, **kwargs: (str(config_path), "OCIO Config (*.ocio)")
        ),
    )
    assert ocio_view.save_config_as() is True
    assert config_path.is_file()

    ocio_view.load_config(config_path)
    assert ocio.GetCurrentConfig().getColorSpace("ColorSpace_1") is not None


def test_config_edit_propagates_signals(ocio_view, qtbot):
    """A config-dock edit broadcasts the app-wide change signals."""
    router = SignalRouter.get_instance()
    with qtbot.waitSignal(router.color_spaces_changed, timeout=1000):
        ocio_view.config_dock.color_space_edit.list.add_button.click()


def test_transform_subscription_rebroadcasts_on_edit(ocio_view):
    """A transform subscription delivers the item transform and rebroadcasts
    when the subscribed item is edited."""
    color_space_edit = ocio_view.config_dock.color_space_edit
    color_space_edit.list.add_button.click()
    model = color_space_edit.model
    label = model.format_subscription_item_label("ColorSpace_1")

    received = []
    TransformManager.subscribe_to_transforms_at(
        0, lambda slot, fwd, inv: received.append(fwd)
    )
    TransformManager.set_subscription(0, model, label)

    count_after_set = len(received)
    assert count_after_set >= 1
    assert isinstance(received[-1], ocio.ColorSpaceTransform)

    index = model.get_index_from_item_name("ColorSpace_1")
    name_index = index.sibling(index.row(), model.NAME.column)
    model.setData(name_index, "renamed_cs")

    assert len(received) > count_after_set


def test_mode_switch_updates_app(ocio_view, qtbot):
    """Switching application mode emits mode_changed and updates the mode box."""
    router = SignalRouter.get_instance()
    try:
        with qtbot.waitSignal(router.mode_changed, timeout=1000):
            OCIOViewMode.set_current_mode(OCIOViewMode.Preview)
        assert OCIOViewMode.current_mode() is OCIOViewMode.Preview
        assert ocio_view.mode_box.member() is OCIOViewMode.Preview
    finally:
        OCIOViewMode.set_current_mode(OCIOViewMode.Edit)
