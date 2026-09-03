"""Deterministic mock LLM client for testing Hashimoto components."""

import json
from src.client.base import BaseLLMClient
from src.models import Message


class MockLLMClient(BaseLLMClient):
    """Mock client returning structured responses or simulated exceptions."""

    def __init__(
        self,
        scripted_responses: list[str] | None = None,
        fail_on_calls: set[int] | None = None,
        auto_pipeline: bool = True,
    ) -> None:
        """Initialize mock client with response queues and optional failure triggers."""
        self.scripted_responses = list(scripted_responses) if scripted_responses else []
        self.fail_on_calls = set(fail_on_calls) if fail_on_calls else set()
        self.auto_pipeline = auto_pipeline
        self.call_history: list[list[Message]] = []
        self._current_index = 0

    def generate(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.1,
        max_tokens: int = 1024,
    ) -> str:
        """Record call and return scripted or auto-generated stage output."""
        call_num = len(self.call_history) + 1
        self.call_history.append(list(messages))

        if call_num in self.fail_on_calls:
            raise RuntimeError(f"Simulated API failure on call #{call_num}")

        if self._current_index < len(self.scripted_responses):
            resp = self.scripted_responses[self._current_index]
            self._current_index += 1
            return resp

        if self.auto_pipeline:
            system_content = messages[0].content if messages else ""

            if "slot filling" in system_content.lower():
                return json.dumps({
                    "project_goals": {
                        "category": "goals",
                        "value": "Build scalable cloud clinic system"
                    },
                    "functional_needs": {
                        "category": "functionality",
                        "value": "Appointment scheduling"
                    },
                })

            if "abductive reasoning and dynamic slot generation" in system_content.lower():
                return json.dumps({
                    "Surprising Fact C": "Stakeholder mentioned unstable rural connectivity",
                    "Reason to Suspect A": "Offline-first synchronization requirement",
                    "New Slot": {
                        "offline_sync_protocol": {
                            "category": "constraints",
                            "value": None
                        },
                        "telehealth_video_integration": {
                            "category": "integration",
                            "value": None
                        }
                    }
                })

            # Question generation matching Figure 7 format
            return json.dumps({
                "Target Slot S": {
                    "offline_sync_protocol": {
                        "category": "constraints",
                        "value": None
                    }
                },
                "Question": f"Could you elaborate on the offline synchronization requirements for turn {call_num}?"
            })

        return "Default interviewer question."
