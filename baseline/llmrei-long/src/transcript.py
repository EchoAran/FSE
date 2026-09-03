"""Utilities for serializing, deserializing, and persisting interview transcripts."""

import json
from pathlib import Path
from src.models import InterviewTranscript


class TranscriptExporter:
    """Handles structured serialization and deserialization of interview transcripts."""

    @staticmethod
    def to_dict(transcript: InterviewTranscript) -> dict:
        """Convert an InterviewTranscript instance into a dictionary."""
        return transcript.model_dump()

    @staticmethod
    def from_dict(data: dict) -> InterviewTranscript:
        """Construct an InterviewTranscript instance from a dictionary."""
        return InterviewTranscript.model_validate(data)

    @staticmethod
    def to_json(transcript: InterviewTranscript, indent: int = 2) -> str:
        """Serialize transcript into a formatted JSON string."""
        return json.dumps(TranscriptExporter.to_dict(transcript), ensure_ascii=False, indent=indent)

    @classmethod
    def load_json(cls, file_path: str | Path) -> InterviewTranscript:
        """Read and deserialize an InterviewTranscript from a JSON file."""
        target = Path(file_path)
        if not target.is_file():
            raise FileNotFoundError(f"Transcript file not found at: {target}")

        with target.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return cls.from_dict(data)

    @classmethod
    def save_json(cls, transcript: InterviewTranscript, output_path: str | Path) -> Path:
        """Write an InterviewTranscript to the specified destination path as JSON."""
        dest = Path(output_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(cls.to_json(transcript), encoding="utf-8")
        return dest
