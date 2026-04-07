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
) -> html.Div:
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
        html.Div: Chart component wrapped in a Div for layout tracking.
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

    return html.Div(
        id={"type": "chart-block", "index": chart_id},
        children=dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.Div(
                            [
                                html.Div([
                                    html.H5(title, className="mb-0 d-inline-block"),
                                    dbc.Badge(chart_type.value.title(), color="secondary", className="ms-2 small"),
                                ]),
                                html.Small(subtitle, className="text-muted") if subtitle else None,
                            ]
                        ),
                        html.Div([
                            dbc.Button(
                                html.I(className="bi bi-arrows-fullscreen"),
                                id={"type": "chart-expand", "index": chart_id},
                                color="link",
                                size="sm",
                                className="p-0 text-muted me-2",
                            ),
                            dbc.Button(
                                html.I(className="bi bi-download"),
                                id={"type": "chart-download", "index": chart_id},
                                color="link",
                                size="sm",
                                className="p-0 text-muted",
                            ),
                        ]),
                    ],
                    className="d-flex justify-content-between align-items-center",
                ),
                dbc.CardBody(
                    [
                        dcc.Graph(
                            id={"type": "chart", "index": chart_id},
                            figure=fig,
                            config={
                                "displayModeBar": True,
                                "scrollZoom": True,
                                "toImageButtonOptions": {"format": "png", "filename": f"chart_{chart_id}"},
                            },
                            style={"height": "100%", "width": "100%"},
                            responsive=True,
                        ),
                        html.Div(id={"type": "chart-selection", "index": chart_id}, className="small mt-2")
                    ],
                    className="p-1 d-flex flex-column",
                    style={"flex": "1", "minHeight": "0"}
                ),
            ],
            className="mb-4 shadow-sm resizable-tile",
            style={"display": "flex", "flexDirection": "column"}
        )
    )
