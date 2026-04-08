"""
Dash app factory module.
Creates and configures the Dash application instance.
"""

import dash
import dash_bootstrap_components as dbc
from src.config import settings
from src.utils.logger import logger


def create_app() -> dash.Dash:
    """
    Creates and returns a Dash application instance.

    Returns:
        dash.Dash: Configured Dash app.
    """
    logger.info("Initializing Dash application...")

    # Choose theme from settings
    theme = getattr(dbc.themes, settings.APP_THEME, dbc.themes.FLATLY)

    app = dash.Dash(
        __name__,
        external_stylesheets=[theme, dbc.icons.BOOTSTRAP, "/assets/custom.css"],
        external_scripts=[],
        suppress_callback_exceptions=True,
        title=settings.APP_TITLE,
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ],
    )

    # Expose the flask server for gunicorn/waitress
    server = app.server

    logger.info("Dash application instance created successfully.")
    return app


# Create the app instance
app = create_app()
server = app.server
