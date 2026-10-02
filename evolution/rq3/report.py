"""Coverage, four-direction views and artifact checks for the RQ3 workflow.

Reporting reads the artifacts that the earlier stages stored. It describes how much
of the configured scope is present, pairs each cross-run matrix with the recorded
four-direction conclusions, and checks the stored files, references and pending
records. It starts no model call, no container and no coding task.
"""

import re
from pathlib import Path
from typing import Any, Sequence

from evolution.rq3.config import RQ3Config
from evolution.rq3.evaluate import (
    CONSISTENCY_SYMBOLS,
    DIMENSIONS,
    EVALUATION_RECORDS_NAME,
    build_cross_run_matrix,
    consistency_references,
    evaluable_items,
    evaluation_directory,
    import_consistency_table,
    join_id_list,
    load_judgments,
)
from evolution.rq3.evidence import (
    BUILD_RUN_SCENARIO,
    EVIDENCE_RECORDS_NAME,
    VERIFICATION_RECORD_NAME,
    evidence_directory,
    load_evidence,
    load_verification_result,
    run_directory,
)
from evolution.rq3.ingest import load_cases
from evolution.rq3.models import (
    CodingResult,
    ConsistencyConclusion,
    CoverageReport,
    CrossRunMatrix,
    EnvironmentRecord,
    EvidenceIndexEntry,
    EvidenceRecord,
    InputItem,
    ReportResult,
    RequirementJudgment,
    RunCoverage,
    SRSInventoryEntry,
    SRSRecord,
    ScenarioRecord,
    TranscriptRecord,
    VerificationIssue,
    VerificationResult,
)
from evolution.rq3.review import (
    REVIEWED_JUDGMENTS_NAME,
    SCENARIO_REQUIRED_FIELDS,
    import_judgment_review,
    load_reviewed_judgments,
    read_scenarios,
    stale_review_rows,
)
from evolution.rq3.storage import atomic_write_json, atomic_write_text, read_csv, read_json, write_csv

REPO_ROOT = Path(__file__).resolve().parents[2]

INPUT_COVERAGE_COLUMNS = [
    "case_id",
    "method_id",
    "source_status",
    "completed_turns",
    "prepare_status",
    "reason",
]
SRS_INVENTORY_COLUMNS = [
    "case_id",
    "method_id",
    "project_name",
    "srs_status",
    "item_count",
    "requirement_ids",
    "scenario_count",
    "pending_scenario_fields",
    "unresolved_reviews",
]
RUN_COVERAGE_COLUMNS = [
    "case_id",
    "method_id",
    "run_index",
    "coding_status",
    "build",
    "run",
    "evidence_count",
    "judgment_count",
]
CONSISTENCY_VIEW_COLUMNS = [
    "case_id",
    "method_id",
    "dimension",
    "symbol",
    "consistency_status",
    "run_indices",
    "requirement_ids",
    "evidence_ids",
    "rationale",
    "limitation",
]
EVIDENCE_COLUMNS = [
    "case_id",
    "method_id",
    "run_index",
    "scenario_id",
    "evidence_id",
    "evidence_type",
    "relative_path",
    "status",
    "detail",
]

REPORT_FILES = [
    "input_coverage.csv",
    "srs_inventory.csv",
    "run_coverage.csv",
    "method_case_consistency.csv",
    "evidence_limitations.csv",
    "environment.json",
    "rq3_report.md",
]

PREPARE_STATUSES = {"ready", "source_incomplete", "input_error", "not_prepared"}
PENDING_STATUS = "pending"
PENDING_SYMBOL = "?"
MISSING_VALUE = "missing"
NOT_PREPARED_REASON = "No prepared input was recorded for this case and method."

SRS_DIRECTORY_NAME = "srs"
RUN_DIRECTORY_PATTERN = re.compile(r"^run_(\d+)$")


# --- Artifact layout ---------------------------------------------------------------


def method_directory(artifacts_root: Path | str, case_id: str, method_id: str) -> Path:
    """Locate the directory that holds the artifacts of one case and method."""
    return Path(artifacts_root).resolve() / "cases" / case_id / method_id


def input_inventory_path(artifacts_root: Path | str) -> Path:
    """Locate the input inventory that preparation writes."""
    return Path(artifacts_root).resolve() / "input_inventory.csv"


def transcript_path(artifacts_root: Path | str, case_id: str, method_id: str) -> Path:
    """Locate the standardized transcript of one case and method."""
    return method_directory(artifacts_root, case_id, method_id) / "transcript.json"


def srs_directory(artifacts_root: Path | str, case_id: str, method_id: str) -> Path:
    """Locate the directory that holds the requirement artifacts of one method."""
    return method_directory(artifacts_root, case_id, method_id) / SRS_DIRECTORY_NAME


def draft_srs_path(artifacts_root: Path | str, case_id: str, method_id: str) -> Path:
    """Locate the draft SRS that generation writes."""
    return srs_directory(artifacts_root, case_id, method_id) / "draft_srs.json"


def reviewed_srs_path(artifacts_root: Path | str, case_id: str, method_id: str) -> Path:
    """Locate the reviewed SRS that the applied review writes."""
    return srs_directory(artifacts_root, case_id, method_id) / "reviewed_srs.json"


