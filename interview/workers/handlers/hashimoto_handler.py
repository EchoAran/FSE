"""Worker handler for the Hashimoto dynamic slot requirements interview baseline."""

from pathlib import Path
from typing import Any, Dict, Optional

from interview.workers.handlers.base_handler import BaseMethodHandler


class HashimotoHandler(BaseMethodHandler):
    """Executes Hashimoto baseline inside the isolated worker subprocess."""

    def __init__(
        self,
        config_path: Path,
        native_dir: Path,
        method_root: Path,
    ) -> None:
        from src.config import InterviewConfig
        from src.interviewer import HashimotoInterviewer
        from src.project_store import ProjectStore

        self.method_root = method_root
        self.native_dir = native_dir
        self.config_path = config_path

        self.config = InterviewConfig.from_yaml(config_path)
        self.config.runs_dir = str(native_dir)

        if not Path(self.config.initial_slots_path).is_absolute():
            self.config.initial_slots_path = str(self.method_root / self.config.initial_slots_path)
        if not Path(self.config.prompts_dir).is_absolute():
            self.config.prompts_dir = str(self.method_root / self.config.prompts_dir)

        self.store = ProjectStore(base_runs_dir=self.config.runs_dir)
        self.interviewer = HashimotoInterviewer(config=self.config)
        self.case_id: Optional[str] = None

    def start(self, case_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize project and generate the initial opening question."""
        from src.models import RequirementCase

        self.case_id = case_payload["case_id"]
        self.store.init_project_dir(self.case_id, case_payload)

        case = RequirementCase(
            case_id=self.case_id,
            project_name=case_payload["project_name"],
            initial_requirements=case_payload["initial_requirements"],
        )
        self.interviewer.initialize(case)
        first_q = self.interviewer.get_first_question()

        self.store.save_initial_state(self.interviewer.export_checkpoint())
        self.store.save_transcript(self.interviewer.export_transcript())

        return {
            "native_project_id": self.case_id,
            "question": first_q,
            "finished": self.interviewer.is_finished,
            "turn_count": self.interviewer.turn_count,
            "finish_message": None,
        }

    def submit_answer(self, answer: str) -> Dict[str, Any]:
        """Submit stakeholder answer and return the next question."""
        next_q = self.interviewer.step(answer)
        checkpoint = self.interviewer.export_checkpoint()
        transcript = self.interviewer.export_transcript()

        self.store.save_state(checkpoint)
        self.store.save_transcript(transcript)

        finish_message = None
        if self.interviewer.is_finished:
            finish_message = "Hashimoto interview completed (turn limit or slot fill rate reached)."

        return {
            "native_project_id": self.case_id or "",
            "question": next_q,
            "finished": self.interviewer.is_finished,
            "turn_count": self.interviewer.turn_count,
            "finish_message": finish_message,
        }

    def inspect(self) -> Dict[str, Any]:
        """Inspect current status without stepping."""
        pending_q = getattr(self.interviewer, "_pending_interviewer_utterance", "") or ""
        return {
            "native_project_id": self.case_id or "",
            "question": pending_q,
            "finished": self.interviewer.is_finished,
            "turn_count": self.interviewer.turn_count,
            "finish_message": None,
        }

    def resume(self, case_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Resume session from persisted checkpoint."""
        self.case_id = case_payload["case_id"]
        if not self.store.project_exists(self.case_id):
            raise FileNotFoundError(f"Cannot resume: project state not found for {self.case_id}")

        checkpoint = self.store.load_state(self.case_id)
        if checkpoint.is_finished:
            return {
                "native_project_id": self.case_id,
                "question": "",
                "finished": True,
                "turn_count": len(checkpoint.turns),
                "finish_message": "Hashimoto interview already completed.",
            }

        self.interviewer.resume_from_checkpoint(checkpoint)
        pending_q = getattr(self.interviewer, "_pending_interviewer_utterance", "") or ""

        return {
            "native_project_id": self.case_id,
            "question": pending_q,
            "finished": self.interviewer.is_finished,
            "turn_count": self.interviewer.turn_count,
            "finish_message": None,
        }
