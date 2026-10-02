"""Chat completions HTTP client specialized for structured JSON responses."""

from __future__ import annotations

import json
import time
from typing import Any

import httpx

from evolution.rq1.config import LLMConfig


class LLMClientError(Exception):
    """Base exception for LLM completion errors."""


class ModelAPIError(LLMClientError):
    """Exception raised when API endpoint returns an unrecoverable HTTP error."""


class ModelOutputError(LLMClientError):
    """Exception raised when model output is empty, invalid JSON, or non-object."""


class ChatCompletionClient:
    """Synchronous HTTP client for OpenAI-compatible chat completion endpoints."""

    def __init__(self, config: LLMConfig) -> None:
        self.config = config
        self.api_key = config.resolve_api_key()
        self._client = httpx.Client(
            timeout=config.timeout_seconds,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

    def __enter__(self) -> ChatCompletionClient:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close underlying HTTP transport resources."""
        self._client.close()

    def complete_json(
        self,
        system_prompt: str,
        user_payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Send chat completion request and parse response into a JSON dictionary."""
        request_body = {
            "model": self.config.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": json.dumps(user_payload, ensure_ascii=False),
                },
            ],
            "temperature": self.config.temperature,
        }

        attempts = 0
        backoff_seconds = 1.0

        while True:
            attempts += 1
            try:
                response = self._client.post(self.config.api_url, json=request_body)
            except (httpx.TimeoutException, httpx.NetworkError) as err:
                if attempts <= self.config.max_retries:
                    print(
                        f"[llm] network failure; retry {attempts}/{self.config.max_retries} "
                        f"in {backoff_seconds:.0f}s",
                        flush=True,
                    )
                    time.sleep(backoff_seconds)
                    backoff_seconds *= 2.0
                    continue
                raise ModelAPIError(f"Network error after {attempts} attempts: {err}") from err

            if response.status_code == 429 or response.status_code >= 500:
                if attempts <= self.config.max_retries:
                    print(
                        f"[llm] HTTP {response.status_code}; retry "
                        f"{attempts}/{self.config.max_retries} in {backoff_seconds:.0f}s",
                        flush=True,
                    )
                    time.sleep(backoff_seconds)
                    backoff_seconds *= 2.0
                    continue
                raise ModelAPIError(
                    f"HTTP {response.status_code} server error after {attempts} attempts: {response.text}"
                )

            if response.is_error:
                raise ModelAPIError(
                    f"HTTP {response.status_code} client error: {response.text}"
                )

            break

        try:
            data = response.json()
        except json.JSONDecodeError as err:
            raise ModelOutputError(f"HTTP response body is not valid JSON: {response.text}") from err

        choices = data.get("choices")
        if not choices or not isinstance(choices, list):
            raise ModelOutputError(f"Missing or invalid 'choices' in response payload: {data}")

        first_choice = choices[0]
        message = first_choice.get("message") if isinstance(first_choice, dict) else None
        content = message.get("content") if isinstance(message, dict) else None

        if not content or not isinstance(content, str):
            raise ModelOutputError(f"Model response content is empty or not a string: {data}")

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as err:
            raise ModelOutputError(
                f"Failed to parse model content as JSON: {content}"
            ) from err

        if not isinstance(parsed, dict):
            raise ModelOutputError(
                f"Model response root is expected to be a JSON object, got {type(parsed).__name__}: {content}"
            )

        return parsed
