"""
Callbacks for the custom graph builder and comparison chart builder.
"""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import uuid
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import callback, Input, Output, State, ALL, MATCH, ctx, no_update, html, dcc
import dash_bootstrap_components as dbc
from src.utils.logger import logger

# --- Constants & Helpers ---
COLOR_PALETTES = {
    "plotly": px.colors.qualitative.Plotly,
    "ggplot2": px.colors.qualitative.G10,
    "seaborn": px.colors.qualitative.Set2,
    "plotly_dark": px.colors.qualitative.Pastel,
    "none": ["#636EFA"] * 10
}

def get_df_from_store(datasets, active_id):
    if not datasets or not active_id or active_id not in datasets:
        return pd.DataFrame()
    return pd.DataFrame(datasets[active_id]["data"])

# --- Graph Builder Callbacks ---

@callback(
    Output("graph-builder-modal", "is_open"),
    Output("comparison-chart-modal", "is_open"),
    Output("report-config-modal", "is_open"),
    Input("open-graph-builder-button", "n_clicks"),
    Input("gb-cancel-button", "n_clicks"),
    Input("open-comparison-builder-button", "n_clicks"),
    Input("comp-cancel-button", "n_clicks"),
    Input("download-report-button", "n_clicks"),
    Input("report-cancel-button", "n_clicks"),
    State("graph-builder-modal", "is_open"),
    State("comparison-chart-modal", "is_open"),
    State("report-config-modal", "is_open"),
    prevent_initial_call=True,
)
def toggle_modals(n1, n2, n3, n4, n5, n6, gb_open, comp_open, report_open):
    trig = ctx.triggered_id
    if trig == "open-graph-builder-button":
        return True, False, False
    if trig == "gb-cancel-button":
        return False, no_update, no_update
    if trig == "open-comparison-builder-button":
        return False, True, False
    if trig == "comp-cancel-button":
        return no_update, False, no_update
    if trig == "download-report-button":
        return False, False, True
    if trig == "report-cancel-button":
        return no_update, no_update, False
    return False, False, False


@callback(
    Output("gb-active-dataset-indicator", "children"),
    Output("gb-x-axis", "options"),
    Output("gb-y-axis", "options"),
    Output("gb-group-by", "options"),
    Input("active-dataset-id", "data"),
    State("datasets-store", "data"),
)
def update_gb_dropdowns(active_id, datasets):
    if not active_id or not datasets or active_id not in datasets:
        return "No active dataset", [], [], []
    
    ds = datasets[active_id]
    cols = ds.get("columns", [])
    options = [{"label": f"{c['name']} ({c['type']})", "value": c['name']} for c in cols]
    
    return f"Creating chart from: {ds['name']} ({ds['filename']})", options, options, options


