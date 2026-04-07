"""
Graph builder modal component.
"""

from dash import dcc, html
import dash_bootstrap_components as dbc

CHART_TYPES = [
    {"label": "Line Chart", "value": "line", "icon": "bi bi-graph-up"},
    {"label": "Bar Chart", "value": "bar", "icon": "bi bi-bar-chart-fill"},
    {"label": "Horizontal Bar", "value": "hbar", "icon": "bi bi-bar-chart-steps"},
    {"label": "Scatter Plot", "value": "scatter", "icon": "bi bi-dot"},
    {"label": "Area Chart", "value": "area", "icon": "bi bi-area-chart"},
    {"label": "Stacked Bar", "value": "stacked_bar", "icon": "bi bi-bar-chart-fill"},
    {"label": "Stacked Area", "value": "stacked_area", "icon": "bi bi-area-chart"},
    {"label": "Pie Chart", "value": "pie", "icon": "bi bi-pie-chart-fill"},
    {"label": "Donut Chart", "value": "donut", "icon": "bi bi-circle-fill"},
    {"label": "Histogram", "value": "histogram", "icon": "bi bi-reception-4"},
    {"label": "Box Plot", "value": "box", "icon": "bi bi-box"},
    {"label": "Heatmap", "value": "heatmap", "icon": "bi bi-grid-3x3-gap-fill"},
    {"label": "Bubble Chart", "value": "bubble", "icon": "bi bi-record-circle"},
    {"label": "Candlestick", "value": "candlestick", "icon": "bi bi-align-middle"},
]

