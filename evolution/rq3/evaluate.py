"""Requirement-level evaluation of the software that one coding run delivered.

The evaluator judges one requirement at a time from recorded observations only,
keeps the raw model exchange, and turns the resulting judgments into the review
table and the cross-run matrix that the reporting stage consumes.
"""

import json
import re
from pathlib import Path
from typing import Any, Sequence

from evolution.rq3.config import EvaluatorConfig
from evolution.rq3.llm_client import LLMClient, LLMClientError
from evolution.rq3.models import (
    ConsistencyConclusion,
    CrossRunMatrix,
    CrossRunMatrixRow,
    EvidenceRecord,
    RequirementEvaluation,
    RequirementJudgment,
    ScenarioEvidence,
    ScenarioRecord,
    SRSItem,
    SRSRecord,
    VerificationResult,
)
from evolution.rq3.storage import atomic_write_json, read_csv, read_json, write_csv

PROMPT_FILE_NAME = "evaluate_requirement.txt"
EVALUATION_RECORDS_NAME = "evaluations.json"
MAX_EVIDENCE_CHARS = 4000

OBSERVED_STATUSES = {"observed_satisfied", "observed_partial", "observed_unsatisfied"}
JUDGMENT_STATUSES = OBSERVED_STATUSES | {"not_observable", "coding_failure"}

DIMENSIONS = ("build_run", "core_requirement", "boundary_constraint", "observable_behavior")
BOUNDARY_TYPES = {"business_rule_constraint", "exception_boundary"}

CONSISTENCY_STATUSES = {
    "consistent_positive",
    "consistent_negative",
    "mixed",
    "evidence_limited",
    "not_applicable",
}
CONSISTENCY_SYMBOLS = {
    "consistent_positive": "✓",
    "consistent_negative": "✗",
    "mixed": "✗",
    "evidence_limited": "—",
    "not_applicable": "—",
}

CONSISTENCY_COLUMNS = [
    "case_id",
    "method_id",
    "dimension",
    "consistency_status",
    "run_indices",
    "requirement_ids",
    "evidence_ids",
    "rationale",
    "limitation",
]

BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip", ".gz", ".bin"}


def load_evaluation_prompt() -> str:
    """Load the system prompt that bounds the requirement judgment."""
    prompt_path = Path(__file__).resolve().parent / "prompts" / PROMPT_FILE_NAME
    return prompt_path.read_text(encoding="utf-8")


def evaluation_directory(artifacts_root: Path | str, case_id: str, method_id: str) -> Path:
    """Locate the directory that holds the judgments of one method."""
    return Path(artifacts_root).resolve() / "cases" / case_id / method_id / "evaluations"


def evaluable_items(srs: SRSRecord, scenarios: Sequence[ScenarioRecord]) -> list[SRSItem]:
    """Select the requirements that the recorded scenarios ask to evaluate."""
    required_ids = {
        scenario.requirement_id for scenario in scenarios if scenario.evaluation_scope == "required"
    }
    return [item for item in srs.items if item.requirement_id in required_ids]


def gather_scenario_evidence(
    case_id: str,
    method_id: str,
    item: SRSItem,
    scenarios: Sequence[ScenarioRecord],
    evidence: Sequence[EvidenceRecord],
    run_index: int,
    artifacts_root: Path | str,
) -> ScenarioEvidence:
    """Assemble the recorded scenarios and observations that belong to one requirement.

    Only observations that carry the same case, method, run and requirement scenes are
    attached, so the judgment rests on one delivered implementation instead of mixing
    runs or methods that share a scenario identifier.
    """
    item_scenarios = [scenario for scenario in scenarios if scenario.requirement_id == item.requirement_id]
    scenario_ids = {scenario.scenario_id for scenario in item_scenarios}
    item_evidence = [
        record
        for record in evidence
        if record.case_id == case_id
        and record.method_id == method_id
        and record.run_index == run_index
        and record.scenario_id in scenario_ids
    ]
    root = Path(artifacts_root).resolve()
    captured = {record.evidence_id: _captured_text(root, record) for record in item_evidence}
    return ScenarioEvidence(
        run_index=run_index,
        scenarios=item_scenarios,
        evidence=item_evidence,
        captured_text=captured,
    )


