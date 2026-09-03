"""Unit tests for SlotFiller, AbductiveSlotGenerator, and QuestionGenerator."""

import json
from src.core.abductive_slot_generator import AbductiveSlotGenerator
from src.core.question_generator import QuestionGenerator
from src.core.slot_filler import SlotFiller
from src.models import Message, Slot
from tests.mock_client import MockLLMClient


def test_slot_filler_updates_values_without_key_mutations() -> None:
    """Verify that SlotFiller updates values for existing slots and preserves unmentioned ones."""
    initial_slots = {
        "project_goals": Slot(name="project_goals", category="goals", value=None),
        "constraints": Slot(name="constraints", category="constraints", value="Pre-existing budget limit"),
    }
    dialogue = [
        Message(role="assistant", content="What is the goal?"),
        Message(role="user", content="We want to automate patient check-in."),
    ]
    mock_response = json.dumps({
        "project_goals": {"category": "goals", "value": "Automate patient check-in"},
        "non_existent_slot": {"category": "extra", "value": "Ignored"},
    })
    client = MockLLMClient(scripted_responses=[mock_response], auto_pipeline=False)
    filler = SlotFiller("Prompt for slot filling", client)

    updated = filler.fill_slots(
        current_slots=initial_slots,
        dialogue_history=dialogue,
        initial_requirements="Clinic Project",
        model="mock-model",
    )

    assert updated["project_goals"].value == "Automate patient check-in"
    assert updated["constraints"].value == "Pre-existing budget limit"
    assert "non_existent_slot" not in updated


def test_abductive_slot_generator_caps_at_five_and_deduplicates() -> None:
    """Verify that AbductiveSlotGenerator creates at most 5 new slots and deduplicates."""
    initial_slots = {
        "existing_slot": Slot(name="existing_slot", category="cat", value=None),
    }
    dialogue = [Message(role="user", content="We also need payment gateway and insurance verification.")]
    mock_response = json.dumps({
        "Surprising Fact C": "Zero credit card adoption in the operating region",
        "Reason to Suspect A": "Need local cash voucher API integration",
        "New Slot": {
            "existing_slot": {"category": "duplicate", "value": None},
            "cash_voucher_integration": {"category": "billing", "value": "ShouldBeNull"},
            "insurance_verification": {"category": "billing", "value": None},
            "slot_3": {"category": "c", "value": None},
            "slot_4": {"category": "c", "value": None},
            "slot_5": {"category": "c", "value": None},
            "slot_6_exceeds_cap": {"category": "c", "value": None},
        }
    })
    client = MockLLMClient(scripted_responses=[mock_response], auto_pipeline=False)
    generator = AbductiveSlotGenerator("Prompt for dynamic slot", client)

    record, new_slots = generator.generate(
        current_slots=initial_slots,
        dialogue_history=dialogue,
        abduction_history=[],
        initial_requirements="Clinic Project",
        model="mock-model",
    )

    assert record is not None
    assert record.surprising_fact == "Zero credit card adoption in the operating region"
    assert len(new_slots) == 5
    assert all(s.value is None for s in new_slots)
    assert not any(s.name == "existing_slot" for s in new_slots)
    assert not any(s.name == "slot_6_exceeds_cap" for s in new_slots)


def test_question_generator_targets_empty_slots() -> None:
    """Verify that QuestionGenerator formulates a question targeting unfilled slots and extracts target slots."""
    slots = {
        "filled_slot": Slot(name="filled_slot", category="goals", value="Completed"),
        "unfilled_slot": Slot(name="unfilled_slot", category="security", value=None),
    }
    mock_json = json.dumps({
        "Target Slot S": {
            "unfilled_slot": {
                "category": "security",
                "value": None
            }
        },
        "Question": "What security standards must the system meet?"
    })
    client = MockLLMClient(
        scripted_responses=[mock_json],
        auto_pipeline=False,
    )
    generator = QuestionGenerator("Prompt for question gen", client)

    targets, question = generator.generate_question(
        current_slots=slots,
        dialogue_history=[],
        initial_requirements="Clinic System",
        latest_abduction=None,
        model="mock-model",
    )

    assert targets == ["unfilled_slot"]
    assert question == "What security standards must the system meet?"
