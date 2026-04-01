"""
Callbacks for manual and scheduled data refresh.
"""

from datetime import datetime
from dash import callback, Input, Output, State, no_update
from src.data.data_manager import data_manager
from src.utils.logger import logger


@callback(
    Output("refresh-timestamp", "children"),
    Output("raw-data-table", "data", allow_duplicate=True),
    Input("refresh-button", "n_clicks"),
    prevent_initial_call=True,
)
def handle_manual_refresh(n_clicks: int) -> tuple[str, list[dict]]:
    """
    Clears the cache and reloads data when the refresh button is clicked.

    Args:
        n_clicks: Number of button clicks.

    Returns:
        tuple: New timestamp string and reloaded data.
    """
    if n_clicks is None:
        return no_update

    logger.info("Manual refresh triggered by user.")
    
    # Clear cache
    data_manager.refresh_all()
    
    # Reload data
    df = data_manager.get_data("csv", query="data/sample/sample_data.csv")
    
    new_ts = datetime.now().strftime("%H:%M:%S")
    return f"Last updated: {new_ts}", df.to_dict("records")
