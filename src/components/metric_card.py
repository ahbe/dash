"""
Generic reusable KPI/metric card component.
Displays value, variation, and icon.
"""

from typing import Any, Optional, Union
from dash import html
import dash_bootstrap_components as dbc


def create_metric_card(
    metric_id: str,
    title: str,
    value: Union[str, int, float] = "0",
    variation: Optional[float] = None,
    variation_suffix: str = "%",
    icon: str = "graph-up",
    color_scheme: str = "primary",
    inverted_polarity: bool = False,
) -> dbc.Card:
    """
    Creates a styled metric card.

    Args:
        metric_id: Unique identifier for the metric.
        title: Title of the metric.
        value: Current value to display.
        variation: Percentage or absolute change from previous period.
        variation_suffix: Suffix for the variation (e.g., "%", "bps").
        icon: Bootstrap icon name.
        color_scheme: Bootstrap color theme.
        inverted_polarity: If True, positive variation is red, negative is green.

    Returns:
        dbc.Card: Metric card component.
    """
    variation_display = None
    if variation is not None:
        is_positive = variation >= 0
        
        # Determine color based on polarity
        if inverted_polarity:
            var_color = "danger" if is_positive else "success"
        else:
            var_color = "success" if is_positive else "danger"
            
        arrow = "▲" if is_positive else "▼"
        variation_display = html.Small(
            f"{arrow} {abs(variation):.1f}{variation_suffix}",
            className=f"text-{var_color} fw-bold ms-2"
        )

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.I(className=f"bi bi-{icon} fs-4 text-{color_scheme} me-2"),
                        html.Span(title, className="text-muted fw-bold text-uppercase small"),
                    ],
                    className="d-flex align-items-center mb-2"
                ),
                html.Div(
                    [
                        html.H3(value, id={"type": "metric-value", "index": metric_id}, className="mb-0"),
                        variation_display if variation_display else html.Div()
                    ],
                    className="d-flex align-items-baseline"
                )
            ]
        ),
        className="mb-4 shadow-sm border-start border-4 border-" + color_scheme
    )
