"""
Data caching layer.
Implements in-memory caching with TTL (Time-To-Live).
Designed to be pluggable (e.g., Redis).
"""

from typing import Any, Optional
import time
from src.utils.logger import logger
from src.config import settings


class DataCache:
    """
    Simple in-memory cache with TTL.
    """

    def __init__(self, ttl: int = settings.CACHE_TTL_SECONDS):
        self.ttl = ttl
        self._cache: dict[str, dict[str, Any]] = {}

    def set(self, key: str, value: Any) -> None:
        """
        Stores a value in the cache.

        Args:
            key: Cache key.
            value: Data to store.
        """
        logger.info(f"Caching data for key: {key}")
        self._cache[key] = {
            "value": value,
            "timestamp": time.time()
        }

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieves a value from the cache if it exists and is not expired.

        Args:
            key: Cache key.

        Returns:
            Optional[Any]: Cached data if valid, None otherwise.
        """
        if key not in self._cache:
            return None

        cached_item = self._cache[key]
        if time.time() - cached_item["timestamp"] > self.ttl:
            logger.info(f"Cache expired for key: {key}")
            del self._cache[key]
            return None

        logger.info(f"Cache hit for key: {key}")
        return cached_item["value"]

    def clear(self) -> None:
        """
        Clears the cache.
        """
        logger.info("Clearing data cache.")
        self._cache = {}


# Global cache instance
cache = DataCache()
