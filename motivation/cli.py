"""Command line entry point of the Motivation Study."""

from __future__ import annotations

import argparse
import sys

from motivation.config.config import MotivationConfig, display_path, load_config
from motivation.llm.client import ChatCompletionClient
from motivation.pipeline.analyze import analyze
from motivation.pipeline.inspect import conversation_report
from motivation.pipeline.prepare import prepare, read_derived_counts
from motivation.pipeline.summarize import summarize
from motivation.storage.manifest import ManifestStatus, read_manifest, update_status


def run_prepare(config: MotivationConfig, args: argparse.Namespace) -> int:
    """Prepare the derived conversation artifacts and report the screening counts."""
    result = prepare(config)
    for source, path in result.input_files.items():
        print(f"{source}: {path}")
    for stage, count in result.counts.items():
        print(f"{stage}: {count}")
    print(f"screening table: {display_path(result.table_path)}")
    print(f"manifest: {display_path(result.manifest_path)}")
    return 0


def run_inspect(config: MotivationConfig, args: argparse.Namespace) -> int:
    """Report the prepared input set with its derived counts, or one conversation trace."""
    if args.conversation_id:
        for line in conversation_report(config, args.conversation_id):
            print(line)
        return 0
    print(f"snapshot: {config.dataset.snapshot}")
    print(f"dataset root: {display_path(config.dataset.root)}")

    manifest = read_manifest(config.results_dir)
    if manifest is None:
        raise FileNotFoundError("manifest not found, run prepare first")
    print(f"manifest status: {manifest['status']}")

    counts = read_derived_counts(config)
    print(f"unique conversations: {counts.unique_conversations}")
    print(f"payload conflicts: {counts.payload_conflicts}")
    print(f"structural candidates: {counts.structural_candidates}")
    for code, count in counts.exclusion_codes.items():
        print(f"exclusion {code}: {count}")
    for status, count in counts.temporal_status.items():
        print(f"artifact context {status}: {count}")
    print(
        "confirmed prior edited after conversation: "
        f"{counts.confirmed_prior_edited_after_conversation}"
    )
    return 0


def run_analyze(config: MotivationConfig, args: argparse.Namespace) -> int:
    """Run the LLM Analyzer and report the produced analysis artifacts."""
    update_status(config.results_dir, ManifestStatus.ANALYZING)
    result = analyze(
        config,
        ChatCompletionClient(config.analyzer),
        conversation_ids=args.conversation_ids,
        limit=args.limit,
        force=args.force,
    )
    update_status(config.results_dir, ManifestStatus.ANALYZED)
    print(f"analyzed: {result.analyzed}")
    print(f"skipped: {result.skipped}")
    print(f"failed: {result.failed}")
    print(f"degraded: {result.degraded}")
    print(f"lsri units: {result.lsri_units}")
    for code, count in result.error_codes.items():
        print(f"error {code}: {count}")
    print(f"analysis: {display_path(result.analysis_path)}")
    print(f"lsri: {display_path(result.lsri_path)}")
    print(f"errors: {display_path(result.errors_path)}")
    return 0


def run_summarize(config: MotivationConfig, args: argparse.Namespace) -> int:
    """Aggregate the analysis and report the produced tables and cases."""
    result = summarize(config)
    update_status(config.results_dir, ManifestStatus.SUMMARIZED)
    print(f"analyzed conversations: {result.analyzed_conversations}")
    print(f"lsri units: {result.lsri_units}")
    print(f"lsri conversations: {result.lsri_conversations}")
    print(f"candidate cases: {result.candidate_cases}")
    print(f"screening flow: {display_path(result.flow_path)}")
    print(f"tables: {display_path(result.tables_dir)}")
    print(f"cases: {display_path(result.cases_dir)}")
    print(f"summary: {display_path(result.summary_path)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser of the Motivation Study."""
    parser = argparse.ArgumentParser(prog="python -m motivation.cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser(
        "prepare", help="expand DevGPT inputs, screen conversations and write derived artifacts"
    )
    prepare_parser.add_argument("--config", required=True, help="Motivation Study configuration file")
    prepare_parser.set_defaults(handler=run_prepare)

    summarize_parser = subparsers.add_parser(
        "summarize", help="aggregate the analysis into the tables, cases and summary document"
    )
    summarize_parser.add_argument(
        "--config", required=True, help="Motivation Study configuration file"
    )
    summarize_parser.set_defaults(handler=run_summarize)

    inspect_parser = subparsers.add_parser(
        "inspect", help="report the prepared input set and the derived counts"
    )
    inspect_parser.add_argument("--config", required=True, help="Motivation Study configuration file")
    inspect_parser.add_argument(
        "--conversation-id",
        help="report the full provenance trace of one conversation",
    )
    inspect_parser.set_defaults(handler=run_inspect)

    analyze_parser = subparsers.add_parser(
        "analyze", help="run the LLM Analyzer and write the conversation analyses"
    )
    analyze_parser.add_argument("--config", required=True, help="Motivation Study configuration file")
    analyze_parser.add_argument(
        "--conversation-id",
        action="append",
        dest="conversation_ids",
        help="analyze only the given conversation id, repeatable",
    )
    analyze_parser.add_argument(
        "--limit", type=int, help="analyze at most this many pending conversations"
    )
    analyze_parser.add_argument(
        "--force", action="store_true", help="re-analyze conversations that already succeeded"
    )
    analyze_parser.set_defaults(handler=run_analyze)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Dispatch one command and report failures as an error line."""
    args = build_parser().parse_args(argv)
    try:
        config = load_config(args.config)
        return args.handler(config, args)
    except (FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())