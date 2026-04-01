"""
CSV and Excel file data connector.
Supports reading from local paths and manual file uploads.
"""

from typing import Any, Optional
import pandas as pd
from src.data.connectors.base_connector import BaseConnector
from src.utils.logger import logger


class CSVConnector(BaseConnector):
    """
    Connector for CSV and XLSX files.
    """

    def __init__(self, name: str = "CSVConnector"):
        super().__init__(name)

    def connect(self) -> None:
        """
        No persistent connection needed for CSV files.
        """
        logger.info(f"{self.name}: Ready to read files.")

    def fetch(self, query: Optional[str] = None, **kwargs: Any) -> pd.DataFrame:
        """
        Reads a CSV or Excel file.

        Args:
            query: Path to the file.
            **kwargs: Additional parameters for pd.read_csv or pd.read_excel.

        Returns:
            pd.DataFrame: Data from the file.
        """
        if not query:
            logger.error(f"{self.name}: No file path provided.")
            return pd.DataFrame()

        try:
            if query.endswith(".csv"):
                return pd.read_csv(query, **kwargs)
            elif query.endswith(".xlsx") or query.endswith(".xls"):
                return pd.read_excel(query, **kwargs)
            else:
                logger.error(f"{self.name}: Unsupported file format for {query}")
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"{self.name}: Failed to read {query}: {e}")
            return pd.DataFrame()

    def is_available(self) -> bool:
        """
        CSV connector is always considered available.
        """
        return True
