import csv
import json
from pathlib import Path
from typing import Any, Sequence

from evolution.rq3.evaluate import (
    JUDGMENT_STATUSES,
    OBSERVED_STATUSES,
    join_id_list,
    split_id_list,
)
from evolution.rq3.models import (
    EvidenceRecord,
    RequirementJudgment,
    ReviewedSRSResult,
    SRSItem,
    SRSRecord,
    SRSReviewDecision,
    ScenarioRecord,
    SourceEvidence,
    TranscriptRecord,
)
from evolution.rq3.srs import VALID_STATUSES, VALID_TYPES, render_srs, validate_srs
from evolution.rq3.storage import atomic_write_json, atomic_write_text, read_csv, read_json, write_csv

REVIEW_COLUMNS = [
    "requirement_id",
    "type",
    "statement",
    "status",
    "evidence_summary",
    "decision",
    "revised_type",
    "revised_statement",
    "revised_status",
    "revised_evidence_json",
    "notes",
]

SCENARIO_COLUMNS = [
    "requirement_id",
    "evaluation_scope",
    "is_core",
    "scenario_id",
    "setup",
    "action",
    "expected_observation",
]

ALLOWED_DECISIONS = {"accept", "revise", "delete", "regenerate_document"}
ALLOWED_SCOPES = {"required", "context_only", "unresolved"}
SCENARIO_REQUIRED_FIELDS = ("action", "expected_observation")

JUDGMENT_COLUMNS = [
    "requirement_id",
    "run_index",
    "status",
    "evidence_ids",
    "rationale",
    "limitation",
    "decision",
    "revised_status",
    "revised_evidence_ids",
    "revised_rationale",
    "revised_limitation",
    "notes",
]

ALLOWED_JUDGMENT_DECISIONS = {"accept", "revise"}

REVIEWED_JUDGMENTS_NAME = "reviewed_judgments.json"


def export_srs_review(
    draft: SRSRecord,
    transcript: TranscriptRecord,
    output_csv: Path | str,
) -> None:
    """Export draft SRS items into a review CSV table, preserving user edits if draft content matches."""
    target_path = Path(output_csv).resolve()

    existing_decisions: dict[str, dict[str, str]] = {}
    if target_path.exists():
        for row in read_csv(target_path):
            req_id = row.get("requirement_id", "").strip()
            if req_id:
                existing_decisions[req_id] = row

    rows: list[dict[str, Any]] = []
    for item in draft.items:
        req_id = item.requirement_id
        evidence_summary = "; ".join(
            f"[{ev.source_kind}:{ev.source_id}] {ev.evidence_span}" for ev in item.source_evidence
        )

        existing = existing_decisions.get(req_id, {})
        matches_baseline = (
            bool(existing.get("type", "").strip())
            and existing.get("type", "").strip() == item.type
            and bool(existing.get("statement", "").strip())
            and existing.get("statement", "").strip() == item.statement
            and bool(existing.get("status", "").strip())
            and existing.get("status", "").strip() == item.status
            and bool(existing.get("evidence_summary", "").strip())
            and existing.get("evidence_summary", "").strip() == evidence_summary
        )

        if matches_baseline:
            row = {
                "requirement_id": req_id,
                "type": item.type,
                "statement": item.statement,
                "status": item.status,
                "evidence_summary": evidence_summary,
                "decision": existing.get("decision", ""),
                "revised_type": existing.get("revised_type", ""),
                "revised_statement": existing.get("revised_statement", ""),
                "revised_status": existing.get("revised_status", ""),
                "revised_evidence_json": existing.get("revised_evidence_json", ""),
                "notes": existing.get("notes", ""),
            }
        else:
            row = {
                "requirement_id": req_id,
                "type": item.type,
                "statement": item.statement,
                "status": item.status,
                "evidence_summary": evidence_summary,
                "decision": "",
                "revised_type": "",
                "revised_statement": "",
                "revised_status": "",
                "revised_evidence_json": "",
                "notes": "",
            }
        rows.append(row)

    write_csv(target_path, rows, REVIEW_COLUMNS)


