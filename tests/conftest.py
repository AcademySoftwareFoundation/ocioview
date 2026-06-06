# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import pytest


@pytest.fixture(scope="session")
def qapp(qapp):
    """
    pytest-qt qapp fixture override, with ocioview-specific setup
    steps.
    """
    from ocioview.setup import setup_app

    setup_app(qapp)
    return qapp


@pytest.fixture
def qtbot(qapp, qtbot):
    """
    pytest-qt qtbot fixture override, injecting the overridden qapp
    fixture before qtbot can initialize the default implementation.
    """
    return qtbot


@pytest.fixture(scope="session")
def ocio():
    import PyOpenColorIO as ocio

    return ocio


@pytest.fixture
def ocio_view(ocio, qtbot):
    from ocioview.main_window import OCIOView

    ocio_view = OCIOView(transient=True)
    ocio_view.show()
    qtbot.addWidget(ocio_view)

    return ocio_view


@pytest.fixture
def ocio_config(ocio):
    """
    .. note::
        This fixture should be used AFTER the `ocio_view` fixture,
        since `OCIOView` instantiation resets the current config,
        invalidating any existing references.
    """
    return ocio.GetCurrentConfig()


@pytest.fixture(autouse=True)
def reset_global_state(qapp):
    """
    Reset ocioview's process-global singletons before each test so tests
    are order-independent and parallel-safe. Depends on ``qapp`` so a
    QApplication exists before any model builds icons.
    """
    import PyOpenColorIO as ocio

    from ocioview.undo import undo_stack
    from ocioview.transform_manager import TransformManager
    from ocioview.ref_space_manager import ReferenceSpaceManager

    # Undo stack
    undo_stack.clear()

    # Transform subscriptions + subscribers
    TransformManager.reset()
    TransformManager._tf_subscribers.clear()
    TransformManager._tf_menu_subscribers.clear()

    # Reference space tracking
    ReferenceSpaceManager._ref_scene_name = None
    ReferenceSpaceManager._ref_display_name = None
    ReferenceSpaceManager._ref_subscribers.clear()

    # Fresh current config
    ocio.SetCurrentConfig(ocio.Config.CreateRaw())
    ReferenceSpaceManager.init_reference_spaces()

    yield


@pytest.fixture
def raw_config(ocio):
    """The current raw config established by ``reset_global_state``."""
    return ocio.GetCurrentConfig()


@pytest.fixture
def make_model(qapp):
    """Factory: instantiate a config item model against the current config."""

    def _make(model_cls):
        return model_cls()

    return _make
