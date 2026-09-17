"""Inter-process communication protocol definitions between orchestrator and worker."""

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class WorkerCommand:
    """Command payload sent from parent adapter to child worker."""

    cmd: str
    case: Optional[Dict[str, Any]] = None
    answer: Optional[str] = None
    options: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert command to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkerCommand":
        """Reconstruct command from dictionary."""
        return cls(
            cmd=data["cmd"],
            case=data.get("case"),
            answer=data.get("answer"),
            options=data.get("options"),
        )


@dataclass
class WorkerResponse:
    """Response payload returned by child worker to parent adapter."""

    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    traceback: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkerResponse":
        """Reconstruct response from dictionary."""
        return cls(
            success=data["success"],
            data=data.get("data"),
            error=data.get("error"),
            traceback=data.get("traceback"),
        )
