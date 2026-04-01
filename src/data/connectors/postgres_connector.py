"""
PostgreSQL database connector using SQLAlchemy.
"""

from typing import Any, Optional
import pandas as pd
from sqlalchemy import create_engine
from src.data.connectors.base_connector import BaseConnector
from src.utils.logger import logger
from src.config import settings


class PostgresConnector(BaseConnector):
    """
    Connector for PostgreSQL databases.
    """

    def __init__(self, name: str = "PostgresConnector"):
        super().__init__(name)
        self.db_url = settings.POSTGRES_URL

    def connect(self) -> None:
        """
        Creates a SQLAlchemy engine.
        """
        if not self.db_url:
            logger.warning(f"{self.name}: POSTGRES_URL not configured.")
            return

        try:
            self.connection = create_engine(self.db_url)
            logger.info(f"{self.name}: Connection engine created.")
        except Exception as e:
            logger.error(f"{self.name}: Failed to create engine: {e}")

    def fetch(self, query: Optional[str] = None, **kwargs: Any) -> pd.DataFrame:
        """
        Executes a SQL query and returns the results as a DataFrame.

        Args:
            query: SQL query string.
            **kwargs: Additional parameters for pd.read_sql.

        Returns:
            pd.DataFrame: Query results.
        """
        if not self.connection:
            self.connect()

        if not self.connection:
            logger.error(f"{self.name}: No active connection.")
            return pd.DataFrame()

        if not query:
            logger.error(f"{self.name}: No query provided.")
            return pd.DataFrame()

        try:
            return pd.read_sql(query, self.connection, **kwargs)
        except Exception as e:
            logger.error(f"{self.name}: Failed to execute query: {e}")
            return pd.DataFrame()

    def is_available(self) -> bool:
        """
        Checks if the database is reachable.
        """
        if not self.db_url:
            return False

        try:
            if not self.connection:
                self.connect()
            with self.connection.connect() as conn:
                return True
        except Exception:
            return False
