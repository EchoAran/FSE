"""OpenAI-compatible client implementation."""

import os
from typing import Any
from src.client.base import BaseLLMClient
from src.models import Message


class OpenAIClient(BaseLLMClient):
    """Client implementing inference against OpenAI or compatible REST endpoints."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        **client_kwargs: Any,
    ) -> None:
        """Initialize the OpenAI client wrapper with credentials or deferred resolution."""
        self._api_key = api_key
        self._base_url = base_url
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
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> str:
        """Send chat messages and return the assistant response."""
        client = self._get_client()
        payload = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        response = client.chat.completions.create(
            model=model,
            messages=payload,  # type: ignore[arg-type]
            temperature=temperature,
            max_tokens=max_tokens,
        )

        choice = response.choices[0]
        content = choice.message.content
        return (content or "").strip()
