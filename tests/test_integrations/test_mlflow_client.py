"""
Tests for the MLflow integration client.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.integrations.mlflow_client import MLflowClient


@patch("src.integrations.mlflow_client.mlflow")
def test_mlflow_client_get_model_info(mock_mlflow, mock_settings):
    """
    Tests fetching model information from MLflow.
    """
    mock_mlflow.tracking.MlflowClient.return_value = MagicMock()
    mock_client = mock_mlflow.tracking.MlflowClient.return_value
    
    # Mock latest versions
    mock_latest_version = MagicMock()
    mock_latest_version.name = "test_model"
    mock_latest_version.version = "1"
    mock_latest_version.current_stage = "Production"
    mock_latest_version.run_id = "run123"
    mock_client.get_latest_versions.return_value = [mock_latest_version]
    
    # Mock run info
    mock_run = MagicMock()
    mock_run.data.metrics = {"accuracy": 0.95}
    mock_run.info.start_time = 1678886400000  # Example timestamp
    mock_client.get_run.return_value = mock_run

    client = MLflowClient("http://test-mlflow.com")
    model_info = client.get_registered_model_info("test_model")

    assert model_info is not None
    assert model_info["name"] == "test_model"
    assert model_info["version"] == "1"
    assert model_info["status"] == "Production"
    assert model_info["metrics"] == {"accuracy": 0.95}
    assert model_info["last_trained"] == "2023-03-15"


def test_mlflow_client_not_configured(mock_settings):
    """
    Tests MLflow client when not configured.
    """
    client = MLflowClient(tracking_uri=None)
    model_info = client.get_registered_model_info("test_model")
    assert model_info is None
