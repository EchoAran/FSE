"""Base handler definition for method execution within worker process."""

from abc import ABC, abstractmethod
from typing import Any, Dict


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

    def close(self) -> None:
        """Optional cleanup upon worker shutdown."""
        pass
