# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import numpy as np

from ocioview.viewer.utils import (
    model_view_matrix,
    orthographic_proj_matrix,
)


def test_orthographic_proj_matrix():
    matrix = orthographic_proj_matrix(
        near=-1, far=1, left=0, right=2, top=2, bottom=0
    )
    expected = np.array(
        [[1, 0, 0, -1], [0, 1, 0, -1], [0, 0, -1, 0], [0, 0, 0, 1]],
        dtype=float,
    )
    np.testing.assert_allclose(matrix, expected)


def test_model_view_matrix():
    matrix = model_view_matrix(
        image_scale=2.0, image_pos=(3, 4), image_size=np.array([10, 20])
    )
    expected = np.array(
        [[20, 0, 0, 6], [0, -40, 0, -8], [0, 0, 1, 0], [0, 0, 0, 1]],
        dtype=float,
    )
    np.testing.assert_allclose(matrix, expected)