def read_srs_review(path: Path | str) -> list[SRSReviewDecision]:
    """Read review decisions from a CSV spreadsheet."""
    resolved_path = Path(path).resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f"Review CSV not found: {resolved_path}")

    raw_rows = read_csv(resolved_path)
    decisions: list[SRSReviewDecision] = []

    for idx, row in enumerate(raw_rows, start=1):
        req_id = row.get("requirement_id", "").strip()
        decision_val = row.get("decision", "").strip()

        if not req_id:
            raise ValueError(f"Missing 'requirement_id' in review CSV at line {idx}")

        if decision_val and decision_val not in ALLOWED_DECISIONS:
            raise ValueError(
                f"Unknown decision '{decision_val}' at line {idx} for {req_id}. "
                f"Allowed: {sorted(ALLOWED_DECISIONS)}"
            )

        decisions.append(
            SRSReviewDecision(
                requirement_id=req_id,
                type=row.get("type", "").strip(),
                statement=row.get("statement", "").strip(),
                status=row.get("status", "").strip(),
                evidence_summary=row.get("evidence_summary", "").strip(),
                decision=decision_val,
                revised_type=row.get("revised_type", "").strip(),
                revised_statement=row.get("revised_statement", "").strip(),
                revised_status=row.get("revised_status", "").strip(),
                revised_evidence_json=row.get("revised_evidence_json", "").strip(),
                notes=row.get("notes", "").strip(),
            )
        )

    return decisions


