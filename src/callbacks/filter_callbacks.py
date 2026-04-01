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
    Output("raw-data-table", "data", allow_duplicate=True),
    Input({"type": "filter", "index": ALL}, "value"),
    State({"type": "filter", "index": ALL}, "id"),
    prevent_initial_call=True,
)
def update_data_on_filter(values: List[Any], ids: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Updates the global data state when any filter changes.

    Args:
        values: List of filter values from pattern-matching inputs.
        ids: List of filter IDs.

    Returns:
        List[Dict[str, Any]]: Filtered data for the table.
    """
    logger.info("Filter change detected. Re-filtering data...")
    
    # Map IDs to values
    filter_dict = {id_obj["index"]: val for id_obj, val in zip(ids, values)}
    
    # Get raw data (cached)
    # In a real app, you'd fetch from data_manager.get_data(...)
    # For now, we assume we have a global df or fetch it here
    df = data_manager.get_data("csv", query="data/sample/sample_data.csv")
    
    # Transform
    transformer = FilterTransformer()
    filtered_df = transformer.transform(df, filters=filter_dict)
    
    logger.info(f"Data filtered: {len(filtered_df)} rows remaining.")
    
    return filtered_df.to_dict("records")
