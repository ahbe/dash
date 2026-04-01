"""
Tests for the generic chart_block component.
"""

import pandas as pd
from dash import dcc
from dash_bootstrap_components import Card
from src.components.chart_block import create_chart_block, ChartType


def test_create_bar_chart_block(sample_dataframe: pd.DataFrame):
    """
    Tests the creation of a bar chart block.
    """
    component = create_chart_block(
        chart_id="test-bar-chart",
        title="Test Bar Chart",
        chart_type=ChartType.BAR,
        df=sample_dataframe,
        x_field="brand",
        y_fields=["usage_count"],
    )

    assert isinstance(component, Card)
    assert "Test Bar Chart" in str(component)
    graph = component.children[1].children
    assert isinstance(graph, dcc.Graph)
    assert graph.id == {"type": "chart", "index": "test-bar-chart"}
    assert graph.figure is not None
    assert graph.figure["data"][0]["type"] == "bar"


def test_create_line_chart_block(sample_dataframe: pd.DataFrame):
    """
    Tests the creation of a line chart block.
    """
    component = create_chart_block(
        chart_id="test-line-chart",
        title="Test Line Chart",
        chart_type=ChartType.LINE,
        df=sample_dataframe,
        x_field="date",
        y_fields=["derogation_bps"],
    )

    assert isinstance(component, Card)
    assert "Test Line Chart" in str(component)
    graph = component.children[1].children
    assert isinstance(graph, dcc.Graph)
    assert graph.figure is not None
    assert graph.figure["data"][0]["type"] == "scatter"
