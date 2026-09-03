"""Main CLI entry point for SparkMe software requirements interview."""

import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

from src.interviewer import SparkMeInterviewer
from src.models import RequirementCase
from src.transcript import TranscriptExporter


def main() -> None:
    """Run interactive terminal session for software requirements elicitation."""
    parser = argparse.ArgumentParser(description="SparkMe Requirements Elicitation CLI")
    parser.add_argument("--case_id", type=str, default="CLI-CASE-001", help="Unique Case ID")
    parser.add_argument("--project_name", type=str, default="Software System", help="Name of the software project")
    parser.add_argument("--initial_requirements", type=str, default="", help="Initial requirements description")
    parser.add_argument("--max_turns", type=int, default=10, help="Max interaction turns")
    parser.add_argument("--output", type=str, default="output/transcript.json", help="Path to output transcript")
    args = parser.parse_args()

    case = RequirementCase(
        case_id=args.case_id,
        project_name=args.project_name,
        initial_requirements=args.initial_requirements,
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
