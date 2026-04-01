"""
Microsoft SharePoint connector using O365 library.
"""

from typing import Any, Optional
import pandas as pd
import io
from src.data.connectors.base_connector import BaseConnector
from src.utils.logger import logger
from src.config import settings

try:
    from O365 import Account
except ImportError:
    Account = None


class SharePointConnector(BaseConnector):
    """
    Connector for Microsoft SharePoint / OneDrive files.
    """

    def __init__(self, name: str = "SharePointConnector"):
        super().__init__(name)
        self.client_id = settings.SHAREPOINT_CLIENT_ID
        self.client_secret = settings.SHAREPOINT_CLIENT_SECRET
        self.tenant_id = settings.SHAREPOINT_TENANT_ID
        self.site_url = settings.SHAREPOINT_URL

    def connect(self) -> None:
        """
        Initializes the O365 account.
        """
        if not Account:
            logger.warning(f"{self.name}: O365 package not installed.")
            return

        if not all([self.client_id, self.client_secret, self.tenant_id]):
            logger.warning(f"{self.name}: Missing configuration for SharePoint.")
            return

        try:
            credentials = (self.client_id, self.client_secret)
            self.connection = Account(credentials, tenant_id=self.tenant_id)
            if not self.connection.is_authenticated:
                logger.info(f"{self.name}: Account not authenticated. Manual step required.")
            else:
                logger.info(f"{self.name}: SharePoint client initialized.")
        except Exception as e:
            logger.error(f"{self.name}: Failed to initialize SharePoint client: {e}")

    def fetch(self, query: Optional[str] = None, **kwargs: Any) -> pd.DataFrame:
        """
        Downloads a file from SharePoint and returns it as a DataFrame.

        Args:
            query: Path to the file in SharePoint.
            **kwargs: Additional parameters for pd.read_csv or pd.read_excel.

        Returns:
            pd.DataFrame: Data from SharePoint.
        """
        if not self.connection:
            self.connect()

        if not self.connection or not self.connection.is_authenticated:
            logger.error(f"{self.name}: No authenticated connection.")
            return pd.DataFrame()

        if not query:
            logger.error(f"{self.name}: No file path provided.")
            return pd.DataFrame()

        try:
            # This is a simplified example. O365 usage depends on specific site/drive structure.
            storage = self.connection.storage()
            drive = storage.get_default_drive()
            file_item = drive.get_item_by_path(query)
            
            content = file_item.get_content()
            
            if query.endswith(".csv"):
                return pd.read_csv(io.BytesIO(content), **kwargs)
            elif query.endswith(".xlsx") or query.endswith(".xls"):
                return pd.read_excel(io.BytesIO(content), **kwargs)
            else:
                logger.error(f"{self.name}: Unsupported file format for {query}")
                return pd.DataFrame()

        except Exception as e:
            logger.error(f"{self.name}: Failed to fetch file {query} from SharePoint: {e}")
            return pd.DataFrame()

    def is_available(self) -> bool:
        """
        Checks if the SharePoint client is authenticated.
        """
        return self.connection is not None and self.connection.is_authenticated
