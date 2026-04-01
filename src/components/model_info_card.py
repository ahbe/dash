"""
MLflow/DVC model performance display card.
"""

from typing import Any, Dict, Optional
from dash import html
import dash_bootstrap_components as dbc


def create_model_info_card(
    model_name: str,
    version: str,
    status: str,
    metrics: Dict[str, float],
    last_trained: Optional[str] = None,
) -> dbc.Card:
    """
    Creates a card to display model registry information.

    Args:
        model_name: Name of the model.
        version: Model version.
        status: Deployment status (e.g., Staging, Production).
        metrics: Dictionary of performance metrics.
        last_trained: Date when the model was last trained.

    Returns:
        dbc.Card: Model info component.
    """
    metric_rows = [
        html.Div(
            [
                html.Span(f"{k.upper()}:", className="fw-bold me-2"),
                html.Span(f"{v:.4f}"),
            ],
            className="mb-1"
        )
        for k, v in metrics.items()
    ]

    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.H6(model_name, className="mb-0"),
                    dbc.Badge(status, color="info", className="ms-2"),
                ],
                className="d-flex align-items-center"
            ),
            dbc.CardBody(
                [
                    html.Div(f"Version: {version}", className="small text-muted mb-2"),
                    html.Hr(className="my-2"),
                    html.Div(metric_rows),
                    html.Hr(className="my-2"),
                    html.Div(f"Last Trained: {last_trained or 'N/A'}", className="small text-muted mt-2"),
                ]
            ),
        ],
        className="mb-4 shadow-sm border-info",
    )
