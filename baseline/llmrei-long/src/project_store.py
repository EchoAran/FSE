"""Project storage and artifact manager for LLMREI-long."""

import json
from pathlib import Path
from typing import Any
import uuid

from src.models import InterviewTranscript, RequirementCase
from src.transcript import TranscriptExporter


class ProjectStore:
    """Manages project persistence on disk under run_id folders, ensuring clean serialization and recovery."""

    def __init__(self, base_runs_dir: Path | str = "runs") -> None:
        self.base_runs_dir = Path(base_runs_dir)

    def get_project_dir(self, project_id: str) -> Path:
        """Return the directory path for a given project ID."""
        return self.base_runs_dir / project_id

    def project_exists(self, project_id: str) -> bool:
        """Check whether the project directory and state file exist."""
        return (self.get_project_dir(project_id) / "state.json").is_file()

    def init_project_dir(self, project_id: str, input_payload: dict[str, Any]) -> Path:
        """Create project directory and write input.json."""
        project_dir = self.get_project_dir(project_id)
        project_dir.mkdir(parents=True, exist_ok=True)

        input_file = project_dir / "input.json"
        with input_file.open("w", encoding="utf-8") as f:
            json.dump(input_payload, f, ensure_ascii=False, indent=2)

        return project_dir

    def load_input(self, project_id: str) -> dict[str, Any]:
        """Load original input payload."""
        input_file = self.get_project_dir(project_id) / "input.json"
        if not input_file.is_file():
            raise FileNotFoundError(f"Input file not found for project: {project_id}")
        with input_file.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save_initial_state(self, transcript: InterviewTranscript) -> None:
        """Save initial transcript right after project creation."""
        project_dir = self.get_project_dir(transcript.case_id)
        project_dir.mkdir(parents=True, exist_ok=True)
        TranscriptExporter.save_json(transcript, project_dir / "state.initial.json")
        TranscriptExporter.save_json(transcript, project_dir / "state.json")

    def save_state(self, transcript: InterviewTranscript) -> None:
        """Atomically persist current transcript to state.json."""
        project_dir = self.get_project_dir(transcript.case_id)
        project_dir.mkdir(parents=True, exist_ok=True)

        target_file = project_dir / "state.json"
        temp_file = project_dir / f"state.json.{uuid.uuid4().hex[:8]}.tmp"
        TranscriptExporter.save_json(transcript, temp_file)
        temp_file.replace(target_file)

    def load_state(self, project_id: str) -> InterviewTranscript:
        """Load latest transcript from state.json."""
        target_file = self.get_project_dir(project_id) / "state.json"
        if not target_file.is_file():
            raise FileNotFoundError(f"State file not found for project: {project_id}")
        return TranscriptExporter.load_json(target_file)

    def save_transcript(self, transcript: InterviewTranscript) -> Path:
        """Save transcript to transcript.json."""
        project_dir = self.get_project_dir(transcript.case_id)
        project_dir.mkdir(parents=True, exist_ok=True)
        return TranscriptExporter.save_json(transcript, project_dir / "transcript.json")

    def load_transcript(self, project_id: str) -> InterviewTranscript:
        """Load transcript from transcript.json."""
        target_file = self.get_project_dir(project_id) / "transcript.json"
        if not target_file.is_file():
            raise FileNotFoundError(f"Transcript file not found for project: {project_id}")
        return TranscriptExporter.load_json(target_file)