def srs_review_path(artifacts_root: Path | str, case_id: str, method_id: str) -> Path:
    """Locate the item review table of one method."""
    return srs_directory(artifacts_root, case_id, method_id) / "srs_review.csv"


def scenarios_path(artifacts_root: Path | str, case_id: str, method_id: str) -> Path:
    """Locate the observation scenario table of one method."""
    return srs_directory(artifacts_root, case_id, method_id) / "scenarios.csv"


def judgment_review_path(artifacts_root: Path | str, case_id: str, method_id: str) -> Path:
    """Locate the requirement judgment review table of one method."""
    return evaluation_directory(artifacts_root, case_id, method_id) / "judgment_review.csv"


def consistency_path(artifacts_root: Path | str, case_id: str, method_id: str) -> Path:
    """Locate the four-direction conclusion table of one method."""
    return evaluation_directory(artifacts_root, case_id, method_id) / "consistency.csv"


def report_directory(artifacts_root: Path | str) -> Path:
    """Locate the directory that receives the report views."""
    return Path(artifacts_root).resolve() / "reports"


# --- Reading stored artifacts ------------------------------------------------------


def load_coding_result(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
    run_index: int,
) -> CodingResult | None:
    """Read the result of one coding run, or report that the run has no result."""
    path = run_directory(artifacts_root, case_id, method_id, run_index) / "result.json"
    if not path.exists():
        return None
    return CodingResult.model_validate(read_json(path))


def load_transcript(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
) -> TranscriptRecord | None:
    """Read the standardized transcript of one case and method."""
    path = transcript_path(artifacts_root, case_id, method_id)
    if not path.exists():
        return None
    return TranscriptRecord.model_validate(read_json(path))


def load_draft_srs(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
) -> SRSRecord | None:
    """Read the draft SRS of one method."""
    path = draft_srs_path(artifacts_root, case_id, method_id)
    if not path.exists():
        return None
    return SRSRecord.model_validate(read_json(path))


def load_reviewed_srs(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
) -> SRSRecord | None:
    """Read the reviewed SRS of one method."""
    path = reviewed_srs_path(artifacts_root, case_id, method_id)
    if not path.exists():
        return None
    return SRSRecord.model_validate(read_json(path))


def load_scenarios(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
    require_filled: bool = True,
) -> list[ScenarioRecord]:
    """Read the observation scenarios of one method.

    Report and verification describe a scenario table that is still a template, so they
    read it with the filled requirement turned off and keep the empty fields. Importing
    and executing scenarios read the same table with the filled requirement on.
    """
    path = scenarios_path(artifacts_root, case_id, method_id)
    if not path.exists():
        return []
    return read_scenarios(path, load_reviewed_srs(artifacts_root, case_id, method_id), require_filled=require_filled)


def load_effective_judgments(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
) -> list[RequirementJudgment]:
    """Read the judgments of one method, preferring the reviewed ones.

    A method whose review was imported keeps both its candidate judgments and the
    confirmed ones. The confirmed judgments describe the reviewed state, so they
    replace the candidates wherever results are built from judgments.
    """
    directory = evaluation_directory(artifacts_root, case_id, method_id)
    reviewed = load_reviewed_judgments(directory)
    if reviewed is not None:
        return reviewed
    if not (directory / EVALUATION_RECORDS_NAME).exists():
        return []
    return load_judgments(directory)


def load_run_evidence(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
    run_index: int,
) -> list[EvidenceRecord]:
    """Read the evidence records of one coding run, or report that none were saved."""
    directory = evidence_directory(artifacts_root, case_id, method_id, run_index)
    if not (directory / EVIDENCE_RECORDS_NAME).exists():
        return []
    return load_evidence(directory)


def load_method_evidence(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
    run_indices: Sequence[int],
) -> list[EvidenceRecord]:
    """Read the evidence records of several runs of one method."""
    records: list[EvidenceRecord] = []
    for run_index in run_indices:
        records.extend(load_run_evidence(artifacts_root, case_id, method_id, run_index))
    return records


def load_run_verification(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
    run_index: int,
) -> VerificationResult | None:
    """Read the build and run verification of one run, or report that none was saved."""
    path = evidence_directory(artifacts_root, case_id, method_id, run_index) / VERIFICATION_RECORD_NAME
    if not path.exists():
        return None
    return load_verification_result(path.parent)


def discover_run_indices(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
    expected_run_indices: Sequence[int] = (),
) -> list[int]:
    """Report the runs that the recorded artifacts describe together with the expected ones.

    A run that only holds a workspace, a result or evidence still counts as recorded,
    so a partly finished scope shows its own state instead of disappearing.
    """
    indices = set(expected_run_indices)
    indices |= _runs_on_disk(method_directory(artifacts_root, case_id, method_id))
    indices |= {
        judgment.run_index
        for judgment in load_effective_judgments(artifacts_root, case_id, method_id)
    }
    return sorted(indices)


