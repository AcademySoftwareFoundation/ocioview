# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import numpy as np
import OpenImageIO as oiio
import PyOpenColorIO as ocio
import pytest
from OpenGL import GL

from ocioview.viewer.image_viewer import ImageViewer

pytestmark = pytest.mark.gpu

GRAY = 0.5


def _write_gray_image(path):
    spec = oiio.ImageSpec(8, 8, 3, "float")
    image_output = oiio.ImageOutput.create(str(path))
    image_output.open(str(path), spec)
    image_output.write_image(np.full((8, 8, 3), GRAY, dtype=np.float32))
    image_output.close()


def test_gpu_output_matches_cpu_processor(qapp, tmp_path):
    image_path = tmp_path / "gray.exr"
    _write_gray_image(image_path)

    viewer = ImageViewer()
    viewer.resize(64, 64)
    viewer.show()
    qapp.processEvents()
    viewer.image_plane.load_image(image_path)
    qapp.processEvents()

    framebuffer = viewer.image_plane.grabFramebuffer()
    center = framebuffer.pixelColor(
        framebuffer.width() // 2, framebuffer.height() // 2
    )
    gpu_rgb = np.array([center.red(), center.green(), center.blue()])

    # CPU reference: apply the same OCIO transform the viewer is displaying to
    # the raw input, then convert to 8-bit the way the framebuffer does.
    rgb = [GRAY, GRAY, GRAY]
    ocio_tf = viewer.image_plane._ocio_tf
    if ocio_tf is not None:
        config = ocio.GetCurrentConfig()
        processor = config.getProcessor(ocio_tf)
        cpu_processor = processor.getDefaultCPUProcessor()
        rgb = list(cpu_processor.applyRGB(rgb))

    expected = np.clip(np.array(rgb) * 255.0, 0, 255).astype(int)

    np.testing.assert_allclose(gpu_rgb, expected, atol=2)
