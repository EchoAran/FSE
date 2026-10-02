from dataclasses import dataclass
import json
import time
from typing import Any
import httpx


class LLMClientError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        request_payload: dict[str, Any] | None = None,
        raw_response: dict[str, Any] | str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.request_payload = request_payload
        self.raw_response = raw_response

    def __str__(self) -> str:
        return self.message


@dataclass(frozen=True)
class LLMResponse:
    content: str | None
    raw_response: dict[str, Any] | str | None
    usage: dict[str, Any] | None
    finish_reason: str | None
    request_payload: dict[str, Any]


class LLMClient:
    """Client for making chat completion requests to OpenAI-compatible endpoints."""

    def __init__(
        self,
        endpoint: str,
        model_name: str,
        api_key: str,
        timeout_seconds: float = 120.0,
        max_retries: int = 3,
    ) -> None:
        self.endpoint = endpoint
        self.model_name = model_name
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries

    def _build_payload(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
    ) -> dict[str, Any]:
        return {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
    ) -> LLMResponse:
        request_payload = self._build_payload(system_prompt, user_prompt, temperature)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        total_attempts = 1 + self.max_retries
        last_error: Exception | None = None

        with httpx.Client(timeout=self.timeout_seconds) as client:
            for attempt in range(total_attempts):
                try:
                    response = client.post(
                        self.endpoint,
                        json=request_payload,
                        headers=headers,
                    )

                    status_code = response.status_code
                    raw_response: dict[str, Any] | str | None
                    try:
                        raw_response = response.json()
                    except Exception:
                        raw_response = response.text if response.text else None

                    if 200 <= status_code < 300:
                        if not isinstance(raw_response, dict):
                            raise LLMClientError(
                                f"Expected JSON object in response, got: {type(raw_response).__name__}",
                                status_code=status_code,
                                request_payload=request_payload,
                                raw_response=raw_response,
                            )

                        choices = raw_response.get("choices")
                        if not isinstance(choices, list) or not choices:
                            raise LLMClientError(
                                "No choices found in API response",
                                status_code=status_code,
                                request_payload=request_payload,
                                raw_response=raw_response,
                            )

                        choice = choices[0]
                        message = choice.get("message", {})
                        content = message.get("content")
                        finish_reason = choice.get("finish_reason")
                        usage = raw_response.get("usage")

                        return LLMResponse(
                            content=content,
                            raw_response=raw_response,
                            usage=usage if isinstance(usage, dict) else None,
                            finish_reason=finish_reason if isinstance(finish_reason, str) else None,
                            request_payload=request_payload,
                        )

                    is_retryable = status_code in (429, 500, 502, 503, 504)
                    error_msg = f"API returned error status {status_code}: {raw_response}"
                    if is_retryable and attempt < self.max_retries:
                        time.sleep(min(2.0 ** attempt, 8.0))
                        continue

                    raise LLMClientError(
                        error_msg,
                        status_code=status_code,
                        request_payload=request_payload,
                        raw_response=raw_response,
                    )

                except (httpx.TimeoutException, httpx.NetworkError) as exc:
                    last_error = exc
                    if attempt < self.max_retries:
                        time.sleep(min(2.0 ** attempt, 8.0))
                        continue
                    raise LLMClientError(
                        f"Network or timeout communication failure after {attempt + 1} attempts: {exc}",
                        request_payload=request_payload,
                    ) from exc
                except LLMClientError:
                    raise
                except Exception as exc:
                    raise LLMClientError(
                        f"Unexpected error during completion call: {exc}",
                        request_payload=request_payload,
                    ) from exc

        raise LLMClientError(
            f"Failed after {total_attempts} attempts: {last_error}",
            request_payload=request_payload,
        )
