# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import pytest
from PySide6 import QtGui


def gl_available() -> bool:
    """Whether a real OpenGL context can be created and made current."""
    surface_format = QtGui.QSurfaceFormat()
    surface_format.setVersion(4, 0)
    surface_format.setProfile(QtGui.QSurfaceFormat.CoreProfile)

    surface = QtGui.QOffscreenSurface()
    surface.setFormat(surface_format)
    surface.create()

    context = QtGui.QOpenGLContext()
    context.setFormat(surface_format)
    if not context.create():
        return False
    made_current = context.makeCurrent(surface)
    context.doneCurrent()
    return bool(made_current)


@pytest.fixture(autouse=True)
def _require_gl(qapp):
    """Skip every gpu-tier test when no OpenGL context is available (headless/CI)."""
    if not gl_available():
        pytest.skip("no OpenGL context available (run with a real display/GPU)")
