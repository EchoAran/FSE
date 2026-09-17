"""User participant representation for receiving messages and submitting stakeholder responses."""

from typing import TYPE_CHECKING
from src.interview_session.session_models import Message, Participant

if TYPE_CHECKING:
    from src.interview_session.interview_session import InterviewSession


class User(Participant):
    """Participant representing the human stakeholder in the interview session."""

    def __init__(self, user_id: str, interview_session: "InterviewSession") -> None:
        """Initialize user participant."""
        super().__init__(title="User", interview_session=interview_session)
        self._user_id = user_id

    async def on_message(self, message: Message) -> None:
        """Handle incoming interviewer messages."""
        pass

    def add_user_message(self, text: str) -> None:
        """Submit a stakeholder response to the interview session chat history."""
        self.interview_session.add_message_to_chat_history(
            role="User",
            content=text,
        )