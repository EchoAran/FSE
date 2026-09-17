"""Hashimoto dynamic slot and abduction requirements interview coordinator."""

from src.client.base import BaseLLMClient
from src.client.openai_client import OpenAIClient
from src.config import InterviewConfig
from src.core.abductive_slot_generator import AbductiveSlotGenerator
from src.core.question_generator import QuestionGenerator
from src.core.slot_filler import SlotFiller
from src.models import (
    AbductionRecord,
    DialogueTurn,
    InterviewCheckpoint,
    InterviewTranscript,
    InterviewTurn,
    Message,
    RequirementCase,
    Slot,
)
from src.prompt.loader import PromptLoader


class HashimotoInterviewer:
    """Orchestrates dynamic slot generation, abduction, and targeted question generation."""

    def __init__(
        self,
        config: InterviewConfig | None = None,
        llm_client: BaseLLMClient | None = None,
        prompt_loader: PromptLoader | None = None,
    ) -> None:
        """Initialize interviewer with configuration, LLM client, and prompt loader."""
        self.config = config or InterviewConfig()
        self.llm_client = llm_client or OpenAIClient(
            api_key=self.config.api_key or None,
            base_url=self.config.base_url or None,
        )
        self.prompt_loader = prompt_loader or PromptLoader()

        slot_filling_prompt = self.prompt_loader.load_prompt("slot_filling.txt", self.config.prompts_dir)
        abductive_slot_prompt = self.prompt_loader.load_prompt("abductive_slot_generation.txt", self.config.prompts_dir)
        question_gen_prompt = self.prompt_loader.load_prompt("question_generation.txt", self.config.prompts_dir)

        self.slot_filler = SlotFiller(slot_filling_prompt, self.llm_client)
        self.abductive_slot_generator = AbductiveSlotGenerator(abductive_slot_prompt, self.llm_client)
        self.question_generator = QuestionGenerator(question_gen_prompt, self.llm_client)

        self._case: RequirementCase | None = None
        self._slots: dict[str, Slot] = {}
        self._abduction_history: list[AbductionRecord] = []
        self._messages: list[Message] = []
        self._turns: list[InterviewTurn] = []
        self._current_turn_index: int = 0
        self._is_initialized: bool = False
        self._is_finished: bool = False
        self._pending_interviewer_utterance: str | None = None
        self._pending_target_slots: list[str] = []

    @property
    def is_initialized(self) -> bool:
        """Return whether the session has been initialized."""
        return self._is_initialized

    @property
    def is_finished(self) -> bool:
        """Return whether the interview has terminated."""
        return self._is_finished

    @property
    def turn_count(self) -> int:
        """Return number of completed dialogue turns."""
        return len(self._turns)

    @property
    def slots(self) -> dict[str, Slot]:
        """Return the current active slot dictionary."""
        return dict(self._slots)

    @property
    def abduction_history(self) -> list[AbductionRecord]:
        """Return the chronological abduction history."""
        return list(self._abduction_history)

    @property
    def pending_target_slots(self) -> list[str]:
        """Return the target slots associated with the active pending question."""
        return list(self._pending_target_slots)

    @property
    def fill_rate(self) -> float:
        """Calculate the proportion of filled slots."""
        if not self._slots:
            return 0.0
        filled = sum(1 for s in self._slots.values() if s.is_filled)
        return filled / len(self._slots)

    def initialize(self, case: RequirementCase | dict) -> None:
        """Set up the session with requirement case and initial RE slots."""
        if isinstance(case, dict):
            self._case = RequirementCase(**case)
        else:
            self._case = case

        initial_slots = self.prompt_loader.load_initial_slots(self.config.initial_slots_path)
        self._slots = {s.name: Slot(name=s.name, category=s.category, value=s.value) for s in initial_slots}
        self._abduction_history = []
        self._messages = []
        self._turns = []
        self._current_turn_index = 0
        self._is_finished = False
        self._pending_interviewer_utterance = None
        self._pending_target_slots = []
        self._is_initialized = True

    def get_first_question(self) -> str:
        """Generate and return the initial opening question targeting initial slots."""
        if not self._is_initialized or self._case is None:
            raise RuntimeError("Interviewer must be initialized before requesting the first question.")

        if self._pending_interviewer_utterance is not None:
            return self._pending_interviewer_utterance

        target_slots, first_question = self.question_generator.generate_question(
            current_slots=self._slots,
            dialogue_history=self._messages,
            initial_requirements=self._case.initial_requirements,
            latest_abduction=None,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

        self._pending_target_slots = target_slots
        self._pending_interviewer_utterance = first_question
        self._messages.append(Message(role="assistant", content=first_question))
        return first_question

    def step(self, interviewee_answer: str) -> str:
        """Execute the interview pipeline (Filling -> Abductive Slot Gen -> Question) atomically."""
        if not self._is_initialized or self._case is None:
            raise RuntimeError("Interviewer must be initialized before calling step().")

        if self._is_finished:
            raise RuntimeError("Interview is already completed. No further steps can be executed.")

        if self._pending_interviewer_utterance is None:
            self.get_first_question()

        current_question = self._pending_interviewer_utterance or ""
        current_target_slots = list(self._pending_target_slots)
        candidate_turn_id = self._current_turn_index + 1
        candidate_messages = list(self._messages) + [Message(role="user", content=interviewee_answer)]

        # Stage 1: Slot Filling (propagating initial_requirements)
        filled_slots = self.slot_filler.fill_slots(
            current_slots=self._slots,
            dialogue_history=candidate_messages,
            initial_requirements=self._case.initial_requirements,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

        # Stage 2: Abductive Slot Generation (new slots <= 5)
        abduction_record, new_slots = self.abductive_slot_generator.generate(
            current_slots=filled_slots,
            dialogue_history=candidate_messages,
            abduction_history=self._abduction_history,
            initial_requirements=self._case.initial_requirements,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

        for slot in new_slots:
            filled_slots[slot.name] = slot

        candidate_abduction_history = list(self._abduction_history)
        if abduction_record is not None:
            candidate_abduction_history.append(abduction_record)

        # Check termination: strictly greater than fill_rate_threshold or max turns reached
        current_fill_rate = sum(1 for s in filled_slots.values() if s.is_filled) / len(filled_slots)
        if candidate_turn_id >= self.config.max_turns or current_fill_rate > self.config.fill_rate_threshold:
            self._slots = filled_slots
            self._abduction_history = candidate_abduction_history
            self._current_turn_index = candidate_turn_id
            self._messages = candidate_messages
            turn = InterviewTurn(
                turn_id=self._current_turn_index,
                interviewer_utterance=current_question,
                interviewee_utterance=interviewee_answer,
                target_slots=current_target_slots,
            )
            self._turns.append(turn)
            self._is_finished = True
            self._pending_interviewer_utterance = None
            self._pending_target_slots = []
            return ""

        # Stage 3: Question Generation (targeting unfilled and abduced slots)
        next_target_slots, next_question = self.question_generator.generate_question(
            current_slots=filled_slots,
            dialogue_history=candidate_messages,
            initial_requirements=self._case.initial_requirements,
            latest_abduction=abduction_record,
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

        # Atomically commit all state changes
        self._slots = filled_slots
        self._abduction_history = candidate_abduction_history
        self._current_turn_index = candidate_turn_id
        turn = InterviewTurn(
            turn_id=self._current_turn_index,
            interviewer_utterance=current_question,
            interviewee_utterance=interviewee_answer,
            target_slots=current_target_slots,
        )
        self._turns.append(turn)
        self._messages = candidate_messages + [Message(role="assistant", content=next_question)]
        self._pending_interviewer_utterance = next_question
        self._pending_target_slots = next_target_slots

        return next_question

    def resume_from_checkpoint(
        self,
        checkpoint: InterviewCheckpoint,
        case: RequirementCase | None = None,
    ) -> None:
        """Losslessly restore session state, slot values, and abduction history from checkpoint."""
        if checkpoint.is_finished:
            raise RuntimeError("Completed interviews cannot be resumed.")
        if not checkpoint.pending_question:
            raise RuntimeError("Unfinished interview has no pending question and cannot be resumed.")

        target_case = case or RequirementCase(
            case_id=checkpoint.case_id,
            project_name=checkpoint.project_name,
            initial_requirements=checkpoint.initial_requirements,
        )
        self.initialize(target_case)

        # Restore tracked slots snapshot
        self._slots = {s.name: Slot(name=s.name, category=s.category, value=s.value) for s in checkpoint.slots}
        self._abduction_history = [
            AbductionRecord(
                surprising_fact=rec.surprising_fact,
                suspected_reason=rec.suspected_reason,
                new_slot=rec.new_slot,
            )
            for rec in checkpoint.abduction_history
        ]
        self._turns = list(checkpoint.turns)
        self._current_turn_index = len(self._turns)

        # Reconstruct dialogue message history
        self._messages = []
        for turn in self._turns:
            self._messages.append(Message(role="assistant", content=turn.interviewer_utterance))
            self._messages.append(Message(role="user", content=turn.interviewee_utterance))

        self._is_finished = checkpoint.is_finished
        self._pending_target_slots = list(checkpoint.pending_target_slots)

        # Restore active pending question without LLM re-generation
        if not self._is_finished and checkpoint.pending_question:
            self._pending_interviewer_utterance = checkpoint.pending_question
            self._messages.append(Message(role="assistant", content=checkpoint.pending_question))
        else:
            self._pending_interviewer_utterance = None

    def resume_from_transcript(
        self,
        checkpoint_or_transcript: InterviewCheckpoint | InterviewTranscript,
        case: RequirementCase | None = None,
    ) -> None:
        """Resume session, strictly requiring an InterviewCheckpoint instance."""
        if isinstance(checkpoint_or_transcript, InterviewCheckpoint):
            self.resume_from_checkpoint(checkpoint_or_transcript, case)
        else:
            raise ValueError(
                "Lossless session resumption requires an InterviewCheckpoint instance. "
                "An InterviewTranscript only contains conversation dialogue history. "
                "Please pass an InterviewCheckpoint loaded via TranscriptExporter.load_checkpoint()."
            )

    def export_transcript(self) -> InterviewTranscript:
        """Return clean public conversation transcript containing only DialogueTurn records."""
        if self._case is None:
            raise RuntimeError("Cannot export transcript from an uninitialized interviewer.")

        clean_turns = [
            DialogueTurn(
                turn_id=t.turn_id,
                interviewer_utterance=t.interviewer_utterance,
                interviewee_utterance=t.interviewee_utterance,
            )
            for t in self._turns
        ]

        return InterviewTranscript(
            case_id=self._case.case_id,
            project_name=self._case.project_name,
            turns=clean_turns,
        )

    def export_checkpoint(self) -> InterviewCheckpoint:
        """Return complete internal execution checkpoint for lossless restoration."""
        if self._case is None:
            raise RuntimeError("Cannot export checkpoint from an uninitialized interviewer.")

        return InterviewCheckpoint(
            case_id=self._case.case_id,
            project_name=self._case.project_name,
            initial_requirements=self._case.initial_requirements,
            turns=list(self._turns),
            slots=list(self._slots.values()),
            abduction_history=list(self._abduction_history),
            pending_question=self._pending_interviewer_utterance,
            pending_target_slots=list(self._pending_target_slots),
            is_finished=self._is_finished,
        )
