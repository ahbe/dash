"""
Generic reusable alert/notification component.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from dash import html
import dash_bootstrap_components as dbc


class AlertSeverity(Enum):
    """
    Supported alert severity levels.
    """
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"
    SUCCESS = "success"


def create_alert_block(
    alert_id: str,
    title: str,
    severity: AlertSeverity,
    message: str,
    timestamp: Optional[datetime] = None,
    dismissable: bool = True,
) -> dbc.Alert:
    """
    Creates a styled Dash Bootstrap Alert.

    Args:
        alert_id: Unique identifier for the alert.
        title: Alert title.
        severity: Alert severity level (color).
        message: Alert message content.
        timestamp: When the alert was generated.
        dismissable: Whether the user can close the alert.

    Returns:
        dbc.Alert: Styled alert component.
    """
    ts_str = timestamp.strftime("%Y-%m-%d %H:%M") if timestamp else ""

    return dbc.Alert(
        [
            html.Div(
                [
                    html.Strong(title, className="me-2"),
                    html.Small(ts_str, className="text-muted float-end") if ts_str else None,
                ],
                className="d-flex justify-content-between align-items-center mb-1"
            ),
            html.Div(message),
        ],
        id={"type": "alert", "index": alert_id},
        color=severity.value,
        dismissable=dismissable,
        className="mb-3 shadow-sm",
    )