def apply_srs_review(
    draft: SRSRecord,
    decisions: list[SRSReviewDecision],
    transcript: TranscriptRecord,
) -> ReviewedSRSResult:
    """Apply human review decisions to produce a finalized reviewed SRSRecord."""
    errors: list[str] = []
    decision_map: dict[str, SRSReviewDecision] = {}
    draft_item_map = {item.requirement_id: item for item in draft.items}

    # 1. Check for unknown and duplicate requirement IDs
    for d in decisions:
        if d.requirement_id not in draft_item_map:
            errors.append(f"Review decision contains unknown requirement_id '{d.requirement_id}' not found in draft")
        if d.requirement_id in decision_map:
            errors.append(f"Duplicate decision for requirement_id '{d.requirement_id}'")
        decision_map[d.requirement_id] = d

    # 2. Check that all draft items have a review decision and baseline fields match exactly
    for item in draft.items:
        req_id = item.requirement_id
        if req_id not in decision_map:
            errors.append(f"Missing review decision for requirement '{req_id}'")
            continue

        decision = decision_map[req_id]
        evidence_summary = "; ".join(
            f"[{ev.source_kind}:{ev.source_id}] {ev.evidence_span}" for ev in item.source_evidence
        )

        if not decision.type or decision.type != item.type:
            errors.append(
                f"Requirement '{req_id}' review record type does not match draft (expected '{item.type}', got '{decision.type}')"
            )
        if not decision.statement or decision.statement != item.statement:
            errors.append(
                f"Requirement '{req_id}' review record statement does not match draft"
            )
        if not decision.status or decision.status != item.status:
            errors.append(
                f"Requirement '{req_id}' review record status does not match draft (expected '{item.status}', got '{decision.status}')"
            )
        if not decision.evidence_summary or decision.evidence_summary != evidence_summary:
            errors.append(
                f"Requirement '{req_id}' review record evidence_summary does not match draft"
            )

        dec_type = decision.decision
        if not dec_type:
            errors.append(f"Requirement '{req_id}' has no review decision (decision is empty)")
        elif dec_type not in ALLOWED_DECISIONS:
            errors.append(f"Invalid decision '{dec_type}' for requirement '{req_id}'")

    # If baseline or decision errors exist, return before considering regeneration
    if errors:
        return ReviewedSRSResult(
            status="review_incomplete",
            errors=errors,
        )

    # 3. Check for valid regenerate_document decision
    for d in decisions:
        if d.decision == "regenerate_document":
            return ReviewedSRSResult(
                status="needs_regeneration",
                errors=[f"Document regeneration requested for requirement '{d.requirement_id}': {d.notes}"],
            )

    # 4. Process accept, revise, delete
    reviewed_items: list[SRSItem] = []

    for item in draft.items:
        req_id = item.requirement_id
        decision = decision_map[req_id]
        dec_type = decision.decision

        if dec_type == "accept":
            reviewed_items.append(item)
        elif dec_type == "delete":
            continue
        elif dec_type == "revise":
            revised_statement = decision.revised_statement.strip()
            if not revised_statement:
                errors.append(f"Revise decision for '{req_id}' must provide a non-empty revised_statement")

            revised_type = decision.revised_type.strip()
            if not revised_type:
                errors.append(f"Revise decision for '{req_id}' must provide revised_type")
            elif revised_type not in VALID_TYPES:
                errors.append(f"Revise decision for '{req_id}' specifies invalid revised_type '{decision.revised_type}'")

            revised_status = decision.revised_status.strip()
            if not revised_status:
                errors.append(f"Revise decision for '{req_id}' must provide revised_status")
            elif revised_status not in VALID_STATUSES:
                errors.append(f"Revise decision for '{req_id}' specifies invalid revised_status '{decision.revised_status}'")

            if revised_status == "unresolved" and revised_type != "unresolved_information":
                errors.append(f"Requirement '{req_id}': status 'unresolved' is only allowed for type 'unresolved_information'")
            if revised_type == "unresolved_information" and revised_status != "unresolved":
                errors.append(f"Requirement '{req_id}': type 'unresolved_information' must have status 'unresolved'")

            revised_evidence_json = decision.revised_evidence_json.strip()
            if not revised_evidence_json:
                errors.append(f"Revise decision for '{req_id}' must provide revised_evidence_json")
                continue

            try:
                ev_data = json.loads(revised_evidence_json)
                if not isinstance(ev_data, list) or not ev_data:
                    errors.append(f"revised_evidence_json for '{req_id}' must be a non-empty JSON array")
                    continue
                revised_evidence = [SourceEvidence.model_validate(e) for e in ev_data]
            except Exception as exc:
                errors.append(f"Failed to parse revised_evidence_json for '{req_id}': {exc}")
                continue

            if not errors:
                try:
                    revised_item = SRSItem(
                        requirement_id=req_id,
                        type=revised_type,  # type: ignore[arg-type]
                        statement=revised_statement,
                        status=revised_status,  # type: ignore[arg-type]
                        source_evidence=revised_evidence,
                    )
                    reviewed_items.append(revised_item)
                except Exception as exc:
                    errors.append(f"Validation failed for revised requirement '{req_id}': {exc}")

    if errors:
        return ReviewedSRSResult(
            status="review_incomplete",
            errors=errors,
        )

    reviewed_srs = SRSRecord(
        case_id=draft.case_id,
        method_id=draft.method_id,
        project_name=draft.project_name,
        items=reviewed_items,
    )

    validation_issues = validate_srs(reviewed_srs, transcript)
    if validation_issues:
        val_errors = [f"{iss.field}: {iss.message}" for iss in validation_issues]
        return ReviewedSRSResult(
            status="review_incomplete",
            errors=val_errors,
        )

    return ReviewedSRSResult(
        status="reviewed",
        reviewed_srs=reviewed_srs,
    )


