"""
Graph builder modal component.
"""

from dash import dcc, html
import dash_bootstrap_components as dbc

CHART_TYPES = [
    {"label": "Line Chart", "value": "line", "icon": "bi bi-graph-up", "description": "Best for trends over time"},
    {"label": "Bar Chart", "value": "bar", "icon": "bi bi-bar-chart-fill", "description": "Compare categories"},
    {"label": "Horizontal Bar", "value": "hbar", "icon": "bi bi-bar-chart-steps", "description": "Compare many categories"},
    {"label": "Scatter Plot", "value": "scatter", "icon": "bi bi-dot", "description": "Show relationship between variables"},
    {"label": "Area Chart", "value": "area", "icon": "bi bi-area-chart", "description": "Show magnitude over time"},
    {"label": "Stacked Bar", "value": "stacked_bar", "icon": "bi bi-bar-chart-fill", "description": "Part-to-whole over categories"},
    {"label": "Stacked Area", "value": "stacked_area", "icon": "bi bi-area-chart", "description": "Part-to-whole over time"},
    {"label": "Pie Chart", "value": "pie", "icon": "bi bi-pie-chart-fill", "description": "Simple part-to-whole"},
    {"label": "Donut Chart", "value": "donut", "icon": "bi bi-circle-fill", "description": "Part-to-whole with hole"},
    {"label": "Histogram", "value": "histogram", "icon": "bi bi-reception-4", "description": "Distribution of data"},
    {"label": "Box Plot", "value": "box", "icon": "bi bi-box", "description": "Statistical distribution summary"},
    {"label": "Heatmap", "value": "heatmap", "icon": "bi bi-grid-3x3-gap-fill", "description": "Density/Correlation matrix"},
    {"label": "Bubble Chart", "value": "bubble", "icon": "bi bi-record-circle", "description": "3D data on 2D plane"},
    {"label": "Candlestick", "value": "candlestick", "icon": "bi bi-align-middle", "description": "Financial OHLC data"},
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
                                            
                                            html.Div(id="gb-active-dataset-indicator", className="small text-muted mb-3 font-italic"),

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
                                        html.H6("Chart Type", className="fw-bold mb-3 text-center"),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.I(className=ct["icon"], style={"fontSize": "1.5rem"}),
                                                                html.Span(ct["label"], className="small mt-1 text-center")
                                                            ],
                                                            className="d-flex flex-column align-items-center p-2 border rounded chart-type-card",
                                                            id={"type": "gb-ct", "index": ct["value"]},
                                                            n_clicks=0,
                                                            style={"width": "120px", "cursor": "pointer"},
                                                            title=ct["description"]
                                                        ) for ct in CHART_TYPES
                                                    ],
                                                    className="d-flex flex-wrap gap-2 mb-4 justify-content-center"
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
        ),

        # Comparison Chart Modal
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Advanced Comparison Builder"), close_button=True),
                dbc.ModalBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div([
                                            html.H6("1. Data Selection", className="fw-bold mb-2"),
                                            html.Label("Select Datasets to Compare", className="small fw-bold text-muted"),
                                            dbc.Checklist(
                                                id="comp-datasets-list",
                                                options=[],
                                                value=[],
                                                className="mb-3 border rounded p-2 bg-white",
                                                style={"maxHeight": "150px", "overflowY": "auto"}
                                            ),
                                            
                                            html.Hr(),
                                            html.H6("2. Axis Configuration", className="fw-bold mb-2"),
                                            
                                            html.Label("Common X-Axis Column", className="small fw-bold"),
                                            dcc.Dropdown(id="comp-x-axis", placeholder="Choose common column...", className="mb-2"),
                                            
                                            html.Label("Y-Axis Column", className="small fw-bold"),
                                            dcc.Dropdown(id="comp-y-axis", placeholder="Choose column...", className="mb-2"),
                                            
                                            html.Label("Aggregation Method", className="small fw-bold"),
                                            dcc.Dropdown(
                                                id="comp-aggregation",
                                                options=[
                                                    {"label": "None (Raw Data)", "value": "none"},
                                                    {"label": "Sum", "value": "sum"},
                                                    {"label": "Average", "value": "mean"},
                                                    {"label": "Count", "value": "count"},
                                                    {"label": "Min", "value": "min"},
                                                    {"label": "Max", "value": "max"},
                                                ],
                                                value="mean",
                                                className="mb-2",
                                            ),

                                            html.Label("Comparison Type", className="small fw-bold"),
                                            dcc.Dropdown(
                                                id="comp-type",
                                                options=[
                                                    {"label": "Side-by-side Bars", "value": "side_bar"},
                                                    {"label": "Overlay Lines", "value": "overlay_line"},
                                                    {"label": "Stacked Areas", "value": "stacked_area"},
                                                    {"label": "Grouped Scatter", "value": "scatter"},
                                                ],
                                                value="side_bar",
                                                className="mb-2",
                                            ),
                                            
                                            dbc.Checklist(
                                                options=[{"label": "Normalize Scales (0-100%)", "value": "norm"}],
                                                value=[], id="comp-normalize", switch=True, className="small mb-2",
                                            ),

                                            html.Hr(),
                                            html.H6("3. Display Options", className="fw-bold mb-2"),
                                            
                                            dbc.Row([
                                                dbc.Col([
                                                    html.Label("X Label", className="small"),
                                                    dbc.Input(id="comp-x-label", size="sm", className="mb-2"),
                                                ], width=6),
                                                dbc.Col([
                                                    html.Label("Y Label", className="small"),
                                                    dbc.Input(id="comp-y-label", size="sm", className="mb-2"),
                                                ], width=6),
                                            ]),
                                            
                                            html.Label("Sort Order", className="small fw-bold"),
                                            dcc.Dropdown(
                                                id="comp-sort-order",
                                                options=[
                                                    {"label": "None", "value": "none"},
                                                    {"label": "Ascending", "value": "asc"},
                                                    {"label": "Descending", "value": "desc"},
                                                ],
                                                value="none",
                                                className="mb-2",
                                            ),

                                            html.Label("Color Theme", className="small fw-bold"),
                                            dcc.Dropdown(
                                                id="comp-theme",
                                                options=[
                                                    {"label": "Default", "value": "plotly"},
                                                    {"label": "Vibrant", "value": "seaborn"},
                                                    {"label": "Dark", "value": "plotly_dark"},
                                                ],
                                                value="plotly",
                                                className="mb-2",
                                            ),
                                        ], className="pe-2"),
                                    ],
                                    md=4,
                                    className="border-end",
                                    style={"maxHeight": "75vh", "overflowY": "auto"}
                                ),
                                dbc.Col(
                                    [
                                        html.Div([
                                            html.H6("Comparison Preview", className="fw-bold d-inline-block me-2"),
                                            dbc.Badge("Cross-Dataset", color="warning", pill=True, className="align-middle"),
                                        ], className="mb-3"),
                                        
                                        dcc.Loading(
                                            html.Div(
                                                dcc.Graph(id="comp-preview-graph", style={"height": "500px"}),
                                                className="border rounded bg-white shadow-sm"
                                            )
                                        ),
                                        html.Div(id="comp-validation-msg", className="text-danger small mt-2 fw-bold"),
                                        
                                        html.Div([
                                            html.Label("Chart Title", className="small fw-bold mt-3"),
                                            dbc.Input(id="comp-title", placeholder="Cross-Dataset Comparison", className="mb-2"),
                                        ]),
                                    ],
                                    md=8,
                                    className="ps-3"
                                )
                            ]
                        )
                    ]
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button("Cancel", id="comp-cancel-button", color="secondary", outline=True, className="me-auto"),
                        dbc.Button("Reset", id="comp-reset-button", color="warning", outline=True, className="me-2"),
                        dbc.Button(
                            [html.I(className="bi bi-plus-lg me-2"), "Add Comparison to Dashboard"],
                            id="comp-add-button",
                            color="success",
                            disabled=True
                        ),
                    ]
                ),
            ],
            id="comparison-chart-modal",
            size="xl",
            is_open=False,
            backdrop="static",
        ),

        # Report Configuration Modal
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Generate Full Report"), close_button=True),
                dbc.ModalBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Report Title", className="small fw-bold"),
                                        dbc.Input(id="report-title", placeholder="Data Analysis Report", value="Data Analysis Report", className="mb-3"),
                                        
                                        html.H6("Include Sections", className="fw-bold mb-3"),
                                        dbc.Checklist(
                                            id="report-sections",
                                            options=[
                                                {"label": "Executive Summary", "value": "summary"},
                                                {"label": "Dataset Overviews", "value": "datasets"},
                                                {"label": "Individual Charts", "value": "charts"},
                                                {"label": "Comparison Charts", "value": "comparisons"},
                                                {"label": "Statistical Appendix", "value": "appendix"},
                                            ],
                                            value=["summary", "datasets", "charts", "comparisons"],
                                            className="mb-3",
                                        ),
                                        
                                        html.Label("Export Format", className="small fw-bold"),
                                        dbc.RadioItems(
                                            id="report-format",
                                            options=[
                                                {"label": "PDF Document (.pdf)", "value": "pdf"},
                                                {"label": "HTML Report (.html)", "value": "html"},
                                            ],
                                            value="pdf",
                                            className="mb-3",
                                        ),
                                    ],
                                    md=6
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.H6("Report Preview (Mockup)", className="fw-bold text-center"),
                                                html.Div(
                                                    [
                                                        html.Div(style={"height": "20px", "width": "80%", "background": "#ddd", "margin": "10px auto"}),
                                                        html.Div(style={"height": "100px", "width": "90%", "background": "#f0f0f0", "margin": "10px auto", "border": "1px dashed #ccc"}),
                                                        html.Div(style={"height": "15px", "width": "70%", "background": "#eee", "margin": "5px auto"}),
                                                        html.Div(style={"height": "15px", "width": "60%", "background": "#eee", "margin": "5px auto"}),
                                                    ],
                                                    className="border rounded p-3 bg-white shadow-sm",
                                                    style={"height": "250px"}
                                                )
                                            ],
                                            className="p-3 bg-light rounded"
                                        )
                                    ],
                                    md=6
                                )
                            ]
                        )
                    ]
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button("Cancel", id="report-cancel-button", color="secondary", outline=True, className="me-auto"),
                        dbc.Button("Generate & Download", id="report-generate-button", color="primary"),
                    ]
                ),
            ],
            id="report-config-modal",
            size="lg",
            is_open=False,
        )
    ])
