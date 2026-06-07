# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from ocioview.transforms.transform_edit_stack import TransformEditStack


MATRIX = [2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1]


def test_matrix_transform_edit_round_trip(qapp):
    """A matrix loaded into the editor round-trips back out unchanged."""
    stack = TransformEditStack()

    matrix_transform = ocio.MatrixTransform()
    matrix_transform.setMatrix(MATRIX)
    group = ocio.GroupTransform()
    group.appendTransform(matrix_transform)

    stack.set_transform(group)

    out = stack.transform()
    assert isinstance(out, ocio.MatrixTransform)
    assert list(out.getMatrix()) == MATRIX


def test_matrix_transform_edit_widget_contract(qapp):
    """The individual transform edit widget exposes the loaded transform."""
    stack = TransformEditStack()

    matrix_transform = ocio.MatrixTransform()
    matrix_transform.setMatrix(MATRIX)
    group = ocio.GroupTransform()
    group.appendTransform(matrix_transform)

    stack.set_transform(group)

    edits = stack.transform_edits()
    assert len(edits) == 1

    edit_transform = edits[0].transform()
    assert isinstance(edit_transform, ocio.MatrixTransform)
    assert list(edit_transform.getMatrix()) == MATRIX
