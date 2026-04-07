"""
Main layout assembly.
Composes the full dashboard page by combining header, sidebar, main content, and footer.
"""

import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input
from src.app import app
from src.layouts.header import create_header
from src.layouts.sidebar import create_sidebar
from src.layouts.main_content import create_main_content
from src.layouts.footer import create_footer
from src.components.graph_builder_modal import create_graph_builder_modal
import src.callbacks.layout_callbacks # Import callbacks to register them

def serve_layout() -> dbc.Container:
    """
    Assembles and returns the full application layout.

    Returns:
        dbc.Container: Full layout container.
    """
    # Trigger initial data load
    from src.data.data_manager import data_manager
    data_manager.get_data("csv", query="data/sample/sample_data.csv")
    
    return dbc.Container(
        [
            dcc.Store(id="custom-graphs-store", storage_type="session", data=[]),
            dcc.Store(id="available-columns-store", data=[]),
            dcc.Download(id="download-graph-data"),
            create_graph_builder_modal(),
            create_header(),
            html.Div(id="dashboard-content-container", children=dbc.Row(
                [
                    dbc.Col(create_sidebar(), width=12, md=3, lg=2, className="px-0"),
                    dbc.Col(create_main_content(), width=12, md=9, lg=10, id="main-content-area"),
                ],
                className="g-0",
            )),
            create_footer(),
        ],
        fluid=True,
        className="px-0",
    )


# Set the app layout
app.layout = html.Div([
    serve_layout(),
    html.Div(id="dummy-output-layout", style={"display": "none"})
])
