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


def test_reassigning_slot_does_not_duplicate_callbacks():
    """Regression: moving a subscription to another slot must disconnect the
    original slot's agent. Otherwise reusing that slot leaves a stale
    connection and its callbacks fire twice."""
    model = ColorSpaceModel()
    label_a = model.format_subscription_item_label("raw")
    label_b = model.format_subscription_item_label("scene_reference")

    calls = []
    TransformManager.subscribe_to_transforms_at(0, lambda *args: calls.append(args))

    TransformManager.set_subscription(0, model, label_a)
    TransformManager.set_subscription(1, model, label_a)  # move the item off slot 0
    TransformManager.set_subscription(0, model, label_b)  # reuse slot 0

    calls.clear()
    model._update_tf_subscribers("scene_reference")
    assert len(calls) == 1


def test_unsubscribe_from_menu_and_init():
    """Menu and subscription-init subscribers can be removed (regression for
    a viewer subscriber leak on tab close)."""

    def menu_callback(menu_items):
        pass

    def init_callback(slot):
        pass

    TransformManager.subscribe_to_transform_menu(menu_callback)
    TransformManager.subscribe_to_transform_subscription_init(init_callback)
    assert menu_callback in TransformManager._tf_menu_subscribers
    assert init_callback in TransformManager._tf_subscribers[-1]

    TransformManager.unsubscribe_from_transform_menu(menu_callback)
    TransformManager.unsubscribe_from_transform_subscription_init(init_callback)
    assert menu_callback not in TransformManager._tf_menu_subscribers
    assert init_callback not in TransformManager._tf_subscribers[-1]
