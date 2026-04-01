"""
Tests for the generic metric_card component.
"""

from dash import html
from dash_bootstrap_components import Card
from src.components.metric_card import create_metric_card


def test_create_metric_card_positive_variation():
    """
    Tests a metric card with positive variation.
    """
    component = create_metric_card(
        metric_id="test-metric-pos",
        title="Positive Metric",
        value="100",
        variation=5.2,
        variation_suffix="%",
        icon="arrow-up",
        color_scheme="success",
    )

    assert isinstance(component, Card)
    assert "Positive Metric" in str(component)
    assert "100" in str(component)
    assert "▲ 5.2%" in str(component)
    assert "text-success" in str(component)


def test_create_metric_card_negative_variation():
    """
    Tests a metric card with negative variation.
    """
    component = create_metric_card(
        metric_id="test-metric-neg",
        title="Negative Metric",
        value="50",
        variation=-3.1,
        variation_suffix="bps",
        icon="arrow-down",
        color_scheme="danger",
    )

    assert isinstance(component, Card)
    assert "Negative Metric" in str(component)
    assert "50" in str(component)
    assert "▼ 3.1bps" in str(component)
    assert "text-danger" in str(component)


def test_create_metric_card_no_variation():
    """
    Tests a metric card without variation.
    """
    component = create_metric_card(
        metric_id="test-metric-no-var",
        title="No Var Metric",
        value="200",
        icon="info-circle",
    )

    assert isinstance(component, Card)
    assert "No Var Metric" in str(component)
    assert "200" in str(component)
    assert "▲" not in str(component)  # No arrow expected
