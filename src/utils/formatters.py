"""
Formatting utilities for numbers, percentages, and currencies.
"""

from typing import Union


def format_currency(value: Union[int, float], currency: str = "€") -> str:
    """
    Formats a number as currency.
    """
    return f"{currency}{value:,.2f}"


def format_percentage(value: Union[int, float], precision: int = 1) -> str:
    """
    Formats a number as a percentage.
    """
    return f"{value:.{precision}f}%"


def format_bps(value: Union[int, float]) -> str:
    """
    Formats a number as Basis Points (bps).
    """
    return f"{value:.1f} bps"
