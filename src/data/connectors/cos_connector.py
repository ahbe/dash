"""
IBM Cloud Object Storage (COS) connector.
"""

from typing import Any, Optional
import pandas as pd
import ibm_boto3
from ibm_botocore.client import Config
from src.data.connectors.base_connector import BaseConnector
from src.utils.logger import logger
from src.config import settings
import io


class COSConnector(BaseConnector):
    """
    Connector for IBM Cloud Object Storage.
    """

    def __init__(self, name: str = "COSConnector"):
        super().__init__(name)
        self.endpoint = settings.COS_ENDPOINT
        self.api_key = settings.COS_API_KEY
        self.instance_crn = settings.COS_INSTANCE_CRN
        self.bucket = settings.COS_BUCKET

    def connect(self) -> None:
        """
        Initializes the COS client.
        """
        if not all([self.endpoint, self.api_key, self.instance_crn]):
            logger.warning(f"{self.name}: Missing configuration for IBM COS.")
            return

        try:
            self.connection = ibm_boto3.resource(
                "s3",
                ibm_api_key_id=self.api_key,
                ibm_service_instance_id=self.instance_crn,
                config=Config(signature_version="oauth"),
                endpoint_url=self.endpoint,
            )
            logger.info(f"{self.name}: COS client initialized.")
        except Exception as e:
            logger.error(f"{self.name}: Failed to initialize COS client: {e}")

    def fetch(self, query: Optional[str] = None, **kwargs: Any) -> pd.DataFrame:
        """
        Downloads a file from COS and returns it as a DataFrame.

        Args:
            query: Object key (file name) in the bucket.
            **kwargs: Additional parameters for pd.read_csv or pd.read_excel.

        Returns:
            pd.DataFrame: Data from the COS object.
        """
        if not self.connection:
            self.connect()

        if not self.connection:
            logger.error(f"{self.name}: No active connection.")
            return pd.DataFrame()

        if not query:
            logger.error(f"{self.name}: No object key provided.")
            return pd.DataFrame()

        try:
            obj = self.connection.Object(self.bucket, query).get()
            data = obj["Body"].read()

            if query.endswith(".csv"):
                return pd.read_csv(io.BytesIO(data), **kwargs)
            elif query.endswith(".xlsx") or query.endswith(".xls"):
                return pd.read_excel(io.BytesIO(data), **kwargs)
            else:
                logger.error(f"{self.name}: Unsupported file format for {query}")
                return pd.DataFrame()

        except Exception as e:
            logger.error(f"{self.name}: Failed to fetch object {query} from COS: {e}")
            return pd.DataFrame()

    def is_available(self) -> bool:
        """
        Checks if the COS service is available and bucket is accessible.
        """
        if not self.connection:
            self.connect()

        if not self.connection:
            return False

        try:
            self.connection.meta.client.head_bucket(Bucket=self.bucket)
            return True
        except Exception:
            return False
