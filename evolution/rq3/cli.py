"""Command line entry points for the RQ3 evaluation workflow.

Every command maps to one module of the workflow, loads only the configuration
that module needs, and selects its cases, methods and coding runs explicitly.
The exit code reports the outcome of the selected operation: success, a failed
model, file or container call, or an invalid argument or configuration.
"""

import argparse
import sys
from pathlib import Path
from typing import Sequence

from evolution.rq3 import coding, container, evaluate, evidence, ingest, report, review, srs
from evolution.rq3.config import RQ3Config, load_config
from evolution.rq3.llm_client import LLMClient
from evolution.rq3.models import CodingResult, CodingTask, RequirementEvaluation, ScenarioRecord
from evolution.rq3.storage import read_json

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_USAGE = 2

GENERATION_RECORD_NAME = "generation_record.json"
DERIVED_REVIEW_FILES = ("reviewed_srs.json", "reviewed_srs.md", "review_status.json")
CODING_SUCCESS_STATUSES = ("completed", "limits_exceeded")


class UsageError(Exception):
    """Report an argument or configuration that the selected command cannot use."""


# --- Argument parsing ---------------------------------------------------------------


def _add_config(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", required=True, help="Path to the RQ3 configuration YAML file.")


def _add_scope(parser: argparse.ArgumentParser, with_runs: bool = False) -> None:
    parser.add_argument("--case-id", action="append", default=[], help="Restrict the command to a case id; repeatable.")
    parser.add_argument("--method-id", action="append", default=[], help="Restrict the command to a method id; repeatable.")
    if with_runs:
        parser.add_argument("--run-index", action="append", type=int, default=[], help="Restrict the command to run indices; repeatable.")
        parser.add_argument("--all", action="store_true", help="Select every enumerated task instead of an explicit run range.")


def build_parser() -> argparse.ArgumentParser:
    """Compose the command table of the RQ3 workflow."""
    parser = argparse.ArgumentParser(
        prog="python -m evolution.rq3.cli",
        description="Run the RQ3 evaluation workflow commands.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Read input state and write standardized transcripts.")
    _add_config(prepare)
    _add_scope(prepare)

    generate = subparsers.add_parser("generate-srs", help="Generate a draft SRS from a prepared transcript.")
    _add_config(generate)
    _add_scope(generate)
    generate.add_argument("--force", action="store_true", help="Regenerate a draft that was already generated.")

    export_srs = subparsers.add_parser("export-srs-review", help="Export the item review table of a draft.")
    _add_config(export_srs)
    _add_scope(export_srs)

    finalize = subparsers.add_parser("finalize-srs", help="Apply the item review and write the reviewed SRS.")
    _add_config(finalize)
    _add_scope(finalize)

    export_scenarios = subparsers.add_parser("export-scenarios", help="Export the observation scenario template.")
    _add_config(export_scenarios)
    _add_scope(export_scenarios)

    import_scenarios = subparsers.add_parser("import-scenarios", help="Read and record the filled scenario table.")
    _add_config(import_scenarios)
    _add_scope(import_scenarios)

    build = subparsers.add_parser("build-image", help="Build the container image that the configuration selects.")
    _add_config(build)

    run = subparsers.add_parser("run", help="Execute explicitly selected coding tasks.")
    _add_config(run)
    _add_scope(run, with_runs=True)

    collect = subparsers.add_parser("collect-evidence", help="Collect evidence for selected coding runs.")
    _add_config(collect)
    _add_scope(collect, with_runs=True)
    collect.add_argument("--invocations", required=True, help="JSON file describing how each scenario is invoked.")

    evaluate_impl = subparsers.add_parser("evaluate-implementations", help="Judge requirements from recorded evidence.")
    _add_config(evaluate_impl)
    _add_scope(evaluate_impl)

    export_eval = subparsers.add_parser("export-evaluation-review", help="Export the requirement judgment review table.")
    _add_config(export_eval)
    _add_scope(export_eval)

    import_eval = subparsers.add_parser("import-evaluation-review", help="Read and record the filled judgment review table.")
    _add_config(import_eval)
    _add_scope(import_eval)

    export_cons = subparsers.add_parser("export-consistency", help="Export the four-direction conclusion table.")
    _add_config(export_cons)
    _add_scope(export_cons)

    import_cons = subparsers.add_parser("import-consistency", help="Read and check the filled four-direction table.")
    _add_config(import_cons)
    _add_scope(import_cons)

    report_view = subparsers.add_parser("report", help="Build the coverage and comparison views from saved artifacts.")
    _add_config(report_view)

    verify = subparsers.add_parser("verify", help="Check stored artifacts for missing files and pending records.")
    _add_config(verify)

    return parser


# --- Configuration and scope --------------------------------------------------------


def _load_config(path: str) -> RQ3Config:
    """Load the configuration file the command was given."""
    try:
        return load_config(path)
    except Exception as exc:
        raise UsageError(f"cannot load configuration '{path}': {exc}") from exc


def _validate(config: RQ3Config, validation: str) -> None:
    """Check that the configuration holds what the selected command needs."""
    try:
        getattr(config, validation)()
    except Exception as exc:
        raise UsageError(f"configuration is not valid for this command: {exc}") from exc


def _resolve_scope(config: RQ3Config, case_ids: Sequence[str], method_ids: Sequence[str]) -> tuple[list[str], list[str]]:
    """Check the requested identifiers and return the selected cases and methods."""
    known_cases = [case.case_id for case in ingest.load_cases(config.paths.cases_file)]
    unknown_cases = sorted(set(case_ids) - set(known_cases))
    if unknown_cases:
        raise UsageError(f"unknown case id(s): {', '.join(unknown_cases)}")
    unknown_methods = sorted(set(method_ids) - set(config.methods))
    if unknown_methods:
        raise UsageError(f"unknown method id(s): {', '.join(unknown_methods)}")

    cases = known_cases if not case_ids else [case_id for case_id in known_cases if case_id in set(case_ids)]
    methods = list(config.methods) if not method_ids else [method for method in config.methods if method in set(method_ids)]
    return cases, methods


def _combinations(config: RQ3Config, args: argparse.Namespace) -> list[tuple[str, str]]:
    """Report the selected case and method pairs in configuration order."""
    cases, methods = _resolve_scope(config, args.case_id, args.method_id)
    return [(case_id, method_id) for case_id in cases for method_id in methods]


def _resolve_run_scope(config: RQ3Config, args: argparse.Namespace) -> tuple[list[str], list[str], list[int]]:
    """Check the requested run range and return the selected cases, methods and runs."""
    cases, methods = _resolve_scope(config, args.case_id, args.method_id)
    runs_per_srs = config.coding.runs_per_srs
    if args.all:
        return cases, methods, list(range(1, runs_per_srs + 1))
    if not args.case_id or not args.run_index:
        raise UsageError("this command needs --case-id and --run-index, or --all.")
    out_of_range = sorted({index for index in args.run_index if index < 1 or index > runs_per_srs})
    if out_of_range:
        raise UsageError(f"run index out of range 1..{runs_per_srs}: {out_of_range}")
    return cases, methods, sorted(set(args.run_index))


# --- Command handlers ---------------------------------------------------------------


def _cmd_prepare(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_prepare")
    cases, methods = _resolve_scope(config, args.case_id, args.method_id)
    items, transcripts = ingest.collect_transcripts(config, cases, methods)
    ingest.write_input_artifacts(items, transcripts, config.paths.artifacts_root)

    errors = [item for item in items if item.prepare_status == "input_error"]
    print(f"prepared {len(transcripts)} transcript(s) from {len(items)} input(s)")
    for item in errors:
        print(f"input error {item.case_id}/{item.method_id}: {item.reason}")
    return EXIT_FAILURE if errors else EXIT_SUCCESS


def _cmd_generate_srs(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_srs")
    root = config.paths.artifacts_root

    failures = 0
    for case_id, method_id in _combinations(config, args):
        transcript = report.load_transcript(root, case_id, method_id)
        if transcript is None:
            print(f"skip {case_id}/{method_id}: no prepared transcript")
            continue
        srs_dir = report.srs_directory(root, case_id, method_id)
        if not args.force and _generation_succeeded(srs_dir / GENERATION_RECORD_NAME):
            print(f"skip {case_id}/{method_id}: a draft was already generated")
            continue

        result = srs.generate_srs(transcript, config.artifact_processor)
        srs.save_srs_generation(result, srs_dir)
        if result.draft is not None:
            _discard_reviewed_srs(srs_dir)
        if result.status == "success":
            print(f"generated {case_id}/{method_id}")
        else:
            failures += 1
            print(f"failed {case_id}/{method_id}: {result.error}")
    return EXIT_FAILURE if failures else EXIT_SUCCESS


def _cmd_export_srs_review(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_prepare")
    root = config.paths.artifacts_root

    exported = 0
    for case_id, method_id in _combinations(config, args):
        draft = report.load_draft_srs(root, case_id, method_id)
        transcript = report.load_transcript(root, case_id, method_id)
        if draft is None or transcript is None:
            print(f"skip {case_id}/{method_id}: no draft or transcript")
            continue
        review.export_srs_review(draft, transcript, report.srs_review_path(root, case_id, method_id))
        exported += 1
    print(f"exported {exported} review table(s)")
    return EXIT_SUCCESS


def _cmd_finalize_srs(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_prepare")
    root = config.paths.artifacts_root

    failures = 0
    for case_id, method_id in _combinations(config, args):
        draft = report.load_draft_srs(root, case_id, method_id)
        transcript = report.load_transcript(root, case_id, method_id)
        if draft is None or transcript is None:
            print(f"skip {case_id}/{method_id}: no draft or transcript")
            continue

        decisions = review.read_srs_review(report.srs_review_path(root, case_id, method_id))
        result = review.apply_srs_review(draft, decisions, transcript)
        review.save_reviewed_srs(result, report.srs_directory(root, case_id, method_id))
        if result.status == "reviewed":
            print(f"finalized {case_id}/{method_id}")
        else:
            failures += 1
            print(f"incomplete {case_id}/{method_id}: {'; '.join(result.errors)}")
    return EXIT_FAILURE if failures else EXIT_SUCCESS


def _cmd_export_scenarios(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_prepare")
    root = config.paths.artifacts_root

    exported = 0
    for case_id, method_id in _combinations(config, args):
        reviewed = report.load_reviewed_srs(root, case_id, method_id)
        if reviewed is None:
            print(f"skip {case_id}/{method_id}: no reviewed SRS")
            continue
        review.export_scenarios_template(reviewed, report.scenarios_path(root, case_id, method_id))
        exported += 1
    print(f"exported {exported} scenario table(s)")
    return EXIT_SUCCESS


def _cmd_import_scenarios(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_prepare")
    root = config.paths.artifacts_root

    imported = 0
    for case_id, method_id in _combinations(config, args):
        reviewed = report.load_reviewed_srs(root, case_id, method_id)
        path = report.scenarios_path(root, case_id, method_id)
        if reviewed is None or not path.exists():
            print(f"skip {case_id}/{method_id}: no reviewed SRS or scenario table")
            continue
        scenarios = review.read_scenarios(path, reviewed)
        review.write_scenarios(path, scenarios)
        imported += 1
        print(f"imported {case_id}/{method_id}: {len(scenarios)} scenario(s)")
    return EXIT_SUCCESS


def _cmd_build_image(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_evidence")
    result = container.build_image(config.coding)
    print(result.log.strip())
    if result.status != "success":
        print(f"error: {result.error}", file=sys.stderr)
        return EXIT_FAILURE
    print(f"built image {result.image}")
    return EXIT_SUCCESS


def _cmd_run(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_coding")
    cases, methods, run_indices = _resolve_run_scope(config, args)
    tasks = _selected_tasks(config, cases, methods, run_indices)
    if not tasks:
        print("no coding task matched the selected scope")
        return EXIT_SUCCESS

    results = coding.run_tasks(tasks, config.coding)
    for result in results:
        print(f"{result.task_id}: {result.status}")
    failures = [result for result in results if result.status not in CODING_SUCCESS_STATUSES]
    return EXIT_FAILURE if failures else EXIT_SUCCESS


def _cmd_collect_evidence(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_evidence")
    cases, methods, run_indices = _resolve_run_scope(config, args)
    invocations = evidence.load_invocations(args.invocations)
    root = config.paths.artifacts_root
    verification_config = evidence.VerificationConfig(
        artifacts_root=root,
        image=config.coding.image,
        network=config.coding.network,
        command_timeout_seconds=config.coding.command_timeout_seconds,
    )

    failures = 0
    collected = 0
    for case_id in cases:
        for method_id in methods:
            scenarios = report.load_scenarios(root, case_id, method_id)
            for run_index in run_indices:
                result = report.load_coding_result(root, case_id, method_id, run_index)
                if result is None:
                    print(f"skip {case_id}/{method_id} run {run_index:02d}: no coding result")
                    continue
                verification, records = _collect_run(result, scenarios, invocations, verification_config)
                directory = evidence.evidence_directory(root, case_id, method_id, run_index)
                evidence.save_evidence(records, directory)
                evidence.save_verification_result(verification, directory)
                collected += 1
                print(f"collected {case_id}/{method_id} run {run_index:02d}: {verification.status}")
                if verification.status != "collected":
                    failures += 1
    print(f"collected evidence for {collected} run(s)")
    return EXIT_FAILURE if failures else EXIT_SUCCESS


def _cmd_evaluate_implementations(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_evaluation")
    root = config.paths.artifacts_root
    evaluator = config.implementation_evaluator
    client = LLMClient(
        endpoint=evaluator.api_url,
        model_name=evaluator.model_name,
        api_key=evaluator.api_key,
        timeout_seconds=evaluator.timeout_seconds,
    )

    failures = 0
    for case_id, method_id in _combinations(config, args):
        reviewed = report.load_reviewed_srs(root, case_id, method_id)
        if reviewed is None:
            print(f"skip {case_id}/{method_id}: no reviewed SRS")
            continue

        scenarios = report.load_scenarios(root, case_id, method_id)
        evaluations = _evaluate_method(root, reviewed, scenarios, evaluator, client)
        directory = evaluate.evaluation_directory(root, case_id, method_id)
        evaluate.save_evaluations(evaluations, directory)
        _discard_reviewed_judgments(directory)
        failed = [evaluation for evaluation in evaluations if evaluation.status != "success"]
        failures += len(failed)
        print(f"evaluated {case_id}/{method_id}: {len(evaluations)} judgment(s), {len(failed)} failed")
    return EXIT_FAILURE if failures else EXIT_SUCCESS


def _cmd_export_evaluation_review(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_prepare")
    root = config.paths.artifacts_root

    exported = 0
    for case_id, method_id in _combinations(config, args):
        directory = evaluate.evaluation_directory(root, case_id, method_id)
        if not (directory / evaluate.EVALUATION_RECORDS_NAME).exists():
            print(f"skip {case_id}/{method_id}: no evaluation records")
            continue
        judgments = evaluate.load_judgments(directory)
        review.export_judgment_review(judgments, report.judgment_review_path(root, case_id, method_id))
        exported += 1
    print(f"exported {exported} judgment review table(s)")
    return EXIT_SUCCESS


def _cmd_import_evaluation_review(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_prepare")
    root = config.paths.artifacts_root

    imported = 0
    for case_id, method_id in _combinations(config, args):
        reviewed = report.load_reviewed_srs(root, case_id, method_id)
        path = report.judgment_review_path(root, case_id, method_id)
        directory = evaluate.evaluation_directory(root, case_id, method_id)
        if (
            reviewed is None
            or not path.exists()
            or not (directory / evaluate.EVALUATION_RECORDS_NAME).exists()
        ):
            print(f"skip {case_id}/{method_id}: no reviewed SRS, evaluation records or judgment review table")
            continue
        candidates = evaluate.load_judgments(directory)
        scenarios = report.load_scenarios(root, case_id, method_id)
        records = report.load_method_evidence(
            root, case_id, method_id, report.discover_run_indices(root, case_id, method_id)
        )
        judgments = review.import_judgment_review(
            path, candidates, case_id, method_id, reviewed.items, scenarios, records
        )
        review.save_reviewed_judgments(judgments, directory)
        imported += 1
        print(f"imported {case_id}/{method_id}: {len(judgments)} reviewed judgment(s)")
    return EXIT_SUCCESS


def _cmd_export_consistency(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_prepare")
    root = config.paths.artifacts_root

    exported = 0
    for case_id, method_id in _combinations(config, args):
        matrix = report.collect_method_matrix(root, case_id, method_id, report.expected_run_indices(config))
        if matrix is None:
            print(f"skip {case_id}/{method_id}: no reviewed SRS")
            continue
        evaluate.export_consistency_table(matrix, report.consistency_path(root, case_id, method_id))
        exported += 1
    print(f"exported {exported} consistency table(s)")
    return EXIT_SUCCESS


def _cmd_import_consistency(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_prepare")
    root = config.paths.artifacts_root
    expected_runs = report.expected_run_indices(config)

    checked = 0
    for case_id, method_id in _combinations(config, args):
        matrix = report.collect_method_matrix(root, case_id, method_id, expected_runs)
        path = report.consistency_path(root, case_id, method_id)
        if matrix is None or not path.exists():
            print(f"skip {case_id}/{method_id}: no reviewed SRS or consistency table")
            continue
        records = report.load_method_evidence(root, case_id, method_id, matrix.run_indices)
        conclusions = evaluate.import_consistency_table(path, matrix, records)
        checked += 1
        print(f"checked {case_id}/{method_id}: {len(conclusions)} conclusion(s)")
    return EXIT_SUCCESS


def _cmd_report(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_prepare")
    root = config.paths.artifacts_root
    expected_runs = report.expected_run_indices(config)

    coverage = report.collect_coverage(config, root)
    matrices = []
    conclusions = []
    for entry in coverage.srs_inventory:
        matrix = report.collect_method_matrix(root, entry.case_id, entry.method_id, expected_runs)
        if matrix is not None:
            matrices.append(matrix)
        conclusions.extend(report.load_conclusions(root, entry.case_id, entry.method_id, expected_runs))

    result = report.build_report(coverage, matrices, conclusions, report.report_directory(root))
    print(f"wrote {len(result.files)} report file(s) to {result.output_dir}")
    print(f"{result.pending_conclusions} conclusion(s) pending, {result.evidence_limitations} evidence limitation(s)")
    return EXIT_SUCCESS


def _cmd_verify(args: argparse.Namespace) -> int:
    config = _load_config(args.config)
    _validate(config, "validate_for_prepare")
    issues = report.verify_artifacts(config, config.paths.artifacts_root)

    for issue in issues:
        location = "/".join(part for part in (issue.case_id, issue.method_id) if part)
        run = f" run {issue.run_index:02d}" if issue.run_index is not None else ""
        print(f"{issue.issue_type}: {location}{run}: {issue.message}")
    print(f"{len(issues)} issue(s) found")
    return EXIT_FAILURE if issues else EXIT_SUCCESS


_HANDLERS = {
    "prepare": _cmd_prepare,
    "generate-srs": _cmd_generate_srs,
    "export-srs-review": _cmd_export_srs_review,
    "finalize-srs": _cmd_finalize_srs,
    "export-scenarios": _cmd_export_scenarios,
    "import-scenarios": _cmd_import_scenarios,
    "build-image": _cmd_build_image,
    "run": _cmd_run,
    "collect-evidence": _cmd_collect_evidence,
    "evaluate-implementations": _cmd_evaluate_implementations,
    "export-evaluation-review": _cmd_export_evaluation_review,
    "import-evaluation-review": _cmd_import_evaluation_review,
    "export-consistency": _cmd_export_consistency,
    "import-consistency": _cmd_import_consistency,
    "report": _cmd_report,
    "verify": _cmd_verify,
}


# --- Shared helpers -----------------------------------------------------------------


def _generation_succeeded(record_path: Path) -> bool:
    """Report whether a saved generation record marks a successful draft."""
    if not record_path.exists():
        return False
    return read_json(record_path).get("status") == "success"


def _discard_reviewed_srs(srs_dir: Path) -> None:
    """Remove the reviewed SRS and its status, which a new draft makes obsolete."""
    for name in DERIVED_REVIEW_FILES:
        path = srs_dir / name
        if path.exists():
            path.unlink()


def _discard_reviewed_judgments(evaluation_dir: Path) -> None:
    """Remove the reviewed judgments, which a new evaluation makes obsolete."""
    path = evaluation_dir / review.REVIEWED_JUDGMENTS_NAME
    if path.exists():
        path.unlink()


def _selected_tasks(
    config: RQ3Config,
    cases: Sequence[str],
    methods: Sequence[str],
    run_indices: Sequence[int],
) -> list[CodingTask]:
    """Enumerate the coding tasks of the selected runs of every reviewed SRS."""
    root = config.paths.artifacts_root
    srs_inputs = [
        report.reviewed_srs_path(root, case_id, method_id)
        for case_id in cases
        for method_id in methods
        if report.reviewed_srs_path(root, case_id, method_id).exists()
    ]
    tasks = coding.create_tasks(srs_inputs, config.coding.runs_per_srs, root)
    selected: list[CodingTask] = []
    for case_id in cases:
        for method_id in methods:
            selected.extend(coding.select_tasks(tasks, case_id=case_id, method_id=method_id, run_indices=run_indices))
    return selected


def _collect_run(
    result: CodingResult,
    scenarios: Sequence[ScenarioRecord],
    invocations: Sequence[evidence.InvocationSpec],
    verification_config: evidence.VerificationConfig,
) -> tuple[evidence.VerificationResult, list[evidence.EvidenceRecord]]:
    """Observe the build, run and scenarios of one delivered implementation."""
    verification = evidence.collect_build_run(result, verification_config)
    records = list(verification.evidence)
    for scenario in scenarios:
        invocation = _invocation_for(result, scenario, invocations)
        records.extend(evidence.collect_scenario(result, scenario, invocation, verification_config))
    return verification, records


def _invocation_for(
    result: CodingResult,
    scenario: ScenarioRecord,
    invocations: Sequence[evidence.InvocationSpec],
) -> evidence.InvocationSpec:
    """Report the invocation description that belongs to one scenario of one run."""
    for invocation in invocations:
        if (
            invocation.case_id == result.case_id
            and invocation.method_id == result.method_id
            and invocation.run_index == result.run_index
            and invocation.scenario_id == scenario.scenario_id
        ):
            return invocation
    raise ValueError(
        f"No invocation describes scenario '{scenario.scenario_id}' for "
        f"{result.case_id}/{result.method_id} run {result.run_index:02d}."
    )


def _evaluate_method(
    artifacts_root: Path,
    reviewed: srs.SRSRecord,
    scenarios: Sequence[ScenarioRecord],
    evaluator: evaluate.EvaluatorConfig,
    client: LLMClient,
) -> list[RequirementEvaluation]:
    """Judge every evaluable requirement of each recorded run of one method."""
    items = evaluate.evaluable_items(reviewed, scenarios)
    run_indices = report.discover_run_indices(artifacts_root, reviewed.case_id, reviewed.method_id)

    evaluations: list[RequirementEvaluation] = []
    for run_index in run_indices:
        result = report.load_coding_result(artifacts_root, reviewed.case_id, reviewed.method_id, run_index)
        if result is None or result.status not in CODING_SUCCESS_STATUSES:
            evaluations.extend(_coding_failure_evaluations(items, run_index, result))
            continue

        records = report.load_run_evidence(artifacts_root, reviewed.case_id, reviewed.method_id, run_index)
        for item in items:
            scenario_evidence = evaluate.gather_scenario_evidence(
                reviewed.case_id, reviewed.method_id, item, scenarios, records, run_index, artifacts_root
            )
            evaluations.append(evaluate.evaluate_requirement(item, scenario_evidence, evaluator, client=client))
    return evaluations


def _coding_failure_evaluations(
    items: Sequence[srs.SRSItem],
    run_index: int,
    result: CodingResult | None,
) -> list[RequirementEvaluation]:
    """Report that a run left no evaluable software for every requirement."""
    status = result.status if result is not None else "missing"
    reason = (
        result.reason
        if result is not None and result.reason
        else f"The run has no successful coding result (status '{status}')."
    )
    return [
        RequirementEvaluation(
            status="success",
            judgment=evaluate.coding_failure_judgment(item, run_index, reason),
            request={"requirement_id": item.requirement_id, "run_index": run_index, "coding_status": status},
        )
        for item in items
    ]


def main(argv: Sequence[str] | None = None) -> int:
    """Run one command and report its outcome as an exit code."""
    args = build_parser().parse_args(argv)
    try:
        return _HANDLERS[args.command](args)
    except UsageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_USAGE
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(main())