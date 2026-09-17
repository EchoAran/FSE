"""Prompt and slot configuration loader with package-root awareness."""

from pathlib import Path
from typing import Any
import yaml
from src.models import Slot


class PromptLoader:
    """Loads prompt templates and initial slot definitions with robust path resolution."""

    def __init__(self, base_path: str | Path | None = None) -> None:
        """Initialize loader with explicit base path or default to package root."""
        if base_path:
            self._base_path = Path(base_path).resolve()
        else:
            self._base_path = Path(__file__).resolve().parent.parent.parent

    def resolve_path(self, relative_or_absolute_path: str | Path) -> Path:
        """Resolve a path against cwd first, then falling back to package root."""
        target = Path(relative_or_absolute_path)
        if target.is_absolute():
            return target

        cwd_candidate = (Path.cwd() / target).resolve()
        package_candidate = (self._base_path / target).resolve()

        if cwd_candidate.exists():
            return cwd_candidate
        if package_candidate.exists():
            return package_candidate

        return cwd_candidate

    def load_prompt(self, prompt_filename: str, prompts_dir: str = "prompts") -> str:
        """Load text content of a prompt template."""
        target_path = Path(prompts_dir) / prompt_filename
        resolved = self.resolve_path(target_path)
        if not resolved.is_file():
            raise FileNotFoundError(f"Prompt template file not found at: {resolved}")
        return resolved.read_text(encoding="utf-8").strip()

    def load_initial_slots(self, slots_path: str = "config/re_initial_slots.yaml") -> list[Slot]:
        """Load initial slot definitions from a YAML configuration file."""
        resolved = self.resolve_path(slots_path)
        if not resolved.is_file():
            raise FileNotFoundError(f"Initial slots file not found at: {resolved}")

        with resolved.open("r", encoding="utf-8") as f:
            data: dict[str, Any] = yaml.safe_load(f) or {}

        slots_list = data.get("slots", [])
        return [Slot(**slot_data) for slot_data in slots_list]
