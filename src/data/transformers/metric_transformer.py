"""
Transformer for computing dashboard metrics.
Calculates derogation %, bps, usage, etc.
"""

from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from src.data.transformers.base_transformer import BaseTransformer


class MetricTransformer(BaseTransformer):
    """
    Computes KPIs from raw derogation data.
    """

    def transform(self, df: pd.DataFrame, **kwargs) -> Dict[str, Any]:
        """
        Computes various metrics from the input DataFrame.

        Args:
            df: Input DataFrame.
            **kwargs: Additional parameters.

        Returns:
            Dict[str, Any]: Dictionary of metric values.
        """
        if df.empty:
            return {
                "derogation_pct": 0.0,
                "derogation_bps": 0.0,
                "usage_count": 0,
                "failed_calls": 0,
                "converted_margin": 0.0,
                "conversion_rate": 0.0,
                "variation": {}
            }

        # Current metrics
        usage_count = df["usage_count"].sum()
        derogation_count = df[df["derogation_flag"] == 1]["usage_count"].sum()
        derogation_pct = (derogation_count / usage_count * 100) if usage_count > 0 else 0.0
        
        derogation_bps = df["derogation_bps"].mean() if not df.empty else 0.0
        failed_calls = df["failed_calls"].sum()
        converted_margin = df["converted_margin"].sum()
        
        total_conv_potential = df["conversion_flag"].count()
        conversion_rate = (df["conversion_flag"].sum() / total_conv_potential * 100) if total_conv_potential > 0 else 0.0

        metrics = {
            "derogation_pct": derogation_pct,
            "derogation_bps": derogation_bps,
            "usage_count": usage_count,
            "failed_calls": failed_calls,
            "converted_margin": converted_margin,
            "conversion_rate": conversion_rate,
        }

        # Compute variations if period comparison is possible
        # For simplicity, we assume 'df' might contain a 'period' column or we filter here
        # In a real app, you'd compare current vs previous period.
        # Here we'll return mock variations for demonstration.
        metrics["variation"] = {
            "derogation_pct": 1.2,
            "derogation_bps": -5.0,
            "usage_count": 10.0,
            "failed_calls": -2.0,
            "converted_margin": 1500.0,
            "conversion_rate": 0.5,
        }

        return metrics
