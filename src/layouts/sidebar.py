"""
Sidebar layout component containing filters and navigation.
"""

from dash import html
import dash_bootstrap_components as dbc
from src.components.filter_block import create_filter_block, FilterType


def create_sidebar() -> html.Div:
    """
    Creates the application sidebar with filters.

    Returns:
        html.Div: Styled sidebar component.
    """
    return html.Div(
        [
            html.H5("Filters", className="mb-4"),
            create_filter_block(
                filter_id="brand",
                label="Brand",
                filter_type=FilterType.MULTI_DROPDOWN,
                options=[
                    {"label": "Brand A", "value": "Brand A"},
                    {"label": "Brand B", "value": "Brand B"},
                    {"label": "Brand C", "value": "Brand C"},
                ],
            ),
            create_filter_block(
                filter_id="segment",
                label="Segment",
                filter_type=FilterType.MULTI_DROPDOWN,
                options=[
                    {"label": "Retail", "value": "Retail"},
                    {"label": "Corporate", "value": "Corporate"},
                    {"label": "SME", "value": "SME"},
                ],
            ),
            create_filter_block(
                filter_id="purpose",
                label="Purpose",
                filter_type=FilterType.MULTI_DROPDOWN,
                options=[
                    {"label": "Home Loan", "value": "Home Loan"},
                    {"label": "Auto Loan", "value": "Auto Loan"},
                ],
            ),
            create_filter_block(
                filter_id="date_range",
                label="Date Range",
                filter_type=FilterType.DATE_RANGE,
            ),
            html.Hr(),
            html.H5("Data Controls", className="mb-4"),
            dbc.Select(
                id="data-source-select",
                options=[
                    {"label": "Local CSV", "value": "csv"},
                    {"label": "SharePoint", "value": "sharepoint"},
                    {"label": "COS", "value": "cos"},
                ],
                value="csv", # Default to CSV
                className="mb-3"
            ),
            dbc.InputGroup(
                [
                    dbc.Input(id="csv-file-path", placeholder="Enter CSV file path", value="data/sample/sample_data.csv"),
                    dbc.Button("Load CSV", id="load-csv-button", n_clicks=0, color="secondary"),
                ],
                className="mb-3",
                id="csv-input-group",
            ),
            dbc.InputGroup(
                [
                    dbc.Input(id="sharepoint-file-path", placeholder="Enter SharePoint file path"),
                    dbc.Button("Load SP", id="load-sharepoint-button", n_clicks=0, color="secondary"),
                ],
                className="mb-3",
                id="sharepoint-input-group",
                style={"display": "none"},
            ),
            dbc.InputGroup(
                [
                    dbc.Input(id="cos-object-key", placeholder="Enter COS object key"),
                    dbc.Button("Load COS", id="load-cos-button", n_clicks=0, color="secondary"),
                ],
                className="mb-3",
                id="cos-input-group",
                style={"display": "none"},
            ),
            dbc.Button("Reload Data", id="reload-data-button", color="primary", className="mb-4 w-100"),
            html.Hr(),
            dbc.Button(
                [html.I(className="bi bi-plus-circle me-2"), "Create Custom Graph"],
                id="open-graph-builder-button",
                color="success",
                className="mb-4 w-100 shadow-sm",
            ),
            html.Hr(),
            html.Div(
                [
                    html.H6("Model Info", className="mb-3"),
                    html.Div(id="model-info-container"),
                ]
            ),
        ],
        className="p-3 bg-light border-end h-100 shadow-sm",
        style={"minHeight": "calc(100vh - 76px)"},
    )
