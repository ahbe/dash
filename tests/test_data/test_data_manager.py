"""
Tests for the data_manager module.
"""

import pandas as pd
from src.data.data_manager import DataManager
from src.data.connectors.base_connector import BaseConnector
import pytest
from typing import Any


class MockConnector(BaseConnector):
    """
    A mock connector for testing purposes.
    """
    def __init__(self, name: str, data: pd.DataFrame = pd.DataFrame()):
        super().__init__(name)
        self._data = data

    def connect(self) -> None:
        pass

    def fetch(self, query: str | None = None, **kwargs: Any) -> pd.DataFrame:
        return self._data

    def is_available(self) -> bool:
        return True


def test_data_manager_registration():
    """
    Tests connector registration in DataManager.
    """
    manager = DataManager()
    mock_conn = MockConnector("mock_source")
    manager.register_connector("mock", mock_conn)
    assert "mock" in manager._connectors


def test_data_manager_get_data_no_cache(sample_dataframe: pd.DataFrame, mocker: Any):
    """
    Tests data retrieval without caching.
    """
    manager = DataManager()
    mock_conn = MockConnector("mock_source", data=sample_dataframe)
    mocker.patch.dict(manager._connectors, {"mock": mock_conn})
    
    # Disable default csv connector for this test
    mocker.patch.object(manager._connectors["csv"], "fetch", return_value=pd.DataFrame())
    
    data = manager.get_data("mock", use_cache=False)
    assert not data.empty
    pd.testing.assert_frame_equal(data, sample_dataframe)


def test_data_manager_caching(sample_dataframe: pd.DataFrame, mocker: Any):
    """
    Tests data caching mechanism.
    """
    manager = DataManager()
    mock_conn = MockConnector("mock_source", data=sample_dataframe)
    mocker.patch.dict(manager._connectors, {"mock": mock_conn})
    
    # Disable default csv connector for this test
    mocker.patch.object(manager._connectors["csv"], "fetch", return_value=pd.DataFrame())
    
    # First call, should fetch and cache
    data1 = manager.get_data("mock", use_cache=True)
    
    # Second call, should retrieve from cache (mock fetch should not be called again)
    mocker.patch.object(mock_conn, "fetch")
    data2 = manager.get_data("mock", use_cache=True)
    
    pd.testing.assert_frame_equal(data1, data2)
    mock_conn.fetch.assert_not_called()  # Ensure fetch was not called again


def test_data_manager_refresh_all(sample_dataframe: pd.DataFrame, mocker: Any):
    """
    Tests cache clearing.
    """
    manager = DataManager()
    mock_conn = MockConnector("mock_source", data=sample_dataframe)
    mocker.patch.dict(manager._connectors, {"mock": mock_conn})
    
    # Disable default csv connector for this test
    mocker.patch.object(manager._connectors["csv"], "fetch", return_value=pd.DataFrame())
    
    manager.get_data("mock") # populate cache
    
    mocker.patch.object(mock_conn, "fetch")
    manager.refresh_all()
    manager.get_data("mock") # should trigger fetch after refresh
    mock_conn.fetch.assert_called_once() # Ensure fetch was called after refresh
