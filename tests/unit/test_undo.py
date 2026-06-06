# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from ocioview.undo import ConfigSnapshotUndoCommand, undo_stack


def test_snapshot_command_undo_redo_round_trip():
    config = ocio.GetCurrentConfig()
    before = config.serialize()
    assert config.getColorSpace("snap_cs") is None

    with ConfigSnapshotUndoCommand("Add snap_cs"):
        ocio.GetCurrentConfig().addColorSpace(
            ocio.ColorSpace(ocio.REFERENCE_SPACE_SCENE, "snap_cs")
        )

    assert undo_stack.count() == 1
    assert ocio.GetCurrentConfig().getColorSpace("snap_cs") is not None

    undo_stack.undo()
    assert ocio.GetCurrentConfig().serialize() == before
    assert ocio.GetCurrentConfig().getColorSpace("snap_cs") is None

    undo_stack.redo()
    assert ocio.GetCurrentConfig().getColorSpace("snap_cs") is not None
