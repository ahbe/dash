"""
Tests for data transformers.
"""

import pandas as pd
import pytest
from src.data.transformers.filter_transformer import FilterTransformer
from src.data.transformers.metric_transformer import MetricTransformer


@pytest.fixture
def large_sample_dataframe() -> pd.DataFrame:
    """
    Provides a larger sample DataFrame for metrics testing.
    """
    data = {
        "date": pd.to_datetime([f"2026-01-0{i%2 + 1}" for i in range(100)]),
        "brand": [f"Brand {i%3}" for i in range(100)],
        "segment": ["Retail", "Corporate"][i%2] for i in range(100)],
        "derogation_flag": [1 if i % 5 == 0 else 0 for i in range(100)],
        "derogation_bps": [float(i) for i in range(100)],
        "usage_count": [i%10 + 1 for i in range(100)],
        "failed_calls": [1 if i % 10 == 0 else 0 for i in range(100)],
        "margin": [float(i * 10) for i in range(100)],
        "conversion_flag": [1 if i % 3 != 0 else 0 for i in range(100)],
        "converted_margin": [float(i * 100) for i in range(100)],
    }
    return pd.DataFrame(data)


def test_filter_transformer_dropdown(sample_dataframe: pd.DataFrame):
    """
    Tests filter transformer with dropdown-like filters.
    """
    transformer = FilterTransformer()
    filtered_df = transformer.transform(sample_dataframe, filters={"brand": ["Brand X"]})
    assert all(filtered_df["brand"] == "Brand X")
    assert len(filtered_df) == 2


def test_filter_transformer_date_range(sample_dataframe: pd.DataFrame):
    """
    Tests filter transformer with date range filters.
    """
    transformer = FilterTransformer()
    filtered_df = transformer.transform(sample_dataframe, filters={"date": ("2026-01-01", "2026-01-01")})
    assert all(filtered_df["date"] == "2026-01-01")
    assert len(filtered_df) == 2


def test_metric_transformer_basic_metrics(large_sample_dataframe: pd.DataFrame):
    """
    Tests basic metric computation.
    """
    transformer = MetricTransformer()
    metrics = transformer.transform(large_sample_dataframe)
    
    assert "derogation_pct" in metrics
    assert "usage_count" in metrics
    assert "failed_calls" in metrics
    assert metrics["usage_count"] == sum(range(1,11)) * 10 # 1 to 10 repeated 10 times


def test_metric_transformer_empty_df():
    """
    Tests metric transformer with an empty DataFrame.
    """
    transformer = MetricTransformer()
    metrics = transformer.transform(pd.DataFrame())
    
    assert metrics["derogation_pct"] == 0.0
    assert metrics["usage_count"] == 0
