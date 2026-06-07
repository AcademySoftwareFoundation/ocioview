# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.

"""
Page-object drivers for ocioview interface tests.

All knowledge of widget structure lives here so test bodies stay expressed as
intent plus config assertions. Editors are located by their model column via
the panel's QDataWidgetMapper, never by widget attribute path, so a UI refactor
that preserves the model/view architecture updates only this module.
"""


def set_widget_value(widget, value) -> None:
    """Set a mapped editor widget's value via the shared custom-widget API."""
    if hasattr(widget, "set_value"):
        widget.set_value(value)
    elif hasattr(widget, "set_items"):
        # List widgets (e.g. StringListWidget) for list-valued columns.
        widget.set_items(value)
    else:
        raise NotImplementedError(
            f"set_widget_value: no value setter for {type(widget).__name__}; "
            f"extend this adapter."
        )


def get_widget_value(widget):
    """Read a mapped editor widget's value via the shared custom-widget API."""
    if hasattr(widget, "value"):
        return widget.value()
    if hasattr(widget, "items"):
        return widget.items()
    raise NotImplementedError(
        f"get_widget_value: no value getter for {type(widget).__name__}; "
        f"extend this adapter."
    )


def _item_view(panel):
    """
    Return a panel's item view (the shared ``BaseItemView`` list or table),
    or ``None`` for singleton panels with no item view.
    """
    return getattr(panel, "list", None) or getattr(panel, "table", None)


class PanelDriver:
    """
    Drives a config item edit panel by intent. The item view (list or table)
    and its add/remove buttons come from the shared ``BaseItemView``; field
    editors are located by model column through the panel's data-widget mapper.
    Tests therefore stay off volatile widget attribute paths.
    """

    def __init__(self, panel):
        self.panel = panel
        self.view = _item_view(panel)

    def add(self, preset=None) -> None:
        """
        Add an item. With no preset, clicks the add button (exercising its
        wiring). With a preset name, adds that preset (preset-only panels,
        whose add button opens a menu instead of adding directly).
        """
        if preset is not None:
            self.view.add_item(preset)
        else:
            self.view.add_button.click()

    def select(self, item_name: str) -> None:
        self.view.set_current_item(item_name)

    def remove(self) -> None:
        self.view.remove_button.click()

    def set_field(self, column_desc, value) -> None:
        widget = self.panel.mapper.mappedWidgetAt(column_desc.column)
        set_widget_value(widget, value)
        self.panel.mapper.submit()

    def field_value(self, column_desc):
        return get_widget_value(
            self.panel.mapper.mappedWidgetAt(column_desc.column)
        )
