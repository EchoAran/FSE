"""Human audit sampling, review sheet export, and quality metric computation module."""

from __future__ import annotations

import csv
import random
from pathlib import Path
from typing import Any

from evolution.rq1.case_artifacts import read_case_jsonl, resolve_case_ids
from evolution.rq1.config import RQ1Config
from evolution.rq1.models import (
    AuditSummary,
    DeduplicationAuditMetrics,
    DeduplicationGroup,
    ExtractedRIU,
    ExtractionUnit,
    OmissionAuditMetrics,
    ResponseRecord,
    RIUQualityAuditMetrics,
    TranscriptRecord,
)
from evolution.rq1.storage import write_csv, write_json


class AuditError(Exception):
    """Base exception for audit operations."""


class AuditValidationError(AuditError):
    """Exception raised when audit data or annotations fail validation."""


def select_audit_cases(
    case_ids: list[str],
    case_count: int,
    random_seed: int,
) -> list[str]:
    """Deterministically select a subset of case identifiers using fixed random seed."""
    distinct_cases = sorted(set(case_ids))
    if case_count > len(distinct_cases):
        raise AuditValidationError(
            f"Requested case count ({case_count}) exceeds available cases ({len(distinct_cases)})"
        )
    rng = random.Random(random_seed)
    selected = rng.sample(distinct_cases, case_count)
    return sorted(selected)


def export_extraction_review(
    selected_cases: list[str],
    responses: list[ResponseRecord],
    extraction_units: list[ExtractionUnit],
    output_path: Path,
) -> None:
    """Export review spreadsheet for RIU extraction quality evaluation."""
    selected_case_set = set(selected_cases)
    units_by_response = {unit.response_id: unit for unit in extraction_units}

    filtered_responses = [
        resp for resp in responses if resp.case_id in selected_case_set
    ]
    filtered_responses.sort(
        key=lambda r: (r.case_id, r.method_id, r.turn_index)
    )

    fieldnames = [
        "case_id",
        "method_id",
        "transcript_id",
        "response_id",
        "turn_index",
        "context_question",
        "answer",
        "riu_id",
        "statement",
        "evidence_text",
        "evidence_start",
        "evidence_end",
        "evidence_faithful",
        "requirement_relevant",
        "segmentation_adequate",
        "review_note",
    ]

    rows: list[dict[str, Any]] = []
    for resp in filtered_responses:
        unit = units_by_response.get(resp.response_id)
        rius = unit.rius if unit is not None else []
        if not rius:
            rows.append(
                {
                    "case_id": resp.case_id,
                    "method_id": resp.method_id,
                    "transcript_id": resp.transcript_id,
                    "response_id": resp.response_id,
                    "turn_index": resp.turn_index,
                    "context_question": resp.context_question,
                    "answer": resp.answer,
                    "riu_id": "",
                    "statement": "",
                    "evidence_text": "",
                    "evidence_start": "",
                    "evidence_end": "",
                    "evidence_faithful": "",
                    "requirement_relevant": "",
                    "segmentation_adequate": "",
                    "review_note": "",
                }
            )
        else:
            for riu in rius:
                rows.append(
                    {
                        "case_id": resp.case_id,
                        "method_id": resp.method_id,
                        "transcript_id": resp.transcript_id,
                        "response_id": resp.response_id,
                        "turn_index": resp.turn_index,
                        "context_question": resp.context_question,
                        "answer": resp.answer,
                        "riu_id": riu.riu_id or "",
                        "statement": riu.statement,
                        "evidence_text": riu.evidence_text,
                        "evidence_start": riu.evidence_start,
                        "evidence_end": riu.evidence_end,
                        "evidence_faithful": "",
                        "requirement_relevant": "",
                        "segmentation_adequate": "",
                        "review_note": "",
                    }
                )

    write_csv(output_path, fieldnames, rows)


def export_deduplication_review(
    selected_cases: list[str],
    raw_rius: list[ExtractedRIU],
    groups: list[DeduplicationGroup],
    output_path: Path,
) -> None:
    """Export review spreadsheet for transcript deduplication correctness evaluation."""
    selected_case_set = set(selected_cases)
    raw_riu_map = {r.riu_id: r for r in raw_rius if r.riu_id}

    fieldnames = [
        "case_id",
        "method_id",
        "transcript_id",
        "representative_riu_id",
        "canonical_statement",
        "member_count",
        "member_riu_ids",
        "member_statements",
        "deduplication_correct",
        "review_note",
    ]

    filtered_groups: list[DeduplicationGroup] = []
    for group in groups:
        rep_id = group.representative_riu_id
        case_id = rep_id.split("::")[0]
        if case_id in selected_case_set:
            filtered_groups.append(group)

    merged_groups = [g for g in filtered_groups if len(g.member_riu_ids) > 1]
    groups_to_export = merged_groups

    rows: list[dict[str, Any]] = []
    for group in groups_to_export:
        parts = group.representative_riu_id.split("::")
        case_id = parts[0]
        method_id = parts[1]
        transcript_id = f"{case_id}::{method_id}"

        member_statements = [
            raw_riu_map[mid].statement
            for mid in group.member_riu_ids
            if mid in raw_riu_map
        ]

        rows.append(
            {
                "case_id": case_id,
                "method_id": method_id,
                "transcript_id": transcript_id,
                "representative_riu_id": group.representative_riu_id,
                "canonical_statement": group.statement,
                "member_count": len(group.member_riu_ids),
                "member_riu_ids": "; ".join(group.member_riu_ids),
                "member_statements": " | ".join(member_statements),
                "deduplication_correct": "",
                "review_note": "",
            }
        )

    rows.sort(
        key=lambda r: (r["case_id"], r["method_id"], r["representative_riu_id"])
    )
    write_csv(output_path, fieldnames, rows)


