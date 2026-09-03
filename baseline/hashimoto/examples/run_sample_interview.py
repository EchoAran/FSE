"""Example execution script running a Hashimoto interview session from the command line."""

import argparse
import json
from pathlib import Path
import sys
import yaml

# Add repository root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.client.base import BaseLLMClient
from src.client.openai_client import OpenAIClient
from src.config import InterviewConfig
from src.interviewer import HashimotoInterviewer
from src.models import Message, RequirementCase
from src.prompt.loader import PromptLoader
from src.transcript import TranscriptExporter


class LocalDemoMockClient(BaseLLMClient):
    """Self-contained mock client for standalone CLI demonstration."""

    def __init__(self) -> None:
        """Initialize call counter."""
        self.call_count = 0

    def generate(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.1,
        max_tokens: int = 1024,
    ) -> str:
        """Generate structured JSON responses matching the active prompt stage."""
        self.call_count += 1
        system_text = messages[0].content if messages else ""

        if "slot filling" in system_text.lower():
            return json.dumps({
                "project_goals": "Cloud clinic queue and EMR management",
                "functional_needs": "Real-time appointment scheduling and digital prescriptions",
            })

        if "abductive reasoning and dynamic slot generation" in system_text.lower():
            return json.dumps({
                "has_abduction": True,
                "surprising_fact": "Clinic operates in rural regions with unstable network connectivity",
                "suspected_reason": "Doctors must record patient consultations offline and sync later",
                "new_slots": [
                    {"name": "offline_synchronization_protocol", "category": "constraints", "value": None},
                    {"name": "conflict_resolution_policy", "category": "business_logic", "value": None},
                ]
            })

        return json.dumps({
            "Target Slot S": {
                "offline_synchronization_protocol": {
                    "category": "constraints",
                    "value": None
                }
            },
            "Question": "Could you describe how offline consultations should sync with the central server once internet reconnects?"
        })


def load_case(case_file: Path) -> RequirementCase:
    """Load a requirements case from a YAML file."""
    with case_file.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return RequirementCase(**data)


def main() -> None:
    """Run an interactive or automated requirements interview session."""
    parser = argparse.ArgumentParser(description="Run a Hashimoto Dynamic Slot + Abduction interview session.")
    parser.add_argument(
        "--case",
        type=Path,
        default=Path("examples/sample_cases/clinic_management.yaml"),
        help="Path to the requirement case YAML file.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/default.yaml"),
        help="Path to the runtime configuration YAML file.",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use a self-contained mock LLM client for offline demonstration.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output/"),
        help="Directory to save resulting interview transcript and checkpoint.",
    )
    args = parser.parse_args()

    root_dir = Path(__file__).parent.parent
    case_path = (root_dir / args.case).resolve() if not args.case.is_absolute() else args.case
    config_path = (root_dir / args.config).resolve() if not args.config.is_absolute() else args.config

    config = InterviewConfig.from_yaml(config_path)
    case = load_case(case_path)
    prompt_loader = PromptLoader(base_path=root_dir)

    if args.mock:
        client: BaseLLMClient = LocalDemoMockClient()
    else:
        client = OpenAIClient()

    interviewer = HashimotoInterviewer(
        config=config,
        llm_client=client,
        prompt_loader=prompt_loader,
    )

    interviewer.initialize(case)
    print(f"=== Starting Hashimoto Requirements Interview for: {case.project_name} ===")
    print(f"Initial Slots: {len(interviewer.slots)} | Fill Rate: {interviewer.fill_rate:.0%}")

    first_question = interviewer.get_first_question()
    print(f"\n[Interviewer (Target: {interviewer.pending_target_slots})]: {first_question}\n")

    while not interviewer.is_finished:
        try:
            user_input = input("[Stakeholder Response (type 'quit' to end)]: ").strip()
            if not user_input or user_input.lower() == "quit":
                break

            next_question = interviewer.step(user_input)
            print(f"[Slots: {len(interviewer.slots)} | Fill Rate: {interviewer.fill_rate:.0%}]")
            if next_question:
                print(f"\n[Interviewer (Target: {interviewer.pending_target_slots})]: {next_question}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nSession interrupted.")
            break

    # Export clean transcript and internal checkpoint
    transcript = interviewer.export_transcript()
    checkpoint = interviewer.export_checkpoint()

    output_dir = (root_dir / args.output_dir).resolve() if not args.output_dir.is_absolute() else args.output_dir
    transcript_path = output_dir / f"{case.case_id}_transcript.json"
    checkpoint_path = output_dir / f"{case.case_id}_checkpoint.json"

    TranscriptExporter.save_transcript(transcript, transcript_path)
    TranscriptExporter.save_checkpoint(checkpoint, checkpoint_path)

    print(f"\nInterview completed.")
    print(f"- Public Transcript: {transcript_path}")
    print(f"- Internal Checkpoint: {checkpoint_path}")
    print(f"Final Tracked Slots: {len(checkpoint.slots)}")
    print(f"Total Abductions: {len(checkpoint.abduction_history)}")


if __name__ == "__main__":
    main()