def collect_method_matrix(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
    expected_run_indices: Sequence[int] = (),
) -> CrossRunMatrix | None:
    """Build the cross-run matrix of one method from its stored artifacts."""
    srs = load_reviewed_srs(artifacts_root, case_id, method_id)
    if srs is None:
        return None
    run_indices = discover_run_indices(artifacts_root, case_id, method_id, expected_run_indices)
    verifications = [
        verification
        for verification in (
            load_run_verification(artifacts_root, case_id, method_id, index) for index in run_indices
        )
        if verification is not None
    ]
    return build_cross_run_matrix(
        srs,
        load_scenarios(artifacts_root, case_id, method_id, require_filled=False),
        load_effective_judgments(artifacts_root, case_id, method_id),
        verifications,
        expected_run_indices=run_indices,
    )


def load_conclusions(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
    expected_run_indices: Sequence[int] = (),
) -> list[ConsistencyConclusion]:
    """Read the filled four-direction conclusions of one method."""
    matrix = collect_method_matrix(artifacts_root, case_id, method_id, expected_run_indices)
    if matrix is None:
        return []
    path = consistency_path(artifacts_root, case_id, method_id)
    if not path.exists():
        return []
    return import_consistency_table(
        path,
        matrix,
        load_method_evidence(artifacts_root, case_id, method_id, matrix.run_indices),
    )


# --- Coverage ----------------------------------------------------------------------


def collect_coverage(config: RQ3Config, artifacts_root: Path | str) -> CoverageReport:
    """Describe the configured scope and the state of the artifacts recorded for it."""
    config.validate_for_prepare()
    root = Path(artifacts_root).resolve()
    expected_runs = expected_run_indices(config)
    inventory = _load_inventory(root)

    input_items: list[InputItem] = []
    srs_inventory: list[SRSInventoryEntry] = []
    runs: list[RunCoverage] = []
    evidence_index: list[EvidenceIndexEntry] = []

    for case in load_cases(config.paths.cases_file):
        for method_id in config.methods:
            input_items.append(
                _input_item(case.case_id, method_id, inventory.get((case.case_id, method_id)))
            )
            srs_inventory.append(_srs_inventory_entry(root, case.case_id, method_id))
            judgments = load_effective_judgments(root, case.case_id, method_id)
            for run_index in discover_run_indices(root, case.case_id, method_id, expected_runs):
                coding = load_coding_result(root, case.case_id, method_id, run_index)
                records = load_run_evidence(root, case.case_id, method_id, run_index)
                runs.append(
                    RunCoverage(
                        case_id=case.case_id,
                        method_id=method_id,
                        run_index=run_index,
                        coding_status=coding.status if coding is not None else MISSING_VALUE,
                        evidence_count=len(records),
                        judgment_count=sum(
                            1 for judgment in judgments if judgment.run_index == run_index
                        ),
                    )
                )
                evidence_index.extend(
                    _evidence_index(root, case.case_id, method_id, run_index, records)
                )

    return CoverageReport(
        environment=_environment(config),
        input_items=input_items,
        srs_inventory=srs_inventory,
        runs=runs,
        evidence=evidence_index,
    )


def expected_run_indices(config: RQ3Config) -> list[int]:
    """Report the runs that the configuration expects for every reviewed SRS."""
    if config.coding is None:
        return []
    return list(range(1, config.coding.runs_per_srs + 1))


def _without_host_prefix(path: Path) -> str:
    """Render a configured path without the host directory prefix."""
    return path.as_posix().replace(REPO_ROOT.as_posix() + "/", "")


def _environment(config: RQ3Config) -> EnvironmentRecord:
    """Describe the configuration that the recorded artifacts were produced with."""
    return EnvironmentRecord(
        cases_file=_without_host_prefix(config.paths.cases_file),
        results_root=_without_host_prefix(config.paths.results_root),
        artifacts_root=_without_host_prefix(config.paths.artifacts_root),
        methods=list(config.methods),
        runs_per_srs=config.coding.runs_per_srs if config.coding is not None else 0,
        artifact_processor_model=(
            config.artifact_processor.model_name if config.artifact_processor is not None else ""
        ),
        coding_model=config.coding.model_name if config.coding is not None else "",
        implementation_evaluator_model=(
            config.implementation_evaluator.model_name
            if config.implementation_evaluator is not None
            else ""
        ),
        container_image=config.coding.image if config.coding is not None else "",
        container_network=config.coding.network if config.coding is not None else "",
    )


def _load_inventory(artifacts_root: Path) -> dict[tuple[str, str], dict[str, str]]:
    """Index the recorded input inventory by case and method."""
    path = input_inventory_path(artifacts_root)
    if not path.exists():
        return {}
    return {
        (row.get("case_id", "").strip(), row.get("method_id", "").strip()): row
        for row in read_csv(path)
    }


def _input_item(case_id: str, method_id: str, row: dict[str, str] | None) -> InputItem:
    """Describe the prepared input state of one case and method."""
    if row is None:
        return InputItem(
            case_id=case_id,
            method_id=method_id,
            source_status="",
            completed_turns="",
            prepare_status="not_prepared",
            reason=NOT_PREPARED_REASON,
        )

    status = row.get("prepare_status", "").strip()
    if status not in PREPARE_STATUSES:
        raise ValueError(
            f"Input inventory row for {case_id}/{method_id} has unknown "
            f"prepare_status '{status}'."
        )
    return InputItem(
        case_id=case_id,
        method_id=method_id,
        source_status=row.get("source_status", "").strip(),
        completed_turns=row.get("completed_turns", "").strip(),
        prepare_status=status,
        reason=row.get("reason", "").strip(),
    )


