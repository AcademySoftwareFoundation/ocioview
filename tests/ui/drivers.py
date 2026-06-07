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
    else:
        raise NotImplementedError(
            f"set_widget_value: no value setter for {type(widget).__name__}; "
            f"extend this adapter."
        )


def get_widget_value(widget):
    """Read a mapped editor widget's value via the shared custom-widget API."""
    if hasattr(widget, "value"):
        return widget.value()
    raise NotImplementedError(
        f"get_widget_value: no value getter for {type(widget).__name__}; "
        f"extend this adapter."
    )


class PanelDriver:
    """
    Drives a ``BaseConfigItemEdit`` panel by intent. Editors are located by
    model column through the panel's data-widget mapper, keeping tests off
    volatile widget attribute paths.
    """

    def __init__(self, panel):
        self.panel = panel

    def add(self) -> None:
        self.panel.list.add_button.click()

    def remove(self) -> None:
        self.panel.list.remove_button.click()

    def select(self, item_name: str) -> None:
        index = self.panel.model.get_index_from_item_name(item_name)
        self.panel.list.set_current_row(index.row())

    def set_field(self, column_desc, value) -> None:
        widget = self.panel.mapper.mappedWidgetAt(column_desc.column)
        set_widget_value(widget, value)
        self.panel.mapper.submit()

    def field_value(self, column_desc):
        return get_widget_value(
            self.panel.mapper.mappedWidgetAt(column_desc.column)
        )
