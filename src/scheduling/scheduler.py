"""
Background scheduler for daily auto-refresh.
Uses APScheduler.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from src.data.data_manager import data_manager
from src.utils.logger import logger
from src.config import settings


def refresh_job() -> None:
    """
    Job to be executed by the scheduler.
    """
    logger.info("Scheduled data refresh starting...")
    data_manager.refresh_all()
    # Pre-fetch data to warm the cache
    data_manager.get_data("csv", query="data/sample/sample_data.csv")
    logger.info("Scheduled data refresh completed.")


def setup_scheduler() -> BackgroundScheduler:
    """
    Configures and starts the background scheduler.

    Returns:
        BackgroundScheduler: The started scheduler instance.
    """
    scheduler = BackgroundScheduler()
    
    # Schedule daily refresh
    scheduler.add_job(
        refresh_job,
        "cron",
        hour=settings.REFRESH_SCHEDULE_HOUR,
        id="daily_refresh"
    )
    
    scheduler.start()
    logger.info(f"Background scheduler started. Daily refresh at {settings.REFRESH_SCHEDULE_HOUR}:00")
    
    return scheduler
