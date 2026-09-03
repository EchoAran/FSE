"""Unit tests verifying 100% lossless checkpoint saving, loading, and session restoration."""

from pathlib import Path
import pytest
from src.config import InterviewConfig
from src.interviewer import HashimotoInterviewer
from src.models import RequirementCase
from src.transcript import TranscriptExporter
from tests.mock_client import MockLLMClient


@pytest.fixture
def sample_case() -> RequirementCase:
    """Provide a sample requirement case fixture."""
    return RequirementCase(
        case_id="CLINIC-001",
        project_name="Smart Clinic Management",
        initial_requirements="Cloud-based clinic workflow with appointment booking and EMR.",
    )


def test_lossless_checkpoint_save_load_and_resume(
    sample_case: RequirementCase,
    tmp_path: Path,
) -> None:
    """Verify that checkpoint restoration restores slots, abduction history, and pending question with 0 LLM calls."""
    mock_client = MockLLMClient()
    interviewer = HashimotoInterviewer(
        config=InterviewConfig(model="mock-gpt", max_turns=5),
        llm_client=mock_client,
    )
    interviewer.initialize(sample_case)

    # 1. Run turn 1
    interviewer.get_first_question()
    q1 = interviewer.step("We need real-time appointment booking.")
    assert q1 != ""

    # 2. Export public transcript and internal checkpoint
    transcript = interviewer.export_transcript()
    checkpoint = interviewer.export_checkpoint()

    # Public transcript contains only clean conversation turns
    assert transcript.case_id == "CLINIC-001"
    assert len(transcript.turns) == 1
    assert not hasattr(transcript, "slots") or "slots" not in transcript.model_dump()

    # Checkpoint contains full execution state
    assert checkpoint.initial_requirements == sample_case.initial_requirements
    assert "telehealth_video_integration" in [s.name for s in checkpoint.slots]
    assert len(checkpoint.abduction_history) == 1
    assert checkpoint.pending_question == q1
    assert checkpoint.is_finished is False

    # 3. Save to JSON and Load back
    checkpoint_file = tmp_path / "hashimoto_checkpoint.json"
    TranscriptExporter.save_checkpoint(checkpoint, checkpoint_file)
    loaded_checkpoint = TranscriptExporter.load_checkpoint(checkpoint_file)

    # 4. Resume in fresh interviewer with empty mock client
    resumed_client = MockLLMClient(auto_pipeline=False)
    resumed_interviewer = HashimotoInterviewer(
        config=InterviewConfig(model="mock-gpt", max_turns=5),
        llm_client=resumed_client,
    )

    # Restore session without passing case explicitly
    resumed_interviewer.resume_from_checkpoint(loaded_checkpoint)

    # Verify ZERO LLM calls were made during restoration
    assert len(resumed_client.call_history) == 0

    # Verify state, slots, abduction history, and pending question are losslessly restored
    assert resumed_interviewer.turn_count == 1
    assert resumed_interviewer.is_finished is False
    assert resumed_interviewer.get_first_question() == q1
    assert "telehealth_video_integration" in resumed_interviewer.slots
    assert "offline_sync_protocol" in resumed_interviewer.slots
    assert len(resumed_interviewer.abduction_history) == 1
    assert resumed_interviewer.abduction_history[0].new_slot == "offline_sync_protocol"

    # 5. Continue with step() on the resumed instance
    resumed_client.auto_pipeline = True
    q2 = resumed_interviewer.step("Medical records must be encrypted end-to-end.")
    assert q2 != ""
    assert resumed_interviewer.turn_count == 2
