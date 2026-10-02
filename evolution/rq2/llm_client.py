from dataclasses import dataclass
import json
import time
from typing import Any
import httpx
from evolution.rq2.config import JudgeConfig


class LLMClientError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        request_payload: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.request_payload = request_payload

    def __str__(self) -> str:
        return self.message


@dataclass(frozen=True)
class ChatCompletionResult:
    content: str | None
    finish_reason: str | None
    request_payload: dict[str, Any]


def build_chat_request_payload(
    model_name: str,
    system_prompt: str,
    user_payload: dict[str, Any],
    temperature: float | None = 0.0,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
        ],
    }
    if temperature is not None:
        payload["temperature"] = temperature
    return payload


class ChatCompletionClient:
    def __init__(self, config: JudgeConfig) -> None:
        self.api_url = config.api_url
        self.model_name = config.model_name
        self.api_key = config.api_key
        self.temperature = config.temperature
        self.timeout_seconds = config.timeout_seconds
        self.max_retries = config.max_retries

    def _build_request_payload(
        self, system_prompt: str, user_payload: dict[str, Any]
    ) -> dict[str, Any]:
        return build_chat_request_payload(
            model_name=self.model_name,
            system_prompt=system_prompt,
            user_payload=user_payload,
            temperature=self.temperature,
        )

    def complete(
        self, system_prompt: str, user_payload: dict[str, Any]
    ) -> ChatCompletionResult:
        request_payload = self._build_request_payload(system_prompt, user_payload)
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
                        self.api_url,
                        json=request_payload,
                        headers=headers,
                    )

                    status_code = response.status_code
                    response_body: dict[str, Any] | str | None
                    try:
                        response_body = response.json()
                    except Exception:
                        response_body = response.text if response.text else None

                    if status_code == 200 and isinstance(response_body, dict):
                        choices = response_body.get("choices")
                        content: str | None = None
                        finish_reason: str | None = None
                        if isinstance(choices, list) and len(choices) > 0 and isinstance(choices[0], dict):
                            message = choices[0].get("message")
                            if isinstance(message, dict):
                                content = message.get("content")
                            finish_reason = choices[0].get("finish_reason")

                        return ChatCompletionResult(
                            content=content,
                            finish_reason=finish_reason,
                            request_payload=request_payload,
                        )

                    is_retryable = status_code == 429 or (500 <= status_code < 600)
                    if is_retryable:
                        if attempt < total_attempts - 1:
                            delay = min(2.0**attempt, 10.0)
                            time.sleep(delay)
                            continue
                        raise LLMClientError(
                            f"HTTP {status_code} error from API after {total_attempts} attempts: {response_body}",
                            status_code=status_code,
                            request_payload=request_payload,
                        )

                    raise LLMClientError(
                        f"Non-retryable HTTP {status_code} error from API: {response_body}",
                        status_code=status_code,
                        request_payload=request_payload,
                    )

                except (httpx.RequestError, httpx.TimeoutException) as exc:
                    last_error = exc
                    if attempt < total_attempts - 1:
                        delay = min(2.0**attempt, 10.0)
                        time.sleep(delay)
                        continue
                    raise LLMClientError(
                        f"Network/timeout error after {total_attempts} attempts: {exc}",
                        request_payload=request_payload,
                    ) from exc

        raise LLMClientError(
            f"Request failed unexpectedly: {last_error}",
            request_payload=request_payload,
        )
