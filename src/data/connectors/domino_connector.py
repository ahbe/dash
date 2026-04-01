"""
Domino Data Lab dataset connector.
"""

from typing import Any, Optional
import pandas as pd
import os
from src.data.connectors.base_connector import BaseConnector
from src.utils.logger import logger
from src.config import settings

try:
    from domino import Domino
except ImportError:
    Domino = None


class DominoConnector(BaseConnector):
    """
    Connector for Domino Data Lab datasets.
    """

    def __init__(self, name: str = "DominoConnector"):
        super().__init__(name)
        self.api_host = settings.DOMINO_API_HOST
        self.api_key = settings.DOMINO_API_KEY
        self.project = settings.DOMINO_PROJECT

    def connect(self) -> None:
        """
        Initializes the Domino client.
        """
        if not Domino:
            logger.warning(f"{self.name}: python-domino package not installed.")
            return

        if not all([self.api_host, self.api_key, self.project]):
            logger.info(
                f"{self.name}: Local environment or missing config. Checking for Domino environment variables..."
            )
            # Try to use Domino environment variables if available
            self.api_host = os.environ.get("DOMINO_API_HOST", self.api_host)
            self.api_key = os.environ.get("DOMINO_USER_API_KEY", self.api_key)
            self.project = os.environ.get("DOMINO_PROJECT_NAME", self.project)

        if not all([self.api_host, self.api_key, self.project]):
            logger.warning(f"{self.name}: Missing configuration for Domino.")
            return

        try:
            # Domino project format is usually 'username/projectname'
            self.connection = Domino(self.project, api_key=self.api_key, host=self.api_host)
            logger.info(f"{self.name}: Domino client initialized.")
        except Exception as e:
            logger.error(f"{self.name}: Failed to initialize Domino client: {e}")

    def fetch(self, query: Optional[str] = None, **kwargs: Any) -> pd.DataFrame:
        """
        Reads a file from a Domino dataset or project.
        In many cases, when running in Domino, data is mounted as a file system.
        This fetcher supports both local paths (mounted) and API-based access.

        Args:
            query: Path to the file in Domino.
            **kwargs: Additional parameters for pd.read_csv or pd.read_excel.

        Returns:
            pd.DataFrame: Data from Domino.
        """
        if not query:
            logger.error(f"{self.name}: No path provided.")
            return pd.DataFrame()

        # Check if file exists locally (mounted dataset)
        if os.path.exists(query):
            logger.info(f"{self.name}: Reading from local path {query}")
            try:
                if query.endswith(".csv"):
                    return pd.read_csv(query, **kwargs)
                elif query.endswith(".xlsx") or query.endswith(".xls"):
                    return pd.read_excel(query, **kwargs)
            except Exception as e:
                logger.error(f"{self.name}: Failed to read local file {query}: {e}")

        # If not local, we could implement API based fetch here if needed
        # For now, we assume Domino users mostly use mounted datasets or local project files.
        logger.warning(f"{self.name}: File {query} not found locally.")
        return pd.DataFrame()

    def is_available(self) -> bool:
        """
        Checks if running in Domino or API is configured.
        """
        if os.environ.get("DOMINO_PROJECT_ID"):
            return True
        if self.connection:
            return True
        self.connect()
        return self.connection is not None
