"""
Callbacks to evaluate thresholds and trigger alerts.
"""

from typing import Any, Dict, List
import pandas as pd
from dash import callback, Input, Output, html
from src.alerts.alert_engine import alert_engine
from src.data.transformers.metric_transformer import MetricTransformer
from src.components.alert_block import create_alert_block


@callback(
    Output("alerts-container", "children"),
    Input("raw-data-table", "data"),
)
def update_alerts(table_data: List[Dict[str, Any]]) -> List[html.Div]:
    """
    Evaluates data and displays alerts if thresholds are exceeded.

    Args:
        table_data: Current filtered data.

    Returns:
        List[html.Div]: List of alert components.
    """
    df = pd.DataFrame(table_data)
    
    # Compute current metrics
    transformer = MetricTransformer()
    metrics = transformer.transform(df)
    
    # Evaluate alerts
    triggered = alert_engine.evaluate(metrics)
    
    # Create alert components
    alert_components = [
        create_alert_block(
            alert_id=a["id"],
            title=a["title"],
            severity=a["severity"],
            message=a["message"],
            timestamp=a["timestamp"],
        )
        for a in triggered
    ]
    
    return alert_components
