from dash import callback, Input, Output, State, html, dcc, no_update, ALL
from dash.exceptions import PreventUpdate
import json
import dash

# This callback saves the layout whenever a chart or gallery item is moved/resized
@callback(
    Output('dummy-output-layout', 'children'),  # Dummy output as we only want to save state
    Input({'type': 'gallery-item', 'index': ALL}, 'style'),
    Input({'type': 'chart-block', 'index': ALL}, 'style'),
    State('custom-graphs-store', 'data'),
    prevent_initial_call=True
)
def save_layout_state(gallery_styles, chart_styles, custom_graphs):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update

    # Extract sizes and positions from style
    layout_state = {
        "gallery_styles": gallery_styles,
        "chart_styles": chart_styles,
        "custom_graphs": custom_graphs
    }
    
    with open("layout_state.json", "w") as f:
        json.dump(layout_state, f, indent=2)
        
    return no_update

# This callback loads the layout when the page loads
@callback(
    Output({'type': 'gallery-item', 'index': ALL}, 'style'),
    Output({'type': 'chart-block', 'index': ALL}, 'style'),
    Input('dashboard-content-container', 'children'), # Trigger when main content is loaded
    prevent_initial_call=True
)
def load_layout_state(children):
    try:
        with open("layout_state.json", "r") as f:
            layout_state = json.load(f)
            return layout_state["gallery_styles"], layout_state["chart_styles"]
    except Exception:
        return no_update, no_update
