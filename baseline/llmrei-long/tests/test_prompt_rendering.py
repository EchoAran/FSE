"""Unit tests for prompt loading, path resolution, and context rendering."""

from pathlib import Path
import pytest
from src.models import RequirementCase
from src.prompt.loader import PromptLoader
from src.prompt.renderer import PromptRenderer


def test_verbatim_prompt_file_size() -> None:
    """Assert that vendor/long_prompt.txt exactly matches the official 5660 bytes."""
    vendor_prompt = Path(__file__).resolve().parent.parent / "vendor" / "long_prompt.txt"
    assert vendor_prompt.is_file()
    assert vendor_prompt.stat().st_size == 5660


def test_prompt_loader_reads_official_prompt() -> None:
    """Verify that PromptLoader correctly reads the official long prompt file."""
    loader = PromptLoader()
    content = loader.load("vendor/long_prompt.txt")

    assert "You are an interviewer, called GPTREI" in content
    assert "ALWAYS ask only one question!" in content
    assert "Interview Cookbook:" in content


def test_prompt_loader_from_arbitrary_base_path() -> None:
    """Verify that PromptLoader resolves relative paths even when base_path changes."""
    parent_dir = Path(__file__).resolve().parent.parent.parent
    loader = PromptLoader(base_path=parent_dir)
    content = loader.load("vendor/long_prompt.txt")
    assert "You are an interviewer, called GPTREI" in content


def test_prompt_loader_missing_file_raises_error() -> None:
    """Verify that PromptLoader raises FileNotFoundError for non-existent paths."""
    loader = PromptLoader()
    with pytest.raises(FileNotFoundError):
        loader.load("non_existent_prompt_path.txt")


def test_prompt_renderer_integrates_case() -> None:
    """Verify that PromptRenderer properly embeds case requirements."""
    base_prompt = "You are GPTREI, a requirements interviewer."
    case = RequirementCase(
        case_id="TEST-001",
        project_name="Inventory Tracker",
        initial_requirements="The system must track stock levels in real time.",
    )

    rendered = PromptRenderer.render(base_prompt, case)

    assert "Project Name: Inventory Tracker" in rendered
    assert "The system must track stock levels in real time." in rendered
    assert rendered.startswith("You are GPTREI")
