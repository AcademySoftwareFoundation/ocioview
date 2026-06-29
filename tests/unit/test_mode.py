# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

from ocioview.mode import OCIOViewMode
from ocioview.signal_router import SignalRouter


def test_set_current_mode_updates_and_restores():
    original = OCIOViewMode.current_mode()
    try:
        OCIOViewMode.set_current_mode(OCIOViewMode.Preview)
        assert OCIOViewMode.current_mode() is OCIOViewMode.Preview
    finally:
        OCIOViewMode.set_current_mode(original)
    assert OCIOViewMode.current_mode() is original


def test_set_current_mode_emits_signal(qtbot):
    original = OCIOViewMode.current_mode()
    target = (
        OCIOViewMode.Preview
        if original is OCIOViewMode.Edit
        else OCIOViewMode.Edit
    )
    router = SignalRouter.get_instance()
    try:
        with qtbot.waitSignal(router.mode_changed, timeout=1000):
            OCIOViewMode.set_current_mode(target)
    finally:
        OCIOViewMode.set_current_mode(original)
