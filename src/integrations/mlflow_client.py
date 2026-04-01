"""
MLflow integration client.
Fetches model registry and run info.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import os
from src.utils.logger import logger
from src.config import settings

try:
    import mlflow
except ImportError:
    mlflow = None


class MLflowClient:
    """
    Client for interacting with MLflow Tracking Server.
    """

    def __init__(self, tracking_uri: Optional[str] = settings.MLFLOW_TRACKING_URI):
        self.tracking_uri = tracking_uri
        self.is_configured = False
        self._setup()

    def _setup(self) -> None:
        """
        Sets up the MLflow connection.
        """
        if mlflow is None:
            logger.warning("MLflow package not installed.")
            return

        if not self.tracking_uri:
            logger.info("MLflow Tracking URI not configured.")
            return

        try:
            mlflow.set_tracking_uri(self.tracking_uri)
            self.is_configured = True
            logger.info(f"MLflow client connected to {self.tracking_uri}")
        except Exception as e:
            logger.error(f"Failed to connect to MLflow: {e}")

    def get_registered_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetches information for a registered model.

        Args:
            model_name: Name of the model.

        Returns:
            Optional[Dict[str, Any]]: Model info if found.
        """
        if not self.is_configured:
            return None

        try:
            client = mlflow.tracking.MlflowClient()
            latest_versions = client.get_latest_versions(model_name, stages=["Production", "Staging"])
            
            if not latest_versions:
                return None

            latest = latest_versions[0]
            run = client.get_run(latest.run_id)
            
            return {
                "name": latest.name,
                "version": latest.version,
                "status": latest.current_stage,
                "metrics": run.data.metrics,
                "last_trained": datetime.fromtimestamp(run.info.start_time / 1000).strftime("%Y-%m-%d") if hasattr(run.info, 'start_time') else "N/A"
            }
        except Exception as e:
            logger.error(f"Error fetching MLflow model info: {e}")
            return None


# Global MLflow client instance
mlflow_client = MLflowClient()
