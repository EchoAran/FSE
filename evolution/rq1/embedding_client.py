"""Batch embedding HTTP client for OpenAI-compatible embedding endpoints."""

from __future__ import annotations

import time
from typing import Any

import httpx
import numpy as np

from evolution.rq1.config import EmbeddingConfig


class EmbeddingClientError(Exception):
    """Base exception for embedding generation failures."""


class EmbeddingAPIError(EmbeddingClientError):
    """Exception raised when API endpoint returns an unrecoverable HTTP or network error."""


class EmbeddingClient:
    """Synchronous HTTP client for OpenAI-compatible text embedding endpoints."""

    def __init__(self, config: EmbeddingConfig) -> None:
        self.config = config
        self.api_key = config.resolve_api_key()
        self._client = httpx.Client(
            timeout=config.timeout_seconds,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

    def __enter__(self) -> EmbeddingClient:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close underlying HTTP transport resources."""
        self._client.close()

    def _post_batch_with_retries(self, batch_texts: list[str], max_retries: int = 3) -> list[list[float]]:
        """Send a single batch of texts to the embedding endpoint with retries."""
        payload: dict[str, Any] = {
            "model": self.config.model_name,
            "input": batch_texts,
            "dimensions": self.config.dimensions,
        }

        attempts = 0
        backoff_seconds = 1.0

        while True:
            attempts += 1
            try:
                response = self._client.post(self.config.api_url, json=payload)
            except (httpx.TimeoutException, httpx.NetworkError) as err:
                if attempts <= max_retries:
                    print(
                        f"[embedding] network failure; retry {attempts}/{max_retries} "
                        f"in {backoff_seconds:.0f}s",
                        flush=True,
                    )
                    time.sleep(backoff_seconds)
                    backoff_seconds *= 2.0
                    continue
                raise EmbeddingAPIError(f"Embedding network error after {attempts} attempts: {err}") from err

            if response.status_code == 429 or response.status_code >= 500:
                if attempts <= max_retries:
                    print(
                        f"[embedding] HTTP {response.status_code}; retry "
                        f"{attempts}/{max_retries} in {backoff_seconds:.0f}s",
                        flush=True,
                    )
                    time.sleep(backoff_seconds)
                    backoff_seconds *= 2.0
                    continue
                raise EmbeddingAPIError(
                    f"Embedding HTTP {response.status_code} server error after {attempts} attempts: {response.text}"
                )

            if response.is_error:
                raise EmbeddingAPIError(
                    f"Embedding HTTP {response.status_code} client error: {response.text}"
                )

            break

        data = response.json()
        raw_items = data.get("data")
        if not isinstance(raw_items, list):
            raise EmbeddingAPIError(f"Unexpected response structure from embedding endpoint: {data}")

        if len(raw_items) != len(batch_texts):
            raise EmbeddingAPIError(
                f"Batch text count ({len(batch_texts)}) does not match response count ({len(raw_items)})."
            )

        sorted_items = sorted(raw_items, key=lambda item: item["index"])
        vectors: list[list[float]] = []
        for expected_idx, item in enumerate(sorted_items):
            if item["index"] != expected_idx:
                raise EmbeddingAPIError(
                    f"Missing or mismatched embedding index: expected {expected_idx}, got {item.get('index')}"
                )
            vec = item.get("embedding")
            if not isinstance(vec, list) or len(vec) != self.config.dimensions:
                raise EmbeddingAPIError(
                    f"Vector dimension mismatch: expected {self.config.dimensions}, got {len(vec) if isinstance(vec, list) else type(vec)}"
                )
            vectors.append(vec)

        return vectors

    def embed(self, texts: list[str]) -> np.ndarray:
        """Generate normalized floating point embeddings for an ordered sequence of texts."""
        if not texts:
            return np.empty((0, self.config.dimensions), dtype=np.float32)

        batch_size = self.config.batch_size
        all_vectors: list[list[float]] = []

        total_batches = (len(texts) + batch_size - 1) // batch_size
        for batch_index, start_idx in enumerate(
            range(0, len(texts), batch_size), start=1
        ):
            batch = texts[start_idx : start_idx + batch_size]
            batch_vectors = self._post_batch_with_retries(batch)
            all_vectors.extend(batch_vectors)
            print(
                f"[embedding] batch {batch_index}/{total_batches} completed",
                flush=True,
            )

        matrix = np.array(all_vectors, dtype=np.float32)

        if matrix.shape != (len(texts), self.config.dimensions):
            raise EmbeddingClientError(
                f"Result shape mismatch: expected ({len(texts)}, {self.config.dimensions}), got {matrix.shape}"
            )

        if not np.all(np.isfinite(matrix)):
            raise EmbeddingClientError("Embedding matrix contains non-finite numbers (NaN or Inf).")

        return matrix