def build_evaluation_user_prompt(item: SRSItem, scenario_evidence: ScenarioEvidence) -> str:
    """Describe one requirement, its scenario identifiers and recorded observations."""
    lines: list[str] = [
        f"Requirement ID: {item.requirement_id}",
        f"Type: {item.type}",
        f"Status: {item.status}",
        f"Statement: {item.statement.strip()}",
        "",
        "=== Scenario Identifiers ===",
    ]
    if scenario_evidence.scenarios:
        for scenario in scenario_evidence.scenarios:
            lines.append(f"[{scenario.scenario_id}]")
            lines.append("")
    else:
        lines.append("No scenario was recorded for this requirement.")
        lines.append("")

    lines.append("=== Allowed Evidence IDs ===")
    lines.append(json.dumps([record.evidence_id for record in scenario_evidence.evidence]))
    lines.append("")
    lines.append("=== Recorded Evidence ===")
    if scenario_evidence.evidence:
        for record in scenario_evidence.evidence:
            lines.append(f"[{record.evidence_id}] ({record.evidence_type}) {record.summary}")
            lines.append(scenario_evidence.captured_text.get(record.evidence_id, ""))
            lines.append("")
    else:
        lines.append("No evidence was recorded for this requirement.")
        lines.append("")
    return "\n".join(lines)


def parse_judgment_response(
    content: str,
    item: SRSItem,
    scenario_evidence: ScenarioEvidence,
) -> RequirementJudgment:
    """Parse a model response into a judgment and check it against the offered evidence."""
    cleaned = _strip_markdown_code_fences(content)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to parse model response as JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("Model response JSON root must be an object")

    status = data.get("status")
    if status not in JUDGMENT_STATUSES:
        raise ValueError(f"Unknown judgment status '{status}'.")

    rationale = data.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        raise ValueError("Model response must provide a non-empty 'rationale'.")

    limitation = data.get("limitation", "")
    if not isinstance(limitation, str):
        raise ValueError("Model response 'limitation' must be a string.")

    raw_ids = data.get("evidence_ids", [])
    if not isinstance(raw_ids, list) or any(not isinstance(entry, str) for entry in raw_ids):
        raise ValueError("Model response 'evidence_ids' must be a list of strings.")

    offered = {record.evidence_id for record in scenario_evidence.evidence}
    unknown = [entry for entry in raw_ids if entry not in offered]
    if unknown:
        raise ValueError(f"Model cited evidence IDs that were not offered: {unknown}.")

    if status in OBSERVED_STATUSES and not raw_ids:
        raise ValueError(f"Judgment status '{status}' must cite at least one evidence ID.")

    return RequirementJudgment(
        requirement_id=item.requirement_id,
        run_index=scenario_evidence.run_index,
        status=status,
        evidence_ids=raw_ids,
        rationale=rationale.strip(),
        limitation=limitation.strip(),
    )