def export_transcript_review(
    selected_cases: list[str],
    transcripts: list[TranscriptRecord],
    extraction_units: list[ExtractionUnit],
    output_path: Path,
) -> None:
    """Export review spreadsheet for fast transcript-level omission screening."""
    selected_case_set = set(selected_cases)
    filtered_transcripts = [
        t for t in transcripts if t.case_id in selected_case_set
    ]
    filtered_transcripts.sort(
        key=lambda t: (t.case_id, t.method_id, t.transcript_id)
    )

    riu_counts_by_transcript: dict[str, int] = {}
    for unit in extraction_units:
        riu_counts_by_transcript[unit.transcript_id] = (
            riu_counts_by_transcript.get(unit.transcript_id, 0) + len(unit.rius)
        )

    fieldnames = [
        "case_id",
        "method_id",
        "transcript_id",
        "completed_turns",
        "extracted_riu_count",
        "has_major_omissions",
        "review_note",
    ]

    rows: list[dict[str, Any]] = []
    for t in filtered_transcripts:
        rows.append(
            {
                "case_id": t.case_id,
                "method_id": t.method_id,
                "transcript_id": t.transcript_id,
                "completed_turns": t.completed_turns,
                "extracted_riu_count": riu_counts_by_transcript.get(t.transcript_id, 0),
                "has_major_omissions": "",
                "review_note": "",
            }
        )

    write_csv(output_path, fieldnames, rows)


def parse_strict_boolean(value: Any, field_name: str, context_id: str) -> bool:
    """Parse string annotation into boolean value or raise validation error on missing/invalid value."""
    if value is None:
        raise AuditValidationError(
            f"Missing required annotation for '{field_name}' in {context_id}"
        )
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "t"}:
        return True
    if normalized in {"0", "false", "no", "n", "f"}:
        return False
    raise AuditValidationError(
        f"Invalid boolean annotation '{value}' for '{field_name}' in {context_id}. "
        f"Must be a valid boolean value (e.g. 1/0, true/false, yes/no)."
    )


def summarize_extraction_review(path: Path) -> RIUQualityAuditMetrics:
    """Compute RIU extraction quality metrics from human audit review records."""
    if not path.is_file():
        raise AuditValidationError(f"Extraction review file not found: {path}")

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        raise AuditValidationError(f"Extraction review file is empty: {path}")

    riu_rows: list[dict[str, str]] = []
    for row in rows:
        riu_id = row.get("riu_id", "").strip()
        if riu_id:
            riu_rows.append(row)

    if not riu_rows:
        raise AuditValidationError(
            f"Extraction review file contains no valid RIU annotations: {path}"
        )

    evidence_faithful_bools = [
        parse_strict_boolean(
            row.get("evidence_faithful"),
            "evidence_faithful",
            row.get("riu_id", "unknown_riu"),
        )
        for row in riu_rows
    ]
    relevance_bools = [
        parse_strict_boolean(
            row.get("requirement_relevant"),
            "requirement_relevant",
            row.get("riu_id", "unknown_riu"),
        )
        for row in riu_rows
    ]
    segmentation_bools = [
        parse_strict_boolean(
            row.get("segmentation_adequate"),
            "segmentation_adequate",
            row.get("riu_id", "unknown_riu"),
        )
        for row in riu_rows
    ]

    total_rius = len(riu_rows)
    return RIUQualityAuditMetrics(
        total_reviewed_rius=total_rius,
        evidence_faithfulness=round(
            sum(1 for b in evidence_faithful_bools if b) / total_rius,
            4,
        ),
        requirement_relevance=round(
            sum(1 for b in relevance_bools if b) / total_rius,
            4,
        ),
        segmentation_adequacy=round(
            sum(1 for b in segmentation_bools if b) / total_rius,
            4,
        ),
    )


def summarize_deduplication_review(path: Path) -> DeduplicationAuditMetrics:
    """Compute deduplication correctness metric from single human reviewer records."""
    if not path.is_file():
        raise AuditValidationError(f"Deduplication review file not found: {path}")

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        return DeduplicationAuditMetrics(
            total_reviewed_groups=0,
            deduplication_correctness=None,
        )

    dedup_bools = [
        parse_strict_boolean(
            row.get("deduplication_correct"),
            "deduplication_correct",
            row.get("representative_riu_id", "unknown_group"),
        )
        for row in rows
    ]

    total_groups = len(rows)
    correct_count = sum(1 for b in dedup_bools if b)
    return DeduplicationAuditMetrics(
        total_reviewed_groups=total_groups,
        deduplication_correctness=round(correct_count / total_groups, 4),
    )


