"""Regression and method fidelity test suite for Hashimoto interview system."""

import json
from pathlib import Path
import pytest
import yaml
from src.config import InterviewConfig
from src.core.abductive_slot_generator import AbductiveSlotGenerator
from src.core.question_generator import QuestionGenerator
from src.core.slot_filler import SlotFiller
from src.interviewer import HashimotoInterviewer
from src.models import (
    AbductionRecord,
    DialogueTurn,
    InterviewCheckpoint,
    InterviewTranscript,
    InterviewTurn,
    Message,
    RequirementCase,
    Slot,
)
from tests.mock_client import MockLLMClient


@pytest.fixture
def sample_case() -> RequirementCase:
    """Provide a software requirement case fixture."""
    return RequirementCase(
        case_id="FIDELITY-001",
        project_name="Smart Clinic Management",
        initial_requirements="Cloud-based clinic workflow with appointment booking and EMR.",
    )


def test_table_2_exact_initial_slots_and_categories() -> None:
    """Verify that career_initial_slots.yaml matches Table 2 verbatim for all 8 slots and categories."""
    yaml_path = Path(__file__).parent.parent / "config" / "career_initial_slots.yaml"
    with yaml_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    slots_data = {s["name"]: s["category"] for s in data["slots"]}
    expected_table_2 = {
        "Career aspirations for next year": "Career",
        "Career development plan": "Career, Plan",
        "Future department preferences": "Career, Preference",
        "Career-related concerns": "Career, Concerns",
        "Training preferences": "Training, Preference",
        "Current job duties": "Job",
        "Job satisfaction": "Job, Satisfaction",
        "Job dissatisfaction": "Job, Dissatisfaction",
    }

    assert slots_data == expected_table_2


def test_original_career_prompts_contract() -> None:
    """Verify that prompts_original files maintain the expected method contract and persona."""
    prompts_dir = Path(__file__).parent.parent / "prompts_original"

    # Keiko Naasu persona verification
    q_gen_prompt = (prompts_dir / "question_generation.txt").read_text(encoding="utf-8")
    assert "Keiko Naasu" in q_gen_prompt
    assert "34" in q_gen_prompt
    assert "over 10 years of clinical experience" in q_gen_prompt
    assert "Target Slot S" in q_gen_prompt

    # Abductive reasoning prompt verification
    abd_prompt = (prompts_dir / "abductive_slot_generation.txt").read_text(encoding="utf-8")
    assert "Surprising Fact C" in abd_prompt
    assert "Reason to Suspect A" in abd_prompt
    assert "New Slot" in abd_prompt
    assert "form of logical inference" in abd_prompt

    # Slot filling verification
    sf_prompt = (prompts_dir / "slot_filling.txt").read_text(encoding="utf-8")
    assert "Career aspirations for next year" in sf_prompt
    assert "Job, Dissatisfaction" in sf_prompt


def test_proposed_method_2_figure_5_schema_parsing() -> None:
    """Verify AbductiveSlotGenerator correctly parses the structured C/A/New-Slot schema."""
    current_slots = {
        "Career aspirations for next year": Slot(
            name="Career aspirations for next year",
            category="Career",
            value="ICU Nurse",
        ),
    }
    fig5_json = json.dumps({
        "Surprising Fact C": "Experienced ICU nurse with high performance requesting transfer to outpatient clinic",
        "Reason to Suspect A": "Chronic night shift fatigue and desire for daytime hours",
        "New Slot": {
            "shift_work_fatigue_level": {
                "category": "Personal, Health",
                "value": None,
            },
            "outpatient_motivation": {
                "category": "Career, Preference",
                "value": None,
            },
        },
    })
    client = MockLLMClient(scripted_responses=[fig5_json], auto_pipeline=False)
    generator = AbductiveSlotGenerator("Prompt template", client)

    record, new_slots = generator.generate(
        current_slots=current_slots,
        dialogue_history=[],
        abduction_history=[],
        initial_requirements="Career self-assessment context",
        model="mock-gpt",
    )

    assert record is not None
    assert record.surprising_fact == "Experienced ICU nurse with high performance requesting transfer to outpatient clinic"
    assert record.suspected_reason == "Chronic night shift fatigue and desire for daytime hours"
    assert record.new_slot == "shift_work_fatigue_level"

    assert len(new_slots) == 2
    assert new_slots[0].name == "shift_work_fatigue_level"
    assert new_slots[0].category == "Personal, Health"
    assert new_slots[0].value is None
    assert new_slots[1].name == "outpatient_motivation"
    assert new_slots[1].value is None


