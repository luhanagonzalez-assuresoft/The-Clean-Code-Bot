"""
Refactored version of ``messy_code.py`` applying SOLID principles.

Modules
-------
- ``cache``: Simple in‑memory cache abstraction.
- ``fetcher``: HTTP data fetcher with retry logic and optional caching.
- ``processor``: Business‑logic processing of the fetched payload.
- ``storage``: JSON file storage abstraction.
- ``runner``: Orchestrates fetching, processing and persisting data.

The public entry point is :class:`Runner.run`.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol

import requests

# --------------------------------------------------------------------------- #
# Logging configuration
# --------------------------------------------------------------------------- #
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Cache abstraction
# --------------------------------------------------------------------------- #
class ICache(Protocol):
    """Cache interface used by the fetcher."""

    def get(self, key: int) -> Optional[Dict[str, Any]]:
        """Return cached value for *key* or ``None`` if missing."""
        ...

    def set(self, key: int, value: Dict[str, Any]) -> None:
        """Store *value* under *key*."""
        ...


class InMemoryCache:
    """Thread‑unsafe in‑memory cache implementation."""

    def __init__(self) -> None:
        self._store: Dict[int, Dict[str, Any]] = {}

    def get(self, key: int) -> Optional[Dict[str, Any]]:
        return self._store.get(key)

    def set(self, key: int, value: Dict[str, Any]) -> None:
        self._store[key] = value


# --------------------------------------------------------------------------- #
# Data fetching abstraction
# --------------------------------------------------------------------------- #
class IDataFetcher(Protocol):
    """Interface for objects that can retrieve data by identifier."""

    def fetch(self, identifier: int) -> Optional[Dict[str, Any]]:
        """Return the JSON payload for *identifier* or ``None`` on failure."""
        ...


class HttpDataFetcher:
    """
    Fetches JSON data from a remote HTTP endpoint with retry support.

    Parameters
    ----------
    base_url: str
        Base URL of the remote service, e.g. ``https://api.example.com/data``.
    cache: ICache | None, optional
        Optional cache to avoid duplicate network calls.
    timeout: float, default 5.0
        Seconds to wait for the server response.
    max_retries: int, default 3
        Number of retry attempts on transient failures.
    backoff_factor: float, default 0.5
        Multiplier for exponential back‑off between retries.
    """

    def __init__(
        self,
        base_url: str,
        *,
        cache: Optional[ICache] = None,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.cache = cache
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def _build_url(self, identifier: int) -> str:
        return f"{self.base_url}/{identifier}"

    def fetch(self, identifier: int) -> Optional[Dict[str, Any]]:
        """Retrieve data for *identifier* respecting the cache and retry policy."""
        # 1️⃣ Check cache first
        if self.cache:
            cached = self.cache.get(identifier)
            if cached is not None:
                logger.debug("Cache hit for id=%s", identifier)
                return cached

        # 2️⃣ Perform HTTP request with retries
        url = self._build_url(identifier)
        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    payload = response.json()
                    if self.cache:
                        self.cache.set(identifier, payload)
                    logger.debug("Fetched id=%s successfully", identifier)
                    return payload
                else:
                    logger.warning(
                        "Unexpected status %s for id=%s (attempt %s)",
                        response.status_code,
                        identifier,
                        attempt,
                    )
            except requests.RequestException as exc:
                logger.warning(
                    "Request error for id=%s (attempt %s): %s", identifier, attempt, exc
                )

            # exponential back‑off before next attempt
            sleep_time = self.backoff_factor * (2 ** (attempt - 1))
            logger.debug("Sleeping %.2f seconds before retry", sleep_time)
            time.sleep(sleep_time)

        logger.error("Failed to fetch data for id=%s after %s attempts", identifier, self.max_retries)
        return None


# --------------------------------------------------------------------------- #
# Data processing abstraction
# --------------------------------------------------------------------------- #
class IDataProcessor(Protocol):
    """Interface for objects that transform raw payloads."""

    def process(self, data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Return a transformed representation of *data*."""
        ...


class SimpleDataProcessor:
    """
    Implements the original transformation logic:

    * integers → multiplied by 10
    * strings  → lower‑cased
    * lists    → integers incremented by 1, other items unchanged
    * other types → passed through unchanged
    """

    @staticmethod
    def _transform_value(value: Any) -> Any:
        if isinstance(value, int):
            return value * 10
        if isinstance(value, str):
            return value.lower()
        if isinstance(value, list):
            return [item + 1 if isinstance(item, int) else item for item in value]
        return value

    def process(self, data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if not data:
            return {}

        return {k: self._transform_value(v) for k, v in data.items()}


# --------------------------------------------------------------------------- #
# Storage abstraction
# --------------------------------------------------------------------------- #
class IStorage(Protocol):
    """Interface for persisting processed data."""

    def save(self, data: Dict[str, Any], name: str) -> None:
        """Persist *data* under the given *name*."""
        ...


class JsonFileStorage:
    """
    Persists dictionaries as pretty‑printed JSON files.

    Parameters
    ----------
    directory: Path | str, default current working directory
        Destination folder for output files. It is created if missing.
    """

    def __init__(self, directory: Path | str = Path.cwd()) -> None:
        self.base_path = Path(directory)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, data: Dict[str, Any], name: str) -> None:
        file_path = self.base_path / name
        try:
            with file_path.open("w", encoding="utf-8") as fp:
                json.dump(data, fp, ensure_ascii=False, indent=2)
            logger.info("Saved output to %s", file_path)
        except OSError as exc:
            logger.error("Failed to write %s: %s", file_path, exc)


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
class Runner:
    """
    Coordinates fetching, processing and storage of a sequence of identifiers.

    Parameters
    ----------
    fetcher: IDataFetcher
        Component responsible for retrieving raw data.
    processor: IDataProcessor
        Component that transforms the raw payload.
    storage: IStorage
        Component that persists the transformed payload.
    sleep_interval: float, default 1.0
        Seconds to pause between successive iterations.
    """

    def __init__(
        self,
        fetcher: IDataFetcher,
        processor: IDataProcessor,
        storage: IStorage,
        *,
        sleep_interval: float = 1.0,
    ) -> None:
        self.fetcher = fetcher
        self.processor = processor
        self.storage = storage
        self.sleep_interval = sleep_interval

    def run(self, identifiers: List[int]) -> None:
        """
        Execute the pipeline for each identifier in *identifiers*.

        The method logs progress and respects ``sleep_interval`` between calls.
        """
        for identifier in identifiers:
            logger.info("Processing identifier %s", identifier)

            raw = self.fetcher.fetch(identifier)
            processed = self.processor.process(raw)
            file_name = f"output_{identifier}.json"
            self.storage.save(processed, file_name)

            logger.debug("Sleeping %.2f seconds", self.sleep_interval)
            time.sleep(self.sleep_interval)


# --------------------------------------------------------------------------- #
# Entry point (kept for backward compatibility)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Configuration – can be externalised (e.g., env vars, config files)
    API_URL = "https://api.example.com/data"
    CACHE = InMemoryCache()
    FETCHER = HttpDataFetcher(API_URL, cache=CACHE)
    PROCESSOR = SimpleDataProcessor()
    STORAGE = JsonFileStorage()

    runner = Runner(FETCHER, PROCESSOR, STORAGE, sleep_interval=1.0)
    runner.run(list(range(5)))  # equivalent to the original loop