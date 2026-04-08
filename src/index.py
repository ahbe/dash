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
import src.callbacks.layout_callbacks
import src.callbacks.dataset_callbacks
import src.callbacks.filter_callbacks
import src.callbacks.chart_callbacks
import src.callbacks.metric_callbacks
import src.callbacks.alert_callbacks
import src.callbacks.graph_builder_callbacks
import src.callbacks.refresh_callbacks
import src.callbacks.model_callbacks

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
            dcc.Store(id="datasets-store", storage_type="session", data={}),
            dcc.Store(id="active-dataset-id", storage_type="session", data=None),
            dcc.Download(id="download-graph-data"),
            dcc.Download(id="download-report"),
            create_graph_builder_modal(),
            create_header(),
            
            # Dataset Tab Bar
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    id="dataset-tabs-container",
                                    className="d-flex align-items-center overflow-auto flex-nowrap"
                                ),
                                width="auto"
                            ),
                            dbc.Col(
                                dbc.Button(
                                    [html.I(className="bi bi-plus-circle me-2"), "Add Dataset"],
                                    id="add-dataset-button",
                                    color="outline-primary",
                                    size="sm",
                                    className="ms-2"
                                ),
                                width="auto"
                            ),
                            dbc.Col(
                                dbc.Button(
                                    [html.I(className="bi bi-file-earmark-pdf me-2"), "Download Full Report"],
                                    id="download-report-button",
                                    color="success",
                                    size="sm",
                                    className="ms-auto"
                                ),
                                width="auto",
                                className="ms-auto pe-4"
                            )
                        ],
                        className="bg-light border-bottom py-2 px-3 align-items-center sticky-top",
                        style={"top": "0", "zIndex": "1020"}
                    )
                ],
                id="dataset-management-bar"
            ),

            html.Div(
                id="dashboard-content-container",
                children=dbc.Row(
                    [
                        dbc.Col(create_sidebar(), width=12, md=3, lg=2, className="px-0"),
                        dbc.Col(
                            dcc.Loading(
                                id="main-content-loading",
                                type="default",
                                children=create_main_content(),
                                overlay_style={"visibility": "visible", "filter": "blur(2px)"},
                            ),
                            width=12, md=9, lg=10, id="main-content-area"
                        ),
                    ],
                    className="g-0",
                ),
            ),
            # Toast for notifications
            html.Div(id="notification-toast-container", style={"position": "fixed", "top": 66, "right": 10, "width": 350, "zIndex": 9999}),
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
