"""Abstract interface for LLM interaction providers."""

from abc import ABC, abstractmethod
from src.models import Message


class BaseLLMClient(ABC):
    """Abstract base class defining contract for language model inference."""

    @abstractmethod
    def generate(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> str:
        """Send chat messages to the model and return the generated completion string."""
        pass
