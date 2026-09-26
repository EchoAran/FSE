"""OpenAI compatible chat completion transport for the Analyzer."""

from __future__ import annotations

import httpx

from motivation.config.config import AnalyzerModelConfig


class CompletionError(RuntimeError):
    """Raised when the Analyzer endpoint cannot return a usable completion."""


class ChatCompletionClient:
    """Synchronous OpenAI compatible chat completion client with transport retries."""

    def __init__(self, config: AnalyzerModelConfig) -> None:
        self._config = config
        self._api_key = config.api_key
        self._http = httpx.Client(timeout=config.timeout_seconds)

    def _payload(self, system_prompt: str, user_prompt: str) -> dict[str, object]:
        """Build the OpenAI compatible request body."""
        return {
            "model": self._config.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": self._config.temperature,
        }

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """Return the assistant message of one chat completion request."""
        headers = {"Authorization": f"Bearer {self._api_key}"}
        payload = self._payload(system_prompt, user_prompt)
        attempts = max(1, self._config.max_retries)
        failure: CompletionError | None = None
        for _ in range(attempts):
            try:
                response = self._http.post(
                    self._config.api_url, json=payload, headers=headers
                )
            except httpx.HTTPError as error:
                failure = CompletionError(f"transport failure: {error}")
                continue
            if response.status_code != 200:
                failure = CompletionError(
                    f"HTTP {response.status_code}: {response.text[:500]}"
                )
                continue
            try:
                content = response.json()["choices"][0]["message"]["content"].strip()
            except (KeyError, IndexError, TypeError, ValueError) as error:
                failure = CompletionError(f"unexpected response payload: {error}")
                continue
            if not content:
                failure = CompletionError("the completion content is empty")
                continue
            return content
        raise failure