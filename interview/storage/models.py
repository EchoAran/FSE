"""Data models and status definitions for interview environment persistence."""

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, Optional


class InterviewStatus(str, Enum):
    """Lifecycle status states for an interview run."""

    INITIALIZED = "initialized"
    RUNNING = "running"
    METHOD_FINISHED = "method_finished"
    FAILED = "failed"
    INTERRUPTED = "interrupted"


@dataclass
class InterviewManifest:
    """Structured record of interview execution metadata without machine-specific paths or timestamps."""

    case_id: str
    method_id: str
    project_name: str
    native_project_id: str
    method_model: Optional[str] = None
    method_max_turns: Optional[int] = None
    interviewee_model: Optional[str] = None
    status: InterviewStatus = InterviewStatus.INITIALIZED
    completed_turns: int = 0
    native_path: str = "native"
    finish_message: Optional[str] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize manifest to a clean dictionary without secret keys, local paths, or timestamps."""
        data = asdict(self)
        data["status"] = self.status.value if isinstance(self.status, InterviewStatus) else str(self.status)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InterviewManifest":
        """Deserialize manifest from dictionary representation."""
        status_raw = data.get("status", InterviewStatus.INITIALIZED.value)
        status = InterviewStatus(status_raw) if status_raw in [e.value for e in InterviewStatus] else InterviewStatus.FAILED

        return cls(
            case_id=data["case_id"],
            method_id=data["method_id"],
            project_name=data.get("project_name", ""),
            native_project_id=data.get("native_project_id", data["case_id"]),
            method_model=data.get("method_model"),
            method_max_turns=data.get("method_max_turns"),
            interviewee_model=data.get("interviewee_model"),
            status=status,
            completed_turns=int(data.get("completed_turns", 0)),
            native_path=data.get("native_path", "native"),
            finish_message=data.get("finish_message"),
            error_message=data.get("error_message"),
        )


@dataclass
class DialogueMessage:
    """A single visible message entry in conversation.jsonl without timestamps."""

    turn_index: int
    role: str
    content: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize dialogue message to dictionary."""
        return {
            "turn_index": self.turn_index,
            "role": self.role,
            "content": self.content,
        }


@dataclass
class PendingAnswer:
    """Record of a generated stakeholder answer awaiting method processing without timestamps."""

    turn_index: int
    question: str
    answer: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize pending answer to dictionary."""
        return {
            "turn_index": self.turn_index,
            "question": self.question,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PendingAnswer":
        """Deserialize pending answer from dictionary."""
        return cls(
            turn_index=int(data["turn_index"]),
            question=data["question"],
            answer=data["answer"],
        )
