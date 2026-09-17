"""Worker handler for proposed_method elicitation pipeline."""

import asyncio
from pathlib import Path
from typing import Any, Dict, Optional

from interview.workers.handlers.base_handler import BaseMethodHandler


class ProposedMethodHandler(BaseMethodHandler):
    """Executes proposed_method elicitation pipeline inside isolated worker."""

    def __init__(
        self,
        config_path: Path,
        native_dir: Path,
        method_root: Path,
    ) -> None:
        from config import AppConfig
        from pipeline import ElicitationPipeline

        self.method_root = method_root
        self.native_dir = native_dir
        self.config_path = config_path

        self.config = AppConfig.load_from_yaml(config_path)
        self.config.runtime.runs_dir = str(native_dir)

        if not Path(self.config.runtime.prompts_dir).is_absolute():
            self.config.runtime.prompts_dir = str(self.method_root / self.config.runtime.prompts_dir)

        self.pipeline: Optional[ElicitationPipeline] = None
        self.case_id: Optional[str] = None

    def start(self, case_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize project and generate opening question."""
        from pipeline import ElicitationPipeline

        self.case_id = case_payload["case_id"]
        self.pipeline = ElicitationPipeline.create(
            project_name=case_payload["project_name"],
            initial_requirements=case_payload["initial_requirements"],
            config=self.config,
            project_id=self.case_id,
            base_runs_dir=self.native_dir,
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            res = loop.run_until_complete(self.pipeline.initialize())
        finally:
            loop.close()

        return {
            "native_project_id": self.case_id,
            "question": res.next_question,
            "finished": res.is_finished,
            "turn_count": res.turn_index,
            "finish_message": None,
        }

    def submit_answer(self, answer: str) -> Dict[str, Any]:
        """Submit stakeholder answer and advance to next turn."""
        if not self.pipeline:
            raise RuntimeError("Pipeline must be initialized or resumed before submit_answer.")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            res = loop.run_until_complete(self.pipeline.step(answer=answer))
        finally:
            loop.close()

        next_q = res.next_question if not res.is_finished else ""
        return {
            "native_project_id": self.case_id or "",
            "question": next_q,
            "finished": res.is_finished,
            "turn_count": res.turn_index,
            "finish_message": res.finish_message if res.is_finished else None,
        }

    def inspect(self) -> Dict[str, Any]:
        """Inspect current status without stepping."""
        if not self.pipeline:
            raise RuntimeError("Pipeline not loaded.")

        state = self.pipeline.store.load_state(self.pipeline.project_id)
        turns = self.pipeline.store.load_turns(self.pipeline.project_id)

        latest_q = ""
        for turn in reversed(turns):
            if turn.role == "Interviewer":
                latest_q = turn.message_content
                break

        return {
            "native_project_id": self.case_id or "",
            "question": latest_q,
            "finished": state.project_status == "Completed",
            "turn_count": state.turn_index,
            "finish_message": "Interview session completed." if state.project_status == "Completed" else None,
        }

    def resume(self, case_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Resume session using ElicitationPipeline.resume."""
        from pipeline import ElicitationPipeline

        self.case_id = case_payload["case_id"]
        self.pipeline = ElicitationPipeline.resume(
            project_id=self.case_id,
            config=self.config,
            base_runs_dir=self.native_dir,
        )

        state = self.pipeline.store.load_state(self.case_id)
        if state.project_status == "Completed":
            return {
                "native_project_id": self.case_id,
                "question": "",
                "finished": True,
                "turn_count": state.turn_index,
                "finish_message": "Interview already completed.",
            }

        if self.pipeline.pending_user_turn:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                res = loop.run_until_complete(
                    self.pipeline.step(answer=self.pipeline.pending_user_turn.message_content)
                )
            finally:
                loop.close()

            return {
                "native_project_id": self.case_id,
                "question": res.next_question if not res.is_finished else "",
                "finished": res.is_finished,
                "turn_count": res.turn_index,
                "finish_message": res.finish_message if res.is_finished else None,
            }

        # Otherwise retrieve the current pending interviewer question
        turns = self.pipeline.store.load_turns(self.case_id)
        latest_q = ""
        for turn in reversed(turns):
            if turn.role == "Interviewer":
                latest_q = turn.message_content
                break

        return {
            "native_project_id": self.case_id,
            "question": latest_q,
            "finished": False,
            "turn_count": state.turn_index,
            "finish_message": None,
        }