def _srs_inventory_entry(artifacts_root: Path, case_id: str, method_id: str) -> SRSInventoryEntry:
    """Describe the requirement artifacts recorded for one method."""
    reviewed = load_reviewed_srs(artifacts_root, case_id, method_id)
    draft = load_draft_srs(artifacts_root, case_id, method_id)
    srs = reviewed or draft
    if reviewed is not None:
        srs_status = "reviewed"
    elif draft is not None:
        srs_status = "draft"
    else:
        srs_status = MISSING_VALUE

    scenarios = load_scenarios(artifacts_root, case_id, method_id, require_filled=False)
    return SRSInventoryEntry(
        case_id=case_id,
        method_id=method_id,
        project_name=srs.project_name if srs is not None else "",
        srs_status=srs_status,
        item_count=len(srs.items) if srs is not None else 0,
        requirement_ids=[item.requirement_id for item in srs.items] if srs is not None else [],
        scenario_count=len(scenarios),
        pending_scenario_fields=_pending_scenario_fields(scenarios),
        unresolved_reviews=len(
            _unfilled_rows(srs_review_path(artifacts_root, case_id, method_id), "decision")
        ),
    )


def _pending_scenario_fields(scenarios: Sequence[ScenarioRecord]) -> list[str]:
    """Report the scenario table columns that still hold an empty cell."""
    return [
        field
        for field in SCENARIO_REQUIRED_FIELDS
        if any(not getattr(scenario, field) for scenario in scenarios)
    ]


def _evidence_index(
    artifacts_root: Path,
    case_id: str,
    method_id: str,
    run_index: int,
    records: Sequence[EvidenceRecord],
) -> list[EvidenceIndexEntry]:
    """Index the evidence artifacts of one run and the state of its build and run check."""
    entries: list[EvidenceIndexEntry] = []
    for record in records:
        present = (artifacts_root / record.relative_path).exists()
        entries.append(
            EvidenceIndexEntry(
                case_id=case_id,
                method_id=method_id,
                run_index=run_index,
                scenario_id=record.scenario_id,
                evidence_id=record.evidence_id,
                evidence_type=record.evidence_type,
                relative_path=record.relative_path,
                status="recorded" if present else "artifact_missing",
                detail="" if present else "The recorded artifact is not present in the artifacts root.",
            )
        )

    verification = load_run_verification(artifacts_root, case_id, method_id, run_index)
    limitation = _verification_limitation(verification)
    if limitation:
        entries.append(
            EvidenceIndexEntry(
                case_id=case_id,
                method_id=method_id,
                run_index=run_index,
                scenario_id="",
                evidence_id="",
                evidence_type="",
                relative_path=Path(
                    evidence_directory(artifacts_root, case_id, method_id, run_index)
                )
                .relative_to(artifacts_root)
                .as_posix(),
                status="collection_incomplete",
                detail=limitation,
            )
        )
    return entries


def _verification_limitation(verification: VerificationResult | None) -> str:
    """Report why the build and run check of one run is not a complete collection."""
    if verification is None:
        return "No build and run verification was recorded for this run."
    if verification.status != "collected":
        return verification.error or f"The build and run verification reported '{verification.status}'."

    notes: list[str] = []
    for label, log in (("build", verification.build), ("run", verification.run)):
        if log is None:
            continue
        if log.timed_out:
            notes.append(f"The {label} command exceeded its timeout.")
        elif log.returncode != 0:
            notes.append(f"The {label} command exited with code {log.returncode}.")
    return " ".join(notes)


def _runs_on_disk(method_dir: Path) -> set[int]:
    """Report the run directories that hold artifacts of one method."""
    runs_dir = method_dir / "runs"
    if not runs_dir.is_dir():
        return set()
    indices: set[int] = set()
    for path in runs_dir.iterdir():
        match = RUN_DIRECTORY_PATTERN.match(path.name)
        if match and path.is_dir():
            indices.add(int(match.group(1)))
    return indices


def _unfilled_rows(path: Path, column: str) -> list[dict[str, str]]:
    """Report the rows of a filling table whose column is still empty."""
    if not path.exists():
        return []
    return [row for row in read_csv(path) if not (row.get(column) or "").strip()]


# --- Report views ------------------------------------------------------------------