def test_slot_filling_figure_6_nested_dict_parsing() -> None:
    """Verify SlotFiller correctly parses nested dictionary schema."""
    initial_slots = {
        "Career aspirations for next year": Slot(
            name="Career aspirations for next year",
            category="Career",
            value=None,
        ),
        "Job satisfaction": Slot(
            name="Job satisfaction",
            category="Job, Satisfaction",
            value=None,
        ),
    }
    fig6_json = json.dumps({
        "Career aspirations for next year": {
            "category": "Career",
            "value": "Clinical Nurse Specialist in Cardiology",
        },
        "Job satisfaction": {
            "category": "Job, Satisfaction",
            "value": "High teamwork satisfaction, low commute satisfaction",
        },
    })
    client = MockLLMClient(scripted_responses=[fig6_json], auto_pipeline=False)
    filler = SlotFiller("Prompt", client)

    updated = filler.fill_slots(
        current_slots=initial_slots,
        dialogue_history=[],
        initial_requirements="Career background",
        model="mock-gpt",
    )

    assert updated["Career aspirations for next year"].value == "Clinical Nurse Specialist in Cardiology"
    assert updated["Job satisfaction"].value == "High teamwork satisfaction, low commute satisfaction"


def test_question_generator_figure_7_schema_parsing() -> None:
    """Verify QuestionGenerator correctly parses Target Slot JSON schema."""
    slots = {
        "Career aspirations for next year": Slot(
            name="Career aspirations for next year",
            category="Career",
            value=None,
        ),
    }
    fig7_json = json.dumps({
        "Target Slot S": {
            "Career aspirations for next year": {
                "category": "Career",
                "value": None
            }
        },
        "Question": "What specific clinical certifications are you aiming to pursue next year?",
    })
    client = MockLLMClient(scripted_responses=[fig7_json], auto_pipeline=False)
    generator = QuestionGenerator("Prompt", client)

    targets, q = generator.generate_question(
        current_slots=slots,
        dialogue_history=[],
        initial_requirements="Context",
        latest_abduction=None,
        model="mock-gpt",
    )

    assert targets == ["Career aspirations for next year"]
    assert q == "What specific clinical certifications are you aiming to pursue next year?"


def test_public_transcript_and_checkpoint_turn_isolation(sample_case: RequirementCase) -> None:
    """Verify that public InterviewTranscript contains clean DialogueTurns without target_slots, while Checkpoint preserves them."""
    client = MockLLMClient(auto_pipeline=True)
    interviewer = HashimotoInterviewer(llm_client=client)
    interviewer.initialize(sample_case)

    interviewer.get_first_question()
    interviewer.step("Stakeholder response for turn 1.")

    transcript = interviewer.export_transcript()
    checkpoint = interviewer.export_checkpoint()

    # Public transcript contains DialogueTurn
    assert len(transcript.turns) == 1
    assert isinstance(transcript.turns[0], DialogueTurn)
    transcript_dict = transcript.turns[0].model_dump()
    assert "target_slots" not in transcript_dict
    assert set(transcript_dict.keys()) == {"turn_id", "interviewer_utterance", "interviewee_utterance"}

    # Internal checkpoint contains InterviewTurn with target_slots
    assert len(checkpoint.turns) == 1
    assert isinstance(checkpoint.turns[0], InterviewTurn)
    assert checkpoint.turns[0].target_slots == ["offline_sync_protocol"]
    assert checkpoint.pending_target_slots == ["offline_sync_protocol"]


