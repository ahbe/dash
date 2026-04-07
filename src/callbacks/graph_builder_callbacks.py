"""
Callbacks for the custom graph builder.
"""

from typing import Any, Dict, List, Optional, Union
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import callback, Input, Output, State, ALL, MATCH, ctx, no_update, html, dcc
import dash_bootstrap_components as dbc
from src.utils.logger import logger


@callback(
    Output("gb-selected-chart-type", "data", allow_duplicate=True),
    Output({"type": "gb-ct", "index": ALL}, "className"),
    Input({"type": "gb-ct", "index": ALL}, "n_clicks"),
    State("gb-selected-chart-type", "data"),
    prevent_initial_call=True,
)
def select_chart_type(n_clicks, current_type):
    """Updates the selected chart type and highlights the active card."""
    if not ctx.triggered:
        return current_type, [f"d-flex flex-column align-items-center p-2 border rounded chart-type-card {'active' if i == current_type else ''}" for i in [ct["id"]["index"] for ct in ctx.inputs_list[0]]]

    trig = ctx.triggered_id
    selected = current_type
    if isinstance(trig, dict) and trig.get("type") == "gb-ct":
        selected = trig["index"]
    
    class_names = []
    for item in ctx.inputs_list[0]:
        idx = item["id"]["index"]
        base_class = "d-flex flex-column align-items-center p-2 border rounded chart-type-card"
        if idx == selected:
            class_names.append(f"{base_class} active")
        else:
            class_names.append(base_class)
            
    return selected, class_names


@callback(
    Output("gb-x-label", "value"),
    Output("gb-y-label", "value"),
    Output("gb-title", "value", allow_duplicate=True),
    Output("gb-selected-chart-type", "data", allow_duplicate=True),
    Input("gb-x-axis", "value"),
    Input("gb-y-axis", "value"),
    State("gb-title", "value"),
    State("available-columns-store", "data"),
    prevent_initial_call=True,
)
def update_label_defaults(x, y, current_title, columns):
    """Sets default labels and suggests chart type based on selected columns."""
    x_label = x if x else ""
    y_label = ", ".join(y) if y else ""
    
    title = current_title
    if not title and x and y:
        title = f"{y_label} by {x_label}"
    
    # Smart Defaults for Chart Type
    suggested_type = no_update
    if x and columns:
        col_info = next((c for c in columns if c["name"] == x), None)
        if col_info:
            if col_info["type"] == "datetime":
                suggested_type = "line"
            elif col_info["type"] == "numeric":
                suggested_type = "scatter"
            elif col_info["type"] == "categorical":
                suggested_type = "bar"
        
    return x_label, y_label, title, suggested_type