def build_report(
    coverage: CoverageReport,
    matrices: Sequence[CrossRunMatrix],
    conclusions: Sequence[ConsistencyConclusion],
    output_dir: Path | str,
) -> ReportResult:
    """Write the coverage tables, the four-direction view and the markdown report."""
    target = Path(output_dir).resolve()
    target.mkdir(parents=True, exist_ok=True)

    matrices_by_key = {(matrix.case_id, matrix.method_id): matrix for matrix in matrices}
    run_rows = [
        _run_coverage_row(run, matrices_by_key.get((run.case_id, run.method_id)))
        for run in coverage.runs
    ]
    consistency_rows, pending = _consistency_view(coverage, matrices_by_key, conclusions)
    evidence_rows, limitations = _evidence_rows(coverage.evidence)

    write_csv(
        target / "input_coverage.csv",
        [item.to_row() for item in coverage.input_items],
        INPUT_COVERAGE_COLUMNS,
    )
    write_csv(
        target / "srs_inventory.csv",
        [_srs_inventory_row(entry) for entry in coverage.srs_inventory],
        SRS_INVENTORY_COLUMNS,
    )
    write_csv(target / "run_coverage.csv", run_rows, RUN_COVERAGE_COLUMNS)
    write_csv(target / "method_case_consistency.csv", consistency_rows, CONSISTENCY_VIEW_COLUMNS)
    write_csv(target / "evidence_limitations.csv", evidence_rows, EVIDENCE_COLUMNS)
    atomic_write_json(target / "environment.json", coverage.environment)
    atomic_write_text(
        target / "rq3_report.md",
        _render_report(coverage, run_rows, consistency_rows, evidence_rows),
    )

    return ReportResult(
        output_dir=str(target),
        files=list(REPORT_FILES),
        pending_conclusions=pending,
        evidence_limitations=limitations,
    )


def _run_coverage_row(run: RunCoverage, matrix: CrossRunMatrix | None) -> dict[str, str]:
    """Describe one run together with the build and run state of its verification."""
    build_cell = ""
    run_cell = ""
    if matrix is not None and run.run_index in matrix.run_indices:
        position = matrix.run_indices.index(run.run_index)
        build_cell = matrix.build[position] or ""
        run_cell = matrix.run[position] or ""
    return {
        "case_id": run.case_id,
        "method_id": run.method_id,
        "run_index": str(run.run_index),
        "coding_status": run.coding_status,
        "build": build_cell,
        "run": run_cell,
        "evidence_count": str(run.evidence_count),
        "judgment_count": str(run.judgment_count),
    }


def _srs_inventory_row(entry: SRSInventoryEntry) -> dict[str, str]:
    """Describe one method's requirement artifacts as a report row."""
    return {
        "case_id": entry.case_id,
        "method_id": entry.method_id,
        "project_name": entry.project_name,
        "srs_status": entry.srs_status,
        "item_count": str(entry.item_count),
        "requirement_ids": join_id_list(entry.requirement_ids),
        "scenario_count": str(entry.scenario_count),
        "pending_scenario_fields": join_id_list(entry.pending_scenario_fields),
        "unresolved_reviews": str(entry.unresolved_reviews),
    }


def _consistency_view(
    coverage: CoverageReport,
    matrices_by_key: dict[tuple[str, str], CrossRunMatrix],
    conclusions: Sequence[ConsistencyConclusion],
) -> tuple[list[dict[str, str]], int]:
    """Pair every dimension of every method with its recorded conclusion.

    A dimension without a recorded conclusion keeps the reference runs and
    requirements of its matrix and is reported as pending, so an unanswered
    dimension is never read as a negative result.
    """
    filled_by_key = {
        (conclusion.case_id, conclusion.method_id, conclusion.dimension): conclusion
        for conclusion in conclusions
    }
    rows: list[dict[str, str]] = []
    pending = 0

    for entry in coverage.srs_inventory:
        key = (entry.case_id, entry.method_id)
        matrix = matrices_by_key.get(key)
        references = (
            consistency_references(matrix)
            if matrix is not None
            else {dimension: ([], []) for dimension in DIMENSIONS}
        )
        for dimension in DIMENSIONS:
            filled = filled_by_key.get((entry.case_id, entry.method_id, dimension))
            if filled is None:
                pending += 1
                run_indices, requirement_ids = references[dimension]
                rows.append(
                    {
                        "case_id": entry.case_id,
                        "method_id": entry.method_id,
                        "dimension": dimension,
                        "symbol": PENDING_SYMBOL,
                        "consistency_status": PENDING_STATUS,
                        "run_indices": join_id_list([str(index) for index in run_indices]),
                        "requirement_ids": join_id_list(requirement_ids),
                        "evidence_ids": "",
                        "rationale": "",
                        "limitation": "",
                    }
                )
                continue

            rows.append(
                {
                    "case_id": filled.case_id,
                    "method_id": filled.method_id,
                    "dimension": filled.dimension,
                    "symbol": CONSISTENCY_SYMBOLS[filled.consistency_status],
                    "consistency_status": filled.consistency_status,
                    "run_indices": join_id_list([str(index) for index in filled.run_indices]),
                    "requirement_ids": join_id_list(filled.requirement_ids),
                    "evidence_ids": join_id_list(filled.evidence_ids),
                    "rationale": filled.rationale,
                    "limitation": filled.limitation,
                }
            )

    return rows, pending


def _evidence_rows(entries: Sequence[EvidenceIndexEntry]) -> tuple[list[dict[str, str]], int]:
    """Describe the indexed evidence artifacts and count the incomplete ones."""
    rows = [
        {
            "case_id": entry.case_id,
            "method_id": entry.method_id,
            "run_index": str(entry.run_index),
            "scenario_id": entry.scenario_id,
            "evidence_id": entry.evidence_id,
            "evidence_type": entry.evidence_type,
            "relative_path": entry.relative_path,
            "status": entry.status,
            "detail": entry.detail,
        }
        for entry in entries
    ]
    limitations = sum(1 for entry in entries if entry.status != "recorded")
    return rows, limitations


