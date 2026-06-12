# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import numpy as np
import OpenImageIO as oiio
import PyOpenColorIO as ocio
import pytest
from OpenGL import GL

from ocioview.viewer.image_viewer import ImageViewer

pytestmark = pytest.mark.gpu


def _write_test_image(path):
    spec = oiio.ImageSpec(4, 4, 3, "float")
    image_output = oiio.ImageOutput.create(str(path))
    image_output.open(str(path), spec)
    image_output.write_image(np.full((4, 4, 3), 0.5, dtype=np.float32))
    image_output.close()


def test_viewer_renders_without_gl_errors(qapp, tmp_path):
    image_path = tmp_path / "test.exr"
    _write_test_image(image_path)

    viewer = ImageViewer()
    viewer.resize(64, 64)
    viewer.show()
    qapp.processEvents()

    viewer.image_plane.load_image(image_path)
    qapp.processEvents()

    framebuffer = viewer.image_plane.grabFramebuffer()
    assert not framebuffer.isNull()

    viewer.image_plane.makeCurrent()
    assert GL.glGetError() == GL.GL_NO_ERROR
    viewer.image_plane.doneCurrent()

    # cleanupGL runs on context destruction; closing must not error.
    viewer.close()
    qapp.processEvents()
