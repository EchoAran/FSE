"""Case-level shared requirement clustering and transcript breadth calculation module."""

from __future__ import annotations

import statistics
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.cluster import AgglomerativeClustering

from evolution.rq1.config import RQ1Config
from evolution.rq1.embedding_client import EmbeddingClient
from evolution.rq1.models import (
    BreadthMetricRecord,
    ClusterAssignment,
    EmbeddingIndexRecord,
    TranscriptClusterCoverage,
    TranscriptRecord,
    UniqueRIU,
)
from evolution.rq1.storage import read_jsonl, write_csv, write_json, write_jsonl


class ClusteringError(Exception):
    """Base exception for clustering and breadth computation failures."""


class EmbeddingAlignmentError(ClusteringError):
    """Exception raised when embeddings and index records fail alignment checks."""


def group_rius_by_case(rius: list[UniqueRIU]) -> dict[str, list[UniqueRIU]]:
    """Group unique RIU instances across all methods by case identifier."""
    grouped: dict[str, list[UniqueRIU]] = {}
    for riu in rius:
        grouped.setdefault(riu.case_id, []).append(riu)
    return grouped


def build_embeddings(
    rius: list[UniqueRIU],
    client: EmbeddingClient,
) -> tuple[list[EmbeddingIndexRecord], np.ndarray]:
    """Generate embeddings for unique RIUs sorted deterministically across cases and transcripts."""
    sorted_rius = sorted(
        rius,
        key=lambda r: (r.case_id, r.transcript_id, r.first_position, r.transcript_riu_id),
    )

    if not sorted_rius:
        empty_matrix = np.empty((0, client.config.dimensions), dtype=np.float32)
        return [], empty_matrix

    statements = [r.statement for r in sorted_rius]
    vectors = client.embed(statements)

    if vectors.shape[0] != len(sorted_rius):
        raise EmbeddingAlignmentError(
            f"Embedding vector count ({vectors.shape[0]}) does not match RIU count ({len(sorted_rius)})"
        )

    records = [
        EmbeddingIndexRecord(
            row_index=idx,
            transcript_riu_id=r.transcript_riu_id,
            case_id=r.case_id,
            statement=r.statement,
        )
        for idx, r in enumerate(sorted_rius)
    ]
    return records, vectors


def cluster_case(
    case_id: str,
    rius: list[UniqueRIU],
    vectors: np.ndarray,
    distance_threshold: float,
) -> list[ClusterAssignment]:
    """Cluster unique RIUs of a single case using Agglomerative Clustering with cosine distance."""
    if not rius:
        return []

    if len(rius) != vectors.shape[0]:
        raise ClusteringError(
            f"Case {case_id} RIU count ({len(rius)}) does not match vector count ({vectors.shape[0]})"
        )

    if len(rius) == 1:
        single_riu = rius[0]
        return [
            ClusterAssignment(
                case_id=case_id,
                transcript_riu_id=single_riu.transcript_riu_id,
                transcript_id=single_riu.transcript_id,
                method_id=single_riu.method_id,
                cluster_id=f"{case_id}::C001",
            )
        ]

    model = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=distance_threshold,
        metric="cosine",
        linkage="average",
        compute_full_tree=True,
    )
    raw_labels = model.fit_predict(vectors)

    earliest_pos_per_label: dict[int, int] = {}
    for idx, label in enumerate(raw_labels):
        if label not in earliest_pos_per_label:
            earliest_pos_per_label[label] = idx

    sorted_raw_labels = sorted(earliest_pos_per_label.keys(), key=lambda l: earliest_pos_per_label[l])
    label_to_cluster_id = {
        label: f"{case_id}::C{cluster_num:03d}"
        for cluster_num, label in enumerate(sorted_raw_labels, start=1)
    }

    assignments: list[ClusterAssignment] = []
    for idx, riu in enumerate(rius):
        cluster_id = label_to_cluster_id[raw_labels[idx]]
        assignments.append(
            ClusterAssignment(
                case_id=case_id,
                transcript_riu_id=riu.transcript_riu_id,
                transcript_id=riu.transcript_id,
                method_id=riu.method_id,
                cluster_id=cluster_id,
            )
        )
    return assignments


