"""Worker handler for SparkMe requirements interview baseline."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

from interview.workers.handlers.base_handler import BaseMethodHandler


class SparkMeHandler(BaseMethodHandler):
    """Executes SparkMe baseline inside the isolated worker subprocess."""

    def __init__(
        self,
        config_path: Path,
        native_dir: Path,
        method_root: Path,
    ) -> None:
        from dotenv import load_dotenv

        self.method_root = method_root
        self.native_dir = native_dir
        self.config_path = config_path

        # Strictly enforce LOGS_DIR pointing to native results directory
        logs_dir = (self.native_dir / "logs").resolve()
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Load environment variables from selected .env with override=True so method settings take precedence
        if config_path.is_file():
            load_dotenv(config_path, override=True)

        # Strictly force isolated LOGS_DIR after loading .env
        os.environ["LOGS_DIR"] = str(logs_dir)

        # Parse MAX_TURNS if defined in config
        max_turns_env = os.getenv("MAX_TURNS", "").strip()
        max_turns: Optional[int] = None
        if max_turns_env:
            try:
                parsed_val = int(max_turns_env)
                if parsed_val > 0:
                    max_turns = parsed_val
            except ValueError:
                pass

        from src.interviewer import SparkMeInterviewer

        self.interviewer = SparkMeInterviewer(max_turns=max_turns)
        self.case_id: Optional[str] = None
        self._first_question: Optional[str] = None

    def start(self, case_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize session and generate opening question."""
        from src.models import RequirementCase
        from src.transcript import TranscriptExporter

        self.case_id = case_payload["case_id"]
        case = RequirementCase(
            case_id=self.case_id,
            project_name=case_payload["project_name"],
            initial_requirements=case_payload["initial_requirements"],
        )
        self.interviewer.initialize(case)
        self._first_question = self.interviewer.get_first_question()

        # Save initial transcript
        transcript = self.interviewer.export_transcript()
        TranscriptExporter.save_transcript(transcript, self.native_dir / "transcript.json")

        return {
            "native_project_id": self.case_id,
            "question": self._first_question,
            "finished": self.interviewer.is_finished,
            "turn_count": self.interviewer.turn_count,
            "finish_message": None,
        }

    def submit_answer(self, answer: str) -> Dict[str, Any]:
        """Submit answer to active session and export transcript."""
        from src.transcript import TranscriptExporter

        next_q = self.interviewer.step(answer)

        # Export current public transcript to native/
        transcript = self.interviewer.export_transcript()
        TranscriptExporter.save_transcript(transcript, self.native_dir / "transcript.json")

        finish_message = None
        if self.interviewer.is_finished:
            # Persist session assets (agenda, memory bank, question bank, token tracker) on completion
            if self.interviewer.session:
                self.interviewer.session.end_session()
            finish_message = "SparkMe interview completed (agenda completed or max turns reached)."

        return {
            "native_project_id": self.case_id or "",
            "question": next_q,
            "finished": self.interviewer.is_finished,
            "turn_count": self.interviewer.turn_count,
            "finish_message": finish_message,
        }

    def inspect(self) -> Dict[str, Any]:
        """Inspect current state."""
        return {
            "native_project_id": self.case_id or "",
            "question": getattr(self.interviewer, "_first_question", "") or "",
            "finished": self.interviewer.is_finished,
            "turn_count": self.interviewer.turn_count,
            "finish_message": None,
        }

    def close(self) -> None:
        """Cleanly close handler and ensure assets are persisted if finished."""
        if hasattr(self, "interviewer") and self.interviewer and self.interviewer.is_finished:
            if self.interviewer.session and not self.interviewer.session.session_completed:
                try:
                    self.interviewer.session.end_session()
                except Exception:
                    pass

    def resume(self, case_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Check whether session can be resumed. SparkMe does not support cross-process resume."""
        raise RuntimeError(
            "SparkMe session is maintained in-memory and cannot be losslessly resumed "
            "after worker process termination. Mark run as interrupted."
        )
