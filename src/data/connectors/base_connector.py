"""
Abstract base class for all data connectors.
Defines the required interface for data source access.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
import pandas as pd
from src.utils.logger import logger


class BaseConnector(ABC):
    """
    Abstract base class for all data connectors.
    """

    def __init__(self, name: str):
        self.name = name
        self.connection = None

    @abstractmethod
    def connect(self) -> None:
        """
        Establishes a connection to the data source.
        """
        pass

    @abstractmethod
    def fetch(self, query: Optional[str] = None, **kwargs: Any) -> pd.DataFrame:
        """
        Fetches data from the data source and returns a pandas DataFrame.

        Args:
            query: Optional query string (SQL, URL, path, etc.)
            **kwargs: Additional parameters for fetching.

        Returns:
            pd.DataFrame: Fetched data.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Checks if the data source is available.

        Returns:
            bool: True if available, False otherwise.
        """
        pass

    def disconnect(self) -> None:
        """
        Closes the connection to the data source.
        """
        if self.connection:
            logger.info(f"Disconnecting from {self.name}...")
            # Implement specific disconnect logic in subclasses if needed
            self.connection = None
