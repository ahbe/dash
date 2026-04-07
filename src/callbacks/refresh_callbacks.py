"""
Callbacks for manual and scheduled data refresh.
"""

from datetime import datetime
import dash
from dash import callback, Input, Output, State, no_update, ctx
from src.data.data_manager import data_manager
from src.utils.logger import logger


@callback(
    Output("csv-input-group", "style"),
    Output("sharepoint-input-group", "style"),
    Output("cos-input-group", "style"),
    Input("data-source-select", "value"),
)
def toggle_source_inputs(selected_source: str) -> tuple[dict, dict, dict]:
    """
    Shows/hides input groups based on the selected data source.
    """
    styles = [{"display": "none"}] * 3
    if selected_source == "csv":
        styles[0] = {"display": "flex"}
    elif selected_source == "sharepoint":
        styles[1] = {"display": "flex"}
    elif selected_source == "cos":
        styles[2] = {"display": "flex"}
    return tuple(styles)


@callback(
    Output("refresh-timestamp", "children"),
    Output({"type": "data-table", "index": "raw-data-table"}, "data", allow_duplicate=True),
    Input("refresh-button", "n_clicks"),
    Input("reload-data-button", "n_clicks"),
    Input("load-csv-button", "n_clicks"),
    Input("load-sharepoint-button", "n_clicks"),
    Input("load-cos-button", "n_clicks"),
    State("data-source-select", "value"),
    State("csv-file-path", "value"),
    State("sharepoint-file-path", "value"),
    State("cos-object-key", "value"),
    prevent_initial_call=True,
)
def handle_manual_refresh(
    refresh_n, reload_n, csv_n, sp_n, cos_n,
    selected_source, csv_path, sp_path, cos_key
) -> tuple[str, list[dict]]:
    """
    Clears the cache and reloads data when any refresh/load button is clicked.
    """
    if not ctx.triggered:
        return no_update

    trigger_id = ctx.triggered_id
    logger.info(f"Data refresh triggered by: {trigger_id}. Clearing data cache and reloading...")

    # Clear cache
    data_manager.refresh_all()

    # Determine query based on source and inputs
    query = "data/sample/sample_data.csv"
    if selected_source == "csv":
        query = csv_path or "data/sample/sample_data.csv"
    elif selected_source == "sharepoint":
        query = sp_path or "path/to/sharepoint/file.xlsx"
    elif selected_source == "cos":
        query = cos_key or "bucket_name/object_key.csv"

    # Fetch data
    df = data_manager.get_data(selected_source, query=query)
    
    if df.empty:
        logger.warning(f"No data returned for source {selected_source} with query {query}")

    new_ts = datetime.now().strftime("%H:%M:%S")
    return f"Last updated: {new_ts}", df.to_dict("records")
