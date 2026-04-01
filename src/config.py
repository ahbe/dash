"""
Centralized configuration module for the Pricing Derogation Dashboard.
Loads settings from environment variables with sensible defaults.
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings and environment variables.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App Info
    APP_TITLE: str = "Pricing Derogation Dashboard"
    APP_THEME: str = "FLATLY"  # Bootstrap theme
    APP_DEBUG: bool = False
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8050

    # PostgreSQL Configuration
    POSTGRES_URL: Optional[str] = None

    # IBM Cloud Object Storage (COS)
    COS_ENDPOINT: Optional[str] = None
    COS_API_KEY: Optional[str] = None
    COS_BUCKET: Optional[str] = None
    COS_INSTANCE_CRN: Optional[str] = None

    # SharePoint / Office 365
    SHAREPOINT_URL: Optional[str] = None
    SHAREPOINT_CLIENT_ID: Optional[str] = None
    SHAREPOINT_CLIENT_SECRET: Optional[str] = None
    SHAREPOINT_TENANT_ID: Optional[str] = None

    # Domino Data Lab
    DOMINO_API_HOST: Optional[str] = None
    DOMINO_API_KEY: Optional[str] = None
    DOMINO_PROJECT: Optional[str] = None

    # MLflow
    MLFLOW_TRACKING_URI: Optional[str] = None

    # Cache & Refresh
    CACHE_TTL_SECONDS: int = 3600
    REFRESH_SCHEDULE_HOUR: int = 2  # 2 AM daily

    # Alerts
    ALERT_RULES_PATH: str = "src/alerts/alert_rules.yaml"

    # Data Paths
    SAMPLE_DATA_PATH: str = "data/sample/sample_data.csv"


# Global settings instance
settings = Settings()