def build_coverage(
    assignments: list[ClusterAssignment],
) -> list[TranscriptClusterCoverage]:
    """Aggregate cluster assignments into transcript-cluster coverage entries."""
    grouped: dict[tuple[str, str, str, str], list[str]] = {}
    for a in assignments:
        key = (a.case_id, a.transcript_id, a.method_id, a.cluster_id)
        grouped.setdefault(key, []).append(a.transcript_riu_id)

    sorted_keys = sorted(grouped.keys(), key=lambda k: (k[0], k[1], k[3]))
    coverage_records: list[TranscriptClusterCoverage] = []
    for case_id, transcript_id, method_id, cluster_id in sorted_keys:
        coverage_records.append(
            TranscriptClusterCoverage(
                case_id=case_id,
                transcript_id=transcript_id,
                method_id=method_id,
                cluster_id=cluster_id,
                transcript_riu_ids=grouped[(case_id, transcript_id, method_id, cluster_id)],
            )
        )
    return coverage_records


def compute_breadth(
    transcripts: list[TranscriptRecord],
    coverage: list[TranscriptClusterCoverage],
) -> list[BreadthMetricRecord]:
    """Compute Breadth as the count of distinct covered clusters for each transcript."""
    covered_clusters_by_transcript: dict[str, set[str]] = {}
    for cov in coverage:
        covered_clusters_by_transcript.setdefault(cov.transcript_id, set()).add(cov.cluster_id)

    metrics: list[BreadthMetricRecord] = []
    for t in transcripts:
        distinct_clusters = covered_clusters_by_transcript.get(t.transcript_id, set())
        metrics.append(
            BreadthMetricRecord(
                transcript_id=t.transcript_id,
                case_id=t.case_id,
                method_id=t.method_id,
                breadth=len(distinct_clusters),
            )
        )
    return metrics


def compute_sensitivity(
    cases: dict[str, list[UniqueRIU]],
    vectors_by_case: dict[str, np.ndarray],
    transcripts: list[TranscriptRecord],
    thresholds: list[float],
) -> list[dict[str, Any]]:
    """Compute Breadth variations across multiple sensitivity distance thresholds."""
    rows: list[dict[str, Any]] = []

    for threshold in thresholds:
        all_assignments: list[ClusterAssignment] = []
        for case_id in sorted(cases.keys()):
            c_rius = cases[case_id]
            c_vectors = vectors_by_case[case_id]
            c_assignments = cluster_case(case_id, c_rius, c_vectors, threshold)
            all_assignments.extend(c_assignments)

        coverage = build_coverage(all_assignments)
        breadth_records = compute_breadth(transcripts, coverage)

        distinct_clusters = len({a.cluster_id for a in all_assignments})
        for b_rec in breadth_records:
            rows.append(
                {
                    "threshold": threshold,
                    "case_id": b_rec.case_id,
                    "transcript_id": b_rec.transcript_id,
                    "method_id": b_rec.method_id,
                    "breadth": b_rec.breadth,
                    "total_clusters": distinct_clusters,
                }
            )
    return rows


