# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

from PySide6 import QtWidgets

from ocioview.widgets.line_edit import PathEdit


def test_path_edit_browse_save_sets_path(qapp, monkeypatch):
    """Browsing for a save path writes the chosen path to the edit.

    The file dialogs return a ``(path, selected_filter)`` tuple; regression
    test for the path not being unpacked (which raised ``TypeError``).
    """
    path_edit = PathEdit(file_mode=QtWidgets.QFileDialog.AnyFile)

    monkeypatch.setattr(
        QtWidgets.QFileDialog,
        "getSaveFileName",
        staticmethod(lambda *args, **kwargs: ("/tmp/foo.ocio", "OCIO (*.ocio)")),
    )

    path_edit._on_browse_action_triggered()

    assert "foo.ocio" in path_edit.value()
