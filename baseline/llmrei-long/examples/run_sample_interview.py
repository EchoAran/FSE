"""Example execution script running an interview session from the command line."""

import argparse
from pathlib import Path
import sys
import yaml

# Add repository root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.client.openai_client import OpenAIClient
from src.config import InterviewConfig
from src.interviewer import LLMREIInterviewer
from src.models import RequirementCase
from src.prompt.loader import PromptLoader
from src.transcript import TranscriptExporter
from tests.mock_client import MockLLMClient


def load_case(case_file: Path) -> RequirementCase:
    """Load a requirements case from a YAML file."""
    with case_file.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return RequirementCase(**data)


def main() -> None:
    """Run an interactive or automated requirements elicitation session."""
    parser = argparse.ArgumentParser(description="Run an LLMREI-long interview session.")
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
        help="Use a mock LLM client for offline demonstration.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output/"),
        help="Directory to save resulting interview transcript.",
    )
    args = parser.parse_args()

    root_dir = Path(__file__).parent.parent
    case_path = (root_dir / args.case).resolve() if not args.case.is_absolute() else args.case
    config_path = (root_dir / args.config).resolve() if not args.config.is_absolute() else args.config

    config = InterviewConfig.from_yaml(config_path)
    case = load_case(case_path)
    prompt_loader = PromptLoader(base_path=root_dir)

    if args.mock:
        client = MockLLMClient()
    else:
        client = OpenAIClient()

    interviewer = LLMREIInterviewer(
        config=config,
        llm_client=client,
        prompt_loader=prompt_loader,
    )

    interviewer.initialize(case)
    print(f"=== Starting Requirements Interview for: {case.project_name} ===")

    first_question = interviewer.get_first_question()
    print(f"\n[Interviewer]: {first_question}\n")

    while not interviewer.is_finished:
        try:
            user_input = input("[Stakeholder Response (type 'quit' to end)]: ").strip()
            if not user_input or user_input.lower() == "quit":
                break

            next_question = interviewer.step(user_input)
            if next_question:
                print(f"\n[Interviewer]: {next_question}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nSession interrupted.")
            break

    # Export structured JSON transcript
    transcript = interviewer.export_transcript()
    output_dir = (root_dir / args.output_dir).resolve() if not args.output_dir.is_absolute() else args.output_dir
    json_path = output_dir / f"{case.case_id}_transcript.json"

    TranscriptExporter.save_json(transcript, json_path)

    print(f"\nInterview completed. Saved transcript to:\n- {json_path}")


if __name__ == "__main__":
    main()