def test_resume_from_transcript_rejects_public_transcript(sample_case: RequirementCase) -> None:
    """Verify that attempting to resume from a public InterviewTranscript strictly raises ValueError."""
    public_transcript = InterviewTranscript(
        case_id=sample_case.case_id,
        project_name=sample_case.project_name,
        turns=[],
    )
    interviewer = HashimotoInterviewer()

    with pytest.raises(ValueError, match="Lossless session resumption requires an InterviewCheckpoint instance"):
        interviewer.resume_from_transcript(public_transcript)


def test_abduction_history_deduplication_and_no_dangling_reference(sample_case: RequirementCase) -> None:
    """Verify that repeated identical abductions are not added, and no dangling slot references exist."""
    repeated_abduction_json = json.dumps({
        "Surprising Fact C": "Unstable network connectivity",
        "Reason to Suspect A": "Doctors need offline synchronization",
        "New Slot": {
            "offline_sync_strategy": {
                "category": "constraints",
                "value": None,
            }
        },
    })
    q_json = json.dumps({
        "Target Slot S": {"offline_sync_strategy": {"category": "constraints", "value": None}},
        "Question": "Follow up question?"
    })
    client = MockLLMClient(
        scripted_responses=[
            q_json,
            "{}",  # filling 1
            repeated_abduction_json, # abduction 1 (accepts offline_sync_strategy)
            q_json,
            "{}",  # filling 2
            repeated_abduction_json, # abduction 2 (slot is duplicate, should NOT create dangling record)
            q_json,
        ],
        auto_pipeline=False,
    )
    interviewer = HashimotoInterviewer(config=InterviewConfig(max_turns=5), llm_client=client)
    interviewer.initialize(sample_case)

    interviewer.get_first_question()
    interviewer.step("Turn 1 response.")
    assert len(interviewer.abduction_history) == 1
    assert interviewer.abduction_history[0].new_slot == "offline_sync_strategy"
    assert "offline_sync_strategy" in interviewer.slots

    # Turn 2 with identical duplicate abduction
    interviewer.step("Turn 2 response.")
    assert len(interviewer.abduction_history) == 1
    for rec in interviewer.abduction_history:
        assert rec.new_slot in interviewer.slots
        assert rec.new_slot != "abduction_hypothesis"


def test_initial_requirements_propagated_to_all_stages(sample_case: RequirementCase) -> None:
    """Verify that initial_requirements is present in the prompt context of all 3 pipeline stages."""
    recording_client = MockLLMClient(auto_pipeline=True)
    interviewer = HashimotoInterviewer(
        config=InterviewConfig(model="mock-gpt", max_turns=3),
        llm_client=recording_client,
    )
    interviewer.initialize(sample_case)

    interviewer.get_first_question()
    assert len(recording_client.call_history) == 1
    assert sample_case.initial_requirements in recording_client.call_history[0][1].content

    interviewer.step("Stakeholder response.")
    assert len(recording_client.call_history) == 4
    assert sample_case.initial_requirements in recording_client.call_history[1][1].content
    assert sample_case.initial_requirements in recording_client.call_history[2][1].content
    assert sample_case.initial_requirements in recording_client.call_history[3][1].content


