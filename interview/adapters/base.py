"""Base abstractions and result models for method adapters."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional

from interview.cases.models import CaseRecord


@dataclass
class AdapterResult:
    """Standardized response from a method adapter operation."""

    native_project_id: str
    question: str
    finished: bool
    turn_count: int
    finish_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert adapter result to dictionary representation."""
        return {
            "native_project_id": self.native_project_id,
            "question": self.question,
            "finished": self.finished,
            "turn_count": self.turn_count,
            "finish_message": self.finish_message,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdapterResult":
        """Reconstruct adapter result from dictionary representation."""
        return cls(
            native_project_id=data["native_project_id"],
            question=data.get("question", ""),
            finished=bool(data.get("finished", False)),
            turn_count=int(data.get("turn_count", 0)),
            finish_message=data.get("finish_message"),
        )


class BaseMethodAdapter(ABC):
    """Unified adapter interface contract required by the interview environment."""

    @abstractmethod
    def start(self, case: CaseRecord) -> AdapterResult:
        """Initialize method session and retrieve the initial interviewer question."""
        pass

    @abstractmethod
    def submit_answer(self, answer: str) -> AdapterResult:
        """Submit stakeholder response and retrieve the next question or completion signal."""
        pass

    @abstractmethod
    def inspect(self) -> AdapterResult:
        """Inspect current status, pending question, and turn count without advancing state."""
        pass

    @abstractmethod
    def resume(self, case: CaseRecord) -> AdapterResult:
        """Resume an interrupted interview session from persisted checkpoint/transcript."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Cleanly terminate worker process and release associated resources."""
        pass