def evaluate_requirement(
    item: SRSItem,
    scenario_evidence: ScenarioEvidence,
    evaluator_config: EvaluatorConfig,
    client: LLMClient | None = None,
) -> RequirementEvaluation:
    """Judge one requirement from the observations recorded for one run.

    A requirement without any recorded observation keeps a program-produced
    not_observable judgment, because the model only interprets observed text.
    """
    evaluator_config.validate_executable()

    system_prompt = load_evaluation_prompt()
    user_prompt = build_evaluation_user_prompt(item, scenario_evidence)
    request_payload = {
        "model": evaluator_config.model_name,
        "requirement_id": item.requirement_id,
        "run_index": scenario_evidence.run_index,
        "evidence_ids": [record.evidence_id for record in scenario_evidence.evidence],
        "temperature": 0.0,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    if not any(record.evidence_type != "observation_limit" for record in scenario_evidence.evidence):
        return RequirementEvaluation(
            status="success",
            judgment=RequirementJudgment(
                requirement_id=item.requirement_id,
                run_index=scenario_evidence.run_index,
                status="not_observable",
                evidence_ids=[record.evidence_id for record in scenario_evidence.evidence],
                rationale="No observation was recorded for the scenarios of this requirement.",
                limitation="\n".join(record.summary for record in scenario_evidence.evidence)
                or "The delivered software produced no evidence for the recorded scenarios.",
            ),
            request=request_payload,
        )

    if client is None:
        client = LLMClient(
            endpoint=evaluator_config.api_url,
            model_name=evaluator_config.model_name,
            api_key=evaluator_config.api_key,
            timeout_seconds=evaluator_config.timeout_seconds,
        )

    try:
        response = client.complete(system_prompt, user_prompt, temperature=0.0)
    except LLMClientError as exc:
        return RequirementEvaluation(
            status="failed",
            request=request_payload,
            raw_response=exc.raw_response,
            error=str(exc),
        )
    except Exception as exc:
        return RequirementEvaluation(
            status="failed",
            request=request_payload,
            error=f"Unexpected evaluation failure: {exc}",
        )

    if not response.content or not response.content.strip():
        return RequirementEvaluation(
            status="failed",
            request=request_payload,
            raw_response=response.raw_response,
            usage=response.usage,
            error="Model returned empty response content",
        )

    try:
        judgment = parse_judgment_response(response.content, item, scenario_evidence)
    except ValueError as exc:
        return RequirementEvaluation(
            status="failed",
            request=request_payload,
            raw_response=response.raw_response,
            usage=response.usage,
            error=str(exc),
        )

    return RequirementEvaluation(
        status="success",
        judgment=judgment,
        request=request_payload,
        raw_response=response.raw_response,
        usage=response.usage,
    )


def coding_failure_judgment(item: SRSItem, run_index: int, reason: str) -> RequirementJudgment:
    """Report that one run left no evaluable software for this requirement."""
    return RequirementJudgment(
        requirement_id=item.requirement_id,
        run_index=run_index,
        status="coding_failure",
        evidence_ids=[],
        rationale=reason,
        limitation="",
    )


def save_evaluations(evaluations: Sequence[RequirementEvaluation], output_dir: Path | str) -> None:
    """Write the requirement evaluations of one method together with their raw model exchange."""
    atomic_write_json(
        Path(output_dir).resolve() / EVALUATION_RECORDS_NAME,
        [evaluation.model_dump(mode="json") for evaluation in evaluations],
    )


def load_judgments(output_dir: Path | str) -> list[RequirementJudgment]:
    """Read the candidate judgments saved for one method."""
    data: Any = read_json(Path(output_dir).resolve() / EVALUATION_RECORDS_NAME)
    judgments: list[RequirementJudgment] = []
    for entry in data:
        evaluation = RequirementEvaluation.model_validate(entry)
        if evaluation.judgment is not None:
            judgments.append(evaluation.judgment)
    return judgments


def build_cross_run_matrix(
    srs: SRSRecord,
    scenarios: Sequence[ScenarioRecord],
    judgments: Sequence[RequirementJudgment],
    verification_results: Sequence[VerificationResult] = (),
    expected_run_indices: Sequence[int] = (),
) -> CrossRunMatrix:
    """Expand the recorded judgments into the four-direction comparison grid.

    The run columns come from the runs the experiment expected together with the runs
    that reported something, so a run without any record still shows empty cells.
    Build and run are reported separately, because a run that only built is not a run
    that started, and a delivery may declare no build command at all. A verification
    result of another case or method is rejected instead of being folded into this grid.
    """
    for result in verification_results:
        if (result.case_id, result.method_id) != (srs.case_id, srs.method_id):
            raise ValueError(
                f"Verification result of {result.case_id}/{result.method_id} does not belong to "
                f"{srs.case_id}/{srs.method_id}."
            )

    run_indices = sorted(
        set(expected_run_indices)
        | {judgment.run_index for judgment in judgments}
        | {result.run_index for result in verification_results}
    )
    verification_by_run = {result.run_index: result for result in verification_results}
    status_by_key = {
        (judgment.requirement_id, judgment.run_index): judgment.status for judgment in judgments
    }
    required_ids = {
        scenario.requirement_id for scenario in scenarios if scenario.evaluation_scope == "required"
    }

    core_ids = _ordered_ids(srs, {scenario.requirement_id for scenario in scenarios if scenario.is_core})
    boundary_ids = _ordered_ids(
        srs,
        {
            item.requirement_id
            for item in srs.items
            if item.type in BOUNDARY_TYPES and item.requirement_id in required_ids
        },
    )
    observable_ids = _ordered_ids(srs, required_ids)

    rows: list[CrossRunMatrixRow] = []
    for dimension, requirement_ids in (
        ("core_requirement", core_ids),
        ("boundary_constraint", boundary_ids),
        ("observable_behavior", observable_ids),
    ):
        for requirement_id in requirement_ids:
            rows.append(
                CrossRunMatrixRow(
                    requirement_id=requirement_id,
                    dimension=dimension,
                    statuses=[status_by_key.get((requirement_id, index)) for index in run_indices],
                )
            )

    return CrossRunMatrix(
        case_id=srs.case_id,
        method_id=srs.method_id,
        run_indices=run_indices,
        build=[_build_status(verification_by_run.get(index)) for index in run_indices],
        run=[_run_status(verification_by_run.get(index)) for index in run_indices],
        rows=rows,
    )


def export_consistency_table(matrix: CrossRunMatrix, output_csv: Path | str) -> None:
    """Export the four-direction table of one method, preserving filled conclusions.

    The table describes the case and method of the matrix. Rows already answered by a
    reviewer keep their status, rationale and limitation; the remaining rows are
    written with the reference data of the matrix.
    """
    target_path = Path(output_csv).resolve()
    existing: dict[str, dict[str, str]] = {}
    if target_path.exists():
        for row in read_csv(target_path):
            if (
                row.get("case_id", "").strip() == matrix.case_id
                and row.get("method_id", "").strip() == matrix.method_id
            ):
                existing[row.get("dimension", "").strip()] = row

    references = consistency_references(matrix)
    rows: list[dict[str, Any]] = []
    for dimension in DIMENSIONS:
        filled = existing.get(dimension)
        if filled and filled.get("consistency_status", "").strip():
            rows.append({column: filled.get(column, "") for column in CONSISTENCY_COLUMNS})
            continue
        run_indices, requirement_ids = references[dimension]
        rows.append(
            {
                "case_id": matrix.case_id,
                "method_id": matrix.method_id,
                "dimension": dimension,
                "consistency_status": "",
                "run_indices": join_id_list([str(index) for index in run_indices]),
                "requirement_ids": join_id_list(requirement_ids),
                "evidence_ids": "",
                "rationale": "",
                "limitation": "",
            }
        )

    write_csv(target_path, rows, CONSISTENCY_COLUMNS)


def import_consistency_table(
    path: Path | str,
    matrix: CrossRunMatrix,
    evidence: Sequence[EvidenceRecord],
) -> list[ConsistencyConclusion]:
    """Read the filled four-direction conclusions of one method and check their references.

    Every reference must exist for the case and method that the matrix describes: run
    indices must be runs of the matrix, requirement identifiers must belong to the
    dimension they are written for, and evidence identifiers must be observations of
    this method that belong to the runs the row itself references. Rows whose
    consistency_status is still empty are reference rows that the reviewer has not
    answered yet, so they are skipped instead of rejected.
    """
    resolved_path = Path(path).resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f"Consistency table not found: {resolved_path}")

    dimension_requirements = {
        dimension: {row.requirement_id for row in matrix.rows if row.dimension == dimension}
        for dimension in DIMENSIONS
    }

    conclusions: list[ConsistencyConclusion] = []
    seen: set[tuple[str, str, str]] = set()
    for index, row in enumerate(read_csv(resolved_path), start=1):
        case_id = row.get("case_id", "").strip()
        method_id = row.get("method_id", "").strip()
        dimension = row.get("dimension", "").strip()
        status = row.get("consistency_status", "").strip()

        if (case_id, method_id) != (matrix.case_id, matrix.method_id):
            raise ValueError(
                f"Row {index} describes {case_id}/{method_id}, which is not the "
                f"{matrix.case_id}/{matrix.method_id} that the matrix holds."
            )
        if dimension not in DIMENSIONS:
            raise ValueError(f"Row {index} has unknown dimension '{dimension}'.")
        if not status:
            continue
        if status not in CONSISTENCY_STATUSES:
            raise ValueError(f"Row {index} has unknown consistency_status '{status}'.")

        key = (case_id, method_id, dimension)
        if key in seen:
            raise ValueError(f"Row {index} repeats the conclusion for {key}.")
        seen.add(key)

        run_indices = _parse_integers(row.get("run_indices", ""), index)
        unknown_runs = [value for value in run_indices if value not in matrix.run_indices]
        if unknown_runs:
            raise ValueError(f"Row {index} cites runs that the matrix does not hold: {unknown_runs}.")

        requirement_ids = split_id_list(row.get("requirement_ids", ""))
        unknown_requirements = [
            value for value in requirement_ids if value not in dimension_requirements[dimension]
        ]
        if unknown_requirements:
            raise ValueError(
                f"Row {index} cites requirements that are not part of dimension "
                f"'{dimension}': {unknown_requirements}."
            )

        evidence_ids = split_id_list(row.get("evidence_ids", ""))
        run_scoped_evidence = {
            record.evidence_id
            for record in evidence
            if record.case_id == matrix.case_id
            and record.method_id == matrix.method_id
            and record.run_index in run_indices
        }
        unknown_evidence = [value for value in evidence_ids if value not in run_scoped_evidence]
        if unknown_evidence:
            raise ValueError(
                f"Row {index} cites evidence that was not recorded for the runs it references "
                f"({', '.join(str(value) for value in run_indices)}): {unknown_evidence}."
            )

        conclusions.append(
            ConsistencyConclusion(
                case_id=case_id,
                method_id=method_id,
                dimension=dimension,
                consistency_status=status,
                run_indices=run_indices,
                requirement_ids=requirement_ids,
                evidence_ids=evidence_ids,
                rationale=row.get("rationale", "").strip(),
                limitation=row.get("limitation", "").strip(),
            )
        )
    return conclusions


