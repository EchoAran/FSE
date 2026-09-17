"""Command line interface for the requirements elicitation interview environment."""

import argparse
from pathlib import Path
import sys
from typing import Optional

from interview.adapters.registry import METHOD_REGISTRY
from interview.cases.loader import CaseLoader
from interview.orchestrator.orchestrator import InterviewOrchestrator
from interview.storage.manifest import ManifestManager


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser for CLI execution."""
    parser = argparse.ArgumentParser(
        description="Unified Requirements Elicitation Interview Environment.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--method",
        "-m",
        choices=list(METHOD_REGISTRY.keys()),
        help="Interview method identifier.",
    )
    parser.add_argument(
        "--case",
        "-c",
        help="Target case ID from dataset/cases.jsonl (e.g. PURE_001).",
    )
    parser.add_argument(
        "--method-config",
        help="Path to method's native configuration YAML or .env file.",
    )
    parser.add_argument(
        "--interviewee-config",
        "-i",
        dest="interviewee_config",
        help="Path to interviewee agent YAML configuration file.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode where a human provides responses on console.",
    )
    parser.add_argument(
        "--inspect",
        action="store_true",
        help="Inspect existing results directory status without stepping.",
    )
    parser.add_argument(
        "--list-cases",
        action="store_true",
        help="List available cases in dataset/cases.jsonl and exit.",
    )
    return parser


def main(args: Optional[list] = None) -> int:
    """Main CLI entrypoint."""
    parser = build_parser()
    parsed = parser.parse_args(args)

    if parsed.list_cases:
        cases = CaseLoader.load_all()
        print(f"\nTotal available cases: {len(cases)}")
        for cid, case in cases.items():
            print(f" - {cid}: {case.project_name}")
        return 0

    if not parsed.method or not parsed.case:
        parser.print_help()
        print("\nError: Both --method and --case are required to run or inspect an interview.", file=sys.stderr)
        return 1

    method_id = parsed.method.strip()
    case_id = parsed.case.strip()

    # Handle inspection only
    if parsed.inspect:
        results_dir = Path("results") / method_id / case_id
        if not ManifestManager.exists(results_dir):
            print(f"No existing interview results found at: {results_dir}")
            return 1
        manifest = ManifestManager.load(results_dir)
        print(f"\n=======================================================")
        print(f" Interview Manifest Inspection: {method_id} x {case_id}")
        print(f" Project Name     : {manifest.project_name}")
        print(f" Status           : {manifest.status.value}")
        print(f" Completed Turns  : {manifest.completed_turns}")
        print(f" Method Model     : {manifest.method_model}")
        print(f" Method Max Turns : {manifest.method_max_turns}")
        print(f" Interviewee Model: {manifest.interviewee_model}")
        if manifest.finish_message:
            print(f" Finish Message   : {manifest.finish_message}")
        if manifest.error_message:
            print(f" Error Message    : {manifest.error_message}")
        print(f" Results Dir      : {results_dir}")
        print(f"=======================================================\n")
        return 0

    # Determine default interviewee config if not specified
    interviewee_config = parsed.interviewee_config
    if not interviewee_config and not parsed.interactive:
        for candidate in [
            Path("interview/config/interviewee.yaml"),
            Path("interview/config/interviewee.example.yaml"),
        ]:
            if candidate.is_file():
                interviewee_config = str(candidate)
                break

    try:
        orchestrator = InterviewOrchestrator(
            method_id=method_id,
            case_id=case_id,
            method_config_path=parsed.method_config,
            interviewee_config_path=interviewee_config,
        )
        orchestrator.run(interactive=parsed.interactive)
        return 0
    except Exception as exc:
        print(f"\n[Error]: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
