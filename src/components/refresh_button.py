"""
Manual data refresh button component.
Shows last refresh timestamp.
"""

from datetime import datetime
from typing import Optional
from dash import html
import dash_bootstrap_components as dbc


def create_refresh_button(
    last_refresh: Optional[datetime] = None,
) -> html.Div:
    """
    Creates a refresh button with a timestamp.

    Args:
        last_refresh: When the data was last refreshed.

    Returns:
        html.Div: Refresh button and timestamp.
    """
    ts_str = last_refresh.strftime("%H:%M:%S") if last_refresh else "Never"

    return html.Div(
        [
            dbc.Button(
                [
                    html.I(className="bi bi-arrow-clockwise me-2"),
                    "Refresh Data"
                ],
                id="refresh-button",
                color="outline-secondary",
                size="sm",
                className="me-2"
            ),
            html.Small(
                f"Last updated: {ts_str}",
                id="refresh-timestamp",
                className="text-muted"
            )
        ],
        className="d-flex align-items-center"
    )
