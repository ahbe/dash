"""
Callbacks to update charts based on filtered data.
"""

from typing import Any, Dict, List
import pandas as pd
import plotly.express as px
from dash import callback, Input, Output, ALL, ctx, MATCH, html, no_update, State
import dash_bootstrap_components as dbc
from src.utils.logger import logger


@callback(
    Output({"type": "chart", "index": ALL}, "figure"),
    Input({"type": "data-table", "index": "raw-data-table"}, "data"),
)
def update_charts(table_data: List[Dict[str, Any]]) -> List[Any]:
    """
    Updates all charts when data changes.

    Args:
        table_data: Filtered data from the table.

    Returns:
        List[Any]: Updated Plotly figures.
    """
    df = pd.DataFrame(table_data)
    
    if df.empty:
        return [px.scatter(title="No data available") for _ in ctx.outputs_list]

    figures = []
    for output in ctx.outputs_list:
        chart_id = output["id"]["index"]
        
        if chart_id == "derogation-trend":
            # Group by date
            trend_df = df.groupby("date").agg({"derogation_pct": "mean"}).reset_index()
            fig = px.line(trend_df, x="date", y="derogation_pct", title="Average Derogation % over Time")
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1D", step="day", stepmode="backward"),
                        dict(count=7, label="1W", step="day", stepmode="backward"),
                        dict(count=1, label="1M", step="month", stepmode="backward"),
                        dict(count=6, label="6M", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1Y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                )
            )
            
        elif chart_id == "brand-distribution":
            fig = px.pie(df, names="brand", values="usage_count", title="Usage by Brand")
            
        elif chart_id == "segment-performance":
            fig = px.bar(df, x="segment", y="converted_margin", color="brand", barmode="group", title="Margin by Segment")
            
        elif chart_id == "purpose-analysis":
            fig = px.bar(df, x="purpose", y="derogation_bps", title="Avg Derogation (bps) by Purpose")
            
        else:
            fig = px.scatter(title=f"Unknown chart: {chart_id}")
            
        fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
        figures.append(fig)
        
    return figures


@callback(
    Output("fs-chart-modal", "is_open", allow_duplicate=True),
    Output("fs-chart-title", "children", allow_duplicate=True),
    Output("fs-chart-graph", "figure", allow_duplicate=True),
    Input({"type": "chart-expand", "index": ALL}, "n_clicks"),
    State({"type": "chart", "index": ALL}, "figure"),
    prevent_initial_call=True,
)
def expand_default_chart(n_clicks, figures):
    """Expands a default chart into the fullscreen modal."""
    if not any(n_clicks):
        return no_update, no_update, no_update

    trig = ctx.triggered_id
    if isinstance(trig, dict) and trig.get("type") == "chart-expand":
        chart_id = trig["index"]
        
        # Find the figure in the states list based on index
        # ctx.states_list[0] contains the State({"type": "chart", "index": ALL}, "figure")
        if hasattr(ctx, 'states_list') and ctx.states_list and len(ctx.states_list) > 0:
            for item in ctx.states_list[0]:
                if item["id"]["index"] == chart_id:
                    fig = item["value"]
                    title = fig.get("layout", {}).get("title", {}).get("text", "Chart")
                    return True, title, fig

    return no_update, no_update, no_update


@callback(
    Output({"type": "chart-selection", "index": MATCH}, "children"),
    Input({"type": "chart", "index": MATCH}, "selectedData"),
)
def update_chart_selection_summary(selected_data):
    """Displays summary statistics for selected data points in default charts."""
    if not selected_data or "points" not in selected_data or not selected_data["points"]:
        return None
    
    points = selected_data["points"]
    count = len(points)
    y_values = [p.get("y") for p in points if p.get("y") is not None]
    
    if not y_values:
        return html.Span(f"Selected {count} points", className="text-info")
    
    try:
        df_y = pd.Series(y_values)
        return html.Div([
            html.Span([html.I(className="bi bi-info-circle me-1"), f"Selected {count} pts"], className="me-3"),
            html.Span([html.B("Avg: "), f"{df_y.mean():.2f}"], className="me-3"),
            html.Span([html.B("Max: "), f"{df_y.max():.2f}"], className="me-1"),
        ], className="text-info d-flex align-items-center flex-wrap")
    except Exception:
        return html.Span(f"Selected {count} points", className="text-info")
