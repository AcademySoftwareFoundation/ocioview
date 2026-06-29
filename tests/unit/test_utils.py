# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

import PyOpenColorIO as ocio

from ocioview.utils import (
    float_to_uint8,
    get_enum_member,
    item_type_label,
    m33_to_m44,
    m44_to_m33,
    next_name,
    v3_to_v4,
    v4_to_v3,
)


def test_next_name_starts_at_one():
    assert next_name("ColorSpace_", []) == "ColorSpace_1"


def test_next_name_increments_past_existing():
    assert next_name("ColorSpace_", ["ColorSpace_1", "ColorSpace_2"]) == "ColorSpace_3"


def test_next_name_is_case_insensitive():
    assert next_name("cs_", ["CS_1"]) == "cs_2"


def test_item_type_label_splits_camel_case():
    assert item_type_label(ocio.ColorSpace) == "Color Space"
    assert item_type_label(ocio.NamedTransform) == "Named Transform"
    assert item_type_label(ocio.Look) == "Look"


def test_get_enum_member_found_and_missing():
    assert get_enum_member(ocio.BitDepth, ocio.BIT_DEPTH_F32.value) == ocio.BIT_DEPTH_F32
    assert get_enum_member(ocio.BitDepth, -999) is None


def test_matrix_vector_conversions_round_trip():
    m33 = list(range(9))
    assert m44_to_m33(m33_to_m44(m33)) == m33
    v3 = [0.1, 0.2, 0.3]
    assert v4_to_v3(v3_to_v4(v3)) == v3


def test_float_to_uint8_clamps():
    assert float_to_uint8(0.0) == 0
    assert float_to_uint8(1.0) == 255
    assert float_to_uint8(2.0) == 255
    assert float_to_uint8(-1.0) == 0
