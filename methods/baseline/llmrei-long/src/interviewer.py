"""Core LLMREI-long interviewer engine driving multi-turn requirements elicitation."""

from src.client.base import BaseLLMClient
from src.client.openai_client import OpenAIClient
from src.config import InterviewConfig
from src.models import InterviewTranscript, InterviewTurn, Message, RequirementCase
from src.prompt.loader import PromptLoader
from src.prompt.renderer import PromptRenderer


INTERVIEW_FINISHED_MARKER = "[[INTERVIEW_FINISHED]]"


class LLMREIInterviewer:
    """Orchestrates an end-to-end requirements elicitation interview using LLMREI-long."""

    def __init__(
        self,
        config: InterviewConfig | None = None,
        llm_client: BaseLLMClient | None = None,
        prompt_loader: PromptLoader | None = None,
    ) -> None:
        """Initialize the interviewer with configuration, LLM client, and prompt loader."""
        self.config = config or InterviewConfig()
        self.llm_client = llm_client or OpenAIClient(
            api_key=self.config.api_key or None,
            base_url=self.config.base_url or None,
        )
        self.prompt_loader = prompt_loader or PromptLoader()

        self._case: RequirementCase | None = None
        self._system_prompt: str = ""
        self._messages: list[Message] = []
        self._turns: list[InterviewTurn] = []
        self._current_turn_index: int = 0
        self._is_initialized: bool = False
        self._is_finished: bool = False
        self._pending_interviewer_utterance: str | None = None

    @property
    def is_initialized(self) -> bool:
        """Return whether the interview has been initialized with a requirement case."""
        return self._is_initialized

    @property
    def is_finished(self) -> bool:
        """Return whether the interview dialogue has reached completion."""
        return self._is_finished

    @property
    def turn_count(self) -> int:
        """Return the number of completed interaction turns."""
        return len(self._turns)

    @property
    def system_prompt(self) -> str:
        """Return the active rendered system prompt."""
        return self._system_prompt

    def initialize(self, case: RequirementCase | dict) -> None:
        """Set up the interview session with the given software requirements case."""
        if isinstance(case, dict):
            self._case = RequirementCase(**case)
        else:
            self._case = case

        raw_prompt = self.prompt_loader.load(self.config.prompt_path)
        self._system_prompt = PromptRenderer.render(raw_prompt, self._case)

        self._messages = [Message(role="system", content=self._system_prompt)]
        self._turns = []
        self._current_turn_index = 0
        self._is_finished = False
        self._pending_interviewer_utterance = None
        self._is_initialized = True

    def get_first_question(self) -> str:
        """Generate and return the initial opening utterance of the interviewer."""
        if not self._is_initialized or self._case is None:
            raise RuntimeError("Interviewer must be initialized before requesting the first question.")

        if self._pending_interviewer_utterance is not None:
            return self._pending_interviewer_utterance

        first_question = self.llm_client.generate(
            messages=self._messages,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        ).strip()

        if not first_question:
            raise RuntimeError("LLM returned an empty interviewer response.")

        if first_question == INTERVIEW_FINISHED_MARKER:
            self._is_finished = True
            return ""

        self._pending_interviewer_utterance = first_question
        self._messages.append(Message(role="assistant", content=first_question))
        return first_question

    def step(self, interviewee_answer: str) -> str:
        """Process a stakeholder response and generate the next interviewer question atomically."""
        if not self._is_initialized or self._case is None:
            raise RuntimeError("Interviewer must be initialized before calling step().")

        if self._is_finished:
            raise RuntimeError("Interview is already completed. No further steps can be executed.")

        if self._pending_interviewer_utterance is None:
            self.get_first_question()

        current_question = self._pending_interviewer_utterance or ""
        candidate_turn_id = self._current_turn_index + 1

        # Check turn limit
        if candidate_turn_id >= self.config.max_turns:
            self._messages.append(Message(role="user", content=interviewee_answer))
            self._current_turn_index = candidate_turn_id
            turn = InterviewTurn(
                turn_id=self._current_turn_index,
                interviewer_utterance=current_question,
                interviewee_utterance=interviewee_answer,
            )
            self._turns.append(turn)
            self._is_finished = True
            self._pending_interviewer_utterance = None
            return ""

        # Prepare tentative messages for LLM generation
        candidate_messages = list(self._messages) + [Message(role="user", content=interviewee_answer)]

        # Generate next question with transactional state guarantee
        next_question = self.llm_client.generate(
            messages=candidate_messages,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        ).strip()

        if not next_question:
            raise RuntimeError("LLM returned an empty interviewer response.")

        # Commit state only upon successful generation
        self._messages = candidate_messages
        self._current_turn_index = candidate_turn_id
        turn = InterviewTurn(
            turn_id=self._current_turn_index,
            interviewer_utterance=current_question,
            interviewee_utterance=interviewee_answer,
        )
        self._turns.append(turn)

        if next_question == INTERVIEW_FINISHED_MARKER:
            self._is_finished = True
            self._pending_interviewer_utterance = None
            return ""

        self._messages.append(Message(role="assistant", content=next_question))
        self._pending_interviewer_utterance = next_question

        return next_question

    def resume_from_transcript(
        self,
        transcript: InterviewTranscript,
        case: RequirementCase | None = None,
    ) -> None:
        """Losslessly restore interviewer state, context, and pending question from transcript."""
        if transcript.is_finished:
            raise RuntimeError("Completed interviews cannot be resumed.")
        if not transcript.pending_question:
            raise RuntimeError("Unfinished interview has no pending question and cannot be resumed.")

        target_case = case or RequirementCase(
            case_id=transcript.case_id,
            project_name=transcript.project_name,
            initial_requirements=transcript.initial_requirements,
        )
        self.initialize(target_case)

        self._turns = list(transcript.turns)
        self._current_turn_index = len(self._turns)

        # Reconstruct completed turns in conversation history
        for turn in self._turns:
            self._messages.append(Message(role="assistant", content=turn.interviewer_utterance))
            self._messages.append(Message(role="user", content=turn.interviewee_utterance))

        self._is_finished = transcript.is_finished

        # Restore pending question without re-calling LLM
        if not self._is_finished and transcript.pending_question:
            self._pending_interviewer_utterance = transcript.pending_question
            self._messages.append(Message(role="assistant", content=transcript.pending_question))
        else:
            self._pending_interviewer_utterance = None

    def export_transcript(self) -> InterviewTranscript:
        """Return the self-contained structured transcript of the current session."""
        if self._case is None:
            raise RuntimeError("Cannot export transcript from an uninitialized interviewer.")

        return InterviewTranscript(
            case_id=self._case.case_id,
            project_name=self._case.project_name,
            initial_requirements=self._case.initial_requirements,
            turns=list(self._turns),
            pending_question=self._pending_interviewer_utterance,
            is_finished=self._is_finished,
        )
