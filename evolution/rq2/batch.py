"""Temporary driver that replays the RQ2 CLI commands case by case.

Every step is one ordinary `python -m evolution.rq2.cli` invocation, in the same
order a manual run would use them. A command that returns a nonzero code is
reported and the driver continues with the next one, so repeating the script
resumes the failed and unfinished work.
"""

import argparse
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys

from evolution.rq2.config import RQ2Config, load_config
from evolution.rq2.ingest import load_cases

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = Path("evolution/rq2/config/default.yaml")


@dataclass(frozen=True)
class BatchSummary:
    total_cases: int
    completed_cases: int
    failures: list[str]

    @property
    def is_complete(self) -> bool:
        return not self.failures


def _display(command: list[str]) -> str:
    return " ".join(["python", *command[1:]])


def _run(command: list[str]) -> int:
    print(f"$ {_display(command)}", flush=True)
    completed = subprocess.run(command, cwd=REPO_ROOT, check=False)
    return completed.returncode


def _cli_commands(config: RQ2Config, config_path: Path) -> list[list[str]]:
    prepare = ["prepare", "--config", str(config_path)]
    evaluate = [
        ["evaluate", "--config", str(config_path), "--judge", rater_id]
        for rater_id in config.judges
    ]
    return [prepare, *evaluate]


def run_batch(config_path: Path, config: RQ2Config, case_ids: list[str] | None = None) -> BatchSummary:
    resolved_config_path = Path(config_path).resolve()
    cases = load_cases(config.paths.cases_file, case_ids=case_ids)
    commands = _cli_commands(config, resolved_config_path)
    interpreter = sys.executable
    failures: list[str] = []
    completed_cases = 0

    for case in cases:
        case_failed = False
        for step in commands:
            command = [interpreter, "-m", "evolution.rq2.cli", *step, "--case-id", case.case_id]
            if _run(command) != 0:
                failures.append(_display(command))
                case_failed = True
        if not case_failed:
            completed_cases += 1

    for step in ("export-templates", "report"):
        command = [interpreter, "-m", "evolution.rq2.cli", step, "--config", str(config_path)]
        if _run(command) != 0:
            failures.append(_display(command))

    return BatchSummary(
        total_cases=len(cases),
        completed_cases=completed_cases,
        failures=failures,
    )


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m evolution.rq2.batch",
        description="Run the RQ2 CLI commands for every case, skipping failures",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to YAML configuration file",
    )
    parser.add_argument(
        "--case-id",
        action="append",
        dest="case_ids",
        default=None,
        help="Specific case ID(s) to process (repeatable)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = create_parser().parse_args(argv)

    try:
        config = load_config(args.config)
    except Exception as exc:
        print(f"Error loading configuration from '{args.config}': {exc}", file=sys.stderr)
        return 1

    try:
        summary = run_batch(args.config, config, case_ids=args.case_ids)
    except Exception as exc:
        print(f"Error during batch execution: {exc}", file=sys.stderr)
        return 1

    print(
        f"Batch finished: {summary.completed_cases}/{summary.total_cases} cases "
        f"completed without a failed command."
    )
    for failure in summary.failures:
        print(f"Failed command: {failure}", file=sys.stderr)

    return 0 if summary.is_complete else 1


if __name__ == "__main__":
    sys.exit(main())
