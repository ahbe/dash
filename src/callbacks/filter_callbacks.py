"""
Callbacks for all filter interactions.
Uses pattern-matching callbacks to handle generic filter components.
"""

from typing import Any, Dict, List
from dash import callback, Input, Output, State, ALL
from src.utils.logger import logger
from src.data.data_manager import data_manager
from src.data.transformers.filter_transformer import FilterTransformer


@callback(
    Output({"type": "data-table", "index": "raw-data-table"}, "data", allow_duplicate=True),
    Input({"type": "filter", "index": ALL}, "value"),
    Input({"type": "date-filter", "index": ALL}, "start_date"),
    Input({"type": "date-filter", "index": ALL}, "end_date"),
    State({"type": "filter", "index": ALL}, "id"),
    State({"type": "date-filter", "index": ALL}, "id"),
    State("data-source-select", "value"),
    State("csv-file-path", "value"),
    State("sharepoint-file-path", "value"),
    State("cos-object-key", "value"),
    prevent_initial_call=True,
)
def update_data_on_filter(
    values: List[Any],
    start_dates: List[Any],
    end_dates: List[Any],
    ids: List[Dict[str, str]],
    date_ids: List[Dict[str, str]],
    selected_source: str,
    csv_path: str,
    sp_path: str,
    cos_key: str,
) -> List[Dict[str, Any]]:
    """
    Updates the global data state when any filter changes.

    Args:
        values: List of filter values from pattern-matching inputs.
        start_dates: List of start dates from date filters.
        end_dates: List of end dates from date filters.
        ids: List of standard filter IDs.
        date_ids: List of date filter IDs.

    Returns:
        List[Dict[str, Any]]: Filtered data for the table.
    """
    logger.info("Filter change detected. Re-filtering data...")

    # Map standard filter IDs to values
    filter_dict = {id_obj["index"]: val for id_obj, val in zip(ids, values)}

    # Map date filter IDs to (start, end) tuples
    for d_id, start, end in zip(date_ids, start_dates, end_dates):
        filter_dict[d_id["index"]] = (start, end)

    # Get raw data (cached)
    query = "data/sample/sample_data.csv"
    if selected_source == "csv":
        query = csv_path or "data/sample/sample_data.csv"
    elif selected_source == "sharepoint":
        query = sp_path or "path/to/sharepoint/file.xlsx"
    elif selected_source == "cos":
        query = cos_key or "bucket_name/object_key.csv"

    df = data_manager.get_data(selected_source, query=query)
    
    # Transform
    transformer = FilterTransformer()
    filtered_df = transformer.transform(df, filters=filter_dict)
    
    logger.info(f"Data filtered: {len(filtered_df)} rows remaining.")
    
    return filtered_df.to_dict("records")
