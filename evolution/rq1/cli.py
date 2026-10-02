"""Unified command line interface for RQ1 evaluation workflow."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from collections.abc import Sequence
from pathlib import Path

from evolution.rq1.audit import (
    build_audit_summary,
    resolve_review_file,
    run_audit_export,
    run_audit_summarize,
)
from evolution.rq1.case_artifacts import (
    case_artifacts_root,
    case_config,
    read_case_csv,
    read_case_jsonl,
    require_case_file,
    resolve_case_ids,
)
from evolution.rq1.clustering import run_clustering
from evolution.rq1.config import RQ1Config, find_repository_root, load_config
from evolution.rq1.elaboration import (
    compute_cluster_depth,
    compute_transcript_depth_counts,
    run_elaboration,
)
from evolution.rq1.ingest import ingest_results
from evolution.rq1.models import (
    AuditSummary,
    BreadthMetricRecord,
    ClusterAssignment,
    ClusterDepthRecord,
    DeduplicationGroup,
    ElaborationDAG,
    ExtractedRIU,
    ExtractionUnit,
    ResponseRecord,
    TranscriptClusterCoverage,
    TranscriptMetrics,
    TranscriptRecord,
    UniqueRIU,
)
from evolution.rq1.report import (
    build_depth_distribution,
    build_report,
    depth_count_metric_names,
)
from evolution.rq1.riu import run_riu
from evolution.rq1.storage import read_json


class CLIValidationError(Exception):
    """Exception raised when artifact cross-stage validation fails."""


def _clean_stage_artifacts(artifacts_dir: Path, artifacts_root: Path) -> None:
    """Safely clear an artifact directory if it is strictly contained within artifacts_root."""
    resolved_dir = artifacts_dir.resolve()
    resolved_root = artifacts_root.resolve()
    if resolved_root in resolved_dir.parents and resolved_dir != resolved_root:
        if resolved_dir.exists():
            shutil.rmtree(resolved_dir)


def _is_review_completed(audit_dir: Path) -> bool:
    """Check whether single-reviewer review spreadsheets are present and fully annotated."""
    extraction_file = resolve_review_file(audit_dir, "extraction_review")
    dedup_file = resolve_review_file(audit_dir, "deduplication_review")
    transcript_file = resolve_review_file(audit_dir, "transcript_review")

    if (
        not extraction_file.is_file()
        or not dedup_file.is_file()
        or not transcript_file.is_file()
    ):
        return False

    with extraction_file.open("r", encoding="utf-8", newline="") as f:
        extraction_rows = list(csv.DictReader(f))
    if not extraction_rows:
        return False
    riu_rows = [r for r in extraction_rows if r.get("riu_id", "").strip()]
    if not riu_rows:
        return False
    for r in riu_rows:
        if (
            str(r.get("evidence_faithful", "")).strip() == ""
            or str(r.get("requirement_relevant", "")).strip() == ""
            or str(r.get("segmentation_adequate", "")).strip() == ""
        ):
            return False

    with dedup_file.open("r", encoding="utf-8", newline="") as f:
        dedup_rows = list(csv.DictReader(f))
    for r in dedup_rows:
        if str(r.get("deduplication_correct", "")).strip() == "":
            return False

    with transcript_file.open("r", encoding="utf-8", newline="") as f:
        transcript_rows = list(csv.DictReader(f))
    if not transcript_rows:
        return False
    for r in transcript_rows:
        if str(r.get("has_major_omissions", "")).strip() == "":
            return False

    return True


def run_ingest(config: RQ1Config, args: argparse.Namespace) -> int:
    """Execute interview conversation ingestion for selected Cases."""
    case_ids = resolve_case_ids(config, getattr(args, "case_id", None))
    for index, case_id in enumerate(case_ids, start=1):
        scoped = case_config(config, case_id)
        print(f"[ingest][{case_id}] Case {index}/{len(case_ids)} starting", flush=True)
        if getattr(args, "force", False):
            _clean_stage_artifacts(
                scoped.paths.artifacts_root / "ingestion",
                scoped.paths.artifacts_root,
            )
        ingest_results(scoped, [case_id])
        print(f"[ingest][{case_id}] completed", flush=True)
    return 0


def run_riu_stage(config: RQ1Config, args: argparse.Namespace) -> int:
    """Execute RIU extraction and deduplication for selected Cases."""
    case_ids = resolve_case_ids(config, getattr(args, "case_id", None))
    for index, case_id in enumerate(case_ids, start=1):
        scoped = case_config(config, case_id)
        print(f"[riu][{case_id}] Case {index}/{len(case_ids)} starting", flush=True)
        if getattr(args, "force", False):
            _clean_stage_artifacts(
                scoped.paths.artifacts_root / "riu",
                scoped.paths.artifacts_root,
            )
        run_riu(scoped)
        print(f"[riu][{case_id}] completed", flush=True)
    return 0


def run_breadth_stage(config: RQ1Config, args: argparse.Namespace) -> int:
    """Execute clustering and Breadth calculation for selected Cases."""
    case_ids = resolve_case_ids(config, getattr(args, "case_id", None))
    for index, case_id in enumerate(case_ids, start=1):
        scoped = case_config(config, case_id)
        print(
            f"[clustering][{case_id}] Case {index}/{len(case_ids)} starting",
            flush=True,
        )
        if getattr(args, "force", False):
            _clean_stage_artifacts(
                scoped.paths.artifacts_root / "clustering",
                scoped.paths.artifacts_root,
            )
        run_clustering(scoped)
        print(f"[clustering][{case_id}] completed", flush=True)
    return 0


def run_depth_stage(config: RQ1Config, args: argparse.Namespace) -> int:
    """Execute elaboration relationship judgment and Depth for selected Cases."""
    case_ids = resolve_case_ids(config, getattr(args, "case_id", None))
    for index, case_id in enumerate(case_ids, start=1):
        scoped = case_config(config, case_id)
        print(
            f"[elaboration][{case_id}] Case {index}/{len(case_ids)} starting",
            flush=True,
        )
        if getattr(args, "force", False):
            _clean_stage_artifacts(
                scoped.paths.artifacts_root / "elaboration",
                scoped.paths.artifacts_root,
            )
        run_elaboration(scoped)
        print(f"[elaboration][{case_id}] completed", flush=True)
    return 0


def run_audit_export_stage(config: RQ1Config, args: argparse.Namespace) -> int:
    """Execute human audit case sampling and review spreadsheet export."""
    if getattr(args, "case_id", None) is not None:
        raise CLIValidationError("audit-export operates on the complete Case set")
    if getattr(args, "force", False):
        _clean_stage_artifacts(
            config.paths.artifacts_root / "audit",
            config.paths.artifacts_root,
        )
    run_audit_export(config)
    return 0


def run_audit_summarize_stage(config: RQ1Config, args: argparse.Namespace) -> int:
    """Execute human audit annotation summarization."""
    if getattr(args, "case_id", None) is not None:
        raise CLIValidationError("audit-summarize operates on the complete Case set")
    run_audit_summarize(config)
    return 0


def run_report_stage(config: RQ1Config, args: argparse.Namespace) -> int:
    """Execute final statistical reporting and test generation."""
    if getattr(args, "case_id", None) is not None:
        raise CLIValidationError("report operates on the complete Case set")
    if getattr(args, "force", False):
        _clean_stage_artifacts(
            config.paths.artifacts_root / "reports",
            config.paths.artifacts_root,
        )
    build_report(config)
    return 0


def run_validate(config: RQ1Config, args: argparse.Namespace | None = None) -> int:
    """Perform deterministic contract verification across all pipeline artifacts."""
    artifacts_root = config.paths.artifacts_root
    requested_case = getattr(args, "case_id", None) if args is not None else None
    case_ids = resolve_case_ids(config, requested_case)
    final_validation = requested_case is None
    audit_dir = artifacts_root / "audit"
    reports_dir = artifacts_root / "reports"

    case_pipeline_files = [
        "ingestion/transcripts.jsonl",
        "ingestion/responses.jsonl",
        "riu/extraction_units.jsonl",
        "riu/raw_rius.jsonl",
        "riu/deduplication_groups.jsonl",
        "riu/unique_rius.jsonl",
        "clustering/cluster_assignments.jsonl",
        "clustering/transcript_cluster_coverage.jsonl",
        "clustering/breadth_metrics.jsonl",
        "elaboration/dags.jsonl",
        "elaboration/cluster_depths.csv",
        "elaboration/transcript_metrics.jsonl",
    ]
    for case_id in case_ids:
        for relative_path in case_pipeline_files:
            require_case_file(config, case_id, relative_path)

    if final_validation:
        extraction_review_file = resolve_review_file(audit_dir, "extraction_review")
        dedup_review_file = resolve_review_file(audit_dir, "deduplication_review")
        transcript_review_file = resolve_review_file(audit_dir, "transcript_review")
        audit_summary_path = audit_dir / "audit_summary.json"
        final_files = [
            extraction_review_file,
            dedup_review_file,
            transcript_review_file,
            audit_summary_path,
            reports_dir / "transcript_metrics.csv",
            reports_dir / "paired_metrics.csv",
            reports_dir / "method_descriptives.csv",
            reports_dir / "omnibus_tests.csv",
            reports_dir / "pairwise_tests.csv",
            reports_dir / "depth_distribution.csv",
            reports_dir / "efficiency_metrics.csv",
            reports_dir / "threshold_sensitivity.csv",
            reports_dir / "audit_summary.json",
            reports_dir / "summary.json",
        ]
        for file_path in final_files:
            if not file_path.is_file():
                raise CLIValidationError(f"Required artifact not found: {file_path}")

        recomputed_summary = build_audit_summary(
            extraction_review=extraction_review_file,
            deduplication_review=dedup_review_file,
            transcript_review=transcript_review_file,
        )
        recorded_audit_summary = AuditSummary.model_validate(
            read_json(audit_summary_path)
        )
        if recomputed_summary != recorded_audit_summary:
            raise CLIValidationError(
                f"Audit summary in {audit_summary_path} does not match recomputed review summary from review spreadsheets"
            )

        recorded_report_summary = AuditSummary.model_validate(
            read_json(reports_dir / "audit_summary.json")
        )
        if recorded_report_summary != recorded_audit_summary:
            raise CLIValidationError(
                f"Audit summary in {reports_dir / 'audit_summary.json'} does not match {audit_summary_path}"
            )

    transcripts = [
        TranscriptRecord.model_validate(r)
        for r in read_case_jsonl(
            config, "ingestion/transcripts.jsonl", case_ids
        )
    ]
    responses = [
        ResponseRecord.model_validate(r)
        for r in read_case_jsonl(config, "ingestion/responses.jsonl", case_ids)
    ]
    extraction_units = [
        ExtractionUnit.model_validate(r)
        for r in read_case_jsonl(config, "riu/extraction_units.jsonl", case_ids)
    ]
    raw_rius = [
        ExtractedRIU.model_validate(r)
        for r in read_case_jsonl(config, "riu/raw_rius.jsonl", case_ids)
    ]
    groups = [
        DeduplicationGroup.model_validate(r)
        for r in read_case_jsonl(
            config, "riu/deduplication_groups.jsonl", case_ids
        )
    ]
    unique_rius = [
        UniqueRIU.model_validate(r)
        for r in read_case_jsonl(config, "riu/unique_rius.jsonl", case_ids)
    ]
    assignments = [
        ClusterAssignment.model_validate(r)
        for r in read_case_jsonl(
            config, "clustering/cluster_assignments.jsonl", case_ids
        )
    ]
    coverage = [
        TranscriptClusterCoverage.model_validate(r)
        for r in read_case_jsonl(
            config, "clustering/transcript_cluster_coverage.jsonl", case_ids
        )
    ]
    breadth_records = [
        BreadthMetricRecord.model_validate(r)
        for r in read_case_jsonl(
            config, "clustering/breadth_metrics.jsonl", case_ids
        )
    ]
    dags = [
        ElaborationDAG.model_validate(r)
        for r in read_case_jsonl(config, "elaboration/dags.jsonl", case_ids)
    ]
    transcript_metrics = [
        TranscriptMetrics.model_validate(r)
        for r in read_case_jsonl(
            config, "elaboration/transcript_metrics.jsonl", case_ids
        )
    ]

    cluster_depth_rows = read_case_csv(
        config, "elaboration/cluster_depths.csv", case_ids
    )
    cluster_depth_records = [
        ClusterDepthRecord.model_validate(row)
        for row in cluster_depth_rows
    ]

    expected_case_method_pairs = {
        (case_id, method_id)
        for case_id in case_ids
        for method_id in config.methods
    }
    actual_case_method_pairs = {
        (transcript.case_id, transcript.method_id) for transcript in transcripts
    }
    if (
        actual_case_method_pairs != expected_case_method_pairs
        or len(transcripts) != len(expected_case_method_pairs)
    ):
        raise CLIValidationError(
            "Transcript artifacts do not contain exactly one record for every selected Case-method pair"
        )

    response_counts_by_transcript: dict[str, int] = {}
    response_map: dict[str, ResponseRecord] = {}
    for resp in responses:
        response_counts_by_transcript[resp.transcript_id] = (
            response_counts_by_transcript.get(resp.transcript_id, 0) + 1
        )
        response_map[resp.response_id] = resp

    for t in transcripts:
        expected_turns = t.completed_turns
        actual_turns = response_counts_by_transcript.get(t.transcript_id, 0)
        if actual_turns != expected_turns:
            raise CLIValidationError(
                f"Transcript {t.transcript_id} response count ({actual_turns}) "
                f"does not match completed_turns ({expected_turns})"
            )

    extraction_unit_response_ids = [unit.response_id for unit in extraction_units]
    if len(extraction_unit_response_ids) != len(set(extraction_unit_response_ids)):
        raise CLIValidationError("Duplicate response_id found across extraction units")
    if set(extraction_unit_response_ids) != set(response_map.keys()):
        raise CLIValidationError(
            "Extraction units do not cover responses 1-to-1"
        )

    raw_riu_map: dict[str, ExtractedRIU] = {}
    for riu in raw_rius:
        if riu.riu_id in raw_riu_map:
            raise CLIValidationError(
                f"Duplicate raw RIU ID in raw_rius.jsonl: {riu.riu_id}"
            )
        raw_riu_map[riu.riu_id] = riu

    extracted_rius_from_units: dict[str, ExtractedRIU] = {}
    for unit in extraction_units:
        resp = response_map[unit.response_id]
        if unit.transcript_id != resp.transcript_id:
            raise CLIValidationError(
                f"Transcript ID mismatch in unit {unit.response_id}: {unit.transcript_id} != {resp.transcript_id}"
            )
        if unit.case_id != resp.case_id or unit.method_id != resp.method_id:
            raise CLIValidationError(
                f"Case/Method mismatch in unit {unit.response_id}"
            )
        for idx, riu in enumerate(unit.rius, start=1):
            if riu.ordinal != idx:
                raise CLIValidationError(
                    f"Ordinal mismatch for {unit.response_id}: expected {idx}, got {riu.ordinal}"
                )
            if not riu.riu_id.startswith(f"{resp.response_id}::"):
                raise CLIValidationError(
                    f"RIU ID prefix mismatch in {riu.riu_id}: does not match {resp.response_id}"
                )
            if (
                resp.answer[riu.evidence_start : riu.evidence_end]
                != riu.evidence_text
            ):
                raise CLIValidationError(
                    f"Evidence text mismatch for RIU {riu.riu_id}"
                )
            if riu.riu_id in extracted_rius_from_units:
                raise CLIValidationError(
                    f"Duplicate RIU ID in extraction units: {riu.riu_id}"
                )
            extracted_rius_from_units[riu.riu_id] = riu

    if set(extracted_rius_from_units.keys()) != set(raw_riu_map.keys()):
        raise CLIValidationError(
            "Raw RIUs in extraction units do not match raw_rius.jsonl"
        )

    for riu_id, unit_riu in extracted_rius_from_units.items():
        raw_riu = raw_riu_map[riu_id]
        if (
            unit_riu.statement != raw_riu.statement
            or unit_riu.evidence_text != raw_riu.evidence_text
            or unit_riu.evidence_start != raw_riu.evidence_start
            or unit_riu.evidence_end != raw_riu.evidence_end
            or unit_riu.ordinal != raw_riu.ordinal
        ):
            raise CLIValidationError(
                f"Raw RIU field content mismatch for {riu_id} between extraction units and raw_rius.jsonl"
            )

    grouped_raw_ids: set[str] = set()
    group_by_members: dict[tuple[str, ...], DeduplicationGroup] = {}
    for grp in groups:
        key = tuple(sorted(grp.member_riu_ids))
        if key in group_by_members:
            raise CLIValidationError(f"Duplicate member set across groups: {key}")
        group_by_members[key] = grp
        for mid in grp.member_riu_ids:
            if mid in grouped_raw_ids:
                raise CLIValidationError(f"Duplicate member across groups: {mid}")
            grouped_raw_ids.add(mid)
    if grouped_raw_ids != set(raw_riu_map.keys()):
        raise CLIValidationError("Deduplication groups do not partition raw RIUs")

    if len(unique_rius) != len(groups):
        raise CLIValidationError(
            f"Unique RIU count ({len(unique_rius)}) != deduplication group count ({len(groups)})"
        )

    for unique_riu in unique_rius:
        key = tuple(sorted(unique_riu.member_riu_ids))
        matching_group = group_by_members.get(key)
        if matching_group is None:
            raise CLIValidationError(
                f"Unique RIU {unique_riu.transcript_riu_id} has no matching deduplication group"
            )
        if (
            matching_group.representative_riu_id
            not in unique_riu.member_riu_ids
        ):
            raise CLIValidationError(
                f"Representative RIU {matching_group.representative_riu_id} not in unique RIU members"
            )
        if unique_riu.statement != matching_group.statement:
            raise CLIValidationError(
                f"Statement mismatch between Unique RIU {unique_riu.transcript_riu_id} and deduplication group"
            )

        prov_riu_ids = [p.riu_id for p in unique_riu.provenance]
        if len(prov_riu_ids) != len(set(prov_riu_ids)):
            raise CLIValidationError(
                f"Duplicate provenance RIU ID in Unique RIU {unique_riu.transcript_riu_id}"
            )
        if set(prov_riu_ids) != set(unique_riu.member_riu_ids):
            raise CLIValidationError(
                f"Provenance RIU IDs do not match member_riu_ids in Unique RIU {unique_riu.transcript_riu_id}"
            )

        for p in unique_riu.provenance:
            raw_riu = raw_riu_map.get(p.riu_id)
            if raw_riu is None:
                raise CLIValidationError(
                    f"Provenance references unknown raw RIU: {p.riu_id}"
                )
            resp = response_map.get(p.response_id)
            if resp is None:
                raise CLIValidationError(
                    f"Provenance references unknown response: {p.response_id}"
                )
            if not p.riu_id.startswith(f"{p.response_id}::"):
                raise CLIValidationError(
                    f"Provenance RIU ID {p.riu_id} does not match response {p.response_id}"
                )
            if p.turn_index != resp.turn_index:
                raise CLIValidationError(
                    f"Provenance turn_index mismatch for {p.riu_id}: {p.turn_index} != {resp.turn_index}"
                )
            if p.context_question != resp.context_question:
                raise CLIValidationError(
                    f"Provenance context_question mismatch for {p.riu_id}"
                )
            if (
                p.evidence_start != raw_riu.evidence_start
                or p.evidence_end != raw_riu.evidence_end
                or p.evidence_text != raw_riu.evidence_text
            ):
                raise CLIValidationError(
                    f"Provenance evidence slice mismatch for {p.riu_id} against raw RIU"
                )
            if (
                resp.answer[p.evidence_start : p.evidence_end]
                != p.evidence_text
            ):
                raise CLIValidationError(
                    f"Provenance text mismatch for Unique RIU {unique_riu.transcript_riu_id}"
                )

    unique_riu_map = {riu.transcript_riu_id: riu for riu in unique_rius}
    assignment_riu_ids = {a.transcript_riu_id for a in assignments}
    if assignment_riu_ids != set(unique_riu_map.keys()):
        raise CLIValidationError(
            "Cluster assignments do not cover unique RIUs exactly"
        )

    coverage_keys = {(c.transcript_id, c.cluster_id) for c in coverage}
    assignment_keys = {(a.transcript_id, a.cluster_id) for a in assignments}
    if coverage_keys != assignment_keys:
        raise CLIValidationError("Coverage does not match cluster assignments")

    for cov in coverage:
        expected_rius = {
            a.transcript_riu_id
            for a in assignments
            if a.transcript_id == cov.transcript_id
            and a.cluster_id == cov.cluster_id
        }
        if set(cov.transcript_riu_ids) != expected_rius:
            raise CLIValidationError(
                f"Coverage transcript_riu_ids mismatch for {cov.transcript_id}::{cov.cluster_id}"
            )

    clusters_per_transcript: dict[str, int] = {
        t.transcript_id: 0 for t in transcripts
    }
    for c in coverage:
        clusters_per_transcript[c.transcript_id] += 1

    for b in breadth_records:
        if b.breadth != clusters_per_transcript[b.transcript_id]:
            raise CLIValidationError(
                f"Breadth metric mismatch for {b.transcript_id}: "
                f"{b.breadth} != {clusters_per_transcript[b.transcript_id]}"
            )

    dag_keys = {(dag.transcript_id, dag.cluster_id): dag for dag in dags}
    if set(dag_keys.keys()) != coverage_keys:
        raise CLIValidationError("DAG composition units do not match coverage")

    for dag in dags:
        node_positions = {n.node_id: idx for idx, n in enumerate(dag.nodes)}
        for edge in dag.edges:
            if edge.source_id == edge.target_id:
                raise CLIValidationError(
                    f"DAG self-loop detected in {dag.transcript_id}::{dag.cluster_id}: {edge.source_id}"
                )
            if (
                edge.source_id not in node_positions
                or edge.target_id not in node_positions
            ):
                raise CLIValidationError(
                    f"DAG edge references nonexistent node in {dag.transcript_id}::{dag.cluster_id}"
                )
            if node_positions[edge.source_id] >= node_positions[edge.target_id]:
                raise CLIValidationError(
                    f"DAG edge violates chronological order: {edge.source_id} -> {edge.target_id}"
                )

    cluster_depth_lookup = {
        (cd.transcript_id, cd.cluster_id): cd.depth
        for cd in cluster_depth_records
    }
    for dag in dags:
        computed_d = compute_cluster_depth(dag)
        expected_d = cluster_depth_lookup.get(
            (dag.transcript_id, dag.cluster_id)
        )
        if computed_d != expected_d:
            raise CLIValidationError(
                f"Cluster depth mismatch for {dag.transcript_id}::{dag.cluster_id}: "
                f"computed {computed_d} != recorded {expected_d}"
            )

    recomputed_transcript_depth_counts = compute_transcript_depth_counts(
        transcripts, cluster_depth_records
    )

    unique_counts: dict[str, int] = {t.transcript_id: 0 for t in transcripts}
    for u in unique_rius:
        unique_counts[u.transcript_id] += 1

    for tm in transcript_metrics:
        if tm.yield_count != unique_counts[tm.transcript_id]:
            raise CLIValidationError(
                f"Yield count mismatch for {tm.transcript_id}: "
                f"{tm.yield_count} != {unique_counts[tm.transcript_id]}"
            )
        if tm.breadth != clusters_per_transcript[tm.transcript_id]:
            raise CLIValidationError(
                f"Breadth mismatch for {tm.transcript_id}: "
                f"{tm.breadth} != {clusters_per_transcript[tm.transcript_id]}"
            )

        expected_depth_counts = recomputed_transcript_depth_counts[tm.transcript_id]
        if tm.depth_counts != expected_depth_counts:
            raise CLIValidationError(
                f"Depth DAG counts mismatch for {tm.transcript_id}: "
                f"recomputed {expected_depth_counts} != recorded {tm.depth_counts}"
            )
        if sum(tm.depth_counts.values()) != tm.breadth:
            raise CLIValidationError(
                f"Depth DAG count does not equal breadth for {tm.transcript_id}: "
                f"{sum(tm.depth_counts.values())} != {tm.breadth}"
            )

    if final_validation:
        report_metrics_path = reports_dir / "transcript_metrics.csv"
        with report_metrics_path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            report_rows = list(reader)

        if len(report_rows) != len(transcripts):
            raise CLIValidationError(
                f"Report metric row count ({len(report_rows)}) != transcript count ({len(transcripts)})"
            )

        expected_case_method_pairs = {
            (t.case_id, t.method_id) for t in transcripts
        }
        report_case_method_pairs = {
            (r["case_id"], r["method_id"]) for r in report_rows
        }
        if report_case_method_pairs != expected_case_method_pairs:
            raise CLIValidationError(
                "Report transcript metrics CSV does not match expected case-method combinations"
            )

        transcript_metrics_by_id = {
            metric.transcript_id: metric for metric in transcript_metrics
        }
        depth_metric_names = depth_count_metric_names(transcript_metrics)
        for row in report_rows:
            transcript_id = row["transcript_id"]
            if transcript_id not in transcript_metrics_by_id:
                raise CLIValidationError(
                    f"Report references unknown transcript: {transcript_id}"
                )
            metric = transcript_metrics_by_id[transcript_id]
            if json.loads(row["depth_counts"]) != metric.depth_counts:
                raise CLIValidationError(
                    f"Report depth counts mismatch for {transcript_id}"
                )
            for depth_metric in depth_metric_names:
                depth = depth_metric.removeprefix("depth_").removesuffix(
                    "_dag_count"
                )
                if int(row[depth_metric]) != metric.depth_counts.get(depth, 0):
                    raise CLIValidationError(
                        f"Report {depth_metric} mismatch for {transcript_id}"
                    )

        expected_distribution = build_depth_distribution(
            transcript_metrics, config.methods
        )
        distribution_path = reports_dir / "depth_distribution.csv"
        with distribution_path.open("r", encoding="utf-8", newline="") as file:
            actual_distribution = list(csv.DictReader(file))
        normalized_distribution = [
            {
                "method_id": row["method_id"],
                "depth": int(row["depth"]),
                "dag_count": int(row["dag_count"]),
            }
            for row in actual_distribution
        ]
        if normalized_distribution != expected_distribution:
            raise CLIValidationError(
                "Report depth distribution does not match transcript depth counts"
            )

    print(
        f"Validation passed: {len(case_ids)} Case and {len(transcripts)} transcripts "
        f"satisfy pipeline contracts."
    )
    return 0


def _case_stage_complete(
    config: RQ1Config,
    case_id: str,
    relative_paths: list[str],
) -> bool:
    """Return whether all final artifacts for one Case stage exist."""
    root = case_artifacts_root(config, case_id)
    return all((root / path).is_file() for path in relative_paths)


def run_all(config: RQ1Config, args: argparse.Namespace) -> int:
    """Execute automatic stages Case by Case, then continue with cross-Case outputs."""
    requested_case = getattr(args, "case_id", None)
    case_ids = resolve_case_ids(config, requested_case)
    force = getattr(args, "force", False)
    automatic_stages = [
        (
            "ingest",
            run_ingest,
            ["ingestion/transcripts.jsonl", "ingestion/responses.jsonl"],
        ),
        (
            "riu",
            run_riu_stage,
            [
                "riu/extraction_units.jsonl",
                "riu/raw_rius.jsonl",
                "riu/deduplication_groups.jsonl",
                "riu/unique_rius.jsonl",
            ],
        ),
        (
            "clustering",
            run_breadth_stage,
            [
                "clustering/cluster_assignments.jsonl",
                "clustering/transcript_cluster_coverage.jsonl",
                "clustering/breadth_metrics.jsonl",
                "clustering/threshold_sensitivity.csv",
            ],
        ),
        (
            "elaboration",
            run_depth_stage,
            [
                "elaboration/dags.jsonl",
                "elaboration/cluster_depths.csv",
                "elaboration/transcript_metrics.jsonl",
            ],
        ),
    ]

    for case_index, case_id in enumerate(case_ids, start=1):
        print(
            f"[all][{case_id}] Case {case_index}/{len(case_ids)} starting",
            flush=True,
        )
        case_args = argparse.Namespace(**vars(args))
        case_args.case_id = case_id
        for stage_name, stage_fn, final_paths in automatic_stages:
            if not force and _case_stage_complete(config, case_id, final_paths):
                print(f"[{stage_name}][{case_id}] already complete; skipped", flush=True)
                continue
            ret = stage_fn(config, case_args)
            if ret != 0:
                print(f"Stage {stage_name} failed with exit code {ret}")
                return ret
        print(f"[all][{case_id}] completed", flush=True)

    if requested_case is not None:
        print(f"[validate][{requested_case}] validating Case artifacts", flush=True)
        return run_validate(config, args)

    audit_dir = config.paths.artifacts_root / "audit"

    if force:
        print("Starting stage: audit-export (forced)")
        ret = run_audit_export_stage(config, args)
        if ret != 0:
            print(f"Stage audit-export failed with exit code {ret}")
            return ret
    elif not _is_review_completed(audit_dir):
        extraction_file = resolve_review_file(audit_dir, "extraction_review")
        dedup_file = resolve_review_file(audit_dir, "deduplication_review")
        transcript_file = resolve_review_file(audit_dir, "transcript_review")
        if not (extraction_file.is_file() and dedup_file.is_file() and transcript_file.is_file()):
            print("Starting stage: audit-export")
            ret = run_audit_export_stage(config, args)
            if ret != 0:
                print(f"Stage audit-export failed with exit code {ret}")
                return ret
    else:
        print("Audit review spreadsheets already completed. Skipping audit-export.")

    if not _is_review_completed(audit_dir):
        print("\nAudit review sheets exported successfully.")
        print("Human review files are located at:")
        print(f"  - {audit_dir / 'extraction_review.csv'}")
        print(f"  - {audit_dir / 'deduplication_review.csv'}")
        print(f"  - {audit_dir / 'transcript_review.csv'}")
        print("\nTo proceed with the report and validation stages, complete single-reviewer evaluation in these files (or save as *_completed.csv).")
        print("\nThen run:")
        print("  python -m evolution.rq1.cli audit-summarize")
        print("  python -m evolution.rq1.cli report")
        print("  python -m evolution.rq1.cli validate")
        print("or re-run 'python -m evolution.rq1.cli all'.")
        return 0

    post_review_stages = [
        ("audit-summarize", run_audit_summarize_stage),
        ("report", run_report_stage),
        ("validate", run_validate),
    ]
    for stage_name, stage_fn in post_review_stages:
        print(f"Starting stage: {stage_name}")
        ret = stage_fn(config, args)
        if ret != 0:
            print(f"Stage {stage_name} failed with exit code {ret}")
            return ret

    print("All RQ1 evaluation pipeline stages completed successfully.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build unified argument parser with common option inheritance across all commands."""
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "--config",
        type=str,
        default=argparse.SUPPRESS,
        help="Path to YAML configuration file.",
    )
    common_parser.add_argument(
        "--force",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Clean and recreate stage output artifacts.",
    )
    common_parser.add_argument(
        "--case-id",
        type=str,
        default=argparse.SUPPRESS,
        help="Process one Case; omit to process the complete Case set.",
    )

    parser = argparse.ArgumentParser(
        prog="python -m evolution.rq1.cli",
        description="RQ1 Evaluation Pipeline CLI",
        parents=[common_parser],
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subcommand_definitions = [
        ("ingest", "Ingest raw interview conversations."),
        ("riu", "Extract and deduplicate RIUs."),
        ("clustering", "Cluster RIUs and compute Breadth."),
        ("breadth", "Alias for clustering stage."),
        ("elaboration", "Evaluate elaboration and compute Depth."),
        ("depth", "Alias for elaboration stage."),
        ("audit-export", "Sample cases and export review sheets."),
        ("audit-summarize", "Summarize completed review sheets."),
        ("report", "Generate metrics and statistical test reports."),
        ("validate", "Verify all artifact pipeline contracts."),
        ("all", "Execute complete pipeline sequentially."),
    ]
    for name, help_text in subcommand_definitions:
        subparsers.add_parser(name, help=help_text, parents=[common_parser])

    return parser


def resolve_default_config_path() -> Path:
    """Locate default configuration file within repository."""
    repo_root = find_repository_root()
    candidates = [
        repo_root / "evolution" / "rq1" / "config" / "default.yaml",
        repo_root / "evolution" / "rq1" / "config" / "default.example.yaml",
        repo_root / "config.yaml",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return candidates[1]


def main(argv: Sequence[str] | None = None) -> int:
    """Entrypoint function for RQ1 evaluation CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "config"):
        args.config = None
    if not hasattr(args, "force"):
        args.force = False
    if not hasattr(args, "case_id"):
        args.case_id = None

    config_path = (
        Path(args.config) if args.config else resolve_default_config_path()
    )
    config = load_config(config_path)

    dispatch_map = {
        "ingest": run_ingest,
        "riu": run_riu_stage,
        "clustering": run_breadth_stage,
        "breadth": run_breadth_stage,
        "elaboration": run_depth_stage,
        "depth": run_depth_stage,
        "audit-export": run_audit_export_stage,
        "audit-summarize": run_audit_summarize_stage,
        "report": run_report_stage,
        "validate": run_validate,
        "all": run_all,
    }

    handler = dispatch_map.get(args.command)
    if handler is None:
        parser.print_help()
        return 1

    return handler(config, args)


if __name__ == "__main__":
    sys.exit(main())
