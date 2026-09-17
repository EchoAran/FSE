"""Utilities for structured JSON serialization, deserialization, and persistence of transcripts and checkpoints."""

import json
from pathlib import Path
from src.models import InterviewCheckpoint, InterviewTranscript


class TranscriptExporter:
    """Handles structured serialization and deserialization of public transcripts and internal checkpoints."""

    @staticmethod
    def to_dict(data_model: InterviewTranscript | InterviewCheckpoint) -> dict:
        """Convert a transcript or checkpoint instance into a dictionary."""
        return data_model.model_dump()

    @staticmethod
    def to_json(data_model: InterviewTranscript | InterviewCheckpoint, indent: int = 2) -> str:
        """Serialize transcript or checkpoint into a formatted JSON string."""
        return json.dumps(TranscriptExporter.to_dict(data_model), ensure_ascii=False, indent=indent)

    @classmethod
    def load_transcript(cls, file_path: str | Path) -> InterviewTranscript:
        """Read and deserialize an InterviewTranscript from a JSON file."""
        target = Path(file_path)
        if not target.is_file():
            raise FileNotFoundError(f"Transcript file not found at: {target}")

        with target.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return InterviewTranscript.model_validate(data)

    @classmethod
    def load_checkpoint(cls, file_path: str | Path) -> InterviewCheckpoint:
        """Read and deserialize an InterviewCheckpoint from a JSON file."""
        target = Path(file_path)
        if not target.is_file():
            raise FileNotFoundError(f"Checkpoint file not found at: {target}")

        with target.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return InterviewCheckpoint.model_validate(data)

    @classmethod
    def save_transcript(cls, transcript: InterviewTranscript, output_path: str | Path) -> Path:
        """Write a clean public InterviewTranscript to the destination JSON file."""
        dest = Path(output_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(cls.to_json(transcript), encoding="utf-8")
        return dest

    @classmethod
    def save_checkpoint(cls, checkpoint: InterviewCheckpoint, output_path: str | Path) -> Path:
        """Write an internal InterviewCheckpoint to the destination JSON file."""
        dest = Path(output_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(cls.to_json(checkpoint), encoding="utf-8")
        return dest
