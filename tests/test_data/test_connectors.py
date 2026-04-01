"""
Tests for data connectors.
"""

import pandas as pd
import pytest
from src.data.connectors.csv_connector import CSVConnector
from src.data.connectors.postgres_connector import PostgresConnector
from src.data.connectors.base_connector import BaseConnector
from unittest.mock import patch, MagicMock
import os


@pytest.fixture
def mock_settings(mocker):
    """
    Mocks settings for connector tests.
    """
    mocker.patch("src.config.settings.POSTGRES_URL", "postgresql://user:pass@host:1234/db")
    mocker.patch("src.config.settings.COS_ENDPOINT", "http://cos.endpoint")
    mocker.patch("src.config.settings.COS_API_KEY", "api_key")
    mocker.patch("src.config.settings.COS_BUCKET", "test_bucket")
    mocker.patch("src.config.settings.COS_INSTANCE_CRN", "crn")
    mocker.patch("src.config.settings.DOMINO_API_HOST", "http://domino.host")
    mocker.patch("src.config.settings.DOMINO_API_KEY", "domino_key")
    mocker.patch("src.config.settings.DOMINO_PROJECT", "test_project")
    mocker.patch("src.config.settings.SHAREPOINT_URL", "http://sharepoint.url")
    mocker.patch("src.config.settings.SHAREPOINT_CLIENT_ID", "sp_client_id")
    mocker.patch("src.config.settings.SHAREPOINT_CLIENT_SECRET", "sp_client_secret")
    mocker.patch("src.config.settings.SHAREPOINT_TENANT_ID", "sp_tenant_id")


def test_csv_connector_fetch_csv(tmp_path, sample_dataframe):
    """
    Tests CSV connector with a CSV file.
    """
    csv_file = tmp_path / "test.csv"
    sample_dataframe.to_csv(csv_file, index=False)

    connector = CSVConnector()
    df = connector.fetch(str(csv_file))

    pd.testing.assert_frame_equal(df, sample_dataframe)


def test_csv_connector_fetch_non_existent():
    """
    Tests CSV connector with a non-existent file.
    """
    connector = CSVConnector()
    df = connector.fetch("non_existent.csv")
    assert df.empty


@patch("src.data.connectors.postgres_connector.create_engine")
def test_postgres_connector_fetch(mock_create_engine, mock_settings, sample_dataframe):
    """
    Tests PostgreSQL connector fetch method.
    """
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine
    
    mock_read_sql = MagicMock(return_value=sample_dataframe)
    with patch("pandas.read_sql", mock_read_sql):
        connector = PostgresConnector()
        df = connector.fetch("SELECT * FROM test_table")
        
        assert not df.empty
        pd.testing.assert_frame_equal(df, sample_dataframe)
        mock_read_sql.assert_called_once_with("SELECT * FROM test_table", mock_engine)


@patch("src.data.connectors.cos_connector.ibm_boto3")
def test_cos_connector_fetch(mock_ibm_boto3, mock_settings, sample_dataframe):
    """
    Tests COS connector fetch method.
    """
    mock_resource = MagicMock()
    mock_ibm_boto3.resource.return_value = mock_resource
    mock_object = MagicMock()
    mock_resource.Object.return_value = mock_object
    mock_object.get.return_value = {"Body": MagicMock(read=lambda: sample_dataframe.to_csv(index=False).encode("utf-8"))}

    connector = COSConnector()
    df = connector.fetch("test_object.csv")
    
    assert not df.empty
    pd.testing.assert_frame_equal(df, sample_dataframe)


@patch("src.data.connectors.domino_connector.Domino")
@patch("src.data.connectors.domino_connector.os.path.exists", return_value=True)
@patch("src.data.connectors.domino_connector.pd.read_csv")
def test_domino_connector_fetch_local(mock_read_csv, mock_exists, mock_domino, mock_settings, sample_dataframe):
    """
    Tests Domino connector fetching from a local (mounted) path.
    """
    mock_read_csv.return_value = sample_dataframe
    connector = DominoConnector()
    df = connector.fetch("domino_data.csv")
    
    assert not df.empty
    pd.testing.assert_frame_equal(df, sample_dataframe)
    mock_read_csv.assert_called_once_with("domino_data.csv")


@patch("src.data.connectors.sharepoint_connector.Account")
def test_sharepoint_connector_fetch(mock_account, mock_settings, sample_dataframe):
    """
    Tests SharePoint connector fetch method.
    """
    mock_account_instance = MagicMock()
    mock_account.return_value = mock_account_instance
    mock_account_instance.is_authenticated = True
    mock_storage = MagicMock()
    mock_account_instance.storage.return_value = mock_storage
    mock_drive = MagicMock()
    mock_storage.get_default_drive.return_value = mock_drive
    mock_file_item = MagicMock()
    mock_drive.get_item_by_path.return_value = mock_file_item
    mock_file_item.get_content.return_value = sample_dataframe.to_csv(index=False).encode("utf-8")

    connector = SharePointConnector()
    df = connector.fetch("sharepoint_file.csv")

    assert not df.empty
    pd.testing.assert_frame_equal(df, sample_dataframe)
