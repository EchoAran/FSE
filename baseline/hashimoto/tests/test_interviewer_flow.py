"""End-to-end interview flow, threshold termination, and error atomicity tests."""

import json
import pytest
from src.config import InterviewConfig
from src.interviewer import HashimotoInterviewer
from src.models import RequirementCase
from tests.mock_client import MockLLMClient


@pytest.fixture
def sample_case() -> RequirementCase:
    """Provide a sample software requirement case fixture."""
    return RequirementCase(
        case_id="CLINIC-001",
        project_name="Smart Clinic Management",
        initial_requirements="Cloud-based clinic workflow with appointment booking and EMR.",
    )


def test_interviewer_initial_state(sample_case: RequirementCase) -> None:
    """Verify initialization of standard RE slots and clean starting state."""
    mock_client = MockLLMClient()
    interviewer = HashimotoInterviewer(
        config=InterviewConfig(model="mock-gpt"),
        llm_client=mock_client,
    )
    interviewer.initialize(sample_case)

    assert interviewer.is_initialized is True
    assert interviewer.is_finished is False
    assert interviewer.turn_count == 0
    assert len(interviewer.slots) == 8
    assert "project_goals" in interviewer.slots
    assert "boundary_conditions" in interviewer.slots
    assert interviewer.fill_rate == 0.0


def test_interviewer_multi_turn_pipeline_execution(sample_case: RequirementCase) -> None:
    """Execute multi-turn interview and verify dynamic slots and abduction history accumulation."""
    mock_client = MockLLMClient()
    interviewer = HashimotoInterviewer(
        config=InterviewConfig(model="mock-gpt", max_turns=3),
        llm_client=mock_client,
    )
    interviewer.initialize(sample_case)

    q0 = interviewer.get_first_question()
    assert "Could you elaborate" in q0 or "offline" in q0
    assert interviewer.turn_count == 0

    # Turn 1
    q1 = interviewer.step("We need web and mobile appointment booking.")
    assert interviewer.turn_count == 1
    assert "telehealth_video_integration" in interviewer.slots
    assert "offline_sync_protocol" in interviewer.slots
    assert len(interviewer.abduction_history) == 1

    # Turn 2
    q2 = interviewer.step("Doctors will access patient records on tablets.")
    assert interviewer.turn_count == 2
    assert interviewer.is_finished is False

    # Turn 3 reaches max_turns (3)
    final_q = interviewer.step("Prescriptions should be sent directly to the local pharmacy.")
    assert interviewer.turn_count == 3
    assert interviewer.is_finished is True
    assert final_q == ""


def test_step_failure_atomicity_and_clean_retry(sample_case: RequirementCase) -> None:
    """Verify that an API exception in step() preserves slot state and enables clean retry."""
    mock_client = MockLLMClient(fail_on_calls={2})
    interviewer = HashimotoInterviewer(
        config=InterviewConfig(model="mock-gpt", max_turns=5),
        llm_client=mock_client,
    )
    interviewer.initialize(sample_case)

    first_q = interviewer.get_first_question()
    assert first_q != ""
    assert interviewer.turn_count == 0

    # Step attempt 1 raises exception in Stage 1
    with pytest.raises(RuntimeError, match="Simulated API failure on call #2"):
        interviewer.step("Answer that encounters network drop.")

    # State must be completely intact
    assert interviewer.turn_count == 0
    assert interviewer.is_finished is False
    assert len(interviewer.abduction_history) == 0
    assert interviewer.fill_rate == 0.0
    assert interviewer.export_transcript().turns == []

    # Retry step
    retry_q = interviewer.step("Answer that encounters network drop.")
    assert retry_q != ""
    assert interviewer.turn_count == 1

    transcript = interviewer.export_transcript()
    assert len(transcript.turns) == 1
    assert transcript.turns[0].turn_id == 1
    assert transcript.turns[0].interviewee_utterance == "Answer that encounters network drop."
