"""
Tests for the generic filter_block component.
"""

from dash import html
from dash_bootstrap_components import Card, CardBody, CardHeader
from dash import dcc
from src.components.filter_block import create_filter_block, FilterType


def test_create_dropdown_filter():
    """
    Tests the creation of a dropdown filter.
    """
    filter_id = "test-dropdown"
    label = "Test Dropdown"
    options = [{"label": "Option1", "value": "1"}]
    component = create_filter_block(filter_id, label, FilterType.DROPDOWN, options=options)
    
    assert isinstance(component, Card)
    assert component.children[0].children.children == label
    dropdown = component.children[1].children
    assert isinstance(dropdown, dcc.Dropdown)
    assert dropdown.id == {"type": "filter", "index": filter_id}
    assert dropdown.options == options


def test_create_date_range_filter():
    """
    Tests the creation of a date range filter.
    """
    filter_id = "test-date-range"
    label = "Test Date Range"
    component = create_filter_block(filter_id, label, FilterType.DATE_RANGE)
    
    assert isinstance(component, Card)
    assert component.children[0].children.children == label
    date_picker = component.children[1].children
    assert isinstance(date_picker, dcc.DatePickerRange)
    assert date_picker.id == {"type": "filter", "index": filter_id}
