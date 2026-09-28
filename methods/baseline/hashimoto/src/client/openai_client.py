"""OpenAI-compatible client implementation."""

import os
import time
from typing import Any
from src.client.base import BaseLLMClient
from src.llm_call_log import LLMCallLogger
from src.models import Message


class OpenAIClient(BaseLLMClient):
    """Client implementing inference against OpenAI or compatible REST endpoints."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        call_logger: LLMCallLogger | None = None,
        **client_kwargs: Any,
    ) -> None:
        """Initialize the OpenAI client wrapper with credentials or deferred resolution."""
        self._api_key = api_key
        self._base_url = base_url
        self._call_logger = call_logger
        self._client_kwargs = client_kwargs
        self._client: Any = None

    def _get_client(self) -> Any:
        """Lazily initialize and return the underlying OpenAI client instance."""
        if self._client is None:
            try:
                from openai import OpenAI
            except ImportError as exc:
                raise ImportError(
                    "The 'openai' package is required to use OpenAIClient. "
                    "Install it via `pip install openai`."
                ) from exc

            resolved_key = self._api_key or os.getenv("OPENAI_API_KEY")
            resolved_base_url = self._base_url or os.getenv("OPENAI_BASE_URL")

            if not resolved_key:
                raise ValueError(
                    "API key must be provided via `api_key` argument or OPENAI_API_KEY environment variable."
                )

            self._client = OpenAI(
                api_key=resolved_key,
                base_url=resolved_base_url,
                **self._client_kwargs,
            )

        return self._client

    def generate(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.1,
        max_tokens: int = 1024,
    ) -> str:
        """Send chat messages, record the call audit entry, and return the assistant response."""
        client = self._get_client()
        payload = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        start_time = time.perf_counter()
        try:
            response = client.chat.completions.create(
                model=model,
                messages=payload,  # type: ignore[arg-type]
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except Exception as exc:
            if self._call_logger is not None:
                self._call_logger.record_call(
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    messages=payload,
                    output=None,
                    latency_ms=(time.perf_counter() - start_time) * 1000.0,
                    prompt_tokens=0,
                    completion_tokens=0,
                    status="error",
                    error_message=str(exc),
                )
            raise

        latency_ms = (time.perf_counter() - start_time) * 1000.0
        choice = response.choices[0]
        content = (choice.message.content or "").strip()

        if self._call_logger is not None:
            usage = response.usage
            self._call_logger.record_call(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=payload,
                output=content,
                latency_ms=latency_ms,
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
            )

        return content