def save_reviewed_srs(result: ReviewedSRSResult, output_dir: Path | str) -> None:
    """Save finalized reviewed SRS artifacts (JSON and coding-facing Markdown)."""
    target_dir = Path(output_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    status_data = {
        "status": result.status,
        "errors": result.errors,
    }
    atomic_write_json(target_dir / "review_status.json", status_data)

    if result.status == "reviewed" and result.reviewed_srs is not None:
        atomic_write_json(target_dir / "reviewed_srs.json", result.reviewed_srs)
        coding_markdown = render_srs(result.reviewed_srs, include_evidence=False)
        atomic_write_text(target_dir / "reviewed_srs.md", coding_markdown)


def export_scenarios_template(
    srs: SRSRecord,
    output_csv: Path | str,
) -> None:
    """Export an observation scenario template CSV based on reviewed SRS items."""
    target_path = Path(output_csv).resolve()

    existing_rows: dict[str, dict[str, str]] = {}
    if target_path.exists():
        for row in read_csv(target_path):
            sc_id = row.get("scenario_id", "").strip()
            if sc_id:
                existing_rows[sc_id] = row

    rows: list[dict[str, Any]] = []
    sc_counter = 1

    for item in srs.items:
        req_id = item.requirement_id
        scope = "unresolved" if item.type == "unresolved_information" else (
            "context_only" if item.type in ("scope_context", "stakeholder_actor") else "required"
        )
        is_core = item.type == "functional_requirement"

        matched = [r for r in existing_rows.values() if r.get("requirement_id") == req_id]
        if matched:
            rows.extend(matched)
        else:
            default_sc_id = f"SCEN-{req_id}-{sc_counter:02d}"
            rows.append({
                "requirement_id": req_id,
                "evaluation_scope": scope,
                "is_core": "true" if is_core else "false",
                "scenario_id": default_sc_id,
                "setup": "",
                "action": "",
                "expected_observation": "",
            })
            sc_counter += 1

    write_csv(target_path, rows, SCENARIO_COLUMNS)


def read_scenarios(
    path: Path | str,
    srs: SRSRecord | None = None,
    require_filled: bool = True,
) -> list[ScenarioRecord]:
    """Read and validate observation scenario records from CSV.

    The scenario identity, its scope and its core flag are always checked. A table that
    is still a template is read with require_filled false, so its rows keep empty action
    and expectation and a report can name the fields that are still open.
    """
    resolved_path = Path(path).resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f"Scenarios CSV not found: {resolved_path}")

    raw_rows = read_csv(resolved_path)
    scenarios: list[ScenarioRecord] = []
    seen_sc_ids: set[str] = set()
    valid_req_ids = {item.requirement_id for item in srs.items} if srs is not None else None

    for idx, row in enumerate(raw_rows, start=1):
        req_id = row.get("requirement_id", "").strip()
        sc_id = row.get("scenario_id", "").strip()
        scope = row.get("evaluation_scope", "").strip()
        is_core_raw = row.get("is_core", "").strip().lower()

        if not req_id:
            raise ValueError(f"Row {idx} is missing requirement_id")
        if valid_req_ids is not None and req_id not in valid_req_ids:
            raise ValueError(f"Row {idx} requirement_id '{req_id}' does not exist in reviewed SRS")

        if not sc_id:
            raise ValueError(f"Row {idx} is missing scenario_id")
        if sc_id in seen_sc_ids:
            raise ValueError(f"Duplicate scenario_id '{sc_id}' at row {idx}")
        seen_sc_ids.add(sc_id)

        if scope not in ALLOWED_SCOPES:
            raise ValueError(f"Row {idx} invalid evaluation_scope '{scope}', allowed: {sorted(ALLOWED_SCOPES)}")

        if is_core_raw in ("true", "1"):
            is_core = True
        elif is_core_raw in ("false", "0"):
            is_core = False
        else:
            raise ValueError(
                f"Row {idx} invalid boolean value '{row.get('is_core')}' for 'is_core', must be 'true' or 'false'"
            )

        if require_filled:
            for field in SCENARIO_REQUIRED_FIELDS:
                if not (row.get(field, "") or "").strip():
                    raise ValueError(f"Row {idx} is missing required '{field}'")

        scenarios.append(
            ScenarioRecord(
                requirement_id=req_id,
                evaluation_scope=scope,  # type: ignore[arg-type]
                is_core=is_core,
                scenario_id=sc_id,
                setup=row.get("setup", "").strip(),
                action=row.get("action", "").strip(),
                expected_observation=row.get("expected_observation", "").strip(),
            )
        )

    return scenarios


def write_scenarios(
    path: Path | str,
    scenarios: list[ScenarioRecord],
) -> None:
    """Write scenario records to a CSV file."""
    rows = [sc.to_row() for sc in scenarios]
    write_csv(path, rows, SCENARIO_COLUMNS)


