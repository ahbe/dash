"""
Generic reusable chart container.
Generates Plotly figures based on chart type and data.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


class ChartType(Enum):
    """
    Supported chart types.
    """
    BAR = "bar"
    LINE = "line"
    SCATTER = "scatter"
    PIE = "pie"
    HEATMAP = "heatmap"
    FUNNEL = "funnel"
    INDICATOR = "indicator"
    TREEMAP = "treemap"


def create_chart_block(
    chart_id: str,
    title: str,
    chart_type: ChartType,
    df: pd.DataFrame = pd.DataFrame(),
    x_field: Optional[str] = None,
    y_fields: Optional[List[str]] = None,
    color_field: Optional[str] = None,
    layout_overrides: Optional[Dict[str, Any]] = None,
    height: int = 400,
    subtitle: Optional[str] = None,
) -> dbc.Card:
    """
    Creates a styled chart container with a Plotly figure.

    Args:
        chart_id: Unique identifier for the chart.
        title: Chart title.
        chart_type: Type of chart to generate.
        df: Data for the chart.
        x_field: Column for the x-axis.
        y_fields: Columns for the y-axis.
        color_field: Column for color coding.
        layout_overrides: Custom Plotly layout settings.
        height: Chart height in pixels.
        subtitle: Optional chart subtitle.

    Returns:
        dbc.Card: Chart component wrapped in a Card.
    """
    fig = go.Figure()

    if not df.empty and x_field and y_fields:
        if chart_type == ChartType.BAR:
            fig = px.bar(df, x=x_field, y=y_fields, color=color_field, barmode="group")
        elif chart_type == ChartType.LINE:
            fig = px.line(df, x=x_field, y=y_fields, color=color_field)
        elif chart_type == ChartType.SCATTER:
            fig = px.scatter(df, x=x_field, y=y_fields[0], color=color_field)
        elif chart_type == ChartType.PIE:
            fig = px.pie(df, names=x_field, values=y_fields[0])
        elif chart_type == ChartType.HEATMAP:
            # Heatmap expects specific data structure, simplified here
            fig = px.density_heatmap(df, x=x_field, y=y_fields[0], z=y_fields[1] if len(y_fields) > 1 else None)
        elif chart_type == ChartType.TREEMAP:
            fig = px.treemap(df, path=[x_field], values=y_fields[0], color=color_field)
        # Add other types as needed

    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=height,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        **(layout_overrides or {})
    )

    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.Div(
                        [
                            html.H5(title, className="mb-0"),
                            html.Small(subtitle, className="text-muted") if subtitle else None,
                        ]
                    ),
                    dbc.Button(
                        html.I(className="bi bi-download"),
                        id={"type": "chart-download", "index": chart_id},
                        color="link",
                        size="sm",
                        className="p-0 text-muted",
                    ),
                ],
                className="d-flex justify-content-between align-items-center",
            ),
            dbc.CardBody(
                dcc.Graph(
                    id={"type": "chart", "index": chart_id},
                    figure=fig,
                    config={"displayModeBar": False},
                ),
                className="p-1",
            ),
        ],
        className="mb-4 shadow-sm",
    )
