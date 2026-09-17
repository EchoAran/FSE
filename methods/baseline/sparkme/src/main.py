"""Main CLI entry point for SparkMe software requirements interview."""

import argparse
import json
from pathlib import Path
import sys

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.interviewer import SparkMeInterviewer
from src.models import RequirementCase
from src.transcript import TranscriptExporter


def main() -> None:
    """Run interactive terminal session for software requirements elicitation."""
    parser = argparse.ArgumentParser(description="SparkMe Requirements Elicitation CLI")
    parser.add_argument("--input", "-i", type=str, default=None, help="Path to input JSON file containing project_name and initial_requirements")
    parser.add_argument("--case_id", type=str, default="CLI-CASE-001", help="Unique Case ID")
    parser.add_argument("--project_name", type=str, default="Software System", help="Name of the software project")
    parser.add_argument("--initial_requirements", type=str, default="", help="Initial requirements description")
    parser.add_argument("--max_turns", type=int, default=None, help="Optional maximum interaction turns")
    parser.add_argument("--output", type=str, default="output/transcript.json", help="Path to output transcript")
    args = parser.parse_args()

    case_id = args.case_id
    project_name = args.project_name
    initial_requirements = args.initial_requirements

    if args.input:
        input_path = Path(args.input)
        if not input_path.is_file():
            print(f"Error: Input file not found: {input_path}", file=sys.stderr)
            sys.exit(1)
        with input_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        project_name = data.get("project_name", project_name)
        initial_requirements = data.get("initial_requirements", initial_requirements)
        case_id = data.get("case_id", case_id)

    case = RequirementCase(
        case_id=case_id,
        project_name=project_name,
        initial_requirements=initial_requirements,
    )

    interviewer = SparkMeInterviewer(max_turns=args.max_turns)
    interviewer.initialize(case)

    print(f"=== Starting SparkMe Interview for {case.project_name} ===")
    first_q = interviewer.get_first_question()
    print(f"\n[Interviewer]: {first_q}")

    while not interviewer.is_finished:
        try:
            user_input = input("\n[Stakeholder]: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "end"):
                break
            next_q = interviewer.step(user_input)
            if interviewer.is_finished:
                print("\n[Interview completed]")
                break
            print(f"\n[Interviewer]: {next_q}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting session...")
            break

    transcript = interviewer.export_transcript()
    TranscriptExporter.save_transcript(transcript, args.output)
    print(f"\nTranscript exported to {args.output}")


if __name__ == "__main__":
    main()
