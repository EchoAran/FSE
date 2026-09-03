"""SparkMe requirements engineering interview coordinator and public interface."""

import asyncio
from typing import Optional

from src.interview_session.interview_session import InterviewSession
from src.models import InterviewTranscript, RequirementCase


class SparkMeInterviewer:
    """High-level facade adapter providing a minimal, synchronous requirements interview interface."""

    def __init__(
        self,
        topics_plan_path: Optional[str] = None,
        max_turns: int = 20,
    ) -> None:
        """Initialize the SparkMe interviewer interface."""
        self.topics_plan_path = topics_plan_path
        self.max_turns = max_turns
        self._case: Optional[RequirementCase] = None
        self._session: Optional[InterviewSession] = None
        self._is_initialized: bool = False
        self._first_question: Optional[str] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    @property
    def is_initialized(self) -> bool:
        """Return whether the session has been initialized with a requirement case."""
        return self._is_initialized

    @property
    def is_finished(self) -> bool:
        """Check if the interview session has reached completion or max turns."""
        if self._session is None:
            return False
        return self._session.session_completed or not self._session.session_in_progress

    @property
    def turn_count(self) -> int:
        """Return the count of completed stakeholder question-answer turns."""
        if self._session is None:
            return 0
        return self._session._user_message_count

    @property
    def session(self) -> Optional[InterviewSession]:
        """Access internal interview session for testing and method inspection."""
        return self._session

    def initialize(self, case: RequirementCase) -> None:
        """Initialize the interview session with the provided requirement case."""
        self._case = case
        self._session = InterviewSession(
            user_id=case.case_id,
            interview_description=case.project_name,
            initial_context=case.initial_requirements,
            max_turns=self.max_turns,
        )
        self._is_initialized = True
        self._first_question = None

    def get_first_question(self) -> str:
        """Start the session and generate the initial opening question."""
        if not self._is_initialized or self._session is None:
            raise RuntimeError("Interviewer must be initialized before calling get_first_question().")

        if self._first_question is not None:
            return self._first_question

        loop = self._get_or_create_event_loop()
        self._first_question = loop.run_until_complete(self._session.start_session())
        return self._first_question

    def step(self, stakeholder_answer: str) -> str:
        """Submit a stakeholder answer and return the next generated question."""
        if not self._is_initialized or self._session is None:
            raise RuntimeError("Interviewer must be initialized before calling step().")

        if self.is_finished:
            raise RuntimeError("Interview is already completed. No further steps can be executed.")

        if not self._first_question:
            self.get_first_question()

        loop = self._get_or_create_event_loop()
        next_q = loop.run_until_complete(self._session.submit_answer(stakeholder_answer))
        return next_q

    def export_transcript(self) -> InterviewTranscript:
        """Export clean public conversation transcript containing only dialogue turns."""
        if not self._is_initialized or self._session is None or self._case is None:
            raise RuntimeError("Cannot export transcript from an uninitialized interviewer.")

        return self._session.export_transcript(
            case_id=self._case.case_id,
            project_name=self._case.project_name,
        )

    def _get_or_create_event_loop(self) -> asyncio.AbstractEventLoop:
        """Retrieve active event loop or instantiate a dedicated instance."""
        if self._loop is None or self._loop.is_closed():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        return self._loop
