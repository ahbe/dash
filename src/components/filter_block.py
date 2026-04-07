"""
Generic reusable filter component.
Supports dropdowns, date ranges, and more using pattern-matching callbacks.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from dash import dcc, html
import dash_bootstrap_components as dbc


class FilterType(Enum):
    """
    Supported filter types.
    """
    DROPDOWN = "dropdown"
    MULTI_DROPDOWN = "multi_dropdown"
    DATE_RANGE = "date_range"
    RANGE_SLIDER = "range_slider"
    TEXT_INPUT = "text_input"


def create_filter_block(
    filter_id: str,
    label: str,
    filter_type: FilterType,
    options: Optional[List[Dict[str, str]]] = None,
    default_value: Any = None,
    placeholder: str = "Select...",
) -> dbc.Card:
    """
    Creates a styled Dash Bootstrap Card containing a filter widget.

    Args:
        filter_id: Unique identifier for the filter (used in pattern-matching).
        label: Display label for the filter.
        filter_type: Type of filter component to create.
        options: List of options for dropdowns.
        default_value: Initial value for the filter.
        placeholder: Placeholder text for the filter.

    Returns:
        dbc.Card: Filter component wrapped in a Card.
    """
    # Pattern-matching ID
    # Date ranges need a separate type because they use start_date/end_date instead of value
    if filter_type == FilterType.DATE_RANGE:
        pm_id = {"type": "date-filter", "index": filter_id}
    else:
        pm_id = {"type": "filter", "index": filter_id}

    if filter_type == FilterType.DROPDOWN:
        widget = dcc.Dropdown(
            id=pm_id,
            options=options or [],
            value=default_value,
            placeholder=placeholder,
            multi=False,
            clearable=True,
        )
    elif filter_type == FilterType.MULTI_DROPDOWN:
        widget = dcc.Dropdown(
            id=pm_id,
            options=options or [],
            value=default_value if default_value else [],
            placeholder=placeholder,
            multi=True,
            clearable=True,
        )
    elif filter_type == FilterType.DATE_RANGE:
        widget = dcc.DatePickerRange(
            id=pm_id,
            start_date=default_value[0] if default_value else None,
            end_date=default_value[1] if default_value else None,
            display_format="YYYY-MM-DD",
        )
    elif filter_type == FilterType.RANGE_SLIDER:
        widget = dcc.RangeSlider(
            id=pm_id,
            min=options[0]["value"] if options else 0,
            max=options[-1]["value"] if options else 100,
            value=default_value or [0, 100],
        )
    elif filter_type == FilterType.TEXT_INPUT:
        widget = dbc.Input(
            id=pm_id,
            value=default_value,
            placeholder=placeholder,
            type="text",
        )
    else:
        widget = html.Div("Unknown filter type")

    return dbc.Card(
        [
            dbc.CardHeader(html.Label(label, className="mb-0 fw-bold")),
            dbc.CardBody(widget, className="p-2"),
        ],
        className="mb-3 shadow-sm",
    )
