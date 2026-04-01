"""
DVC integration client.
Parses DVC metrics and pipeline status.
"""

import json
import os
from typing import Any, Dict, Optional
from src.utils.logger import logger


class DVCClient:
    """
    Client for interacting with DVC (Data Version Control).
    """

    def __init__(self, project_path: str = "."):
        self.project_path = project_path

    def get_metrics(self) -> Dict[str, Any]:
        """
        Parses metrics from metrics.json if it exists.

        Returns:
            Dict[str, Any]: Metrics data.
        """
        metrics_path = os.path.join(self.project_path, "metrics.json")
        if not os.path.exists(metrics_path):
            logger.info("DVC metrics.json not found.")
            return {}

        try:
            with open(metrics_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error parsing DVC metrics: {e}")
            return {}

    def get_pipeline_status(self) -> str:
        """
        Checks for dvc.yaml to determine pipeline status.

        Returns:
            str: Status message.
        """
        if os.path.exists(os.path.join(self.project_path, "dvc.yaml")):
            return "Active"
        return "Not Initialized"


# Global DVC client instance
dvc_client = DVCClient()
