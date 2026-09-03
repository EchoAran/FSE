"""Demonstration script running the original nursing career interview system."""

import json
from pathlib import Path
import sys

# Add repository root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.client.base import BaseLLMClient
from src.config import InterviewConfig
from src.interviewer import HashimotoInterviewer
from src.models import Message, RequirementCase


class CareerMockClient(BaseLLMClient):
    """Deterministic mock client for career domain."""

    def __init__(self) -> None:
        """Initialize mock responses for career stages."""
        self.call_count = 0

    def generate(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.1,
        max_tokens: int = 1024,
    ) -> str:
        """Generate domain responses based on the active prompt content."""
        self.call_count += 1
        system_text = messages[0].content.lower() if messages else ""

        # Slot filling
        if "slot filling" in system_text and "career counseling" in system_text:
            return json.dumps({
                "Career aspirations for next year": {
                    "category": "Career",
                    "value": "Critical Care Clinical Nurse Specialist"
                },
                "Career development plan": {
                    "category": "Career, Plan",
                    "value": "Complete advanced trauma life support and CCRN certification"
                },
                "Future department preferences": {
                    "category": "Career, Preference",
                    "value": "Outpatient Cardiology Clinic"
                },
            })

        # Abductive slot generation
        if "abductive reasoning" in system_text and "dynamic slot generation" in system_text:
            return json.dumps({
                "Surprising Fact C": "Experienced ICU nurse with high appraisal requesting transfer to outpatient clinic",
                "Reason to Suspect A": "Chronic night shift fatigue and desire for predictable daytime working hours",
                "New Slot": {
                    "shift_work_fatigue_level": {
                        "category": "Personal, Health",
                        "value": None
                    },
                    "outpatient_preference_motivation": {
                        "category": "Career, Preference",
                        "value": None
                    }
                }
            })

        # Question generation
        if self.call_count == 1:
            # Opening question
            return json.dumps({
                "Target Slot S": {
                    "Career aspirations for next year": {
                        "category": "Career",
                        "value": None
                    }
                },
                "Question": "Could you share your primary career goals and aspirations for the coming year?"
            })
        else:
            # Follow-up question targeting abduced slot
            return json.dumps({
                "Target Slot S": {
                    "shift_work_fatigue_level": {
                        "category": "Personal, Health",
                        "value": None
                    }
                },
                "Question": "Could you share how your current night shift schedule affects your daily routine and work-life balance?"
            })


def main() -> None:
    """Run a sample career interview using original paper assets."""
    root_dir = Path(__file__).parent.parent
    config = InterviewConfig(
        model="career-gpt",
        max_turns=3,
        initial_slots_path="config/career_initial_slots.yaml",
        prompts_dir="prompts_original",
    )

    nurse_profile = RequirementCase(
        case_id="NURSE-001",
        project_name="Senior Nurse Career Consultation",
        initial_requirements="Nurse with 5 years ICU experience seeking career transition guidance.",
    )

    mock_client = CareerMockClient()
    interviewer = HashimotoInterviewer(config=config, llm_client=mock_client)
    interviewer.initialize(nurse_profile)

    print("=== Hashimoto Career Interview System ===")
    print(f"Loaded Initial Career Slots: {len(interviewer.slots)}")

    q0 = interviewer.get_first_question()
    print(f"\n[Interviewer Q1 (Target: {interviewer.pending_target_slots})]: {q0}\n")

    q1 = interviewer.step("I've worked ICU for 5 years, but night shifts are draining and I'm interested in outpatient.")
    print(f"[Slots: {len(interviewer.slots)} | Abductions: {len(interviewer.abduction_history)}]")
    print(f"\n[Interviewer Q2 (Target: {interviewer.pending_target_slots})]: {q1}\n")

    transcript = interviewer.export_transcript()
    checkpoint = interviewer.export_checkpoint()
    print("Career interview completed.")
    print(f"- Public Transcript Turns: {len(transcript.turns)}")
    print(f"- Public Turn 1: {transcript.turns[0].model_dump()}")
    print(f"- Checkpoint Turn 1 Target Slots: {checkpoint.turns[0].target_slots}")
    print(f"- Internal Checkpoint Slots: {len(checkpoint.slots)}")
    print(f"- Internal Abductions: {len(checkpoint.abduction_history)}")


if __name__ == "__main__":
    main()
