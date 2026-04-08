"""
Callbacks for dashboard layout management.
"""
from dash import callback, Input, Output, State, ALL, MATCH, no_update, ctx

# Per-tile actions that don't depend on GridStack
@callback(
    Output({"type": "chart-container", "index": MATCH}, "style"),
    Input({"type": "chart-delete", "index": MATCH}, "n_clicks"),
    State({"type": "chart-container", "index": MATCH}, "style"),
    prevent_initial_call=True
)
def handle_chart_delete(n_clicks, current_style):
    if n_clicks:
        style = current_style or {}
        style["display"] = "none"
        return style
    return no_update

@callback(
    Output({"type": "chart-pin", "index": MATCH}, "className"),
    Input({"type": "chart-pin", "index": MATCH}, "n_clicks"),
    State({"type": "chart-pin", "index": MATCH}, "className"),
    prevent_initial_call=True
)
def toggle_pin(n_clicks, current_class):
    if n_clicks:
        if "active" in current_class:
            return current_class.replace(" active", "")
        return current_class + " active"
    return no_update
