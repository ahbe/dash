"""
Top navigation bar / header component.
"""

import dash_bootstrap_components as dbc
from dash import html
from src.config import settings
from src.components.refresh_button import create_refresh_button


def create_header() -> dbc.Navbar:
    """
    Creates the application header/navbar.

    Returns:
        dbc.Navbar: Styled navbar component.
    """
    brand = dbc.Row(
        [
            dbc.Col(html.I(className="bi bi-bar-chart-fill fs-3 text-white me-2")),
            dbc.Col(dbc.NavbarBrand(settings.APP_TITLE, className="ms-2 fs-4")),
        ],
        align="center",
        className="g-0",
    )

    return dbc.Navbar(
        dbc.Container(
            [
                html.A(brand, href="/", style={"textDecoration": "none"}),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(create_refresh_button()),
                        ],
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ],
            fluid=True,
        ),
        color="primary",
        dark=True,
        className="mb-4 shadow",
    )
