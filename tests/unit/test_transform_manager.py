# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

from ocioview.items.color_space_model import ColorSpaceModel
from ocioview.transform_manager import TransformManager


def test_set_and_get_subscription_slot():
    model = ColorSpaceModel()
    label = model.format_subscription_item_label("raw")

    TransformManager.set_subscription(0, model, label)
    assert TransformManager.get_subscription_slot(model, label) == 0


def test_subscription_slot_color_and_icon():
    model = ColorSpaceModel()
    label = model.format_subscription_item_label("raw")
    TransformManager.set_subscription(3, model, label)

    assert TransformManager.get_subscription_slot_color(3) is not None
    assert TransformManager.get_subscription_slot_icon(3) is not None
    # An unset slot lookup returns the sentinel color/icon of None
    assert TransformManager.get_subscription_slot_color(-1) is None


def test_reset_clears_subscriptions():
    model = ColorSpaceModel()
    label = model.format_subscription_item_label("raw")
    TransformManager.set_subscription(0, model, label)

    TransformManager.reset()
    assert TransformManager.get_subscription_slot(model, label) == -1