@callback(
    Output("gb-selected-chart-type", "data", allow_duplicate=True),
    Output({"type": "gb-ct", "index": ALL}, "className"),
    Input({"type": "gb-ct", "index": ALL}, "n_clicks"),
    State("gb-selected-chart-type", "data"),
    prevent_initial_call=True,
)
def select_chart_type(n_clicks, current_type):
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
    Output("gb-x-label", "value", allow_duplicate=True),
    Output("gb-y-label", "value", allow_duplicate=True),
    Output("gb-title", "value", allow_duplicate=True),
    Output("gb-selected-chart-type", "data", allow_duplicate=True),
    Input("gb-x-axis", "value"),
    Input("gb-y-axis", "value"),
    State("gb-title", "value"),
    State("active-dataset-id", "data"),
    State("datasets-store", "data"),
    prevent_initial_call=True,
)
def update_label_defaults(x, y, current_title, active_id, datasets):
    x_label = x if x else ""
    y_label = ", ".join(y) if y else ""
    
    title = current_title
    if not title and x and y:
        title = f"{y_label} by {x_label}"
    
    suggested_type = no_update
    if x and active_id and datasets and active_id in datasets:
        ds = datasets[active_id]
        col_info = next((c for c in ds["columns"] if c["name"] == x), None)
        if col_info:
            dtype = col_info["type"].lower()
            if "datetime" in dtype or "date" in dtype:
                suggested_type = "line"
            elif "float" in dtype or "int" in dtype:
                suggested_type = "scatter"
            else:
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
    State("active-dataset-id", "data"),
    State("datasets-store", "data"),
    prevent_initial_call=True,
)
def update_gb_preview(x, y, chart_type, agg, group, secondary_y, x_label, y_label, title, theme, show_labels, show_grid, sort_order, active_id, datasets):
    if not active_id or not x or not y:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="Select X and Y axes to preview",
            xaxis={"visible": False}, yaxis={"visible": False},
            annotations=[{"text": "Waiting for axis selection...", "showarrow": False, "font": {"size": 16}}]
        )
        return empty_fig, True, "Please select X and Y axes."

    df = get_df_from_store(datasets, active_id)
    if df.empty:
        return go.Figure(), True, "Dataset is empty."

    # Validation
    if chart_type in ["pie", "donut"] and len(y) > 1:
        return no_update, True, "Pie/Donut charts only support one Y column."
    if chart_type == "bubble" and len(y) < 2:
        return no_update, True, "Bubble chart requires at least 2 Y columns (Size is 2nd)."
    if chart_type == "candlestick" and len(y) < 4:
        return no_update, True, "Candlestick requires 4 columns (O,H,L,C)."

    plot_df = df.copy()
    
    # Sort Order
    if sort_order == "asc":
        plot_df = plot_df.sort_values(by=x)
    elif sort_order == "desc":
        plot_df = plot_df.sort_values(by=x, ascending=False)

    # Aggregation
    if agg != "none":
        try:
            if group:
                plot_df = plot_df.groupby([x, group])[y].agg(agg).reset_index()
            else:
                plot_df = plot_df.groupby(x)[y].agg(agg).reset_index()
        except Exception as e:
            return no_update, True, f"Aggregation error: {e}"

    try:
        color_col = group if group else None
        
        # Chart Creation
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
            if not group: return no_update, True, "Heatmap requires a 'Group By' column."
            fig = px.density_heatmap(df, x=x, y=group, z=y[0], title=title, template=theme)
        elif chart_type == "bubble":
            fig = px.scatter(plot_df, x=x, y=y[0], size=y[1], color=color_col, title=title, template=theme)
        elif chart_type == "candlestick":
            fig = go.Figure(data=[go.Candlestick(x=plot_df[x], open=plot_df[y[0]], high=plot_df[y[1]], low=plot_df[y[2]], close=plot_df[y[3]])])
            fig.update_layout(title=title, template=theme)
        else:
            fig = px.line(plot_df, x=x, y=y, title=title, template=theme)

        # Interactivity & Layout
        fig.update_layout(
            xaxis_title=x_label,
            yaxis_title=y_label,
            hovermode="x unified" if chart_type in ["line", "area", "stacked_area"] else "closest",
            dragmode="select",
            clickmode="event+select",
            margin=dict(l=50, r=50, t=80, b=50),
        )
        
        # Grid & Labels
        fig.update_xaxes(showgrid="show" in show_grid)
        fig.update_yaxes(showgrid="show" in show_grid)
        if "show" in show_labels:
            if chart_type in ["bar", "hbar"]:
                fig.update_traces(texttemplate='%{y:.2s}', textposition='outside', cliponaxis=False)

        # Time Series Detection
        is_dt = False
        try:
            # More robust datetime check and conversion
            dt_series = pd.to_datetime(df[x], errors='coerce')
            if dt_series.notna().any(): # Check if any value successfully converted
                is_dt = True
                plot_df[x] = dt_series # Use converted series
        except Exception as e:
            logger.debug(f"Datetime conversion failed for {x}: {e}")

        if is_dt:
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=[
                        dict(count=1, label="1D", step="day", stepmode="backward"),
                        dict(count=7, label="1W", step="day", stepmode="backward"),
                        dict(count=1, label="1M", step="month", stepmode="backward"),
                        dict(count=3, label="3M", step="month", stepmode="backward"),
                        dict(count=6, label="6M", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1Y", step="year", stepmode="backward"),
                        dict(step="all")
                    ]
                )
            )
            # Add crosshair cursor
            fig.update_xaxes(showspikes=True, spikemode="across", spikedash="dot", spikecolor="#999999", spikethickness=1)
            fig.update_yaxes(showspikes=True, spikemode="across", spikedash="dot", spikecolor="#999999", spikethickness=1)
            fig.update_layout(hoverdistance=1) # Snap to data points

        if "enable" in secondary_y and len(y) > 1:
            # If secondary Y is enabled and multiple Y columns, use first for y1, second for y2
            fig.add_trace(go.Scatter(x=plot_df[x], y=plot_df[y[1]], name=f"{y[1]} (Secondary)", yaxis="y2", mode="lines"))
            fig.update_layout(yaxis2=dict(title=y[1], overlaying='y', side='right', showgrid=False))
            # Adjust initial traces to use y1
            for i, trace in enumerate(fig.data):
                if i == 0: # First Y-axis
                    trace.yaxis = "y"
                elif i == 1 and len(y) > 1: # Second Y-axis
                    trace.yaxis = "y2" 

        return fig, False, ""

    except Exception as e:
        logger.error(f"GB Preview Error: {e}")
        return go.Figure(), True, f"Error: {e}"