def run_clustering(config: RQ1Config) -> None:
    """Execute the full Case-level clustering and Breadth calculation pipeline."""
    artifacts_root = config.paths.artifacts_root
    transcripts_path = artifacts_root / "ingestion" / "transcripts.jsonl"
    unique_rius_path = artifacts_root / "riu" / "unique_rius.jsonl"

    if not transcripts_path.is_file():
        raise ClusteringError(f"Transcripts artifact not found: {transcripts_path}")
    if not unique_rius_path.is_file():
        raise ClusteringError(f"Unique RIUs artifact not found: {unique_rius_path}")

    transcript_rows = read_jsonl(transcripts_path)
    transcripts = [TranscriptRecord.model_validate(r) for r in transcript_rows]

    unique_riu_rows = read_jsonl(unique_rius_path)
    unique_rius = [UniqueRIU.model_validate(r) for r in unique_riu_rows]
    case_ids = sorted({t.case_id for t in transcripts})
    print(
        f"[clustering] embedding {len(unique_rius)} RIUs for {len(case_ids)} Case",
        flush=True,
    )

    clustering_dir = artifacts_root / "clustering"
    clustering_dir.mkdir(parents=True, exist_ok=True)

    with EmbeddingClient(config.embedding) as emb_client:
        index_records, matrix = build_embeddings(unique_rius, emb_client)
    print(f"[clustering] embedded {len(index_records)} RIUs", flush=True)

    index_path = clustering_dir / "embedding_index.jsonl"
    matrix_path = clustering_dir / "embeddings.npy"

    write_jsonl(index_path, index_records)
    np.save(matrix_path, matrix)

    cases = group_rius_by_case(unique_rius)
    sorted_cases = sorted(cases.keys())

    vectors_by_case: dict[str, np.ndarray] = {}
    riu_to_vector_idx = {rec.transcript_riu_id: rec.row_index for rec in index_records}

    for case_id in sorted_cases:
        c_rius = cases[case_id]
        sorted_c_rius = sorted(
            c_rius,
            key=lambda r: (r.case_id, r.transcript_id, r.first_position, r.transcript_riu_id),
        )
        cases[case_id] = sorted_c_rius
        case_indices = [riu_to_vector_idx[r.transcript_riu_id] for r in sorted_c_rius]
        vectors_by_case[case_id] = matrix[case_indices]

    main_threshold = config.clustering.distance_threshold
    all_main_assignments: list[ClusterAssignment] = []
    for case_id in sorted_cases:
        case_assignments = cluster_case(
            case_id,
            cases[case_id],
            vectors_by_case[case_id],
            main_threshold,
        )
        all_main_assignments.extend(case_assignments)

    coverage = build_coverage(all_main_assignments)
    breadth_metrics = compute_breadth(transcripts, coverage)

    write_jsonl(clustering_dir / "cluster_assignments.jsonl", all_main_assignments)
    write_jsonl(clustering_dir / "transcript_cluster_coverage.jsonl", coverage)
    write_jsonl(clustering_dir / "breadth_metrics.jsonl", breadth_metrics)

    sensitivity_rows = compute_sensitivity(
        cases,
        vectors_by_case,
        transcripts,
        config.clustering.sensitivity_thresholds,
    )
    sensitivity_fieldnames = [
        "threshold",
        "case_id",
        "transcript_id",
        "method_id",
        "breadth",
        "total_clusters",
    ]
    write_csv(
        clustering_dir / "threshold_sensitivity.csv",
        sensitivity_fieldnames,
        sensitivity_rows,
    )

    total_clusters = len({a.cluster_id for a in all_main_assignments})
    breadth_by_method: dict[str, list[int]] = {m: [] for m in config.methods}
    for bm in breadth_metrics:
        breadth_by_method[bm.method_id].append(bm.breadth)

    summary: dict[str, Any] = {
        "distance_threshold": main_threshold,
        "total_cases": len(sorted_cases),
        "total_unique_rius": len(unique_rius),
        "total_clusters": total_clusters,
        "methods": {},
    }

    for method_id in config.methods:
        b_list = breadth_by_method[method_id]
        summary["methods"][method_id] = {
            "mean_breadth": float(statistics.mean(b_list)) if b_list else 0.0,
            "median_breadth": float(statistics.median(b_list)) if b_list else 0.0,
            "min_breadth": min(b_list) if b_list else 0,
            "max_breadth": max(b_list) if b_list else 0,
        }

    write_json(clustering_dir / "summary.json", summary)
    print(
        f"[clustering] completed {len(sorted_cases)} Case with {total_clusters} clusters",
        flush=True,
    )
