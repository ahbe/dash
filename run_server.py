"""
Entry point for production.
Serves the app using Gunicorn or Waitress.
"""

import os
from src.index import app
from src.app import server
from src.config import settings
from src.utils.logger import logger
from src.scheduling.scheduler import setup_scheduler
import src.callbacks.filter_callbacks
import src.callbacks.metric_callbacks
import src.callbacks.chart_callbacks
import src.callbacks.alert_callbacks
import src.callbacks.refresh_callbacks
import src.callbacks.model_callbacks


# Initialize background scheduler
scheduler = setup_scheduler()

if __name__ == "__main__":
    if os.name == "nt":
        # Windows
        from waitress import serve
        logger.info(f"Starting Waitress server on port {settings.APP_PORT}...")
        serve(server, host=settings.APP_HOST, port=settings.APP_PORT)
    else:
        # Linux (Gunicorn usually handles this via CLI, but this is a fallback)
        logger.info(f"Starting production server on port {settings.APP_PORT}...")
        # In Linux, you'd typically run: gunicorn run_server:server