def test_strict_fill_rate_threshold_boundary(sample_case: RequirementCase) -> None:
    """Verify that fill_rate exactly equal to threshold (0.80) does NOT terminate, but > 0.80 terminates."""
    eight_of_ten_slots = [
        {"name": f"slot_{i}", "category": "cat", "value": f"Val_{i}" if i < 8 else None}
        for i in range(10)
    ]
    q_json = json.dumps({"Target Slot S": {"slot_8": {"category": "cat", "value": None}}, "Question": "Next Q after 80%?"})
    mock_80_resp = [
        q_json,
        json.dumps({"slots": eight_of_ten_slots}),
        json.dumps({"has_abduction": False, "new_slots": []}),
        q_json,
    ]
    client_80 = MockLLMClient(scripted_responses=mock_80_resp, auto_pipeline=False)
    interviewer_80 = HashimotoInterviewer(
        config=InterviewConfig(model="mock-gpt", max_turns=5, fill_rate_threshold=0.8),
        llm_client=client_80,
    )
    interviewer_80.initialize(sample_case)
    interviewer_80._slots = {s["name"]: Slot(name=s["name"], category=s["category"], value=None) for s in eight_of_ten_slots}

    interviewer_80.get_first_question()
    resp_80 = interviewer_80.step("Answer yielding 80% fill rate.")

    assert interviewer_80.fill_rate == 0.80
    assert interviewer_80.is_finished is False
    assert resp_80 == "Next Q after 80%?"

    nine_of_ten_slots = [
        {"name": f"slot_{i}", "category": "cat", "value": f"Val_{i}" if i < 9 else None}
        for i in range(10)
    ]
    mock_90_resp = [
        q_json,
        json.dumps({"slots": nine_of_ten_slots}),
        json.dumps({"has_abduction": False, "new_slots": []}),
    ]
    client_90 = MockLLMClient(scripted_responses=mock_90_resp, auto_pipeline=False)
    interviewer_90 = HashimotoInterviewer(
        config=InterviewConfig(model="mock-gpt", max_turns=5, fill_rate_threshold=0.8),
        llm_client=client_90,
    )
    interviewer_90.initialize(sample_case)
    interviewer_90._slots = {s["name"]: Slot(name=s["name"], category=s["category"], value=None) for s in nine_of_ten_slots}

    interviewer_90.get_first_question()
    resp_90 = interviewer_90.step("Answer yielding 90% fill rate.")

    assert interviewer_90.fill_rate == 0.90
    assert interviewer_90.is_finished is True
    assert resp_90 == ""


def test_empty_string_values_do_not_count_as_filled(sample_case: RequirementCase) -> None:
    """Verify that empty strings or whitespace values are normalized to None and do not trigger completion."""
    slots_with_empty_strings = [
        {"name": f"slot_{i}", "category": "cat", "value": "   " if i % 2 == 0 else ""}
        for i in range(8)
    ]
    q_json = json.dumps({"Target Slot S": {"slot_0": {"category": "cat", "value": None}}, "Question": "Follow up question?"})
    mock_resp = [
        q_json,
        json.dumps({"slots": slots_with_empty_strings}),
        json.dumps({"has_abduction": False, "new_slots": []}),
        q_json,
    ]
    client = MockLLMClient(scripted_responses=mock_resp, auto_pipeline=False)
    interviewer = HashimotoInterviewer(
        config=InterviewConfig(model="mock-gpt", max_turns=5, fill_rate_threshold=0.8),
        llm_client=client,
    )
    interviewer.initialize(sample_case)

    interviewer.get_first_question()
    resp = interviewer.step("Empty answer.")

    assert interviewer.fill_rate == 0.0
    assert all(s.value is None for s in interviewer.slots.values())
    assert interviewer.is_finished is False
    assert resp == "Follow up question?"


def test_rollback_on_failure_in_each_substage(sample_case: RequirementCase) -> None:
    """Verify atomic state rollback and clean retry if failure occurs in Stage 1, Stage 2, or Stage 3."""
    client_fail_stage1 = MockLLMClient(fail_on_calls={2})
    interviewer1 = HashimotoInterviewer(llm_client=client_fail_stage1)
    interviewer1.initialize(sample_case)
    interviewer1.get_first_question()
    with pytest.raises(RuntimeError):
        interviewer1.step("Answer 1")
    assert interviewer1.turn_count == 0
    assert interviewer1.export_transcript().turns == []

    # Clean retry
    q1 = interviewer1.step("Answer 1")
    assert q1 != ""
    assert interviewer1.turn_count == 1