@callback(
    Output("gb-preview-graph", "figure"),
    Output("gb-add-button", "disabled"),
    Output("gb-validation-msg", "children"),
    Input("gb-x-axis", "value"),
    Input("gb-y-axis", "value"),
    Input("gb-selected-chart-type", "data"),
    Input("gb-aggregation", "value"),
    Input("gb-group-by", "value"),
    Input("gb-secondary-y", "value"),
    Input("gb-x-label", "value"),
    Input("gb-y-label", "value"),
    Input("gb-title", "value"),
    Input("gb-theme", "value"),
    Input("gb-show-labels", "value"),
    Input("gb-show-grid", "value"),
    Input("gb-sort-order", "value"),
    State({"type": "data-table", "index": "raw-data-table"}, "data"),
    prevent_initial_call=True,
)
def update_preview(x, y, chart_type, agg, group, secondary_y, x_label, y_label, title, theme, show_labels, show_grid, sort_order, table_data):
    """Generates the chart preview based on all configuration settings."""
    if not table_data or not x or not y:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="Select X and Y axes to preview",
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[{"text": "Waiting for axis selection...", "showarrow": False, "font": {"size": 20}}]
        )
        return empty_fig, True, "Please select X and Y axes."

    df = pd.DataFrame(table_data)
    
    # Validation for specific charts
    if chart_type == "pie" and len(y) > 1:
        return no_update, True, "Pie chart only supports one Y-axis column."
    if chart_type == "bubble" and len(y) < 2:
        return no_update, True, "Bubble chart requires at least 2 Y columns (Size is 2nd column)."
    if chart_type == "candlestick" and len(y) < 4:
        return no_update, True, "Candlestick requires 4 Y columns (Open, High, Low, Close)."

    # Handle Sort Order
    if sort_order == "asc":
        df = df.sort_values(by=x)
    elif sort_order == "desc":
        df = df.sort_values(by=x, ascending=False)

    # Handle Aggregation
    plot_df = df.copy()
    if agg != "none":
        try:
            if group:
                plot_df = df.groupby([x, group])[y].agg(agg).reset_index()
            else:
                plot_df = df.groupby(x)[y].agg(agg).reset_index()
        except Exception as e:
            return no_update, True, f"Aggregation error: {e}"

    try:
        fig = None
        color_col = group if group else None
        
        # Base Chart Selection
        if chart_type == "line":
            fig = px.line(plot_df, x=x, y=y, color=color_col, title=title, template=theme)
        elif chart_type == "bar":
            fig = px.bar(plot_df, x=x, y=y, color=color_col, title=title, template=theme, barmode="group")
        elif chart_type == "hbar":
            fig = px.bar(plot_df, x=y[0], y=x, color=color_col, orientation="h", title=title, template=theme)
        elif chart_type == "scatter":
            fig = px.scatter(plot_df, x=x, y=y, color=color_col, title=title, template=theme)
        elif chart_type == "area":
            fig = px.area(plot_df, x=x, y=y, color=color_col, title=title, template=theme)
        elif chart_type == "stacked_bar":
            fig = px.bar(plot_df, x=x, y=y, color=color_col, title=title, template=theme, barmode="stack")
        elif chart_type == "stacked_area":
            fig = px.area(plot_df, x=x, y=y, color=color_col, title=title, template=theme)
        elif chart_type in ["pie", "donut"]:
            fig = px.pie(plot_df, names=x, values=y[0], title=title, template=theme, hole=0.4 if chart_type == "donut" else 0)
        elif chart_type == "histogram":
            fig = px.histogram(df, x=x, y=y[0], color=color_col, title=title, template=theme)
        elif chart_type == "box":
            fig = px.box(df, x=x, y=y[0], color=color_col, title=title, template=theme)
        elif chart_type == "heatmap":
            if not group:
                return no_update, True, "Heatmap requires a 'Group By' column for the Y-axis."
            fig = px.density_heatmap(df, x=x, y=group, z=y[0], title=title, template=theme)
        elif chart_type == "bubble":
            fig = px.scatter(plot_df, x=x, y=y[0], size=y[1], color=color_col, title=title, template=theme)
        elif chart_type == "candlestick":
            fig = go.Figure(data=[go.Candlestick(x=plot_df[x], open=plot_df[y[0]], high=plot_df[y[1]], low=plot_df[y[2]], close=plot_df[y[3]])])
            fig.update_layout(title=title, template=theme)

        if fig:
            # Apply common layout updates
            fig.update_layout(
                xaxis_title=x_label,
                yaxis_title=y_label,
                showlegend=True,
                margin=dict(l=40, r=40, t=60, b=40),
                hovermode="x unified" if chart_type in ["line", "area", "stacked_area"] else "closest",
                dragmode="select",
                clickmode="event+select",
            )
            
            # Show Labels
            if "show" in show_labels:
                if chart_type in ["bar", "hbar", "stacked_bar"]:
                    fig.update_traces(texttemplate='%{y:.2s}', textposition='outside')
            
            # Grid lines
            fig.update_xaxes(showgrid="show" in show_grid)
            fig.update_yaxes(showgrid="show" in show_grid)

            # Time Series Features
            is_datetime = False
            try:
                pd.to_datetime(df[x], errors='raise')
                is_datetime = True
            except:
                pass

            if is_datetime:
                fig.update_xaxes(
                    rangeslider_visible=True,
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1, label="1D", step="day", stepmode="backward"),
                            dict(count=7, label="1W", step="day", stepmode="backward"),
                            dict(count=1, label="1M", step="month", stepmode="backward"),
                            dict(count=6, label="6M", step="month", stepmode="backward"),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(count=1, label="1Y", step="year", stepmode="backward"),
                            dict(step="all")
                        ])
                    )
                )

            # Secondary Y-Axis logic (simplified)
            if "enable" in secondary_y and len(y) > 1:
                fig.update_layout(yaxis2=dict(title=y[1], overlaying='y', side='right'))
                if len(fig.data) > 1:
                    fig.data[1].yaxis = "y2"

            return fig, False, ""
        
        return go.Figure(), True, "Invalid chart configuration."

    except Exception as e:
        logger.error(f"Error generating preview: {e}")
        return go.Figure(), True, f"Error: {str(e)}"