def _render_report(
    coverage: CoverageReport,
    run_rows: Sequence[dict[str, str]],
    consistency_rows: Sequence[dict[str, str]],
    evidence_rows: Sequence[dict[str, str]],
) -> str:
    """Render the coverage tables and the four-direction view as markdown."""
    environment = coverage.environment
    lines: list[str] = [
        "# RQ3 Evaluation Report",
        "",
        "## Environment",
        "",
        f"- Artifacts root: `{environment.artifacts_root}`",
        f"- Source results root: `{environment.results_root}`",
        f"- Case file: `{environment.cases_file}`",
        f"- Methods: {', '.join(environment.methods) or 'none'}",
        f"- Runs per SRS: {environment.runs_per_srs}",
        f"- Artifact processor model: {environment.artifact_processor_model or 'not configured'}",
        f"- Coding model: {environment.coding_model or 'not configured'}",
        f"- Evaluator model: {environment.implementation_evaluator_model or 'not configured'}",
        f"- Container image: {environment.container_image or 'not configured'}",
        f"- Container network: {environment.container_network or 'not configured'}",
        "",
        "Evidence paths in the tables below are relative to the artifacts root.",
        "",
        "## Input coverage",
        "",
    ]
    lines.extend(
        _markdown_table(
            INPUT_COVERAGE_COLUMNS,
            [item.to_row() for item in coverage.input_items],
        )
    )
    lines.extend(["", "## SRS inventory", ""])
    lines.extend(
        _markdown_table(
            SRS_INVENTORY_COLUMNS,
            [_srs_inventory_row(entry) for entry in coverage.srs_inventory],
        )
    )
    lines.extend(["", "## Run coverage", ""])
    lines.extend(_markdown_table(RUN_COVERAGE_COLUMNS, run_rows))
    lines.extend(
        [
            "",
            "## Four-direction comparison",
            "",
            "An unanswered dimension is reported as `pending`; a symbol of `?` means that no",
            "conclusion was recorded and is not an observed failure.",
            "",
        ]
    )
    lines.extend(_markdown_table(CONSISTENCY_VIEW_COLUMNS, consistency_rows))
    lines.extend(
        [
            "",
            "## Evidence limitations",
            "",
            "`recorded` marks an artifact that is present, `artifact_missing` marks a record whose",
            "file is absent, and `collection_incomplete` marks a run whose build and run check did",
            "not complete or did not succeed.",
            "",
        ]
    )
    lines.extend(_markdown_table(EVIDENCE_COLUMNS, evidence_rows))
    lines.append("")
    return "\n".join(lines)


def _markdown_table(columns: Sequence[str], rows: Sequence[dict[str, str]]) -> list[str]:
    """Render rows as a markdown table with the given columns."""
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(_cell(row.get(column, "")) for column in columns) + " |")
    return lines


def _cell(value: Any) -> str:
    """Render one table cell without breaking the markdown row."""
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


# --- Artifact verification ---------------------------------------------------------


def verify_artifacts(config: RQ3Config, artifacts_root: Path | str) -> list[VerificationIssue]:
    """Check the stored artifacts for missing files, broken references and pending records."""
    config.validate_for_prepare()
    root = Path(artifacts_root).resolve()
    expected_runs = expected_run_indices(config)

    issues: list[VerificationIssue] = []
    inventory_path = input_inventory_path(root)
    if not inventory_path.exists():
        issues.append(
            VerificationIssue(
                issue_type="missing_input_inventory",
                message=f"{inventory_path} does not exist; prepare has not recorded any input.",
            )
        )

    inventory = _load_inventory(root)
    for case in load_cases(config.paths.cases_file):
        for method_id in config.methods:
            issues.extend(
                _verify_combination(
                    root,
                    case.case_id,
                    method_id,
                    inventory.get((case.case_id, method_id)),
                    expected_runs,
                )
            )
    return issues


def _verify_combination(
    artifacts_root: Path,
    case_id: str,
    method_id: str,
    row: dict[str, str] | None,
    expected_run_indices: Sequence[int],
) -> list[VerificationIssue]:
    """Check one case and method against the artifacts recorded for it."""
    issues: list[VerificationIssue] = []
    prepared = row is not None and row.get("prepare_status", "").strip() == "ready"

    if row is None:
        issues.append(
            _issue(
                "missing_inventory_entry",
                "No input inventory row was recorded for this case and method.",
                case_id,
                method_id,
            )
        )
    elif row.get("prepare_status", "").strip() == "input_error":
        issues.append(
            _issue(
                "input_error",
                row.get("reason", "").strip() or "The input of this case and method is damaged.",
                case_id,
                method_id,
            )
        )

    if prepared:
        transcript_file = transcript_path(artifacts_root, case_id, method_id)
        if not transcript_file.exists():
            issues.append(
                _issue(
                    "missing_transcript",
                    f"{transcript_file} does not exist.",
                    case_id,
                    method_id,
                )
            )
        else:
            issues.extend(_verify_transcript(transcript_file, case_id, method_id))

    reviewed = load_reviewed_srs(artifacts_root, case_id, method_id)
    if prepared and reviewed is None:
        issue_type = (
            "unreviewed_srs"
            if load_draft_srs(artifacts_root, case_id, method_id) is not None
            else "missing_srs"
        )
        message = (
            "Only a draft SRS exists; the reviewed SRS has not been written."
            if issue_type == "unreviewed_srs"
            else "No draft and no reviewed SRS was recorded."
        )
        issues.append(_issue(issue_type, message, case_id, method_id))

    issues.extend(_verify_srs_review(artifacts_root, case_id, method_id))
    issues.extend(_verify_evidence(artifacts_root, case_id, method_id, reviewed, expected_run_indices))
    issues.extend(_verify_method_products(artifacts_root, case_id, method_id, reviewed))
    issues.extend(_verify_judgment_review(artifacts_root, case_id, method_id, reviewed))
    issues.extend(_verify_conclusions(artifacts_root, case_id, method_id, reviewed, expected_run_indices))
    return issues


