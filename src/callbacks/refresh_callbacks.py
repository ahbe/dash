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
    Output("datasets-store", "data", allow_duplicate=True),
    Input("refresh-button", "n_clicks"),
    Input("reload-data-button", "n_clicks"),
    Input("load-csv-button", "n_clicks"),
    Input("load-sharepoint-button", "n_clicks"),
    Input("load-cos-button", "n_clicks"),
    State("data-source-select", "value"),
    State("csv-file-path", "value"),
    State("sharepoint-file-path", "value"),
    State("cos-object-key", "value"),
    State("active-dataset-id", "data"),
    State("datasets-store", "data"),
    prevent_initial_call=True,
)
def handle_manual_refresh(
    refresh_n, reload_n, csv_n, sp_n, cos_n,
    selected_source, csv_path, sp_path, cos_key,
    active_id, datasets
) -> tuple:
    """
    Clears the cache and reloads data for the ACTIVE dataset when any refresh/load button is clicked.
    """
    if not ctx.triggered or not active_id:
        return no_update, no_update, no_update

    trigger_id = ctx.triggered_id
    logger.info(f"Data refresh for {active_id} triggered by: {trigger_id}. Clearing data cache and reloading...")

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
        return f"Refresh failed at {datetime.now().strftime('%H:%M:%S')}", no_update, no_update

    # Update the specific dataset in the store to maintain isolation
    new_datasets = datasets.copy()
    if active_id in new_datasets:
        new_datasets[active_id]["data"] = df.to_dict("records")
        new_datasets[active_id]["row_count"] = len(df)
        new_datasets[active_id]["col_count"] = len(df.columns)
        new_datasets[active_id]["filename"] = query.split("/")[-1]

    new_ts = datetime.now().strftime("%H:%M:%S")
    return f"Last updated: {new_ts}", df.to_dict("records"), new_datasets