@callback(
    Output("download-graph-data", "data"),
    Input("gb-export-selected", "n_clicks"),
    State("gb-preview-graph", "selectedData"),
    prevent_initial_call=True,
)
def export_selected_data(n_clicks, selected_data):
    """Exports selected data points to CSV."""
    if not n_clicks or not selected_data or "points" not in selected_data:
        return no_update
    
    # Extract data from points
    data = []
    for p in selected_data["points"]:
        point_data = p.get("customdata", {})
        if not point_data:
            # Fallback to x and y if customdata is not available
            point_data = {"x": p.get("x"), "y": p.get("y")}
        data.append(point_data)
        
    df = pd.DataFrame(data)
    return dcc.send_data_frame(df.to_csv, "selected_data.csv", index=False)


@callback(
    Output("gb-selection-summary", "children"),
    Input("gb-preview-graph", "selectedData"),
)
def update_selection_summary(selected_data):
    """Displays summary statistics for selected data points."""
    if not selected_data or "points" not in selected_data or not selected_data["points"]:
        return None
    
    points = selected_data["points"]
    count = len(points)
    y_values = [p.get("y") for p in points if p.get("y") is not None]
    
    if not y_values:
        return dbc.Alert(f"Selected {count} points.", color="info", className="py-2")
    
    df_y = pd.Series(y_values)
    summary = [
        html.Span([html.B("Count: "), f"{count}"], className="me-3"),
        html.Span([html.B("Mean: "), f"{df_y.mean():.2f}"], className="me-3"),
        html.Span([html.B("Median: "), f"{df_y.median():.2f}"], className="me-3"),
        html.Span([html.B("Min: "), f"{df_y.min():.2f}"], className="me-3"),
        html.Span([html.B("Max: "), f"{df_y.max():.2f}"], className="me-3"),
        dbc.Button("Export Selected", id="gb-export-selected", size="sm", color="primary", outline=True, className="ms-auto")
    ]
    
    return dbc.Card(
        dbc.CardBody(summary, className="d-flex align-items-center py-2 px-3"),
        className="bg-light border shadow-sm"
    )


@callback(
    Output("custom-graphs-store", "data"),
    Output("graph-builder-modal", "is_open", allow_duplicate=True),
    Input("gb-add-button", "n_clicks"),
    State("gb-preview-graph", "figure"),
    State("gb-title", "value"),
    State("gb-selected-chart-type", "data"),
    State("custom-graphs-store", "data"),
    prevent_initial_call=True,
)
def add_graph_to_store(n_clicks, fig, title, chart_type, existing_graphs):
    """Saves the current chart configuration to the store and closes modal."""
    if not n_clicks:
        return no_update, no_update
    
    new_graph = {
        "id": f"custom-{len(existing_graphs)}",
        "title": title or "Custom Chart",
        "chart_type": chart_type,
        "figure": fig,
    }
    existing_graphs.append(new_graph)
    return existing_graphs, False


@callback(
    Output("custom-graph-gallery", "children"),
    Input("custom-graphs-store", "data"),
)
def update_gallery(graphs):
    """Renders the custom graph gallery from stored charts."""
    if not graphs:
        return []
    
    cards = []
    for g in graphs:
        card = dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.Div(
                            [
                                html.Div([
                                    html.H6(g["title"], className="mb-0 d-inline-block"),
                                    dbc.Badge(g["chart_type"].replace("_", " ").title(), color="secondary", className="ms-2 small"),
                                ]),
                                html.Div([
                                    dbc.Button(html.I(className="bi bi-arrows-fullscreen"), id={"type": "gb-expand", "index": g["id"]}, color="link", size="sm", className="text-muted me-1"),
                                    dbc.Button(html.I(className="bi bi-trash"), id={"type": "gb-delete", "index": g["id"]}, color="link", size="sm", className="text-danger"),
                                ]),
                            ],
                            className="d-flex justify-content-between align-items-center py-2"
                        )
                    ),
                    dbc.CardBody(
                        [
                            dcc.Graph(
                                id={"type": "gallery-graph", "index": g["id"]},
                                figure=g["figure"],
                                config={
                                    "displayModeBar": True,
                                    "scrollZoom": True,
                                    "toImageButtonOptions": {"format": "png", "filename": "custom_chart"},
                                },
                                style={"height": "100%", "width": "100%"},
                                responsive=True,
                            ),
                            html.Div(id={"type": "gallery-selection", "index": g["id"]}, className="small mt-2 px-2 pb-2")
                        ],
                        className="p-0 d-flex flex-column",
                        style={"flex": "1", "minHeight": "0"}
                    ),
                ],
                className="mb-4 shadow-sm gallery-card resizable-tile",
                style={"display": "flex", "flexDirection": "column"}
            ),
            md=12, lg=6, xl=4,
            id={"type": "gallery-item", "index": g["id"]}
        )
        cards.append(card)
        
    return dbc.Row(cards)


