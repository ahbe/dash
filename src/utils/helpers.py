"""
General helper functions.
"""

import uuid
from typing import Any, Dict


def generate_unique_id(prefix: str = "id") -> str:
    """
    Generates a unique identifier.
    """
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def get_nested_value(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """
    Retrieves a value from a nested dictionary using a dot-separated path.
    """
    keys = path.split(".")
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return default
    return data
