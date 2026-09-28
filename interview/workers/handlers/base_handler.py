"""Base handler definition for method execution within worker process."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


def read_llm_call_totals(log_path: Path) -> Dict[str, int]:
    """Sum prompt/completion/total tokens across a method's llm_calls.jsonl log."""
    totals = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    with log_path.open("r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue
            record = json.loads(stripped)
            totals["prompt_tokens"] += int(record["prompt_tokens"])
            totals["completion_tokens"] += int(record["completion_tokens"])
            totals["total_tokens"] += int(record["total_tokens"])
    return totals


class BaseMethodHandler(ABC):
    """Abstract interface executed inside child worker process for a method."""

    @abstractmethod
    def start(self, case_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Start the method session with the given case payload."""
        pass

    @abstractmethod
    def submit_answer(self, answer: str) -> Dict[str, Any]:
        """Submit stakeholder answer to the method and advance turn."""
        pass

    @abstractmethod
    def inspect(self) -> Dict[str, Any]:
        """Inspect current state without advancing."""
        pass

    @abstractmethod
    def resume(self, case_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Resume an ongoing or interrupted session."""
        pass

    @abstractmethod
    def token_usage(self) -> Dict[str, int]:
        """Return the method's cumulative token usage for all LLM calls so far."""
        pass

    def close(self) -> None:
        """Optional cleanup upon worker shutdown."""
        pass