def split_id_list(text: str) -> list[str]:
    """Split a spreadsheet cell that lists identifiers separated by semicolons or commas."""
    return [entry.strip() for entry in re.split(r"[;,]", text) if entry.strip()]


def join_id_list(entries: Sequence[str]) -> str:
    """Join identifiers into a spreadsheet cell that split_id_list reads back."""
    return "; ".join(entries)


def _build_status(result: VerificationResult | None) -> str | None:
    """Report the build outcome that was observed for one run."""
    return _command_status(result, "build")


def _run_status(result: VerificationResult | None) -> str | None:
    """Report the run outcome that was observed for one run."""
    return _command_status(result, "run")


def _command_status(result: VerificationResult | None, field_name: str) -> str | None:
    """Translate one entry of a run's verification into a matrix cell.

    An empty cell marks a run that reported nothing, and a delivery that declared no
    such command is reported as undeclared instead of as a successful execution.
    """
    if result is None:
        return None
    if result.status != "collected":
        return result.status
    log = result.build if field_name == "build" else result.run
    if log is None:
        return "not_declared"
    if log.timed_out:
        return "timed_out"
    return "succeeded" if log.returncode == 0 else "failed"


def _ordered_ids(srs: SRSRecord, requirement_ids: set[str]) -> list[str]:
    """Keep the identifiers of one dimension in the order of the requirement document."""
    return [item.requirement_id for item in srs.items if item.requirement_id in requirement_ids]