@callback(
    Output("fs-chart-modal", "is_open", allow_duplicate=True),
    Output("fs-chart-title", "children", allow_duplicate=True),
    Output("fs-chart-graph", "figure", allow_duplicate=True),
    Input({"type": "gb-expand", "index": ALL}, "n_clicks"),
    Input("fs-close-button", "n_clicks"),
    State("custom-graphs-store", "data"),
    prevent_initial_call=True,
)
def toggle_fullscreen_modal(expand_n, close_n, graphs):
    """Handles opening and closing the full-screen chart modal."""
    if ctx.triggered_id == "fs-close-button":
        return False, no_update, no_update
    
    if not any(expand_n):
        return no_update, no_update, no_update
    
    trig = ctx.triggered_id
    if isinstance(trig, dict) and trig.get("type") == "gb-expand":
        graph_id = trig["index"]
        graph = next((g for g in graphs if g["id"] == graph_id), None)
        if graph:
            return True, graph["title"], graph["figure"]
            
    return False, no_update, no_update


@callback(
    Output("graph-builder-modal", "is_open"),
    Output("gb-x-axis", "value"),
    Output("gb-y-axis", "value"),
    Output("gb-group-by", "value"),
    Output("gb-aggregation", "value"),
    Output("gb-title", "value", allow_duplicate=True),
    Output("gb-selected-chart-type", "data", allow_duplicate=True),
    Input("open-graph-builder-button", "n_clicks"),
    Input("gb-cancel-button", "n_clicks"),
    Input("gb-reset-button", "n_clicks"),
    State("graph-builder-modal", "is_open"),
    prevent_initial_call=True,
)
def toggle_modal(open_n, cancel_n, reset_n, is_open):
    """Toggles the graph builder modal or resets settings."""
    trig = ctx.triggered_id
    if trig == "gb-reset-button":
        return True, None, None, None, "none", "", "line"
    
    if trig == "open-graph-builder-button":
        return True, no_update, no_update, no_update, no_update, no_update, no_update
        
    return False, no_update, no_update, no_update, no_update, no_update, no_update


@callback(
    Output("available-columns-store", "data"),
    Input({"type": "data-table", "index": "raw-data-table"}, "data"),
)
def update_available_columns(table_data):
    """Updates the list of available columns from the loaded data."""
    if not table_data:
        return []
    df = pd.DataFrame(table_data)
    cols = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        if "datetime" in dtype or col.lower() in ["date", "timestamp"]:
            type_label = "datetime"
        elif "int" in dtype or "float" in dtype:
            type_label = "numeric"
        elif "object" in dtype or "category" in dtype:
            type_label = "categorical"
        else:
            type_label = "text"
        cols.append({"name": col, "type": type_label})
    return cols


@callback(
    Output("gb-x-axis", "options"),
    Output("gb-y-axis", "options"),
    Output("gb-group-by", "options"),
    Input("available-columns-store", "data"),
)
def populate_dropdowns(columns):
    """Populates axis dropdowns with available columns."""
    options = [{"label": f"{c['name']} ({c['type']})", "value": c['name']} for c in columns]
    return options, options, options


@callback(
    Output("custom-graphs-store", "data", allow_duplicate=True),
    Input({"type": "gb-delete", "index": ALL}, "n_clicks"),
    State("custom-graphs-store", "data"),
    prevent_initial_call=True,
)
def delete_graph(n_clicks, graphs):
    """Deletes a chart from the store."""
    if not any(n_clicks):
        return no_update
    
    trig = ctx.triggered_id
    if isinstance(trig, dict) and trig.get("type") == "gb-delete":
        graph_id = trig["index"]
        graphs = [g for g in graphs if g["id"] != graph_id]
        return graphs
    return no_update


@callback(
    Output({"type": "gallery-selection", "index": MATCH}, "children"),
    Input({"type": "gallery-graph", "index": MATCH}, "selectedData"),
)
def update_gallery_selection_summary(selected_data):
    """Displays summary statistics for selected data points in gallery charts."""
    if not selected_data or "points" not in selected_data or not selected_data["points"]:
        return None
    
    count = len(selected_data["points"])
    y_values = [p.get("y") for p in selected_data["points"] if p.get("y") is not None]
    
    if not y_values:
        return f"Selected {count} points"
    
    mean_val = pd.Series(y_values).mean()
    return f"Selected {count} points | Mean Y: {mean_val:.2f}"
