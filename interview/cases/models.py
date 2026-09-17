"""Data models for requirements interview cases."""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class CaseRecord:
    """Represents a validated requirements elicitation case."""

    case_id: str
    project_name: str
    initial_requirements: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert case to a dictionary representation."""
        return {
            "case_id": self.case_id,
            "project_name": self.project_name,
            "initial_requirements": self.initial_requirements,
        }
