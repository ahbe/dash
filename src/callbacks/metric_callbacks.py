"""
Callbacks to update metric cards with live data.
"""

from typing import Any, Dict, List
import pandas as pd
from dash import callback, Input, Output, ALL
from src.data.transformers.metric_transformer import MetricTransformer


@callback(
    Output({"type": "metric-value", "index": ALL}, "children"),
    Input({"type": "data-table", "index": "raw-data-table"}, "data"),
)
def update_metrics(table_data: List[Dict[str, Any]]) -> List[Any]:
    """
    Computes and updates metrics when data changes.

    Args:
        table_data: Data from the main table.

    Returns:
        List[Any]: Updated values for each metric card.
    """
    df = pd.DataFrame(table_data)
    
    transformer = MetricTransformer()
    metrics = transformer.transform(df)
    
    # Mapping of metric_id to computed value
    mapping = {
        "derogation-pct": f"{metrics['derogation_pct']:.1f}%",
        "derogation-bps": f"{metrics['derogation_bps']:.1f}",
        "usage-count": f"{metrics['usage_count']:,}",
        "failed-calls": f"{metrics['failed_calls']:,}",
        "converted-margin": f"€{metrics['converted_margin']:,.0f}",
        "conversion-rate": f"{metrics['conversion_rate']:.1f}%",
    }
    
    # We need to return the list in the same order as pattern-matching indices
    # However, pattern-matching callback order depends on how they are rendered.
    # To be safe, we'd normally use State to get the order, but here we'll assume standard layout order.
    # In production, use ctx.outputs_list to match exactly.
    from dash import ctx
    
    output_values = []
    for output in ctx.outputs_list:
        metric_id = output["id"]["index"]
        output_values.append(mapping.get(metric_id, "N/A"))
        
    return output_values
