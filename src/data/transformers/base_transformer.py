"""
Abstract base class for all data transformers.
Defines the required interface for data manipulation.
"""

from abc import ABC, abstractmethod
import pandas as pd


class BaseTransformer(ABC):
    """
    Abstract base class for all data transformers.
    """

    @abstractmethod
    def transform(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Transforms the input DataFrame and returns the result.

        Args:
            df: Input DataFrame.
            **kwargs: Additional transformation parameters.

        Returns:
            pd.DataFrame: Transformed data.
        """
        pass
