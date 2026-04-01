"""
Tests for the DVC integration client.
"""

import pytest
from unittest.mock import patch, mock_open
from src.integrations.dvc_client import DVCClient
import json
import os


def test_dvc_client_get_metrics_success(tmp_path):
    """
    Tests fetching DVC metrics when metrics.json exists.
    """
    metrics_data = {"f1_score": 0.85, "accuracy": 0.92}
    metrics_file = tmp_path / "metrics.json"
    with open(metrics_file, "w") as f:
        json.dump(metrics_data, f)

    client = DVCClient(project_path=str(tmp_path))
    metrics = client.get_metrics()
    assert metrics == metrics_data


def test_dvc_client_get_metrics_not_found(tmp_path):
    """
    Tests fetching DVC metrics when metrics.json does not exist.
    """
    client = DVCClient(project_path=str(tmp_path))
    metrics = client.get_metrics()
    assert metrics == {}


def test_dvc_client_get_pipeline_status_active(tmp_path):
    """
    Tests DVC pipeline status when dvc.yaml exists.
    """
    dvc_yaml = tmp_path / "dvc.yaml"
    dvc_yaml.write_text("stages:\n  train: ")

    client = DVCClient(project_path=str(tmp_path))
    status = client.get_pipeline_status()
    assert status == "Active"


def test_dvc_client_get_pipeline_status_not_initialized(tmp_path):
    """
    Tests DVC pipeline status when dvc.yaml does not exist.
    """
    client = DVCClient(project_path=str(tmp_path))
    status = client.get_pipeline_status()
    assert status == "Not Initialized"
