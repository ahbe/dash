"""
Footer component.
"""

from dash import html
import dash_bootstrap_components as dbc


def create_footer() -> html.Footer:
    """
    Creates the application footer.

    Returns:
        html.Footer: Footer component.
    """
    return html.Footer(
        dbc.Container(
            [
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            html.P(
                                [
                                    "© 2024 Pricing Derogation Dashboard. Built with ",
                                    html.A("Dash", href="https://dash.plotly.com/", target="_blank", className="text-primary"),
                                    " and ",
                                    html.A("uv", href="https://github.com/astral-sh/uv", target="_blank", className="text-primary"),
                                    ".",
                                ],
                                className="text-muted small",
                            ),
                            md=8,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.A(html.I(className="bi bi-github ms-3 text-muted"), href="#"),
                                    html.A(html.I(className="bi bi-linkedin ms-3 text-muted"), href="#"),
                                ],
                                className="text-end",
                            ),
                            md=4,
                        ),
                    ],
                    className="py-3",
                ),
            ],
            fluid=True,
        )
    )
