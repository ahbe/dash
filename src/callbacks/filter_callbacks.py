"""
Callbacks for all filter interactions.
Uses pattern-matching callbacks to handle generic filter components.
"""

from typing import Any, Dict, List
import pandas as pd
from dash import callback, Input, Output, State, ALL
from src.utils.logger import logger
from src.data.data_manager import data_manager
from src.data.transformers.filter_transformer import FilterTransformer


@callback(
    Output({"type": "data-table", "index": "raw-data-table"}, "data", allow_duplicate=True),
    Output({"type": "data-table", "index": "raw-data-table"}, "columns", allow_duplicate=True),
    Input({"type": "filter", "index": ALL}, "value"),
    Input({"type": "date-filter", "index": ALL}, "start_date"),
    Input({"type": "date-filter", "index": ALL}, "end_date"),
    Input("active-dataset-id", "data"),
    State({"type": "filter", "index": ALL}, "id"),
    State({"type": "date-filter", "index": ALL}, "id"),
    State("datasets-store", "data"),
    prevent_initial_call="initial_duplicate",
)
def update_data_on_filter(
    values: List[Any],
    start_dates: List[Any],
    end_dates: List[Any],
    active_id: str,
    ids: List[Dict[str, str]],
    date_ids: List[Dict[str, str]],
    datasets: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Updates the global data state when any filter changes or when the active dataset changes.
    """
    if not active_id or not datasets or active_id not in datasets:
        return [], []

    logger.info(f"Filter/Dataset change detected for {active_id}. Re-filtering data...")

    # Map standard filter IDs to values
    filter_dict = {id_obj["index"]: val for id_obj, val in zip(ids, values)}

    # Map date filter IDs to (start, end) tuples
    for d_id, start, end in zip(date_ids, start_dates, end_dates):
        filter_dict[d_id["index"]] = (start, end)

    # Get raw data from the datasets store (isolated by active_id)
    raw_data = datasets[active_id]["data"]
    df = pd.DataFrame(raw_data)
    
    # Transform
    transformer = FilterTransformer()
    filtered_df = transformer.transform(df, filters=filter_dict)
    
    logger.info(f"Data filtered for active tab: {len(filtered_df)} rows remaining.")
    
    columns = [{"name": i, "id": i} for i in filtered_df.columns]
    return filtered_df.to_dict("records"), columns


@callback(
    Output({"type": "filter", "index": ALL}, "options"),
    Input("active-dataset-id", "data"),
    Input("datasets-store", "data"),
    State({"type": "filter", "index": ALL}, "id"),
    prevent_initial_call="initial_duplicate"
)
def update_filter_options(active_id, datasets, filter_ids):
    """
    Populates filter dropdowns with unique values from the dataset.
    """
    if not active_id or not datasets or active_id not in datasets:
        return [[] for _ in filter_ids]

    df = pd.DataFrame(datasets[active_id]["data"])
    
    options_list = []
    for f_id in filter_ids:
        col_name = f_id["index"]
        if col_name in df.columns:
            unique_vals = sorted(df[col_name].dropna().unique())
            options = [{"label": str(v), "value": v} for v in unique_vals]
            options_list.append(options)
        else:
            options_list.append([])
            
    return options_list
