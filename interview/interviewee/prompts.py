"""Prompt template loader and renderer for the interviewee agent."""

from pathlib import Path
from typing import Optional, Union

from interview.cases.models import CaseRecord

DEFAULT_PROMPT_TEMPLATE_PATH = Path(__file__).resolve().parent / "prompt.txt"


def load_prompt_template(template_path: Optional[Union[str, Path]] = None) -> str:
    """Load the raw text prompt template from file."""
    path = Path(template_path) if template_path else DEFAULT_PROMPT_TEMPLATE_PATH
    if not path.is_file():
        raise FileNotFoundError(f"Interviewee prompt template file not found: {path}")
    return path.read_text(encoding="utf-8")


def build_system_prompt(
    case: CaseRecord,
    template_path: Optional[Union[str, Path]] = None,
) -> str:
    """Render the prompt.txt template with case project name and initial requirements."""
    template = load_prompt_template(template_path)
    return template.format(
        project_name=case.project_name,
        initial_requirements=case.initial_requirements,
    )
