"""
Input validation utilities.
"""

from typing import Any, List, Optional


def validate_date_range(start_date: Optional[str], end_date: Optional[str]) -> bool:
    """
    Validates that the start date is before the end date.
    """
    if not start_date or not end_date:
        return True
    return start_date <= end_date


def validate_required_cols(df_cols: List[str], required_cols: List[str]) -> bool:
    """
    Validates that all required columns are present in the DataFrame.
    """
    return all(col in df_cols for col in required_cols)
