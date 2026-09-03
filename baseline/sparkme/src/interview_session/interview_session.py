"""Interview session orchestrator coordinating Interviewer, AgendaManager, and ExplorationPlanner."""

import asyncio
import copy
from datetime import datetime, timedelta
import os
from pathlib import Path
from typing import Dict, List, Optional
import uuid

import faiss
import numpy as np
from tiktoken import get_encoding

from src.agents.agenda_manager.agenda_manager import AgendaManager, AgendaManagerConfig
from src.agents.base_agent import BaseAgent
from src.agents.exploration_planner.exploration_planner import (
    ExplorationPlanner,
    ExplorationPlannerConfig,
)
from src.agents.interviewer.interviewer import (
    Interviewer,
    InterviewerConfig,
    TTSConfig,
)
from src.content.memory_bank.memory import Memory
from src.content.memory_bank.memory_bank_vector_db import VectorMemoryBank
from src.content.question_bank.question_bank_vector_db import QuestionBankVectorDB
from src.content.session_agenda.session_agenda import SessionAgenda
from src.interview_session.session_models import Message, MessageType, Participant
from src.interview_session.user.user import User
from src.models import DialogueTurn, InterviewTranscript
from src.utils.logger.session_logger import SessionLogger, setup_logger
from src.utils.token_tracker import TokenUsageTracker