def consistency_references(matrix: CrossRunMatrix) -> dict[str, tuple[list[int], list[str]]]:
    """Derive the reference runs and requirements of each consistency dimension."""
    references: dict[str, tuple[list[int], list[str]]] = {
        "build_run": (
            [
                index
                for position, index in enumerate(matrix.run_indices)
                if matrix.build[position] or matrix.run[position]
            ],
            [],
        )
    }
    for dimension in ("core_requirement", "boundary_constraint", "observable_behavior"):
        rows = [row for row in matrix.rows if row.dimension == dimension]
        indices = [
            index
            for position, index in enumerate(matrix.run_indices)
            if any(row.statuses[position] for row in rows)
        ]
        references[dimension] = (indices, [row.requirement_id for row in rows])
    return references


def _captured_text(artifacts_root: Path, record: EvidenceRecord) -> str:
    """Read the content of one evidence artifact for the model prompt."""
    path = artifacts_root / record.relative_path
    if not path.exists():
        return f"[{record.evidence_type} artifact {record.relative_path} is not present]"
    if path.suffix.lower() in BINARY_SUFFIXES:
        return f"[{record.evidence_type} artifact of {path.stat().st_size} byte(s)]"
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > MAX_EVIDENCE_CHARS:
        return text[:MAX_EVIDENCE_CHARS] + "\n[truncated]"
    return text


def _parse_integers(text: str, index: int) -> list[int]:
    """Parse a spreadsheet cell that lists run indices."""
    values: list[int] = []
    for entry in split_id_list(text):
        try:
            values.append(int(entry))
        except ValueError as exc:
            raise ValueError(f"Row {index} has a non-numeric run index '{entry}'.") from exc
    return values


def _strip_markdown_code_fences(text: str) -> str:
    """Strip markdown code fence blocks if wrapped around JSON."""
    cleaned = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if match:
        return match.group(1).strip()
    return cleaned