def summarize_transcript_review(path: Path) -> OmissionAuditMetrics:
    """Compute omission metrics from fast transcript-level screening review."""
    if not path.is_file():
        raise AuditValidationError(f"Transcript review file not found: {path}")

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        raise AuditValidationError(f"Transcript review file is empty: {path}")

    omission_bools = [
        parse_strict_boolean(
            row.get("has_major_omissions"),
            "has_major_omissions",
            row.get("transcript_id", "unknown_transcript"),
        )
        for row in rows
    ]

    total_transcripts = len(rows)
    omission_count = sum(1 for b in omission_bools if b)
    return OmissionAuditMetrics(
        total_reviewed_transcripts=total_transcripts,
        transcripts_with_major_omissions=omission_count,
        major_omission_rate=round(omission_count / total_transcripts, 4)
        if total_transcripts > 0
        else 0.0,
        has_major_omissions=omission_count > 0,
    )


def build_audit_summary(
    extraction_review: Path,
    deduplication_review: Path,
    transcript_review: Path | None = None,
) -> AuditSummary:
    """Build unified audit summary across RIU quality, deduplication, and omission reviews."""
    if transcript_review is None:
        transcript_review = extraction_review.parent / "transcript_review.csv"

    riu_metrics = summarize_extraction_review(extraction_review)
    deduplication_metrics = summarize_deduplication_review(deduplication_review)
    omission_metrics = summarize_transcript_review(transcript_review)
    return AuditSummary(
        riu_quality=riu_metrics,
        deduplication=deduplication_metrics,
        omission=omission_metrics,
    )


def resolve_review_file(audit_dir: Path, base_name: str) -> Path:
    """Resolve path to completed review file (*_completed.csv) or default review file (*.csv)."""
    completed_path = audit_dir / f"{base_name}_completed.csv"
    if completed_path.is_file():
        return completed_path
    return audit_dir / f"{base_name}.csv"


def run_audit_export(config: RQ1Config) -> None:
    """Execute audit sampling and export review spreadsheets."""
    artifacts_root = config.paths.artifacts_root
    case_ids = resolve_case_ids(config, None)

    transcripts = [
        TranscriptRecord.model_validate(row)
        for row in read_case_jsonl(
            config, "ingestion/transcripts.jsonl", case_ids
        )
    ]
    responses = [
        ResponseRecord.model_validate(row)
        for row in read_case_jsonl(config, "ingestion/responses.jsonl", case_ids)
    ]
    extraction_units = [
        ExtractionUnit.model_validate(row)
        for row in read_case_jsonl(config, "riu/extraction_units.jsonl", case_ids)
    ]
    raw_rius = [
        ExtractedRIU.model_validate(row)
        for row in read_case_jsonl(config, "riu/raw_rius.jsonl", case_ids)
    ]
    groups = [
        DeduplicationGroup.model_validate(row)
        for row in read_case_jsonl(
            config, "riu/deduplication_groups.jsonl", case_ids
        )
    ]

    all_case_ids = sorted({t.case_id for t in transcripts})
    selected_cases = select_audit_cases(
        case_ids=all_case_ids,
        case_count=config.audit.case_count,
        random_seed=config.audit.random_seed,
    )

    audit_dir = artifacts_root / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)

    export_extraction_review(
        selected_cases=selected_cases,
        responses=responses,
        extraction_units=extraction_units,
        output_path=audit_dir / "extraction_review.csv",
    )

    export_deduplication_review(
        selected_cases=selected_cases,
        raw_rius=raw_rius,
        groups=groups,
        output_path=audit_dir / "deduplication_review.csv",
    )

    export_transcript_review(
        selected_cases=selected_cases,
        transcripts=transcripts,
        extraction_units=extraction_units,
        output_path=audit_dir / "transcript_review.csv",
    )


def run_audit_summarize(config: RQ1Config) -> AuditSummary:
    """Read single-reviewer completed sheets and generate audit summary artifact."""
    audit_dir = config.paths.artifacts_root / "audit"
    extraction_file = resolve_review_file(audit_dir, "extraction_review")
    dedup_file = resolve_review_file(audit_dir, "deduplication_review")
    transcript_file = resolve_review_file(audit_dir, "transcript_review")

    if not extraction_file.is_file():
        raise AuditError(
            f"Extraction review file not found: {extraction_file}. "
            f"Please complete single-reviewer review before running summarize."
        )
    if not dedup_file.is_file():
        raise AuditError(
            f"Deduplication review file not found: {dedup_file}. "
            f"Please complete single-reviewer review before running summarize."
        )
    if not transcript_file.is_file():
        raise AuditError(
            f"Transcript review file not found: {transcript_file}. "
            f"Please complete single-reviewer review before running summarize."
        )

    summary = build_audit_summary(
        extraction_review=extraction_file,
        deduplication_review=dedup_file,
        transcript_review=transcript_file,
    )
    write_json(audit_dir / "audit_summary.json", summary)
    return summary
