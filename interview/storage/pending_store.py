"""Store for transient pending_answer.json during interview turn transitions."""

import json
from pathlib import Path
from typing import Optional

from interview.storage.models import PendingAnswer


class PendingAnswerStore:
    """Manages writing, reading, and clearing uncommitted stakeholder answers without timestamps."""

    FILENAME = "pending_answer.json"

    @classmethod
    def get_path(cls, results_dir: Path) -> Path:
        """Return path to pending_answer.json."""
        return results_dir / cls.FILENAME

    @classmethod
    def exists(cls, results_dir: Path) -> bool:
        """Check if pending_answer.json exists."""
        return cls.get_path(results_dir).is_file()

    @classmethod
    def save(cls, results_dir: Path, pending: PendingAnswer) -> None:
        """Atomically persist pending answer."""
        results_dir.mkdir(parents=True, exist_ok=True)
        target_path = cls.get_path(results_dir)
        temp_path = results_dir / f"{cls.FILENAME}.tmp"

        with temp_path.open("w", encoding="utf-8") as f:
            json.dump(pending.to_dict(), f, ensure_ascii=False, indent=2)

        temp_path.replace(target_path)

    @classmethod
    def load(cls, results_dir: Path) -> Optional[PendingAnswer]:
        """Load pending answer if file exists."""
        target_path = cls.get_path(results_dir)
        if not target_path.is_file():
            return None

        with target_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return PendingAnswer.from_dict(data)

    @classmethod
    def delete(cls, results_dir: Path) -> None:
        """Remove pending_answer.json if present."""
        target_path = cls.get_path(results_dir)
        if target_path.is_file():
            target_path.unlink()