class InterviewSession:
    """Core interview session orchestrating multi-agent collaboration."""

    def __init__(
        self,
        user_id: str = "default_user",
        interview_description: str = "Software Requirements Elicitation",
        interview_plan_path: Optional[str] = None,
        initial_context: Optional[str] = None,
        max_turns: Optional[int] = 20,
    ) -> None:
        """Initialize the interview session and all collaborating agents."""
        self.user_id = user_id
        self._interview_description = interview_description
        self._initial_additional_context = initial_context or ""
        self.max_turns = max_turns

        # Resolve topics path
        if interview_plan_path is None:
            default_path = Path(__file__).parent.parent.parent / "data" / "configs" / "topics.json"
            interview_plan_path = str(default_path) if default_path.exists() else "data/configs/topics.json"

        # Session Agenda setup
        self.session_agenda = SessionAgenda.initialize_session_agenda(
            user_id=self.user_id,
            initial_user_portrait_path=None,
            interview_plan_path=interview_plan_path,
            interview_description=self._interview_description,
        )
        self.session_id = self.session_agenda.session_id + 1

        # Memory bank setup
        self.memory_bank = VectorMemoryBank.load_from_file(self.user_id)
        self.memory_bank.set_session_id(self.session_id)

        # Question bank setup
        self.historical_question_bank = QuestionBankVectorDB.load_from_file(self.user_id)
        self.historical_question_bank.set_session_id(self.session_id)
        self.proposed_question_bank = QuestionBankVectorDB()

        # Logger setup
        setup_logger(self.user_id, self.session_id, console_output_files=["execution_log"])

        # Token usage tracking
        self.token_tracker = TokenUsageTracker(
            session_id=str(self.session_id),
            user_id=self.user_id,
        )
        BaseAgent.token_tracker = self.token_tracker

        # Chat history
        self.chat_history: list[Message] = []

        # State tracking
        self.session_in_progress = True
        self.session_completed = False
        self._user_message_count = 0
        self._last_message_time = datetime.now()
        self._last_user_message: Optional[Message] = None
        self.timeout_minutes = int(os.getenv("SESSION_TIMEOUT_MINUTES", "10"))

        # User participant
        self.user = User(user_id=self.user_id, interview_session=self)

        # Agent 1: Interviewer
        self._interviewer = Interviewer(
            config=InterviewerConfig(
                user_id=self.user_id,
                tts=TTSConfig(enabled=False),
                interview_description=self._interview_description,
            ),
            interview_session=self,
        )

        # Agent 2: Agenda Manager
        scribe_config = AgendaManagerConfig(user_id=self.user_id)
        scribe_model = os.getenv("AGENDA_MANAGER_MODEL_NAME")
        if scribe_model:
            scribe_config["model_name"] = scribe_model
            scribe_base_url = os.getenv("AGENDA_MANAGER_VLLM_BASE_URL")
            if scribe_base_url:
                scribe_config["base_url"] = scribe_base_url

        self.agenda_manager = AgendaManager(
            config=scribe_config,
            interview_session=self,
        )

        # Agent 3: Exploration Planner
        planner_config = ExplorationPlannerConfig(
            user_id=self.user_id,
            turn_trigger=int(os.getenv("EXPLORATION_PLANNER_TURN_TRIGGER", "3")),
            num_rollouts=int(os.getenv("EXPLORATION_PLANNER_NUM_ROLLOUTS", "3")),
            rollout_horizon=int(os.getenv("EXPLORATION_PLANNER_ROLLOUT_HORIZON", "3")),
            max_strategic_questions=int(os.getenv("EXPLORATION_PLANNER_MAX_QUESTIONS", "5")),
            alpha=float(os.getenv("EXPLORATION_PLANNER_ALPHA", "0.5")),
            beta=float(os.getenv("EXPLORATION_PLANNER_BETA", "0.3")),
            gamma=float(os.getenv("EXPLORATION_PLANNER_GAMMA", "0.2")),
        )
        planner_model = os.getenv("EXPLORATION_PLANNER_MODEL_NAME")
        if planner_model:
            planner_config["model_name"] = planner_model
            planner_base_url = os.getenv("EXPLORATION_PLANNER_VLLM_BASE_URL")
            if planner_base_url:
                planner_config["base_url"] = planner_base_url

        self.exploration_planner = ExplorationPlanner(
            config=planner_config,
            interview_session=self,
        )

        # Subscription map
        self._subscriptions: Dict[str, List[Participant]] = {
            "Interviewer": [self.agenda_manager, self.user],
            "User": [self._interviewer, self.agenda_manager, self.exploration_planner],
        }

        self.tokenizer = get_encoding("cl100k_base")

    async def _notify_participants(self, message: Message) -> None:
        """Notify subscriber participants asynchronously and wait for turn tasks."""
        subscribers = self._subscriptions.get(message.role, [])
        tasks = []
        for sub in subscribers:
            if self.session_in_progress:
                task = asyncio.create_task(sub.on_message(message))
                tasks.append(task)

        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=False)
            except Exception:
                for t in tasks:
                    if not t.done():
                        t.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
                raise

        if message.role == "User":
            self._last_user_message = message
            self._user_message_count += 1
            BaseAgent.current_turn = self._user_message_count

            if self.max_turns is not None and self._user_message_count >= self.max_turns:
                self.session_in_progress = False
                self.session_completed = True
            elif self.session_agenda.all_core_topics_completed():
                self.session_in_progress = False
                self.session_completed = True

    def add_message_to_chat_history(
        self,
        role: str,
        content: str = "",
        message_type: str = MessageType.CONVERSATION,
        metadata: Optional[dict] = None,
    ) -> Message:
        """Add a message to the session chat history and return it."""
        if not self.session_in_progress:
            raise RuntimeError("Cannot add message: session is already completed.")

        message = Message(
            id=str(uuid.uuid4()),
            type=message_type,
            role=role,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata or {},
        )

        if role == "User":
            self._last_message_time = message.timestamp
        elif role == "Interviewer" and self._last_user_message is not None:
            self._last_user_message = None

        self.chat_history.append(message)
        SessionLogger.log_to_file("chat_history", f"{message.role}: {message.content}")
        return message

    async def start_session(self) -> str:
        """Generate and return the initial opening question from the interviewer."""
        if self._initial_additional_context:
            self.session_agenda.user_portrait = {"initial_requirements": self._initial_additional_context}

        await self._interviewer.on_message(None)
        latest_msg = self.chat_history[-1] if self.chat_history else None
        if latest_msg and latest_msg.role == "Interviewer":
            await self._notify_participants(latest_msg)
        return self.get_latest_interviewer_question()

    def _create_state_snapshot(self) -> dict:
        """Capture domain state snapshot for transactional safety without deepcopying HTTP/Lock clients."""
        manager = self.session_agenda.interview_topic_manager
        return {
            "chat_history": copy.deepcopy(self.chat_history),
            "user_message_count": self._user_message_count,
            "session_in_progress": self.session_in_progress,
            "session_completed": self.session_completed,
            "last_user_message": copy.deepcopy(self._last_user_message),
            # SessionAgenda domain state
            "user_portrait": copy.deepcopy(self.session_agenda.user_portrait),
            "last_meeting_summary": self.session_agenda.last_meeting_summary,
            "interview_description": self.session_agenda.interview_description,
            "additional_notes": copy.deepcopy(self.session_agenda.additional_notes),
            "strategic_priorities": copy.deepcopy(self.session_agenda.strategic_priorities),
            "emergent_insights": copy.deepcopy(self.session_agenda.emergent_insights),
            "current_snapshot": self.session_agenda.current_snapshot,
            # Topic Manager domain state
            "manager_core_topic_dict": copy.deepcopy(manager.core_topic_dict),
            "manager_active_topic_id_list": copy.deepcopy(manager.active_topic_id_list),
            "manager_coverage_stats": copy.deepcopy(manager.coverage_stats),
            "manager_enable_emergent": manager.enable_emergent_subtopics,
            "manager_subtopic_embeddings": {k: np.copy(v) for k, v in manager.subtopic_embeddings.items()},
            "manager_similarity_threshold": manager.similarity_threshold,
            # MemoryBank domain state
            "memory_bank_memories": copy.deepcopy(self.memory_bank.memories) if self.memory_bank else [],
            "memory_bank_embeddings": {k: np.copy(v) for k, v in self.memory_bank.embeddings.items()} if self.memory_bank else {},
            "memory_bank_session_id": getattr(self.memory_bank, "session_id", None),
            # QuestionBank domain state
            "question_bank_questions": copy.deepcopy(self.proposed_question_bank.questions) if self.proposed_question_bank else [],
            "question_bank_embeddings": {k: np.copy(v) for k, v in self.proposed_question_bank.embeddings.items()} if self.proposed_question_bank else {},
            "question_bank_session_id": getattr(self.proposed_question_bank, "session_id", None),
            # Planner domain state
            "strategic_state": copy.deepcopy(self.exploration_planner.strategic_state) if hasattr(self.exploration_planner, "strategic_state") else None,
            "planner_last_planning_turn": getattr(self.exploration_planner, "_last_planning_turn", 0),
            # AgendaManager internal turn tracking
            "agenda_last_interviewer_message": getattr(self.agenda_manager, "_last_interviewer_message", None),
            "agenda_new_memories": copy.deepcopy(getattr(self.agenda_manager, "_new_memories", [])),
            "agenda_all_session_memories": copy.deepcopy(getattr(self.agenda_manager, "_all_session_memories", [])),
            "agenda_memory_id_map": copy.deepcopy(getattr(self.agenda_manager, "_memory_id_map", {})),
            # Event streams
            "agenda_events": copy.deepcopy(self.agenda_manager.event_stream) if hasattr(self.agenda_manager, "event_stream") else [],
            "interviewer_events": copy.deepcopy(self._interviewer.event_stream) if hasattr(self._interviewer, "event_stream") else [],
            "planner_events": copy.deepcopy(self.exploration_planner.event_stream) if hasattr(self.exploration_planner, "event_stream") else [],
        }

    def _restore_state_snapshot(self, snapshot: dict) -> None:
        """Roll back all components to pre-turn snapshot without replacing client instances."""
        self.chat_history = snapshot["chat_history"]
        self._user_message_count = snapshot["user_message_count"]
        self.session_in_progress = snapshot["session_in_progress"]
        self.session_completed = snapshot["session_completed"]
        self._last_user_message = snapshot["last_user_message"]
        BaseAgent.current_turn = self._user_message_count

        # Restore SessionAgenda and Topic Manager in-place
        self.session_agenda.user_portrait = snapshot["user_portrait"]
        self.session_agenda.last_meeting_summary = snapshot["last_meeting_summary"]
        self.session_agenda.interview_description = snapshot["interview_description"]
        self.session_agenda.additional_notes = snapshot["additional_notes"]
        self.session_agenda.strategic_priorities = snapshot["strategic_priorities"]
        self.session_agenda.emergent_insights = snapshot["emergent_insights"]
        self.session_agenda.current_snapshot = snapshot["current_snapshot"]

        manager = self.session_agenda.interview_topic_manager
        manager.core_topic_dict = snapshot["manager_core_topic_dict"]
        manager.active_topic_id_list = snapshot["manager_active_topic_id_list"]
        manager.coverage_stats = snapshot["manager_coverage_stats"]
        manager.enable_emergent_subtopics = snapshot["manager_enable_emergent"]
        manager.subtopic_embeddings = snapshot["manager_subtopic_embeddings"]
        manager.similarity_threshold = snapshot["manager_similarity_threshold"]

        # Restore MemoryBank in-place and rebuild FAISS index
        if self.memory_bank:
            self.memory_bank.memories = snapshot["memory_bank_memories"]
            self.memory_bank.embeddings = snapshot["memory_bank_embeddings"]
            self.memory_bank.session_id = snapshot["memory_bank_session_id"]
            if hasattr(self.memory_bank, "index") and hasattr(self.memory_bank, "embedding_dimension"):
                self.memory_bank.index = faiss.IndexFlatL2(self.memory_bank.embedding_dimension)
                for mem in self.memory_bank.memories:
                    emb = self.memory_bank.embeddings.get(mem.id)
                    if emb is not None:
                        self.memory_bank.index.add(emb.reshape(1, -1))

        # Restore QuestionBank in-place and rebuild FAISS index
        if self.proposed_question_bank:
            self.proposed_question_bank.questions = snapshot["question_bank_questions"]
            self.proposed_question_bank.embeddings = snapshot["question_bank_embeddings"]
            self.proposed_question_bank.session_id = snapshot["question_bank_session_id"]
            if hasattr(self.proposed_question_bank, "index") and hasattr(self.proposed_question_bank, "embedding_dimension"):
                self.proposed_question_bank.index = faiss.IndexFlatL2(self.proposed_question_bank.embedding_dimension)
                for q in self.proposed_question_bank.questions:
                    emb = self.proposed_question_bank.embeddings.get(q.id)
                    if emb is not None:
                        self.proposed_question_bank.index.add(emb.reshape(1, -1))

        # Restore AgendaManager internal turn states
        if hasattr(self.agenda_manager, "_last_interviewer_message"):
            self.agenda_manager._last_interviewer_message = snapshot["agenda_last_interviewer_message"]
        if hasattr(self.agenda_manager, "_new_memories"):
            self.agenda_manager._new_memories = snapshot["agenda_new_memories"]
        if hasattr(self.agenda_manager, "_all_session_memories"):
            self.agenda_manager._all_session_memories = snapshot["agenda_all_session_memories"]
        if hasattr(self.agenda_manager, "_memory_id_map"):
            self.agenda_manager._memory_id_map = snapshot["agenda_memory_id_map"]
        if hasattr(self.agenda_manager, "event_stream"):
            self.agenda_manager.event_stream = snapshot["agenda_events"]

        # Restore Interviewer event stream
        if hasattr(self._interviewer, "event_stream"):
            self._interviewer.event_stream = snapshot["interviewer_events"]

        # Restore Planner state
        if hasattr(self.exploration_planner, "event_stream"):
            self.exploration_planner.event_stream = snapshot["planner_events"]
        if snapshot["strategic_state"] is not None and hasattr(self.exploration_planner, "strategic_state"):
            self.exploration_planner.strategic_state = snapshot["strategic_state"]
        if hasattr(self.exploration_planner, "_last_planning_turn"):
            self.exploration_planner._last_planning_turn = snapshot["planner_last_planning_turn"]

        # Comprehensively re-bind all tools across all agents
        if hasattr(self._interviewer, "tools") and self._interviewer.tools:
            if "recall" in self._interviewer.tools:
                self._interviewer.tools["recall"].memory_bank = self.memory_bank

        if hasattr(self.agenda_manager, "tools") and self.agenda_manager.tools:
            if "update_memory_bank_and_session" in self.agenda_manager.tools:
                self.agenda_manager.tools["update_memory_bank_and_session"].memory_bank = self.memory_bank
                self.agenda_manager.tools["update_memory_bank_and_session"].session_agenda = self.session_agenda
            if "update_session_agenda" in self.agenda_manager.tools:
                self.agenda_manager.tools["update_session_agenda"].session_agenda = self.session_agenda
            if "update_subtopic_coverage" in self.agenda_manager.tools:
                self.agenda_manager.tools["update_subtopic_coverage"].session_agenda = self.session_agenda
            if "feedback_subtopic_coverage" in self.agenda_manager.tools:
                self.agenda_manager.tools["feedback_subtopic_coverage"].session_agenda = self.session_agenda
            if "update_subtopic_notes" in self.agenda_manager.tools:
                self.agenda_manager.tools["update_subtopic_notes"].session_agenda = self.session_agenda
            if "recall" in self.agenda_manager.tools:
                self.agenda_manager.tools["recall"].memory_bank = self.memory_bank

        if hasattr(self.exploration_planner, "tools") and self.exploration_planner.tools:
            if "suggest_strategic_questions" in self.exploration_planner.tools:
                self.exploration_planner.tools["suggest_strategic_questions"].strategic_state = self.exploration_planner.strategic_state
                self.exploration_planner.tools["suggest_strategic_questions"].session_agenda = self.session_agenda
            if "add_emergent_subtopic" in self.exploration_planner.tools:
                self.exploration_planner.tools["add_emergent_subtopic"].session_agenda = self.session_agenda
            if "identify_emergent_insights" in self.exploration_planner.tools:
                self.exploration_planner.tools["identify_emergent_insights"].session_agenda = self.session_agenda

    async def submit_answer(self, answer: str) -> str:
        """Submit a stakeholder answer transactionally and return the next interviewer question."""
        if not self.session_in_progress:
            return ""

        snapshot = self._create_state_snapshot()

        try:
            user_message = self.add_message_to_chat_history(role="User", content=answer)
            await self._notify_participants(user_message)

            latest_msg = self.chat_history[-1] if self.chat_history else None
            if latest_msg and latest_msg.role == "Interviewer":
                await self._notify_participants(latest_msg)

            if not self.session_in_progress:
                return ""

            return self.get_latest_interviewer_question()
        except Exception:
            self._restore_state_snapshot(snapshot)
            raise

    def get_latest_interviewer_question(self) -> str:
        """Retrieve the most recent interviewer question from chat history."""
        for msg in reversed(self.chat_history):
            if msg.role == "Interviewer":
                return msg.content
        return ""

    def export_transcript(self, case_id: str = "", project_name: str = "") -> InterviewTranscript:
        """Export clean public transcript containing only dialogue turns."""
        turns: list[DialogueTurn] = []
        turn_id = 1

        i = 0
        while i < len(self.chat_history):
            msg = self.chat_history[i]
            if msg.role == "Interviewer":
                question = msg.content
                answer = ""
                if i + 1 < len(self.chat_history) and self.chat_history[i + 1].role == "User":
                    answer = self.chat_history[i + 1].content
                    i += 1
                if answer:
                    turns.append(
                        DialogueTurn(
                            turn_id=turn_id,
                            interviewer_utterance=question,
                            interviewee_utterance=answer,
                        )
                    )
                    turn_id += 1
            i += 1

        return InterviewTranscript(
            case_id=case_id,
            project_name=project_name or self._interview_description,
            initial_requirements=self._initial_additional_context,
            turns=turns,
            is_completed=self.session_completed or not self.session_in_progress,
        )

    def end_session(self) -> None:
        """End the interview session cleanly and persist all method assets to disk."""
        self.session_in_progress = False
        self.session_completed = True
        if self.memory_bank:
            self.memory_bank.save_to_file(self.user_id)
        if self.proposed_question_bank:
            self.proposed_question_bank.save_to_file(self.user_id)
        if self.session_agenda:
            self.session_agenda.save(save_type="original")
        if hasattr(self, "token_tracker") and self.token_tracker:
            self.token_tracker.save_final_summary()