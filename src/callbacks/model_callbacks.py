"""
Callbacks to fetch MLflow/DVC model info.
"""

from dash import callback, Input, Output, html
from src.integrations.mlflow_client import mlflow_client
from src.integrations.dvc_client import dvc_client
from src.components.model_info_card import create_model_info_card


@callback(
    Output("model-info-container", "children"),
    Input("refresh-button", "n_clicks"),
)
def update_model_info(n_clicks: int) -> html.Div:
    """
    Updates the model info card in the sidebar.

    Args:
        n_clicks: Refresh button clicks.

    Returns:
        html.Div: Model info card component or empty state.
    """
    # Fetch from MLflow
    model_name = "derogation_model"
    model_info = mlflow_client.get_registered_model_info(model_name)
    
    if not model_info:
        # Fallback to DVC metrics if MLflow is not configured
        dvc_metrics = dvc_client.get_metrics()
        if dvc_metrics:
            return create_model_info_card(
                model_name=model_name,
                version="DVC-Tracked",
                status="Active",
                metrics=dvc_metrics,
                last_trained="Recently"
            )
        else:
            return html.Div("Model registry not configured.", className="small text-muted italic")

    return create_model_info_card(
        model_name=model_info["name"],
        version=model_info["version"],
        status=model_info["status"],
        metrics=model_info["metrics"],
        last_trained=model_info["last_trained"]
    )
