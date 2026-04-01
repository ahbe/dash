"""
Entry point for local development.
Starts the Dash development server.
"""

from src.index import app
from src.config import settings
from src.utils.logger import logger
from src.scheduling.scheduler import setup_scheduler
import src.callbacks.filter_callbacks
import src.callbacks.metric_callbacks
import src.callbacks.chart_callbacks
import src.callbacks.alert_callbacks
import src.callbacks.refresh_callbacks
import src.callbacks.model_callbacks


if __name__ == "__main__":
    logger.info("Starting local development server...")
    
    # Initialize background scheduler
    scheduler = setup_scheduler()
    
    try:
        app.run(
            debug=True,
            host=settings.APP_HOST,
            port=settings.APP_PORT
        )
    except (KeyboardInterrupt, SystemExit):
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("App stopped.")
