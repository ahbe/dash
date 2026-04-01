"""
Transformer for applying filters to DataFrames.
"""

from typing import Any, Dict, List, Union
import pandas as pd
from src.data.transformers.base_transformer import BaseTransformer


class FilterTransformer(BaseTransformer):
    """
    Applies column-based filters to a DataFrame.
    """

    def transform(self, df: pd.DataFrame, filters: Dict[str, Any] = None, **kwargs) -> pd.DataFrame:
        """
        Applies filters to the DataFrame.

        Args:
            df: Input DataFrame.
            filters: Dictionary of {column_name: value(s)}.
            **kwargs: Additional parameters.

        Returns:
            pd.DataFrame: Filtered DataFrame.
        """
        if df.empty or not filters:
            return df

        filtered_df = df.copy()

        for col, value in filters.items():
            if col not in filtered_df.columns or value is None:
                continue

            if isinstance(value, list):
                if value:  # Non-empty list
                    filtered_df = filtered_df[filtered_df[col].isin(value)]
            elif isinstance(value, tuple) and len(value) == 2:
                # Range filter (e.g., date range or slider)
                start, end = value
                if start is not None:
                    filtered_df = filtered_df[filtered_df[col] >= start]
                if end is not None:
                    filtered_df = filtered_df[filtered_df[col] <= end]
            else:
                filtered_df = filtered_df[filtered_df[col] == value]

        return filtered_df
