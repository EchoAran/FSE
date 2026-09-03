"""Public transcript serialization and persistence utility."""

import json
from pathlib import Path
from src.models import InterviewTranscript


class TranscriptExporter:
    """Handles exporting and loading public interview transcripts to/from JSON."""

    @staticmethod
    def save_transcript(transcript: InterviewTranscript, file_path: str | Path) -> None:
        """Save a public InterviewTranscript instance to a JSON file."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(transcript.model_dump(), f, indent=2, ensure_ascii=False)

    @staticmethod
    def load_transcript(file_path: str | Path) -> InterviewTranscript:
        """Load an InterviewTranscript instance from a JSON file."""
        path = Path(file_path)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return InterviewTranscript(**data)
