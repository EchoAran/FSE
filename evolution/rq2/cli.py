import argparse
from pathlib import Path
import sys

from evolution.rq2.config import load_config
from evolution.rq2.evaluate import evaluate_judge
from evolution.rq2.ingest import prepare_inputs
from evolution.rq2.ratings import export_templates
from evolution.rq2.report import generate_reports


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m evolution.rq2.cli",
        description="RQ2 evaluation infrastructure and flow quality assessment CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. prepare
    prepare_p = subparsers.add_parser("prepare", help="Prepare input inventory and transcripts")
    prepare_p.add_argument(
        "--config",
        type=Path,
        default=Path("evolution/rq2/config/default.yaml"),
        help="Path to YAML configuration file",
    )
    prepare_p.add_argument(
        "--case-id",
        action="append",
        dest="case_ids",
        default=None,
        help="Specific case ID(s) to prepare (repeatable)",
    )

    # 2. evaluate
    eval_p = subparsers.add_parser("evaluate", help="Run evaluation for a specified LLM judge")
    eval_p.add_argument(
        "--config",
        type=Path,
        default=Path("evolution/rq2/config/default.yaml"),
        help="Path to YAML configuration file",
    )
    eval_p.add_argument(
        "--judge",
        required=True,
        dest="judge",
        help="Judge identifier (e.g. llm_expert_1 or llm_expert_2)",
    )
    eval_p.add_argument(
        "--case-id",
        action="append",
        dest="case_ids",
        default=None,
        help="Specific case ID(s) to evaluate (repeatable)",
    )
    eval_p.add_argument(
        "--rerun",
        action="store_true",
        default=False,
        help="Explicitly re-run tasks even if matching completed record exists",
    )

    # 3. export-templates
    export_p = subparsers.add_parser("export-templates", help="Rebuild LLM CSVs and export human blank templates")
    export_p.add_argument(
        "--config",
        type=Path,
        default=Path("evolution/rq2/config/default.yaml"),
        help="Path to YAML configuration file",
    )

    # 4. report
    report_p = subparsers.add_parser("report", help="Generate summary statistics, paired comparisons, and agreement report")
    report_p.add_argument(
        "--config",
        type=Path,
        default=Path("evolution/rq2/config/default.yaml"),
        help="Path to YAML configuration file",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        config = load_config(args.config)
    except Exception as exc:
        print(f"Error loading configuration from '{args.config}': {exc}", file=sys.stderr)
        return 1

    if args.command == "prepare":
        try:
            summary = prepare_inputs(config, case_ids=args.case_ids)
            print(
                f"Prepared {summary.total_items} items across {summary.total_cases} cases: "
                f"{summary.ready_count} ready, {summary.incomplete_count} incomplete, {summary.error_count} errors."
            )
            return 1 if summary.has_errors else 0
        except Exception as exc:
            print(f"Error during input preparation: {exc}", file=sys.stderr)
            return 1

    elif args.command == "evaluate":
        try:
            summary = evaluate_judge(
                config=config,
                rater_id=args.judge,
                case_ids=args.case_ids,
                rerun=args.rerun,
            )
            print(
                f"Evaluation for {summary.rater_id}: total {summary.total_tasks} tasks, "
                f"{summary.completed_count} completed, {summary.skipped_count} skipped, {summary.failed_count} failed."
            )
            if summary.has_failures:
                for res in summary.results:
                    if res.status == "failed":
                        print(
                            f"Task failed [{res.case_id}][{res.method_id}][{res.rater_id}]: {res.error_message}",
                            file=sys.stderr,
                        )
                return 1
            return 0
        except Exception as exc:
            print(f"Error during evaluation: {exc}", file=sys.stderr)
            return 1

    elif args.command == "export-templates":
        try:
            summary = export_templates(config)
            print(
                f"Templates exported: llm_expert_1={summary.llm_expert_1_rows} rows, "
                f"llm_expert_2={summary.llm_expert_2_rows} rows, "
                f"human_expert_1={summary.human_expert_1_existing_rows} existing + {summary.human_expert_1_added_rows} added, "
                f"human_expert_2={summary.human_expert_2_existing_rows} existing + {summary.human_expert_2_added_rows} added."
            )
            return 0
        except Exception as exc:
            print(f"Error exporting templates: {exc}", file=sys.stderr)
            return 1

    elif args.command == "report":
        try:
            summary = generate_reports(config)
            print(f"Reports successfully generated at {summary.report_md_path.parent}:")
            print(f"- Coverage: {summary.coverage_path.name}")
            print(f"- Score distributions: {summary.distributions_path.name}")
            print(f"- Score summary: {summary.summary_path.name}")
            print(f"- Paired comparisons: {summary.paired_path.name}")
            print(f"- Agreement: {summary.agreement_path.name}")
            print(f"- Markdown report: {summary.report_md_path.name}")
            return 0
        except Exception as exc:
            print(f"Error generating reports: {exc}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
