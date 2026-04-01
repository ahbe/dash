"""
Main layout assembly.
Composes the full dashboard page by combining header, sidebar, main content, and footer.
"""

import dash_bootstrap_components as dbc
from dash import html
from src.app import app
from src.layouts.header import create_header
from src.layouts.sidebar import create_sidebar
from src.layouts.main_content import create_main_content
from src.layouts.footer import create_footer


def serve_layout() -> dbc.Container:
    """
    Assembles and returns the full application layout.

    Returns:
        dbc.Container: Full layout container.
    """
    return dbc.Container(
        [
            create_header(),
            dbc.Row(
                [
                    dbc.Col(create_sidebar(), width=12, md=3, lg=2, className="px-0"),
                    dbc.Col(create_main_content(), width=12, md=9, lg=10),
                ],
                className="g-0",
            ),
            create_footer(),
        ],
        fluid=True,
        className="px-0",
    )


# Set the app layout
app.layout = serve_layout
