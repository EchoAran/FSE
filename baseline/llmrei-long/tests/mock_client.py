"""Deterministic mock LLM client for automated testing."""

from src.client.base import BaseLLMClient
from src.models import Message


class MockLLMClient(BaseLLMClient):
    """Mock client returning deterministic responses or simulated exceptions."""

    def __init__(
        self,
        scripted_responses: list[str] | None = None,
        fail_on_calls: set[int] | None = None,
    ) -> None:
        """Initialize mock client with optional sequential responses and fail triggers."""
        self.scripted_responses = list(scripted_responses) if scripted_responses else []
        self.fail_on_calls = set(fail_on_calls) if fail_on_calls else set()
        self.call_history: list[list[Message]] = []
        self._current_index = 0

    def generate(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> str:
        """Record the call and return next response or raise simulated error."""
        call_num = len(self.call_history) + 1
        self.call_history.append(list(messages))

        if call_num in self.fail_on_calls:
            raise RuntimeError(f"Simulated API failure on call #{call_num}")

        if self._current_index < len(self.scripted_responses):
            response = self.scripted_responses[self._current_index]
            self._current_index += 1
            return response

        return f"Interviewer follow-up question {len(self.call_history)} based on stakeholder response."
