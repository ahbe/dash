"""
Central data orchestrator.
Registers data sources and provides a unified interface for data access with caching.
"""

from typing import Any, Dict, Optional
import pandas as pd
from src.data.connectors.base_connector import BaseConnector
from src.data.connectors.csv_connector import CSVConnector
from src.data.connectors.postgres_connector import PostgresConnector
from src.data.connectors.cos_connector import COSConnector
from src.data.connectors.domino_connector import DominoConnector
from src.data.connectors.sharepoint_connector import SharePointConnector
from src.data.cache import cache
from src.utils.logger import logger
from src.config import settings


class DataManager:
    """
    Manages multiple data sources and handles fetching/caching.
    """

    def __init__(self):
        self._connectors: Dict[str, BaseConnector] = {}
        self._register_default_connectors()

    def _register_default_connectors(self) -> None:
        """
        Registers all available connectors.
        """
        self.register_connector("csv", CSVConnector())
        self.register_connector("postgres", PostgresConnector())
        self.register_connector("cos", COSConnector())
        self.register_connector("domino", DominoConnector())
        self.register_connector("sharepoint", SharePointConnector())

    def register_connector(self, name: str, connector: BaseConnector) -> None:
        """
        Registers a new data connector.

        Args:
            name: Unique name for the connector.
            connector: Connector instance.
        """
        logger.info(f"Registering data connector: {name}")
        self._connectors[name] = connector

    def get_data(
        self,
        source_name: str,
        query: Optional[str] = None,
        use_cache: bool = True,
        **kwargs: Any
    ) -> pd.DataFrame:
        """
        Fetches data from a specific source with optional caching.

        Args:
            source_name: Name of the registered connector.
            query: Query string or path.
            use_cache: Whether to use the cache.
            **kwargs: Additional parameters for fetching.

        Returns:
            pd.DataFrame: Fetched data.
        """
        cache_key = f"{source_name}:{query}:{kwargs}"
        
        if use_cache:
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return cached_data

        if source_name not in self._connectors:
            logger.error(f"Data source '{source_name}' not registered.")
            return pd.DataFrame()

        connector = self._connectors[source_name]
        data = connector.fetch(query, **kwargs)
        
        if use_cache and not data.empty:
            cache.set(cache_key, data)
            
        return data

    def refresh_all(self) -> None:
        """
        Clears the cache to force a fresh fetch on next requests.
        """
        cache.clear()


# Global data manager instance
data_manager = DataManager()
