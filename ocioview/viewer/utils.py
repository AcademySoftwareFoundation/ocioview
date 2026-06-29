# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

from pathlib import Path

import numpy as np
import OpenImageIO as oiio


def load_image(image_path: Path) -> np.ndarray:
    """
    Load RGB image data via OpenImageIO.

    :param image_path: Path to image to load
    :return: NumPy array
    """
    image_buf = oiio.ImageBuf(image_path.as_posix())
    spec = image_buf.spec()

    # Convert to RGB, filling missing color channels with 0.0
    if spec.nchannels < 3:
        image_buf = oiio.ImageBufAlgo.channels(
            image_buf,
            tuple(list(range(spec.nchannels)) + ([0.0] * (3 - spec.nchannels))),
            newchannelnames=("R", "G", "B"),
        )
    elif spec.nchannels > 3:
        image_buf = oiio.ImageBufAlgo.channels(
            image_buf, (0, 1, 2), newchannelnames=("R", "G", "B")
        )

    # Get pixels as 32-bit float NumPy array
    return image_buf.get_pixels(oiio.FLOAT)


def orthographic_proj_matrix(
    near: float,
    far: float,
    left: float,
    right: float,
    top: float,
    bottom: float,
) -> np.ndarray:
    """Build an orthographic projection matrix from camera frustum params."""
    right_minus_left = right - left
    top_minus_bottom = top - bottom
    far_minus_near = far - near

    tx = -(right + left) / right_minus_left
    ty = -(top + bottom) / top_minus_bottom
    tz = -(far + near) / far_minus_near

    a = 2 / right_minus_left
    b = 2 / top_minus_bottom
    c = -2 / far_minus_near

    return np.array(
        [[a, 0, 0, tx], [0, b, 0, ty], [0, 0, c, tz], [0, 0, 0, 1]]
    )


def model_view_matrix(image_scale, image_pos, image_size) -> np.ndarray:
    """
    Build the image-plane model-view matrix from the current zoom scale,
    pan position, and image size. Y is flipped for the OIIO/OpenGL origin
    difference.
    """
    matrix = np.eye(4)
    matrix *= [1.0, -1.0, 1.0, 1.0]
    matrix *= [image_scale, image_scale, 1.0, 1.0]
    matrix[:2, -1] += [
        image_pos[0] * image_scale,
        -image_pos[1] * image_scale,
    ]
    matrix *= list(image_size) + [1.0, 1.0]
    return matrix