def create_graph_builder_modal() -> html.Div:
    """
    Creates the modal for custom graph configuration and other supporting modals.
    """
    return html.Div([
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Create Custom Graph"), close_button=True),
                dbc.ModalBody(
                    [
                        dbc.Row(
                            [
                                # Left Panel: Configuration
                                dbc.Col(
                                    [
                                        html.Div([
                                            html.H6("Axis Configuration", className="fw-bold mb-3"),
                                            
                                            html.Label("X-Axis (Dimension/Time)", className="small fw-bold"),
                                            dcc.Dropdown(id="gb-x-axis", placeholder="Select column...", className="mb-3"),
                                            
                                            html.Label("Y-Axis (Measures - Multi-select)", className="small fw-bold"),
                                            dcc.Dropdown(id="gb-y-axis", multi=True, placeholder="Select columns...", className="mb-2"),
                                            
                                            dbc.Checklist(
                                                options=[{"label": "Use Secondary Y-Axis", "value": "enable"}],
                                                value=[],
                                                id="gb-secondary-y",
                                                switch=True,
                                                className="mb-3 small",
                                            ),
                                            
                                            html.Label("Aggregation Method", className="small fw-bold"),
                                            dcc.Dropdown(
                                                id="gb-aggregation",
                                                options=[
                                                    {"label": "None (Raw Data)", "value": "none"},
                                                    {"label": "Sum", "value": "sum"},
                                                    {"label": "Average", "value": "mean"},
                                                    {"label": "Count", "value": "count"},
                                                    {"label": "Min", "value": "min"},
                                                    {"label": "Max", "value": "max"},
                                                    {"label": "Median", "value": "median"},
                                                ],
                                                value="none",
                                                className="mb-3",
                                            ),
                                            
                                            html.Label("Group By / Color By", className="small fw-bold"),
                                            dcc.Dropdown(id="gb-group-by", placeholder="Optional category...", className="mb-3"),

                                            html.Hr(),
                                            html.H6("Display Options", className="fw-bold mb-3"),
                                            
                                            dbc.Row([
                                                dbc.Col([
                                                    html.Label("X-Axis Label", className="small"),
                                                    dbc.Input(id="gb-x-label", size="sm", className="mb-2"),
                                                ], width=6),
                                                dbc.Col([
                                                    html.Label("Y-Axis Label", className="small"),
                                                    dbc.Input(id="gb-y-label", size="sm", className="mb-2"),
                                                ], width=6),
                                            ]),

                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Checklist(
                                                        options=[{"label": "Show Labels", "value": "show"}],
                                                        value=[], id="gb-show-labels", switch=True, className="small mb-2",
                                                    ),
                                                ], width=6),
                                                dbc.Col([
                                                    dbc.Checklist(
                                                        options=[{"label": "Show Grid", "value": "show"}],
                                                        value=["show"], id="gb-show-grid", switch=True, className="small mb-2",
                                                    ),
                                                ], width=6),
                                            ]),

                                            html.Label("Sort Order", className="small fw-bold"),
                                            dcc.Dropdown(
                                                id="gb-sort-order",
                                                options=[
                                                    {"label": "None", "value": "none"},
                                                    {"label": "Ascending", "value": "asc"},
                                                    {"label": "Descending", "value": "desc"},
                                                ],
                                                value="none",
                                                className="mb-3",
                                            ),
                                        ], className="pe-3"),
                                    ],
                                    md=4,
                                    className="border-end",
                                    style={"maxHeight": "70vh", "overflowY": "auto"}
                                ),
                                
                                # Right Panel: Chart Selection & Preview
                                dbc.Col(
                                    [
                                        html.H6("Chart Type", className="fw-bold mb-3"),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.I(className=ct["icon"], style={"fontSize": "1.5rem"}),
                                                                html.Span(ct["label"], className="small mt-1")
                                                            ],
                                                            className="d-flex flex-column align-items-center p-2 border rounded chart-type-card",
                                                            id={"type": "gb-ct", "index": ct["value"]},
                                                            n_clicks=0,
                                                            style={"width": "100px", "cursor": "pointer"}
                                                        ) for ct in CHART_TYPES
                                                    ],
                                                    className="d-flex flex-wrap gap-2 mb-4"
                                                )
                                            ],
                                            id="gb-chart-type-selector-container",
                                        ),
                                        
                                        dcc.Store(id="gb-selected-chart-type", data="line"),
                                        
                                        html.Div([
                                            html.H6("Chart Preview", className="fw-bold d-inline-block me-2"),
                                            dbc.Badge("Real-time", color="info", pill=True, className="align-middle"),
                                        ], className="mb-2"),
                                        
                                        dcc.Loading(
                                            html.Div(
                                                dcc.Graph(
                                                    id="gb-preview-graph",
                                                    style={"height": "400px"},
                                                    config={
                                                        "displayModeBar": True,
                                                        "scrollZoom": True,
                                                        "modeBarButtonsToAdd": [
                                                            "drawline",
                                                            "drawopenpath",
                                                            "drawclosedpath",
                                                            "drawcircle",
                                                            "drawrect",
                                                            "eraselayer",
                                                        ],
                                                    }
                                                ),
                                                className="border rounded bg-white"
                                            )
                                        ),
                                        
                                        html.Div(id="gb-selection-summary", className="mt-2"),
                                        html.Div(id="gb-validation-msg", className="text-danger small mt-2"),
                                    ],
                                    md=8,
                                    className="ps-3"
                                ),
                            ]
                        ),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Chart Title", className="small fw-bold"),
                                        dbc.Input(id="gb-title", placeholder="My Custom Chart", className="mb-2"),
                                    ],
                                    md=6,
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Color Theme", className="small fw-bold"),
                                        dcc.Dropdown(
                                            id="gb-theme",
                                            options=[
                                                {"label": "Default (Modern)", "value": "plotly"},
                                                {"label": "Pastel", "value": "ggplot2"},
                                                {"label": "Vibrant", "value": "seaborn"},
                                                {"label": "Dark Mode", "value": "plotly_dark"},
                                                {"label": "Monochrome", "value": "none"},
                                            ],
                                            value="plotly",
                                            className="mb-2",
                                        ),
                                    ],
                                    md=6,
                                ),
                            ]
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button("Cancel", id="gb-cancel-button", color="secondary", outline=True, className="me-auto"),
                        dbc.Button("Reset Settings", id="gb-reset-button", color="warning", outline=True, className="me-2"),
                        dbc.Button(
                            [html.I(className="bi bi-plus-lg me-2"), "Add to Dashboard"],
                            id="gb-add-button",
                            color="success",
                            disabled=True
                        ),
                    ]
                ),
            ],
            id="graph-builder-modal",
            size="xl",
            is_open=False,
            backdrop="static",
        ),
        
        # Full Screen Modal
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(id="fs-chart-title"), close_button=True),
                dbc.ModalBody(
                    [
                        dcc.Graph(
                            id="fs-chart-graph",
                            style={"height": "75vh"},
                            config={"displayModeBar": True, "scrollZoom": True}
                        ),
                        html.Div(id="fs-selection-summary", className="mt-3")
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="fs-close-button", color="secondary")
                ),
            ],
            id="fs-chart-modal",
            size="xl",
            is_open=False,
        )
    ])