def _verify_transcript(path: Path, case_id: str, method_id: str) -> list[VerificationIssue]:
    """Check that a prepared transcript holds a readable message stream."""
    try:
        TranscriptRecord.model_validate(read_json(path))
    except (ValueError, OSError) as exc:
        return [
            _issue(
                "invalid_transcript",
                f"{path} is not a readable transcript: {exc}",
                case_id,
                method_id,
            )
        ]
    return []


def _verify_srs_review(artifacts_root: Path, case_id: str, method_id: str) -> list[VerificationIssue]:
    """Report item rows that a reviewer has not decided yet."""
    return [
        _issue(
            "unfilled_review_decision",
            f"Requirement '{row.get('requirement_id', '').strip()}' has no review decision.",
            case_id,
            method_id,
        )
        for row in _unfilled_rows(srs_review_path(artifacts_root, case_id, method_id), "decision")
    ]


def _verify_evidence(
    artifacts_root: Path,
    case_id: str,
    method_id: str,
    reviewed: SRSRecord | None,
    expected_run_indices: Sequence[int],
) -> list[VerificationIssue]:
    """Check the recorded runs, their evidence files and their scenario references."""
    issues: list[VerificationIssue] = []
    scenarios = load_scenarios(artifacts_root, case_id, method_id, require_filled=False)
    scenario_ids = {scenario.scenario_id for scenario in scenarios}
    known_requirements = {item.requirement_id for item in reviewed.items} if reviewed is not None else None

    for scenario in scenarios:
        if known_requirements is not None and scenario.requirement_id not in known_requirements:
            issues.append(
                _issue(
                    "unknown_requirement_reference",
                    f"Scenario '{scenario.scenario_id}' refers to requirement "
                    f"'{scenario.requirement_id}', which the reviewed SRS does not hold.",
                    case_id,
                    method_id,
                )
            )

    run_indices = discover_run_indices(artifacts_root, case_id, method_id, expected_run_indices)
    for run_index in run_indices:
        result = load_coding_result(artifacts_root, case_id, method_id, run_index)
        if result is None:
            issues.append(
                _issue(
                    "missing_coding_result",
                    "The run has no coding result record.",
                    case_id,
                    method_id,
                    run_index,
                )
            )
        else:
            issues.extend(_verify_run_products(artifacts_root, case_id, method_id, run_index))
        for record in load_run_evidence(artifacts_root, case_id, method_id, run_index):
            if not (artifacts_root / record.relative_path).exists():
                issues.append(
                    _issue(
                        "missing_evidence_artifact",
                        f"Evidence '{record.evidence_id}' refers to "
                        f"'{record.relative_path}', which does not exist.",
                        case_id,
                        method_id,
                        run_index,
                    )
                )
            if (
                scenarios
                and record.scenario_id != BUILD_RUN_SCENARIO
                and record.scenario_id not in scenario_ids
            ):
                issues.append(
                    _issue(
                        "unknown_scenario_reference",
                        f"Evidence '{record.evidence_id}' refers to scenario "
                        f"'{record.scenario_id}', which the method does not hold.",
                        case_id,
                        method_id,
                        run_index,
                    )
                )
    return issues


def _verify_run_products(
    artifacts_root: Path,
    case_id: str,
    method_id: str,
    run_index: int,
) -> list[VerificationIssue]:
    """Report the evidence files that a run with a coding result still lacks."""
    directory = evidence_directory(artifacts_root, case_id, method_id, run_index)
    expected = (
        (directory / EVIDENCE_RECORDS_NAME, "missing_evidence_records", "recorded evidence"),
        (directory / VERIFICATION_RECORD_NAME, "missing_verification_record", "build and run verification"),
    )
    return [
        _issue(issue_type, f"The run has no {label} file at {path}.", case_id, method_id, run_index)
        for path, issue_type, label in expected
        if not path.exists()
    ]


def _verify_method_products(
    artifacts_root: Path,
    case_id: str,
    method_id: str,
    reviewed: SRSRecord | None,
) -> list[VerificationIssue]:
    """Report the downstream products that a reviewed SRS makes expected."""
    if reviewed is None:
        return []
    directory = evaluation_directory(artifacts_root, case_id, method_id)
    expected = (
        (directory / EVALUATION_RECORDS_NAME, "missing_evaluation_records"),
        (judgment_review_path(artifacts_root, case_id, method_id), "missing_judgment_review"),
        (directory / REVIEWED_JUDGMENTS_NAME, "missing_reviewed_judgments"),
        (consistency_path(artifacts_root, case_id, method_id), "missing_consistency_table"),
    )
    return [
        _issue(issue_type, f"{path} does not exist.", case_id, method_id)
        for path, issue_type in expected
        if not path.exists()
    ]


