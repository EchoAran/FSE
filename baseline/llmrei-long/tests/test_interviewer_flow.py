"""End-to-end conversational flow, error atomicity, and lossless session restoration tests."""

from pathlib import Path
import pytest
from src.config import InterviewConfig
from src.interviewer import LLMREIInterviewer
from src.models import RequirementCase
from src.prompt.loader import PromptLoader
from src.transcript import TranscriptExporter
from tests.mock_client import MockLLMClient


@pytest.fixture
def sample_case() -> RequirementCase:
    """Provide a sample requirement case fixture."""
    return RequirementCase(
        case_id="CLINIC-01",
        project_name="Smart Clinic Management",
        initial_requirements="Doctors need an automated patient queue and medical record system.",
    )


@pytest.fixture
def configured_interviewer(sample_case: RequirementCase) -> LLMREIInterviewer:
    """Provide a configured interviewer instance backed by a mock client."""
    config = InterviewConfig(
        model="mock-gpt",
        max_turns=3,
        prompt_path="vendor/long_prompt.txt",
    )
    mock_responses = [
        "Hello! I'm GPTREI. Are you in line with the scope of this interview?",
        "Could you describe the main patient queue challenges?",
        "How should emergency cases be prioritized?",
        "Thank you, that concludes our requirements elicitation session.",
    ]
    mock_client = MockLLMClient(scripted_responses=mock_responses)
    loader = PromptLoader()

    interviewer = LLMREIInterviewer(
        config=config,
        llm_client=mock_client,
        prompt_loader=loader,
    )
    interviewer.initialize(sample_case)
    return interviewer


def test_interviewer_initial_state(configured_interviewer: LLMREIInterviewer) -> None:
    """Verify interviewer initialization flags and turn count."""
    assert configured_interviewer.is_initialized is True
    assert configured_interviewer.is_finished is False
    assert configured_interviewer.turn_count == 0


def test_interviewer_multi_turn_flow(configured_interviewer: LLMREIInterviewer) -> None:
    """Execute a 3-turn simulated interview and verify conversational progression."""
    first_q = configured_interviewer.get_first_question()
    assert "Hello! I'm GPTREI" in first_q
    assert configured_interviewer.turn_count == 0

    q1 = configured_interviewer.step("Yes, I am ready to discuss the clinic requirements.")
    assert "main patient queue challenges" in q1
    assert configured_interviewer.turn_count == 1

    q2 = configured_interviewer.step("Patients currently wait too long during morning peak hours.")
    assert "emergency cases" in q2
    assert configured_interviewer.turn_count == 2

    # Step 3 reaches max_turns limit (max_turns=3)
    final_resp = configured_interviewer.step("Emergency cases must immediately bypass the standard queue.")
    assert configured_interviewer.turn_count == 3
    assert configured_interviewer.is_finished is True
    assert final_resp == ""


def test_step_failure_atomicity_and_retry(sample_case: RequirementCase) -> None:
    """Verify that an API error in step() leaves state unchanged and enables clean retry."""
    config = InterviewConfig(model="mock-gpt", max_turns=5)
    mock_client = MockLLMClient(
        scripted_responses=[
            "Hello! I am GPTREI.",
            "Follow-up question after successful retry.",
        ],
        fail_on_calls={2},
    )
    interviewer = LLMREIInterviewer(config=config, llm_client=mock_client)
    interviewer.initialize(sample_case)

    # Turn 0: initial question
    first_q = interviewer.get_first_question()
    assert first_q == "Hello! I am GPTREI."
    assert interviewer.turn_count == 0

    # Turn 1 attempt 1: fails
    with pytest.raises(RuntimeError, match="Simulated API failure on call #2"):
        interviewer.step("Answer encountering network drop.")

    # State remains uncorrupted
    assert interviewer.turn_count == 0
    assert interviewer.is_finished is False
    assert interviewer.export_transcript().turns == []

    # Turn 1 attempt 2: retry succeeds
    retry_q = interviewer.step("Answer encountering network drop.")
    assert retry_q == "Follow-up question after successful retry."
    assert interviewer.turn_count == 1

    transcript = interviewer.export_transcript()
    assert len(transcript.turns) == 1
    assert transcript.turns[0].turn_id == 1
    assert transcript.turns[0].interviewee_utterance == "Answer encountering network drop."
    assert transcript.turns[0].interviewer_utterance == "Hello! I am GPTREI."


def test_lossless_transcript_save_load_and_resume(
    sample_case: RequirementCase,
    tmp_path: Path,
) -> None:
    """Verify that session resumption restores context and pending question with zero extra LLM calls."""
    mock_client = MockLLMClient(
        scripted_responses=[
            "Hello! I am GPTREI. Ready to discuss requirements?",
            "What features should the patient portal include?",
            "How should doctors view patient history?",
        ]
    )
    interviewer = LLMREIInterviewer(
        config=InterviewConfig(model="mock-gpt", max_turns=5),
        llm_client=mock_client,
    )
    interviewer.initialize(sample_case)

    first_q = interviewer.get_first_question()
    q1 = interviewer.step("We need a self-service patient appointment portal.")
    assert q1 == "What features should the patient portal include?"

    # 1. Export transcript midway (1 completed turn, pending question displayed)
    transcript = interviewer.export_transcript()
    assert transcript.initial_requirements == sample_case.initial_requirements
    assert transcript.pending_question == "What features should the patient portal include?"
    assert transcript.is_finished is False

    json_path = tmp_path / "midway_transcript.json"
    TranscriptExporter.save_json(transcript, json_path)

    # 2. Load from JSON
    loaded_transcript = TranscriptExporter.load_json(json_path)

    # 3. Resume in a fresh interviewer with a tracking mock client
    resumed_client = MockLLMClient(
        scripted_responses=["How should doctors view patient history?"]
    )
    resumed_interviewer = LLMREIInterviewer(
        config=InterviewConfig(model="mock-gpt", max_turns=5),
        llm_client=resumed_client,
    )

    # Resume session without passing case explicitly
    resumed_interviewer.resume_from_transcript(loaded_transcript)

    # Verify ZERO LLM calls were made during resumption
    assert len(resumed_client.call_history) == 0

    # Verify context and pending question are losslessly restored
    assert resumed_interviewer.turn_count == 1
    assert resumed_interviewer.is_finished is False
    assert resumed_interviewer.get_first_question() == "What features should the patient portal include?"
    assert "Doctors need an automated patient queue" in resumed_interviewer.system_prompt

    # 4. Continue next turn seamlessly
    q2 = resumed_interviewer.step("Appointment scheduling, medical test results, and doctor messaging.")
    assert q2 == "How should doctors view patient history?"
    assert resumed_interviewer.turn_count == 2
    assert len(resumed_client.call_history) == 1