def export_judgment_review(
    judgments: Sequence[RequirementJudgment],
    output_csv: Path | str,
) -> None:
    """Export candidate judgments into a review CSV table.

    A row keeps the reviewer decision and the revised fields only while the candidate
    status, evidence, rationale and limitation stay the same. A candidate that the
    evaluation changed requires a fresh review, so its decision is cleared. The notes
    stay, because they are reviewer commentary rather than a decision.
    """
    target_path = Path(output_csv).resolve()

    existing: dict[tuple[str, str], dict[str, str]] = {}
    if target_path.exists():
        for row in read_csv(target_path):
            key = (row.get("requirement_id", "").strip(), row.get("run_index", "").strip())
            existing[key] = row

    rows: list[dict[str, Any]] = []
    for judgment in judgments:
        match = existing.get((judgment.requirement_id, str(judgment.run_index)), {})
        reviewed = _reviewed_candidate(match, judgment)
        rows.append(
            {
                "requirement_id": judgment.requirement_id,
                "run_index": str(judgment.run_index),
                "status": judgment.status,
                "evidence_ids": join_id_list(judgment.evidence_ids),
                "rationale": judgment.rationale,
                "limitation": judgment.limitation,
                "decision": reviewed.get("decision", "").strip(),
                "revised_status": reviewed.get("revised_status", "").strip(),
                "revised_evidence_ids": reviewed.get("revised_evidence_ids", "").strip(),
                "revised_rationale": reviewed.get("revised_rationale", "").strip(),
                "revised_limitation": reviewed.get("revised_limitation", "").strip(),
                "notes": match.get("notes", "").strip(),
            }
        )

    write_csv(target_path, rows, JUDGMENT_COLUMNS)


def _reviewed_candidate(row: dict[str, str], judgment: RequirementJudgment) -> dict[str, str]:
    """Return the earlier review of a row only while the candidate judgment is unchanged."""
    if row.get("status", "").strip() != judgment.status:
        return {}
    if row.get("evidence_ids", "").strip() != join_id_list(judgment.evidence_ids):
        return {}
    if row.get("rationale", "").strip() != judgment.rationale:
        return {}
    if row.get("limitation", "").strip() != judgment.limitation:
        return {}
    return row


def stale_review_rows(
    path: Path | str,
    candidates: Sequence[RequirementJudgment],
) -> list[str]:
    """Report the review rows that do not describe the current candidate judgments.

    A table is filled against the candidates of one evaluation and is exported again
    whenever an evaluation replaces them. A row whose recorded status, evidence,
    rationale or limitation differs from the candidate of the same requirement and run,
    or that has no candidate at all, was filled against an earlier evaluation.
    """
    resolved_path = Path(path).resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f"Judgment review CSV not found: {resolved_path}")

    current = {(judgment.requirement_id, str(judgment.run_index)): judgment for judgment in candidates}
    stale: list[str] = []
    for row in read_csv(resolved_path):
        requirement_id = row.get("requirement_id", "").strip()
        run_text = row.get("run_index", "").strip()
        judgment = current.get((requirement_id, run_text))
        unchanged = judgment is not None and bool(_reviewed_candidate(row, judgment))
        if not unchanged:
            stale.append(f"requirement '{requirement_id}' in run '{run_text}'")
    return stale


