"""
Main content area layout component.
Composes metrics, charts, and alerts.
"""

from dash import html
import dash_bootstrap_components as dbc
from src.components.metric_card import create_metric_card
from src.components.chart_block import create_chart_block, ChartType
from src.components.data_table_block import create_data_table_block


def create_main_content() -> html.Div:
    """
    Creates the main dashboard content area.

    Returns:
        html.Div: Main content layout.
    """
    return html.Div(
        [
            # Alerts Area
            html.Div(id="alerts-container", className="mb-4"),
            
            # KPI Metrics Row
            dbc.Row(
                [
                    dbc.Col(create_metric_card("derogation-pct", "Derogation %", icon="percent", color_scheme="primary"), md=4, lg=2),
                    dbc.Col(create_metric_card("derogation-bps", "Derogation (bps)", icon="calculator", color_scheme="info"), md=4, lg=2),
                    dbc.Col(create_metric_card("usage-count", "Usage Count", icon="people", color_scheme="success"), md=4, lg=2),
                    dbc.Col(create_metric_card("failed-calls", "Failed Calls", icon="exclamation-octagon", color_scheme="danger", inverted_polarity=True), md=4, lg=2),
                    dbc.Col(create_metric_card("converted-margin", "Converted Margin", icon="currency-euro", color_scheme="warning"), md=4, lg=2),
                    dbc.Col(create_metric_card("conversion-rate", "Conversion Rate", icon="check2-circle", color_scheme="primary"), md=4, lg=2),
                ],
                className="mb-4 g-3",
            ),
            
            # Charts Grid
            dbc.Row(
                [
                    # Time series charts
                    dbc.Col(
                        create_chart_block("derogation-trend", "Derogation Trend", ChartType.LINE, subtitle="Daily derogation volume over time"),
                        width=12, lg=8, className="mb-4"
                    ),
                    
                    # Pie charts
                    dbc.Col(
                        create_chart_block("brand-distribution", "Brand Distribution", ChartType.PIE, subtitle="Market share by brand"),
                        width=12, lg=4, className="mb-4"
                    ),
                ],
                className="g-4",
            ),

            dbc.Row(
                [
                    dbc.Col(
                        create_chart_block("segment-performance", "Segment Performance", ChartType.BAR),
                        width=12, lg=6, className="mb-4"
                    ),
                    
                    dbc.Col(
                        create_chart_block("purpose-analysis", "Purpose Analysis", ChartType.BAR),
                        width=12, lg=6, className="mb-4"
                    ),
                ],
                className="g-4",
            ),
            
            # Custom Graph Gallery
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            id="custom-graph-gallery-container",
                            children=[
                                html.Div(id="custom-graph-gallery", className="p-3 border rounded bg-white shadow-sm", 
                                       children=[html.P("Your custom charts will appear here...", className="text-center text-muted mb-0")])
                            ]
                        ),
                        width=12, className="mb-4"
                    ),
                ]
            ),

            # Data Table
            dbc.Row(
                [
                    dbc.Col(
                        create_data_table_block("raw-data-table", title="Detailed Derogation Data"),
                        width=12, className="mb-4"
                    ),
                ]
            ),
        ],
        className="p-4 bg-light min-vh-100",
    )