def _verify_judgment_review(
    artifacts_root: Path,
    case_id: str,
    method_id: str,
    reviewed: SRSRecord | None,
) -> list[VerificationIssue]:
    """Check the judgment review table for pending rows, replaced candidates and broken references."""
    path = judgment_review_path(artifacts_root, case_id, method_id)
    issues = [
        _issue(
            "unfilled_judgment_decision",
            f"Judgment for requirement '{row.get('requirement_id', '').strip()}' in run "
            f"{row.get('run_index', '').strip()} has no review decision.",
            case_id,
            method_id,
        )
        for row in _unfilled_rows(path, "decision")
    ]
    if reviewed is None or not path.exists():
        return issues

    directory = evaluation_directory(artifacts_root, case_id, method_id)
    if not (directory / EVALUATION_RECORDS_NAME).exists():
        return issues
    candidates = load_judgments(directory)
    stale = stale_review_rows(path, candidates)
    if stale:
        issues.extend(
            _issue(
                "stale_judgment_review",
                "The judgment review table does not describe the current candidate judgments: "
                f"{location}. Export the table from the current evaluations.",
                case_id,
                method_id,
            )
            for location in stale
        )
        return issues

    scenarios = load_scenarios(artifacts_root, case_id, method_id, require_filled=False)
    records = load_method_evidence(
        artifacts_root,
        case_id,
        method_id,
        discover_run_indices(artifacts_root, case_id, method_id),
    )
    try:
        import_judgment_review(path, candidates, case_id, method_id, reviewed.items, scenarios, records)
    except ValueError as exc:
        issues.append(_issue("invalid_judgment_reference", str(exc), case_id, method_id))

    issues.extend(_verify_judgment_coverage(artifacts_root, case_id, method_id, reviewed, scenarios))
    return issues


def _verify_judgment_coverage(
    artifacts_root: Path,
    case_id: str,
    method_id: str,
    reviewed: SRSRecord,
    scenarios: Sequence[ScenarioRecord],
) -> list[VerificationIssue]:
    """Report the evaluable requirements that no judgment covers for a run with a result."""
    items = evaluable_items(reviewed, scenarios)
    covered = {
        (judgment.requirement_id, judgment.run_index)
        for judgment in load_effective_judgments(artifacts_root, case_id, method_id)
    }
    issues: list[VerificationIssue] = []
    for run_index in discover_run_indices(artifacts_root, case_id, method_id):
        if load_coding_result(artifacts_root, case_id, method_id, run_index) is None:
            continue
        for item in items:
            if (item.requirement_id, run_index) not in covered:
                issues.append(
                    _issue(
                        "missing_requirement_judgment",
                        f"Requirement '{item.requirement_id}' has no judgment for run {run_index:02d}.",
                        case_id,
                        method_id,
                        run_index,
                    )
                )
    return issues


def _verify_conclusions(
    artifacts_root: Path,
    case_id: str,
    method_id: str,
    reviewed: SRSRecord | None,
    expected_run_indices: Sequence[int],
) -> list[VerificationIssue]:
    """Check the four-direction conclusion table for pending rows, broken references and coverage."""
    path = consistency_path(artifacts_root, case_id, method_id)
    issues = [
        _issue(
            "unfilled_conclusion",
            f"Dimension '{row.get('dimension', '').strip()}' has no consistency status.",
            case_id,
            method_id,
        )
        for row in _unfilled_rows(path, "consistency_status")
    ]
    if reviewed is None or not path.exists():
        return issues

    matrix = collect_method_matrix(artifacts_root, case_id, method_id, expected_run_indices)
    if matrix is None:
        return issues

    records = load_method_evidence(artifacts_root, case_id, method_id, matrix.run_indices)
    try:
        import_consistency_table(path, matrix, records)
    except ValueError as exc:
        issues.append(_issue("invalid_conclusion_reference", str(exc), case_id, method_id))

    issues.extend(_verify_conclusion_coverage(path, matrix))
    return issues


def _verify_conclusion_coverage(path: Path, matrix: CrossRunMatrix) -> list[VerificationIssue]:
    """Report the comparison dimensions that the conclusion table does not list."""
    listed = {row.get("dimension", "").strip() for row in read_csv(path)}
    return [
        _issue(
            "missing_conclusion_row",
            f"Dimension '{dimension}' has no row in the conclusion table.",
            matrix.case_id,
            matrix.method_id,
        )
        for dimension in DIMENSIONS
        if dimension not in listed
    ]


def _issue(
    issue_type: str,
    message: str,
    case_id: str = "",
    method_id: str = "",
    run_index: int | None = None,
) -> VerificationIssue:
    """Compose one artifact verification issue."""
    return VerificationIssue(
        issue_type=issue_type,
        message=message,
        case_id=case_id,
        method_id=method_id,
        run_index=run_index,
    )