# --- Comparison Builder Callbacks ---

@callback(
    Output("comp-datasets-list", "options"),
    Input("datasets-store", "data"),
)
def populate_comp_datasets(datasets):
    if not datasets: return []
    return [{"label": ds["name"], "value": ds_id} for ds_id, ds in datasets.items()]


@callback(
    Output("comp-x-axis", "options"),
    Output("comp-y-axis", "options"),
    Input("comp-datasets-list", "value"),
    State("datasets-store", "data"),
)
def update_comp_dropdowns(selected_ids, datasets):
    if not selected_ids or len(selected_ids) < 1: return [], []
    
    # Find common columns
    common_cols = set()
    for i, ds_id in enumerate(selected_ids):
        if ds_id in datasets:
            cols = {c["name"] for c in datasets[ds_id]["columns"]}
            if i == 0: common_cols = cols
            else: common_cols &= cols
            
    options = [{"label": c, "value": c} for c in sorted(list(common_cols))]
    return options, options


@callback(
    Output("comp-preview-graph", "figure"),
    Output("comp-add-button", "disabled"),
    Output("comp-validation-msg", "children"),
    Output("comp-x-label", "value", allow_duplicate=True),
    Output("comp-y-label", "value", allow_duplicate=True),
    Output("comp-title", "value", allow_duplicate=True),
    Input("comp-datasets-list", "value"),
    Input("comp-x-axis", "value"),
    Input("comp-y-axis", "value"),
    Input("comp-aggregation", "value"),
    Input("comp-type", "value"),
    Input("comp-normalize", "value"),
    Input("comp-sort-order", "value"),
    Input("comp-theme", "value"),
    Input("comp-x-label", "value"),
    Input("comp-y-label", "value"),
    Input("comp-title", "value"),
    State("datasets-store", "data"),
    prevent_initial_call=True,
)
def update_comp_preview(ds_ids, x, y, agg, comp_type, normalize, sort_order, theme, x_label, y_label, title, datasets):
    if not ds_ids or len(ds_ids) < 2 or not x or not y:
        return go.Figure(), True, "Select at least 2 datasets and X/Y axes.", x_label, y_label, title

    fig = go.Figure()
    
    # Auto-update labels if they are empty
    new_x_label = x_label if x_label else x
    new_y_label = y_label if y_label else (f"{agg.title()}({y})" if agg != "none" else y)
    new_title = title if title else f"Comparison: {new_y_label} by {new_x_label}"

    try:
        for ds_id in ds_ids:
            if ds_id not in datasets: continue
            ds = datasets[ds_id]
            df = pd.DataFrame(ds["data"])
            
            # Sort data
            if sort_order == "asc":
                df = df.sort_values(by=x)
            elif sort_order == "desc":
                df = df.sort_values(by=x, ascending=False)

            # Aggregation
            plot_df = df.copy()
            if agg != "none":
                try:
                    plot_df = df.groupby(x)[y].agg(agg).reset_index()
                except Exception as e:
                    logger.warning(f"Aggregation failed: {e}")
                    plot_df = df.groupby(x)[y].first().reset_index()
            
            y_vals = plot_df[y].fillna(0)
            if "norm" in normalize:
                if y_vals.max() != y_vals.min():
                    y_vals = (y_vals - y_vals.min()) / (y_vals.max() - y_vals.min()) * 100
                else:
                    y_vals = y_vals * 0 + 100
            
            if comp_type == "overlay_line":
                fig.add_trace(go.Scatter(
                    x=plot_df[x], y=y_vals, name=ds["name"], 
                    mode='lines+markers',
                    hovertemplate="<b>" + ds["name"] + "</b><br>" + x + ": %{x}<br>" + y + ": %{y:.2f}<extra></extra>"
                ))
            elif comp_type == "side_bar":
                fig.add_trace(go.Bar(
                    x=plot_df[x], y=y_vals, name=ds["name"],
                    hovertemplate="<b>" + ds["name"] + "</b><br>" + x + ": %{x}<br>" + y + ": %{y:.2f}<extra></extra>"
                ))
            elif comp_type == "stacked_area":
                fig.add_trace(go.Scatter(
                    x=plot_df[x], y=y_vals, name=ds["name"], 
                    stackgroup='one', fill='tonexty',
                    hovertemplate="<b>" + ds["name"] + "</b><br>" + x + ": %{x}<br>" + y + ": %{y:.2f}<extra></extra>"
                ))
            elif comp_type == "scatter":
                fig.add_trace(go.Scatter(
                    x=plot_df[x], y=y_vals, name=ds["name"], mode='markers',
                    marker=dict(size=10, opacity=0.7),
                    hovertemplate="<b>" + ds["name"] + "</b><br>" + x + ": %{x}<br>" + y + ": %{y:.2f}<extra></extra>"
                ))
                
        fig.update_layout(
            title=new_title,
            xaxis_title=new_x_label,
            yaxis_title=f"{new_y_label} {'(Normalized %)' if 'norm' in normalize else ''}",
            template=theme,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig, False, "", new_x_label, new_y_label, new_title

    except Exception as e:
        logger.error(f"Comp Preview Error: {e}")
        return go.Figure(), True, f"Error: {e}", x_label, y_label, title

# --- Dashboard & Gallery Callbacks ---

@callback(
    Output("custom-graphs-store", "data", allow_duplicate=True),
    Output("graph-builder-modal", "is_open", allow_duplicate=True),
    Output("comparison-chart-modal", "is_open", allow_duplicate=True),
    Input("gb-add-button", "n_clicks"),
    Input("comp-add-button", "n_clicks"),
    State("gb-preview-graph", "figure"),
    State("gb-title", "value"),
    State("gb-selected-chart-type", "data"),
    State("comp-preview-graph", "figure"),
    State("custom-graphs-store", "data"),
    prevent_initial_call=True,
)
def add_to_dashboard(n_gb, n_comp, gb_fig, gb_title, gb_type, comp_fig, existing):
    trig = ctx.triggered_id
    if existing is None:
        existing = []
        
    if trig == "gb-add-button":
        # Ensure figure is up to date before storing
        new_g = {"id": str(uuid.uuid4())[:8], "title": gb_title or "Custom Chart", "type": gb_type, "figure": gb_fig}
        existing.append(new_g)
        return existing, False, no_update
    if trig == "comp-add-button":
        # Force a deep copy or ensure figure object is correctly captured
        fig_to_store = go.Figure(comp_fig)
        new_g = {"id": str(uuid.uuid4())[:8], "title": "Comparison Chart", "type": "comparison", "figure": fig_to_store}
        existing.append(new_g)
        return existing, no_update, False
    return no_update, no_update, no_update


@callback(
    Output("custom-graph-gallery", "children"),
    Input("custom-graphs-store", "data"),
)
def render_gallery(graphs):
    if not graphs: return []
    
    # The render_gallery callback now returns content for the custom-graph-gallery div
    # within the GridStack structure. We need to generate the individual cards.
    if not graphs: return []

    gallery_items = []
    for g in graphs:
        card_content = dbc.Card(
            [
                dbc.CardHeader(
                    html.Div([
                        html.Div([
                            html.B(g.get("title", "Untitled"), className="me-2"),
                            dbc.Badge(g.get("type", "unknown").replace("_", " ").title(), color="primary", pill=True, className="small")
                        ]),
                        html.Div([
                            dbc.Button(html.I(className="bi bi-arrows-fullscreen"), id={"type": "gb-fs", "index": g["id"]}, color="link", size="sm", className="text-muted p-0 me-2"),
                            dbc.Button(html.I(className="bi bi-trash"), id={"type": "gb-del", "index": g["id"]}, color="link", size="sm", className="text-danger p-0"),
                        ], className="d-flex align-items-center")
                    ], className="d-flex justify-content-between align-items-center py-1")
                ),
                dbc.CardBody(
                    [
                        dcc.Graph(
                            figure=g["figure"],
                            id={"type": "gal-graph", "index": g["id"]},
                            config={"displayModeBar": True, "scrollZoom": True, "displaylogo": False},
                            style={"height": "100%", "width": "100%"}
                        ),
                        html.Div(id={"type": "gal-summary", "index": g["id"]}, className="small mt-1 text-muted")
                    ], className="p-2 d-flex flex-column", style={"flex": "1", "minHeight": "0"}
                ),
            ],
            className="shadow-sm h-100 d-flex flex-column resizable-chart",
        )
        
        gallery_items.append(
            dbc.Col(
                html.Div(
                    card_content,
                    id={"type": "chart-container", "index": g['id']},
                    className="chart-block-wrapper",
                    style={"height": "400px", "minHeight": "200px"}
                ),
                width=12, lg=6, className="mb-4"
            )
        )

    return dbc.Row(gallery_items, className="g-4")


@callback(
    Output("custom-graphs-store", "data", allow_duplicate=True),
    Input({"type": "gb-del", "index": ALL}, "n_clicks"),
    State("custom-graphs-store", "data"),
    prevent_initial_call=True,
)
def delete_from_gallery(n_clicks, existing):
    if not any(n_clicks): return no_update
    trig = ctx.triggered_id
    if isinstance(trig, dict) and trig.get("type") == "gb-del":
        return [g for g in existing if g["id"] != trig["index"]]
    return no_update


@callback(
    Output("fs-chart-modal", "is_open"),
    Output("fs-chart-title", "children"),
    Output("fs-chart-graph", "figure"),
    Input({"type": "gb-fs", "index": ALL}, "n_clicks"),
    Input("fs-close-button", "n_clicks"),
    State("custom-graphs-store", "data"),
    prevent_initial_call=True,
)
def handle_fullscreen(n_expand, n_close, graphs):
    trig = ctx.triggered_id
    if trig == "fs-close-button": return False, "", go.Figure()
    if isinstance(trig, dict) and trig.get("type") == "gb-fs":
        g = next((x for x in graphs if x["id"] == trig["index"]), None)
        if g: return True, g["title"], g["figure"]
    return False, no_update, no_update

# --- Report Generation ---

@callback(
    Output("download-report", "data"),
    Output("notification-toast-container", "children", allow_duplicate=True),
    Input("report-generate-button", "n_clicks"),
    State("report-title", "value"),
    State("report-sections", "value"),
    State("report-format", "value"),
    State("datasets-store", "data"),
    State("custom-graphs-store", "data"),
    prevent_initial_call=True,
)
def generate_report(n_clicks, title, sections, fmt, datasets, graphs):
    if not n_clicks: return no_update
    
    logger.info(f"Generating {fmt} report: {title}")
    
    # We use HTML as the base for both formats. 
    # For a real PDF, we would need a library like xhtml2pdf or reportlab.
    # Given the environment, we will provide a high-quality HTML report.
    
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 1200px; margin: 0 auto; padding: 40px; }}
            .header {{ text-align: center; border-bottom: 3px solid #004a99; padding-bottom: 20px; margin-bottom: 40px; }}
            h1 {{ color: #004a99; margin-bottom: 10px; }}
            h2 {{ color: #0056b3; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-top: 40px; }}
            h3 {{ color: #444; }}
            .metric-container {{ display: flex; flex-wrap: wrap; gap: 20px; margin: 20px 0; }}
            .metric-card {{ background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 20px; min-width: 180px; flex: 1; text-align: center; }}
            .metric-value {{ font-size: 24px; font-weight: bold; color: #007bff; }}
            .metric-label {{ font-size: 14px; color: #6c757d; text-transform: uppercase; }}
            .chart-box {{ background: white; border: 1px solid #dee2e6; border-radius: 8px; margin: 30px 0; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
            .chart-title {{ font-weight: bold; font-size: 18px; margin-bottom: 15px; border-bottom: 1px dashed #ddd; padding-bottom: 5px; }}
            .data-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            .data-table th, .data-table td {{ border: 1px solid #dee2e6; padding: 12px; text-align: left; }}
            .data-table th {{ background-color: #f1f3f5; font-weight: bold; }}
            .footer {{ margin-top: 60px; text-align: center; font-size: 12px; color: #999; border-top: 1px solid #eee; padding-top: 20px; }}
            .badge {{ display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; background: #007bff; color: white; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{title}</h1>
            <p>Pricing Derogation Analytics Report</p>
            <p>Generated on: {report_date}</p>
        </div>
    """
    
    if "summary" in sections:
        content += "<h2>Executive Summary</h2>"
        # Calculate some top-level metrics from all datasets combined if possible, or just summary stats
        total_rows = sum(ds.get('row_count', 0) for ds in datasets.values())
        content += f"""
        <p>This comprehensive analytics report encompasses data from <b>{len(datasets)}</b> active datasets, 
        containing a total of <b>{total_rows:,}</b> records. The analysis includes <b>{len(graphs)}</b> specialized visualizations.</p>
        
        <div class="metric-container">
            <div class="metric-card">
                <div class="metric-value">{len(datasets)}</div>
                <div class="metric-label">Datasets</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{len(graphs)}</div>
                <div class="metric-label">Visualizations</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{total_rows:,}</div>
                <div class="metric-label">Total Records</div>
            </div>
        </div>
        """
        
    if "datasets" in sections:
        content += "<h2>Dataset Inventory</h2>"
        content += "<table class='data-table'><thead><tr><th>Dataset Name</th><th>Source File</th><th>Rows</th><th>Columns</th><th>Status</th></tr></thead><tbody>"
        for ds in datasets.values():
            content += f"""
            <tr>
                <td><b>{ds['name']}</b></td>
                <td><code>{ds['filename']}</code></td>
                <td>{ds.get('row_count', 0):,}</td>
                <td>{ds.get('col_count', 0)}</td>
                <td><span class="badge">Loaded</span></td>
            </tr>
            """
        content += "</tbody></table>"
            
    if "charts" in sections:
        content += "<h2>Visual Analytics</h2>"
        if not graphs:
            content += "<p>No visualizations were added to this report.</p>"
        else:
            for g in graphs:
                # To make this offline compatible and include actual charts, 
                # we use Plotly's to_html method for each figure.
                fig = go.Figure(g['figure'])
                chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
                
                content += f"""
                <div class="chart-box">
                    <div class="chart-title">{g['title']} <span class="badge" style="float:right">{g.get('type', 'Custom').title()}</span></div>
                    <div class="chart-content">
                        {chart_html}
                    </div>
                </div>
                """
            
    content += f"""
        <div class="footer">
            <p>&copy; 2026 Daher Pricing Analytics. All rights reserved.</p>
            <p>Confidential Business Intelligence Report</p>
        </div>
    </body>
    </html>
    """
    
    filename = f"Report_{title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.{fmt}"
    
    if fmt == "pdf":
        # Rename to .html to avoid corruption error when opening, and warn user
        filename = filename.replace(".pdf", ".html")
        toast_msg = f"Report generated as HTML (best for charts). Open in browser to print as PDF."
    else:
        toast_msg = f"Report '{filename}' is ready for download."

    toast = dbc.Toast(
        toast_msg,
        header="Report Ready",
        icon="info",
        duration=5000,
        is_open=True,
        style={"width": "100%"}
    )
        
    return dict(content=content, filename=filename), toast


@callback(
    Output({"type": "gal-summary", "index": MATCH}, "children"),
    Input({"type": "gal-graph", "index": MATCH}, "selectedData"),
)
def update_gallery_selection(selected):
    if not selected or "points" not in selected or not selected["points"]: return ""
    pts = selected["points"]
    y_vals = [p.get("y") for p in pts if p.get("y") is not None]
    if not y_vals: return f"Selected {len(pts)} points"
    return f"Selected {len(pts)} points | Mean: {sum(y_vals)/len(y_vals):.2f}"


@callback(
    Output("custom-graphs-store", "data", allow_duplicate=True),
    Input({"type": "gb-move-left", "index": ALL}, "n_clicks"),
    Input({"type": "gb-move-right", "index": ALL}, "n_clicks"),
    State("custom-graphs-store", "data"),
    prevent_initial_call=True,
)
def move_graph_in_gallery(n_left, n_right, existing):
    """Reorders graphs in the gallery by moving them left or right."""
    if not any(n_left or []) and not any(n_right or []):
        return no_update
        
    trig = ctx.triggered_id
    if isinstance(trig, dict) and trig.get("type") in ["gb-move-left", "gb-move-right"]:
        graph_id = trig["index"]
        # Find current index
        idx = next((i for i, g in enumerate(existing) if g["id"] == graph_id), None)
        if idx is None: 
            return no_update
        
        new_existing = list(existing)
        if trig["type"] == "gb-move-left" and idx > 0:
            new_existing[idx], new_existing[idx-1] = new_existing[idx-1], new_existing[idx]
        elif trig["type"] == "gb-move-right" and idx < len(new_existing) - 1:
            new_existing[idx], new_existing[idx+1] = new_existing[idx+1], new_existing[idx]
            
        return new_existing
        
    return no_update


@callback(
    Output("comp-datasets-list", "value", allow_duplicate=True),
    Output("comp-x-axis", "value", allow_duplicate=True),
    Output("comp-y-axis", "value", allow_duplicate=True),
    Output("comp-aggregation", "value", allow_duplicate=True),
    Output("comp-type", "value", allow_duplicate=True),
    Output("comp-normalize", "value", allow_duplicate=True),
    Output("comp-sort-order", "value", allow_duplicate=True),
    Output("comp-theme", "value", allow_duplicate=True),
    Output("comp-x-label", "value", allow_duplicate=True),
    Output("comp-y-label", "value", allow_duplicate=True),
    Output("comp-title", "value", allow_duplicate=True),
    Input("comp-reset-button", "n_clicks"),
    prevent_initial_call=True
)
def reset_comp_builder(n_clicks):
    return [], None, None, "mean", "side_bar", [], "none", "plotly", "", "", ""


@callback(
    Output("gb-x-axis", "value", allow_duplicate=True),
    Output("gb-y-axis", "value", allow_duplicate=True),
    Output("gb-aggregation", "value", allow_duplicate=True),
    Output("gb-group-by", "value", allow_duplicate=True),
    Output("gb-secondary-y", "value", allow_duplicate=True),
    Output("gb-x-label", "value", allow_duplicate=True),
    Output("gb-y-label", "value", allow_duplicate=True),
    Output("gb-title", "value", allow_duplicate=True),
    Output("gb-show-labels", "value", allow_duplicate=True),
    Output("gb-show-grid", "value", allow_duplicate=True),
    Output("gb-sort-order", "value", allow_duplicate=True),
    Output("gb-theme", "value", allow_duplicate=True),
    Input("gb-reset-button", "n_clicks"),
    prevent_initial_call=True
)
def reset_gb_builder(n_clicks):
    return None, None, "none", None, [], "", "", "", [], ["show"], "none", "plotly"
