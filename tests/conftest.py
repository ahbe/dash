"""
Pytest fixtures for the dashboard application.
Provides sample dataframes and mock connectors for testing.
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta


@pytest.fixture(scope="session")
def sample_dataframe() -> pd.DataFrame:
    """
    Provides a sample DataFrame for testing.
    """
    data = {
        "date": ["2026-01-01", "2026-01-02", "2026-01-01", "2026-01-02"],
        "brand": ["Brand X", "Brand Y", "Brand X", "Brand Z"],
        "segment": ["Retail", "Corporate", "Retail", "SME"],
        "purpose": ["Home Loan", "Auto Loan", "Home Loan", "Personal Loan"],
        "derogation_flag": [1, 0, 1, 0],
        "derogation_bps": [150.0, 50.0, 200.0, 75.0],
        "usage_count": [10, 5, 12, 8],
        "failed_calls": [1, 0, 2, 0],
        "margin": [100.0, 200.0, 150.0, 250.0],
        "conversion_flag": [1, 1, 0, 1],
        "converted_margin": [1000.0, 1000.0, 0.0, 2000.0],
        "derogation_pct": [100.0, 0.0, 100.0, 0.0],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_data_manager(mocker) -> Any:
    """
    Mocks the DataManager to return a predefined DataFrame.
    """
    mock_manager = mocker.Mock()
    mock_manager.get_data.return_value = sample_dataframe()
    mock_manager.refresh_all.return_value = None
    return mock_manager