def import_judgment_review(
    path: Path | str,
    candidates: Sequence[RequirementJudgment],
    case_id: str,
    method_id: str,
    requirements: Sequence[SRSItem],
    scenarios: Sequence[ScenarioRecord],
    evidence: Sequence[EvidenceRecord],
) -> list[RequirementJudgment]:
    """Read reviewed judgments from a CSV table and check their references.

    The table must describe the current candidate judgments, so a table that was filled
    against an earlier evaluation is rejected instead of importing its outdated
    judgments. Each row must decide accept or revise. References are checked against the
    requirements and scenarios that were recorded, and the cited evidence must be an
    observation of the same case, method, run and of the scenarios of the reviewed
    requirement, so a judgment cannot rest on another run or another delivered
    implementation. A row without a decision is still waiting for the reviewer, so it
    is skipped.
    """
    resolved_path = Path(path).resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f"Judgment review CSV not found: {resolved_path}")

    stale = stale_review_rows(resolved_path, candidates)
    if stale:
        raise ValueError(
            "The judgment review table does not describe the current candidate judgments: "
            + ", ".join(stale)
            + ". Export the table from the current evaluations before importing it."
        )

    known_requirements = {item.requirement_id for item in requirements}
    scenario_ids = {
        requirement_id: {
            scenario.scenario_id for scenario in scenarios if scenario.requirement_id == requirement_id
        }
        for requirement_id in known_requirements
    }
    judgments: list[RequirementJudgment] = []
    seen: set[tuple[str, int]] = set()

    for index, row in enumerate(read_csv(resolved_path), start=1):
        requirement_id = row.get("requirement_id", "").strip()
        run_text = row.get("run_index", "").strip()
        decision = row.get("decision", "").strip()

        if requirement_id not in known_requirements:
            raise ValueError(f"Row {index} has unknown requirement_id '{requirement_id}'.")
        if not run_text.isdigit():
            raise ValueError(f"Row {index} must provide an integer run_index, got '{run_text}'.")
        if not decision:
            continue
        if decision not in ALLOWED_JUDGMENT_DECISIONS:
            raise ValueError(
                f"Row {index} decision must be one of {sorted(ALLOWED_JUDGMENT_DECISIONS)}, got '{decision}'."
            )

        run_index = int(run_text)
        key = (requirement_id, run_index)
        if key in seen:
            raise ValueError(f"Row {index} repeats the judgment for {key}.")
        seen.add(key)

        if decision == "accept":
            status = row.get("status", "").strip()
            evidence_ids = split_id_list(row.get("evidence_ids", ""))
            rationale = row.get("rationale", "").strip()
            limitation = row.get("limitation", "").strip()
        else:
            status = row.get("revised_status", "").strip()
            evidence_ids = split_id_list(row.get("revised_evidence_ids", ""))
            rationale = row.get("revised_rationale", "").strip()
            limitation = row.get("revised_limitation", "").strip()

        if status not in JUDGMENT_STATUSES:
            raise ValueError(f"Row {index} has unknown status '{status}'.")

        recorded_evidence = {
            record.evidence_id
            for record in evidence
            if record.case_id == case_id
            and record.method_id == method_id
            and record.run_index == run_index
            and record.scenario_id in scenario_ids[requirement_id]
        }
        unknown = [evidence_id for evidence_id in evidence_ids if evidence_id not in recorded_evidence]
        if unknown:
            raise ValueError(
                f"Row {index} cites evidence that was not recorded for {case_id}/{method_id}, "
                f"run {run_index} and requirement '{requirement_id}': {unknown}."
            )
        if status in OBSERVED_STATUSES and not evidence_ids:
            raise ValueError(f"Row {index} status '{status}' must cite at least one evidence ID.")

        judgments.append(
            RequirementJudgment(
                requirement_id=requirement_id,
                run_index=run_index,
                status=status,  # type: ignore[arg-type]
                evidence_ids=evidence_ids,
                rationale=rationale,
                limitation=limitation,
            )
        )

    return judgments


def save_reviewed_judgments(judgments: Sequence[RequirementJudgment], output_dir: Path | str) -> None:
    """Write the judgments that a reviewer confirmed for one method."""
    atomic_write_json(
        Path(output_dir).resolve() / REVIEWED_JUDGMENTS_NAME,
        [judgment.model_dump(mode="json") for judgment in judgments],
    )


def load_reviewed_judgments(output_dir: Path | str) -> list[RequirementJudgment] | None:
    """Read the reviewed judgments of one method, or report that none were imported."""
    path = Path(output_dir).resolve() / REVIEWED_JUDGMENTS_NAME
    if not path.exists():
        return None
    data: Any = read_json(path)
    return [RequirementJudgment.model_validate(entry) for entry in data]
