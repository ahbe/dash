"""
Callbacks for dataset management (tabs, adding, switching, closing).
"""

import uuid
import pandas as pd
from dash import callback, Input, Output, State, ALL, ctx, no_update, html
import dash_bootstrap_components as dbc
from src.data.data_manager import data_manager
from src.utils.logger import logger

@callback(
    Output("datasets-store", "data", allow_duplicate=True),
    Output("active-dataset-id", "data", allow_duplicate=True),
    Output("notification-toast-container", "children", allow_duplicate=True),
    Input("add-dataset-button", "n_clicks"),
    State("datasets-store", "data"),
    prevent_initial_call=True,
)
def add_new_dataset(n_clicks, datasets):
    """Adds a sample dataset for demonstration (in a real app, this would open a file uploader)."""
    if not n_clicks:
        return no_update, no_update
    
    ds_id = str(uuid.uuid4())[:8]
    # Use a fresh copy of datasets to avoid shared state if any (though it's a State variable)
    new_datasets = datasets.copy() if datasets else {}
    
    # In a real implementation, we might have multiple sample files
    filename = "sample_data.csv"
    query = "data/sample/sample_data.csv"
        
    # Get a fresh copy of the data
    df = data_manager.get_data("csv", query=query).copy()
    
    # Simulate different data if it's Dataset 2+ for demonstration
    if len(datasets) >= 1:
        # Just shuffle or take a sample or modify slightly so it's clearly different
        df = df.sample(frac=0.8, random_state=len(datasets)).reset_index(drop=True)
        # Modify some values slightly
        numeric_cols = df.select_dtypes(include=['number']).columns
        if not numeric_cols.empty:
            df[numeric_cols[0]] = df[numeric_cols[0]] * (1.1 + (0.1 * len(datasets)))
    
    new_ds = {
        "id": ds_id,
        "name": f"Dataset {len(datasets) + 1}",
        "filename": f"variation_{len(datasets)}_{filename}",
        "row_count": len(df),
        "col_count": len(df.columns),
        "data": df.to_dict("records"),
        "columns": [{"name": c, "type": str(df[c].dtype)} for c in df.columns]
    }
    
    new_datasets[ds_id] = new_ds
    
    toast = dbc.Toast(
        f"Dataset '{new_ds['name']}' loaded successfully. {new_ds['row_count']} rows, {new_ds['col_count']} columns.",
        id="dataset-load-toast",
        header="Data Loaded",
        icon="success",
        duration=4000,
        is_open=True,
        style={"width": "100%"}
    )
    
    return new_datasets, ds_id, toast


@callback(
    Output("dataset-tabs-container", "children"),
    Input("datasets-store", "data"),
    Input("active-dataset-id", "data"),
)
def render_dataset_tabs(datasets, active_id):
    """Renders the horizontal tab bar for datasets."""
    if not datasets:
        return html.Div("No datasets loaded", className="text-muted small px-3")
    
    tabs = []
    for ds_id, ds in datasets.items():
        is_active = ds_id == active_id
        tabs.append(
            html.Div(
                [
                    html.I(className="bi bi-file-earmark-spreadsheet me-2"),
                    html.Span(ds["name"], className="tab-name"),
                    dbc.Badge(f"{ds['row_count']}", color="secondary", pill=True, className="tab-badge"),
                    html.I(className="bi bi-x tab-close", id={"type": "close-ds", "index": ds_id}),
                ],
                id={"type": "ds-tab", "index": ds_id},
                className=f"dataset-tab {'active' if is_active else ''}",
            )
        )
    return tabs


@callback(
    Output("active-dataset-id", "data", allow_duplicate=True),
    Input({"type": "ds-tab", "index": ALL}, "n_clicks"),
    State("active-dataset-id", "data"),
    prevent_initial_call=True,
)
def switch_active_dataset(n_clicks, current_active):
    """Switches the active dataset when a tab is clicked."""
    if not ctx.triggered:
        return current_active
    
    trig = ctx.triggered_id
    if isinstance(trig, dict) and trig.get("type") == "ds-tab":
        return trig["index"]
    
    return current_active


@callback(
    Output("datasets-store", "data", allow_duplicate=True),
    Output("active-dataset-id", "data", allow_duplicate=True),
    Input({"type": "close-ds", "index": ALL}, "n_clicks"),
    State("datasets-store", "data"),
    State("active-dataset-id", "data"),
    prevent_initial_call=True,
)
def close_dataset(n_clicks, datasets, active_id):
    """Removes a dataset and updates the active dataset if necessary."""
    if not any(n_clicks):
        return no_update, no_update
    
    trig = ctx.triggered_id
    if isinstance(trig, dict) and trig.get("type") == "close-ds":
        ds_id = trig["index"]
        if ds_id in datasets:
            del datasets[ds_id]
            
            # Update active ID if we closed the active one
            new_active = active_id
            if active_id == ds_id:
                new_active = list(datasets.keys())[0] if datasets else None
                
            return datasets, new_active
            
    return no_update, no_update


@callback(
    Output("datasets-store", "data", allow_duplicate=True),
    Output("active-dataset-id", "data", allow_duplicate=True),
    Input("dummy-output-layout", "children"), # Initial load trigger
    State("datasets-store", "data"),
    prevent_initial_call="initial_duplicate" # Allow initial call to duplicate outputs
)
def initial_dataset_load(_, existing_datasets):
    """Loads the initial dataset on app start if none exists."""
    if existing_datasets:
        return no_update, no_update
    
    # Load initial sample data
    df = data_manager.get_data("csv", query="data/sample/sample_data.csv")
    ds_id = "initial-ds"
    
    initial_ds = {
        "id": ds_id,
        "name": "Sample Data",
        "filename": "sample_data.csv",
        "row_count": len(df),
        "col_count": len(df.columns),
        "data": df.to_dict("records"),
        "columns": [{"name": c, "type": str(df[c].dtype)} for c in df.columns]
    }
    
    return {ds_id: initial_ds}, ds_id
