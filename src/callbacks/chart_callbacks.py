"""
Callbacks to update charts based on filtered data.
"""

from typing import Any, Dict, List
import pandas as pd
import plotly.express as px
from dash import callback, Input, Output, ALL, ctx
from src.utils.logger import logger


@callback(
    Output({"type": "chart", "index": ALL}, "figure"),
    Input("raw-data-table", "data"),
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
