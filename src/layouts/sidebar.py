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
