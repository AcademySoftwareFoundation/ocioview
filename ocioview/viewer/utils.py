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
