"""Sample script running a requirements elicitation interview with SparkMe."""

import argparse
import os
from pathlib import Path
import sys
import yaml

# Add sparkme root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.interviewer import SparkMeInterviewer
from src.models import RequirementCase
from src.transcript import TranscriptExporter


def parse_args() -> argparse.Namespace:
    """Parse command line options."""
    parser = argparse.ArgumentParser(description="Run a SparkMe software requirements elicitation interview.")
    parser.add_argument("--case", type=str, default="examples/sample_cases/clinic_management.yaml", help="Path to requirement case YAML")
    parser.add_argument("--max-turns", type=int, default=3, help="Maximum number of interaction turns")
    parser.add_argument("--logs-dir", type=str, default=None, help="Directory for execution logs")
    parser.add_argument("--output", type=str, default="output/clinic_transcript.json", help="Path to export public transcript")
    return parser.parse_args()


def main() -> None:
    """Execute the interview workflow."""
    args = parse_args()

    if args.logs_dir:
        os.environ["LOGS_DIR"] = args.logs_dir
    else:
        os.environ.setdefault("LOGS_DIR", "logs")

    case_path = Path(args.case)
    with case_path.open("r", encoding="utf-8") as f:
        case_data = yaml.safe_load(f)

    case = RequirementCase(**case_data)
    print(f"=== SparkMe Requirements Interview ===")
    print(f"Project: {case.project_name} (Case ID: {case.case_id})")
    print(f"Initial Context: {case.initial_requirements.strip()}\n")

    interviewer = SparkMeInterviewer(max_turns=args.max_turns)
    interviewer.initialize(case)

    # 1. First Question
    q0 = interviewer.get_first_question()
    print(f"[Interviewer Q1]: {q0}\n")

    # 2. Stepping through turns
    sample_answers = [
        "We need rural clinics to access patient records offline because regional internet drops frequently.",
        "When offline, doctors should be able to write prescriptions and queue them for automated dispatch upon reconnection.",
        "Role-based access is required so nurses can view vitals while only doctors modify diagnostic notes.",
    ]

    for i, answer in enumerate(sample_answers[: args.max_turns - 1], start=1):
        print(f"[Stakeholder A{i}]: {answer}")
        next_q = interviewer.step(answer)
        if interviewer.is_finished:
            print(f"\n[Interview Completed at turn {interviewer.turn_count}]")
            break
        print(f"\n[Interviewer Q{i+1}]: {next_q}\n")

    # 3. Export Transcript
    transcript = interviewer.export_transcript()
    TranscriptExporter.save_transcript(transcript, args.output)
    print(f"\nPublic transcript saved to: {args.output}")
    print(f"- Completed Turns: {len(transcript.turns)}")
    print(f"- Is Completed: {transcript.is_completed}")


if __name__ == "__main__":
    main()
