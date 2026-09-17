"""Project storage and artifact manager for Hashimoto Dynamic Slot + Abduction."""

import json
from pathlib import Path
from typing import Any
import uuid

from src.models import InterviewCheckpoint, InterviewTranscript, RequirementCase, Slot
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

    def save_initial_state(self, checkpoint: InterviewCheckpoint) -> None:
        """Save initial checkpoint right after project creation."""
        project_dir = self.get_project_dir(checkpoint.case_id)
        project_dir.mkdir(parents=True, exist_ok=True)
        TranscriptExporter.save_checkpoint(checkpoint, project_dir / "state.initial.json")
        TranscriptExporter.save_checkpoint(checkpoint, project_dir / "state.json")

    def save_state(self, checkpoint: InterviewCheckpoint) -> None:
        """Atomically persist current checkpoint to state.json."""
        project_dir = self.get_project_dir(checkpoint.case_id)
        project_dir.mkdir(parents=True, exist_ok=True)

        target_file = project_dir / "state.json"
        temp_file = project_dir / f"state.json.{uuid.uuid4().hex[:8]}.tmp"
        TranscriptExporter.save_checkpoint(checkpoint, temp_file)
        temp_file.replace(target_file)

    def load_state(self, project_id: str) -> InterviewCheckpoint:
        """Load latest checkpoint from state.json."""
        target_file = self.get_project_dir(project_id) / "state.json"
        if not target_file.is_file():
            raise FileNotFoundError(f"State file not found for project: {project_id}")
        return TranscriptExporter.load_checkpoint(target_file)

    def save_transcript(self, transcript: InterviewTranscript) -> Path:
        """Save clean public transcript to transcript.json."""
        project_dir = self.get_project_dir(transcript.case_id)
        project_dir.mkdir(parents=True, exist_ok=True)
        return TranscriptExporter.save_transcript(transcript, project_dir / "transcript.json")

    def load_transcript(self, project_id: str) -> InterviewTranscript:
        """Load clean transcript from transcript.json."""
        target_file = self.get_project_dir(project_id) / "transcript.json"
        if not target_file.is_file():
            raise FileNotFoundError(f"Transcript file not found for project: {project_id}")
        return TranscriptExporter.load_transcript(target_file)

    def save_final_artifacts(
        self,
        checkpoint: InterviewCheckpoint,
        transcript: InterviewTranscript,
    ) -> tuple[Path, Path, Path]:
        """Save final_state.json, transcript.json, and generate summary.md."""
        project_dir = self.get_project_dir(checkpoint.case_id)
        project_dir.mkdir(parents=True, exist_ok=True)

        final_state_path = project_dir / "final_state.json"
        TranscriptExporter.save_checkpoint(checkpoint, final_state_path)

        transcript_path = project_dir / "transcript.json"
        TranscriptExporter.save_transcript(transcript, transcript_path)

        summary_path = project_dir / "summary.md"
        summary_content = self.generate_summary_markdown(checkpoint)
        summary_path.write_text(summary_content, encoding="utf-8")

        return final_state_path, transcript_path, summary_path

    @staticmethod
    def generate_summary_markdown(checkpoint: InterviewCheckpoint) -> str:
        """Generate a structured Markdown specification report from checkpoint."""
        total_slots = len(checkpoint.slots)
        filled_slots = sum(1 for s in checkpoint.slots if s.is_filled)
        fill_rate = (filled_slots / total_slots) if total_slots > 0 else 0.0

        lines: list[str] = []
        lines.append(f"# Requirements Specification & Interview Summary: {checkpoint.project_name}")
        lines.append("")
        lines.append(f"- **Project ID / Case ID**: `{checkpoint.case_id}`")
        lines.append(f"- **Total Turns Completed**: {len(checkpoint.turns)}")
        lines.append(f"- **Slot Completion Rate**: {filled_slots}/{total_slots} ({fill_rate:.1%})")
        lines.append(f"- **Interview Status**: {'Completed' if checkpoint.is_finished else 'In Progress'}")
        lines.append("")
        lines.append("## 1. Initial Requirements Context")
        lines.append("")
        lines.append(checkpoint.initial_requirements.strip() or "*(No initial requirements text provided)*")
        lines.append("")
        lines.append("## 2. Elicited Requirement Slots")
        lines.append("")
        lines.append("| Category | Slot Name | Status | Extracted Value |")
        lines.append("|---|---|---|---|")
        for slot in sorted(checkpoint.slots, key=lambda s: (s.category, s.name)):
            status = "Filled" if slot.is_filled else "Unfilled"
            val = slot.value.replace("\n", " ") if slot.value else "—"
            lines.append(f"| {slot.category} | {slot.name} | {status} | {val} |")
        lines.append("")

        if checkpoint.abduction_history:
            lines.append("## 3. Abductive Reasoning History")
            lines.append("")
            lines.append("| # | Surprising Fact | Suspected Reason / Implicit Need | Probe Slot |")
            lines.append("|---|---|---|---|")
            for idx, rec in enumerate(checkpoint.abduction_history, 1):
                fact = rec.surprising_fact.replace("\n", " ")
                reason = rec.suspected_reason.replace("\n", " ")
                lines.append(f"| {idx} | {fact} | {reason} | `{rec.new_slot}` |")
            lines.append("")

        lines.append("## 4. Full Interview Transcript")
        lines.append("")
        for turn in checkpoint.turns:
            lines.append(f"### Turn {turn.turn_id}")
            if turn.target_slots:
                targets = ", ".join(f"`{s}`" for s in turn.target_slots)
                lines.append(f"*Target Slots*: {targets}")
                lines.append("")
            lines.append(f"**Interviewer**: {turn.interviewer_utterance}")
            lines.append("")
            lines.append(f"**Stakeholder**: {turn.interviewee_utterance}")
            lines.append("")

        return "\n".join(lines)
