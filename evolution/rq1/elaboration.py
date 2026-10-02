"""Pairwise elaboration relationship evaluation and Depth metric calculation module."""

from __future__ import annotations

import statistics
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from evolution.rq1.config import RQ1Config
from evolution.rq1.llm_client import ChatCompletionClient
from evolution.rq1.models import (
    BreadthMetricRecord,
    ClusterAssignment,
    ClusterDepthRecord,
    DecisionUnit,
    ElaborationDAG,
    ElaborationDecision,
    ElaborationEdge,
    ElaborationNode,
    ElaborationOutput,
    ElaborationPair,
    TranscriptClusterCoverage,
    TranscriptMetrics,
    TranscriptRecord,
    UniqueRIU,
)
from evolution.rq1.storage import (
    append_jsonl,
    read_jsonl,
    write_csv,
    write_json,
    write_jsonl,
)


class ElaborationError(Exception):
    """Base exception for elaboration evaluation failures."""


class ElaborationValidationError(ElaborationError):
    """Exception raised when candidate pairs or model responses fail validation."""


class ElaborationCheckpointError(ElaborationError):
    """Exception raised when elaboration checkpoint records fail verification."""


def _print_progress(completed: int, total: int) -> None:
    """Print bounded progress updates for elaboration units."""
    if completed == total or completed % 10 == 0:
        print(f"[elaboration] {completed}/{total} units completed", flush=True)


def build_nodes(
    rius: list[UniqueRIU],
    assignments: list[ClusterAssignment],
) -> dict[tuple[str, str], list[ElaborationNode]]:
    """Construct chronological elaboration nodes for each transcript and cluster unit."""
    riu_lookup: dict[str, UniqueRIU] = {}
    for riu in rius:
        if riu.transcript_riu_id in riu_lookup:
            raise ElaborationValidationError(
                f"Duplicate unique RIU identifier encountered: {riu.transcript_riu_id}"
            )
        riu_lookup[riu.transcript_riu_id] = riu

    grouped_nodes: dict[tuple[str, str], list[ElaborationNode]] = {}

    for assignment in assignments:
        if assignment.transcript_riu_id not in riu_lookup:
            raise ElaborationValidationError(
                f"Cluster assignment references unknown RIU identifier: {assignment.transcript_riu_id}"
            )

        riu = riu_lookup[assignment.transcript_riu_id]
        if riu.transcript_id != assignment.transcript_id:
            raise ElaborationValidationError(
                f"Transcript mismatch for RIU {riu.transcript_riu_id}: "
                f"{riu.transcript_id} != {assignment.transcript_id}"
            )
        if riu.case_id != assignment.case_id:
            raise ElaborationValidationError(
                f"Case mismatch for RIU {riu.transcript_riu_id}: "
                f"{riu.case_id} != {assignment.case_id}"
            )
        if riu.method_id != assignment.method_id:
            raise ElaborationValidationError(
                f"Method mismatch for RIU {riu.transcript_riu_id}: "
                f"{riu.method_id} != {assignment.method_id}"
            )

        if not riu.provenance:
            raise ElaborationValidationError(
                f"Unique RIU has no provenance entries: {riu.transcript_riu_id}"
            )

        earliest_prov = min(
            riu.provenance,
            key=lambda prov: (prov.turn_index, prov.evidence_start),
        )

        node = ElaborationNode(
            node_id=riu.transcript_riu_id,
            turn_index=earliest_prov.turn_index,
            evidence_start=earliest_prov.evidence_start,
            statement=riu.statement,
            evidence_text=earliest_prov.evidence_text,
            context_question=earliest_prov.context_question,
        )

        unit_key = (assignment.transcript_id, assignment.cluster_id)
        grouped_nodes.setdefault(unit_key, []).append(node)

    for unit_key, nodes in grouped_nodes.items():
        node_ids = [n.node_id for n in nodes]
        if len(node_ids) != len(set(node_ids)):
            raise ElaborationValidationError(
                f"Duplicate node identifiers detected within unit {unit_key}"
            )
        nodes.sort(key=lambda n: (n.turn_index, n.evidence_start, n.node_id))

    return grouped_nodes


def build_candidate_pairs(
    nodes: list[ElaborationNode],
) -> list[ElaborationPair]:
    """Generate directed pairs where the earlier node strictly precedes the later node."""
    pairs: list[ElaborationPair] = []
    total_nodes = len(nodes)
    for earlier_idx in range(total_nodes):
        for later_idx in range(earlier_idx + 1, total_nodes):
            pairs.append(
                ElaborationPair(
                    earlier_node_id=nodes[earlier_idx].node_id,
                    later_node_id=nodes[later_idx].node_id,
                )
            )
    return pairs


def judge_pairs(
    transcript_id: str,
    cluster_id: str,
    nodes: list[ElaborationNode],
    pairs: list[ElaborationPair],
    prompt: str,
    client: ChatCompletionClient,
    batch_size: int,
) -> list[ElaborationDecision]:
    """Evaluate candidate pairs through batched language model completions."""
    if not pairs:
        return []

    node_lookup = {node.node_id: node for node in nodes}
    for pair in pairs:
        if pair.earlier_node_id not in node_lookup:
            raise ElaborationValidationError(
                f"Candidate pair references unknown earlier node: {pair.earlier_node_id}"
            )
        if pair.later_node_id not in node_lookup:
            raise ElaborationValidationError(
                f"Candidate pair references unknown later node: {pair.later_node_id}"
            )
        if pair.earlier_node_id == pair.later_node_id:
            raise ElaborationValidationError(
                f"Candidate pair contains identical nodes: {pair.earlier_node_id}"
            )

    expected_all = {(p.earlier_node_id, p.later_node_id) for p in pairs}
    elaboration_pairs: set[tuple[str, str]] = set()
    node_positions = {node.node_id: index for index, node in enumerate(nodes)}

    for batch_start in range(0, len(pairs), batch_size):
        batch_pairs = pairs[batch_start : batch_start + batch_size]
        referenced_ids = {p.earlier_node_id for p in batch_pairs} | {
            p.later_node_id for p in batch_pairs
        }
        batch_nodes = [node for node in nodes if node.node_id in referenced_ids]

        payload = {
            "transcript_id": transcript_id,
            "cluster_id": cluster_id,
            "nodes": [
                {
                    "node_id": node.node_id,
                    "turn_index": node.turn_index,
                    "statement": node.statement,
                    "evidence_text": node.evidence_text,
                    "context_question": node.context_question,
                }
                for node in batch_nodes
            ],
            "pairs": [
                {
                    "earlier_node_id": pair.earlier_node_id,
                    "later_node_id": pair.later_node_id,
                }
                for pair in batch_pairs
            ],
        }

        response_dict = client.complete_json(prompt, payload)
        parsed_output = ElaborationOutput.model_validate(response_dict)

        returned_node_ids = {
            node_id
            for selection in parsed_output.elaboration_pairs
            for node_id in (selection.node_a_id, selection.node_b_id)
        }
        unexpected_nodes = returned_node_ids - referenced_ids
        if unexpected_nodes:
            raise ElaborationValidationError(
                f"Model returned nodes outside the current batch for unit "
                f"{transcript_id}::{cluster_id}: {sorted(unexpected_nodes)}"
            )

        returned_pairs: list[tuple[str, str]] = []
        for selection in parsed_output.elaboration_pairs:
            if selection.node_a_id == selection.node_b_id:
                raise ElaborationValidationError(
                    f"Model returned a self-pair for unit {transcript_id}::{cluster_id}: "
                    f"{selection.node_a_id}"
                )
            if node_positions[selection.node_a_id] < node_positions[selection.node_b_id]:
                returned_pairs.append((selection.node_a_id, selection.node_b_id))
            else:
                returned_pairs.append((selection.node_b_id, selection.node_a_id))

        unexpected = set(returned_pairs) - expected_all
        if unexpected:
            raise ElaborationValidationError(
                f"Model returned invalid elaboration pairs for unit "
                f"{transcript_id}::{cluster_id}: {sorted(unexpected)}"
            )

        elaboration_pairs.update(returned_pairs)

    return [
        ElaborationDecision(
            earlier_node_id=pair.earlier_node_id,
            later_node_id=pair.later_node_id,
            relation=(
                "elaboration"
                if (pair.earlier_node_id, pair.later_node_id) in elaboration_pairs
                else "none"
            ),
        )
        for pair in pairs
    ]


def build_dag(
    transcript_id: str,
    cluster_id: str,
    nodes: list[ElaborationNode],
    decisions: list[ElaborationDecision],
) -> ElaborationDAG:
    """Construct a directed acyclic graph from valid elaboration decisions."""
    node_positions = {node.node_id: idx for idx, node in enumerate(nodes)}
    expected_prefix = f"{transcript_id}::"

    for node in nodes:
        if not node.node_id.startswith(expected_prefix):
            raise ElaborationValidationError(
                f"Node {node.node_id} does not belong to transcript {transcript_id}"
            )

    seen_edges: set[tuple[str, str]] = set()
    edges: list[ElaborationEdge] = []

    for decision in decisions:
        if decision.relation != "elaboration":
            continue

        source_id = decision.earlier_node_id
        target_id = decision.later_node_id

        if source_id not in node_positions:
            raise ElaborationValidationError(
                f"Edge source node does not exist in unit: {source_id}"
            )
        if target_id not in node_positions:
            raise ElaborationValidationError(
                f"Edge target node does not exist in unit: {target_id}"
            )
        if source_id == target_id:
            raise ElaborationValidationError(
                f"Self-loop edge detected: {source_id} -> {target_id}"
            )
        if node_positions[source_id] >= node_positions[target_id]:
            raise ElaborationValidationError(
                f"Edge violates chronological order: {source_id} -> {target_id}"
            )

        edge_tuple = (source_id, target_id)
        if edge_tuple in seen_edges:
            raise ElaborationValidationError(
                f"Duplicate edge detected: {source_id} -> {target_id}"
            )

        seen_edges.add(edge_tuple)
        edges.append(ElaborationEdge(source_id=source_id, target_id=target_id))

    return ElaborationDAG(
        transcript_id=transcript_id,
        cluster_id=cluster_id,
        nodes=nodes,
        edges=edges,
    )


def compute_cluster_depth(dag: ElaborationDAG) -> int:
    """Calculate maximum path length through chronological dynamic programming."""
    if not dag.nodes:
        raise ElaborationError(
            f"Cannot compute depth for empty DAG in {dag.transcript_id}::{dag.cluster_id}"
        )

    depth_map = {node.node_id: 1 for node in dag.nodes}
    outgoing_edges: dict[str, list[str]] = {node.node_id: [] for node in dag.nodes}

    for edge in dag.edges:
        outgoing_edges[edge.source_id].append(edge.target_id)

    for node in dag.nodes:
        current_depth = depth_map[node.node_id]
        for target_id in outgoing_edges[node.node_id]:
            if current_depth + 1 > depth_map[target_id]:
                depth_map[target_id] = current_depth + 1

    return max(depth_map.values())


def compute_transcript_depth_counts(
    transcripts: list[TranscriptRecord],
    cluster_depths: list[ClusterDepthRecord],
) -> dict[str, dict[str, int]]:
    """Count DAGs at each exact depth for every transcript."""
    counts_by_transcript: dict[str, dict[str, int]] = {
        transcript.transcript_id: {} for transcript in transcripts
    }

    for record in cluster_depths:
        if record.transcript_id not in counts_by_transcript:
            raise ElaborationError(
                f"Cluster depth record references unknown transcript: {record.transcript_id}"
            )
        depth_key = str(record.depth)
        transcript_counts = counts_by_transcript[record.transcript_id]
        transcript_counts[depth_key] = transcript_counts.get(depth_key, 0) + 1

    return {
        transcript_id: dict(
            sorted(counts.items(), key=lambda item: int(item[0]))
        )
        for transcript_id, counts in counts_by_transcript.items()
    }


def run_elaboration(
    config: RQ1Config,
    client: ChatCompletionClient | None = None,
) -> None:
    """Execute end-to-end elaboration relationship judgment and depth metric pipeline."""
    artifacts_root = config.paths.artifacts_root
    transcripts_path = artifacts_root / "ingestion" / "transcripts.jsonl"
    unique_rius_path = artifacts_root / "riu" / "unique_rius.jsonl"
    assignments_path = artifacts_root / "clustering" / "cluster_assignments.jsonl"
    coverage_path = artifacts_root / "clustering" / "transcript_cluster_coverage.jsonl"
    breadth_path = artifacts_root / "clustering" / "breadth_metrics.jsonl"

    if not transcripts_path.is_file():
        raise ElaborationError(f"Transcripts artifact not found: {transcripts_path}")
    if not unique_rius_path.is_file():
        raise ElaborationError(f"Unique RIUs artifact not found: {unique_rius_path}")
    if not assignments_path.is_file():
        raise ElaborationError(
            f"Cluster assignments artifact not found: {assignments_path}"
        )
    if not coverage_path.is_file():
        raise ElaborationError(
            f"Transcript cluster coverage artifact not found: {coverage_path}"
        )
    if not breadth_path.is_file():
        raise ElaborationError(
            f"Breadth metrics artifact not found: {breadth_path}"
        )

    transcripts = [
        TranscriptRecord.model_validate(row)
        for row in read_jsonl(transcripts_path)
    ]
    unique_rius = [
        UniqueRIU.model_validate(row)
        for row in read_jsonl(unique_rius_path)
    ]
    assignments = [
        ClusterAssignment.model_validate(row)
        for row in read_jsonl(assignments_path)
    ]
    coverage_records = [
        TranscriptClusterCoverage.model_validate(row)
        for row in read_jsonl(coverage_path)
    ]
    breadth_records = [
        BreadthMetricRecord.model_validate(row)
        for row in read_jsonl(breadth_path)
    ]

    unit_nodes = build_nodes(unique_rius, assignments)

    sorted_coverage = sorted(
        coverage_records,
        key=lambda cov: (cov.case_id, cov.transcript_id, cov.cluster_id),
    )
    expected_unit_keys = [
        (cov.transcript_id, cov.cluster_id) for cov in sorted_coverage
    ]

    for unit_key in expected_unit_keys:
        if unit_key not in unit_nodes:
            raise ElaborationValidationError(
                f"Coverage unit {unit_key} has no corresponding nodes constructed"
            )

    unit_candidate_pairs: dict[tuple[str, str], list[ElaborationPair]] = {
        unit_key: build_candidate_pairs(unit_nodes[unit_key])
        for unit_key in expected_unit_keys
    }

    elaboration_dir = artifacts_root / "elaboration"
    elaboration_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = elaboration_dir / "decision_units.jsonl"
    errors_path = elaboration_dir / "errors.jsonl"

    completed_units: dict[tuple[str, str], DecisionUnit] = {}

    if checkpoint_path.is_file():
        for row in read_jsonl(checkpoint_path):
            unit = DecisionUnit.model_validate(row)
            unit_key = (unit.transcript_id, unit.cluster_id)

            if unit_key not in unit_candidate_pairs:
                raise ElaborationCheckpointError(
                    f"Checkpoint contains unknown composition unit: {unit_key}"
                )
            if unit_key in completed_units:
                raise ElaborationCheckpointError(
                    f"Duplicate checkpoint composition unit: {unit_key}"
                )

            expected_pairs = unit_candidate_pairs[unit_key]
            expected_keys = [
                (p.earlier_node_id, p.later_node_id) for p in expected_pairs
            ]
            checkpoint_keys = [
                (d.earlier_node_id, d.later_node_id) for d in unit.decisions
            ]

            if len(checkpoint_keys) != len(set(checkpoint_keys)):
                raise ElaborationCheckpointError(
                    f"Checkpoint contains duplicate decisions for unit {unit_key}"
                )

            if set(checkpoint_keys) != set(expected_keys):
                missing = set(expected_keys) - set(checkpoint_keys)
                unexpected = set(checkpoint_keys) - set(expected_keys)
                raise ElaborationCheckpointError(
                    f"Checkpoint decisions do not match candidate pairs for unit {unit_key}. "
                    f"Missing: {sorted(missing)}, Unexpected: {sorted(unexpected)}"
                )

            nodes = unit_nodes[unit_key]
            node_positions = {node.node_id: idx for idx, node in enumerate(nodes)}
            for decision in unit.decisions:
                if decision.earlier_node_id not in node_positions:
                    raise ElaborationCheckpointError(
                        f"Checkpoint decision references unknown earlier node: {decision.earlier_node_id}"
                    )
                if decision.later_node_id not in node_positions:
                    raise ElaborationCheckpointError(
                        f"Checkpoint decision references unknown later node: {decision.later_node_id}"
                    )
                if (
                    node_positions[decision.earlier_node_id]
                    >= node_positions[decision.later_node_id]
                ):
                    raise ElaborationCheckpointError(
                        f"Checkpoint decision violates chronological order: "
                        f"{decision.earlier_node_id} -> {decision.later_node_id}"
                    )

            completed_units[unit_key] = unit

    prompt_path = Path(__file__).parent / "prompts" / "judge_elaboration.txt"
    if not prompt_path.is_file():
        raise ElaborationError(f"Prompt template file not found: {prompt_path}")
    prompt_text = prompt_path.read_text(encoding="utf-8")

    file_lock = threading.Lock()

    def process_unit(
        unit_key: tuple[str, str],
        active_client: ChatCompletionClient,
    ) -> DecisionUnit:
        transcript_id, cluster_id = unit_key
        nodes = unit_nodes[unit_key]
        pairs = unit_candidate_pairs[unit_key]

        if not pairs:
            return DecisionUnit(
                transcript_id=transcript_id,
                cluster_id=cluster_id,
                decisions=[],
            )

        decisions = judge_pairs(
            transcript_id=transcript_id,
            cluster_id=cluster_id,
            nodes=nodes,
            pairs=pairs,
            prompt=prompt_text,
            client=active_client,
            batch_size=config.elaboration.pair_batch_size,
        )
        unit = DecisionUnit(
            transcript_id=transcript_id,
            cluster_id=cluster_id,
            decisions=decisions,
        )
        with file_lock:
            append_jsonl(checkpoint_path, unit)
        return unit

    pending_unit_keys = [
        key for key in expected_unit_keys if key not in completed_units
    ]
    total_units = len(expected_unit_keys)
    print(
        f"[elaboration] starting with {len(completed_units)}/{total_units} units restored",
        flush=True,
    )

    immediate_keys = [
        key for key in pending_unit_keys if len(unit_candidate_pairs[key]) == 0
    ]
    llm_keys = [
        key for key in pending_unit_keys if len(unit_candidate_pairs[key]) > 0
    ]

    for key in immediate_keys:
        t_id, c_id = key
        unit = DecisionUnit(
            transcript_id=t_id,
            cluster_id=c_id,
            decisions=[],
        )
        with file_lock:
            append_jsonl(checkpoint_path, unit)
        completed_units[key] = unit
        _print_progress(len(completed_units), total_units)

    if llm_keys:
        def execute_workers(active_client: ChatCompletionClient) -> None:
            with ThreadPoolExecutor(
                max_workers=config.llm.concurrency
            ) as executor:
                future_to_key = {
                    executor.submit(
                        process_unit,
                        key,
                        active_client,
                    ): key
                    for key in llm_keys
                }

                for future in as_completed(future_to_key):
                    key = future_to_key[future]
                    t_id, c_id = key
                    try:
                        unit = future.result()
                        completed_units[key] = unit
                        _print_progress(len(completed_units), total_units)
                    except Exception as exc:
                        with file_lock:
                            append_jsonl(
                                errors_path,
                                {
                                    "stage": "elaboration",
                                    "transcript_id": t_id,
                                    "cluster_id": c_id,
                                    "error_type": type(exc).__name__,
                                    "error_message": str(exc),
                                },
                            )
                        for pending_future in future_to_key:
                            pending_future.cancel()
                        raise

        if client is not None:
            execute_workers(client)
        else:
            with ChatCompletionClient(config.llm) as active_client:
                execute_workers(active_client)

    all_dags: list[ElaborationDAG] = []
    all_cluster_depths: list[ClusterDepthRecord] = []

    for cov in sorted_coverage:
        unit_key = (cov.transcript_id, cov.cluster_id)
        unit = completed_units[unit_key]
        nodes = unit_nodes[unit_key]

        dag = build_dag(
            transcript_id=cov.transcript_id,
            cluster_id=cov.cluster_id,
            nodes=nodes,
            decisions=unit.decisions,
        )
        all_dags.append(dag)

        depth = compute_cluster_depth(dag)
        all_cluster_depths.append(
            ClusterDepthRecord(
                case_id=cov.case_id,
                transcript_id=cov.transcript_id,
                method_id=cov.method_id,
                cluster_id=cov.cluster_id,
                node_count=len(dag.nodes),
                edge_count=len(dag.edges),
                depth=depth,
            )
        )

    transcript_depth_counts = compute_transcript_depth_counts(
        transcripts=transcripts,
        cluster_depths=all_cluster_depths,
    )

    yield_by_transcript: dict[str, int] = {
        transcript.transcript_id: 0 for transcript in transcripts
    }
    for riu in unique_rius:
        yield_by_transcript[riu.transcript_id] += 1

    breadth_by_transcript: dict[str, int] = {
        transcript.transcript_id: 0 for transcript in transcripts
    }
    clusters_by_transcript: dict[str, set[str]] = {
        transcript.transcript_id: set() for transcript in transcripts
    }
    for cov in coverage_records:
        if cov.transcript_id not in clusters_by_transcript:
            raise ElaborationValidationError(
                f"Coverage references unknown transcript: {cov.transcript_id}"
            )
        clusters_by_transcript[cov.transcript_id].add(cov.cluster_id)

    for t_id, cluster_set in clusters_by_transcript.items():
        breadth_by_transcript[t_id] = len(cluster_set)

    seen_breadth_transcripts: set[str] = set()
    transcript_lookup = {t.transcript_id: t for t in transcripts}
    for b_rec in breadth_records:
        if b_rec.transcript_id in seen_breadth_transcripts:
            raise ElaborationValidationError(
                f"Duplicate breadth record encountered: {b_rec.transcript_id}"
            )
        seen_breadth_transcripts.add(b_rec.transcript_id)

        if b_rec.transcript_id not in transcript_lookup:
            raise ElaborationValidationError(
                f"Breadth record references unknown transcript: {b_rec.transcript_id}"
            )
        t_meta = transcript_lookup[b_rec.transcript_id]
        if b_rec.case_id != t_meta.case_id or b_rec.method_id != t_meta.method_id:
            raise ElaborationValidationError(
                f"Metadata mismatch in breadth record for {b_rec.transcript_id}: "
                f"({b_rec.case_id}, {b_rec.method_id}) != ({t_meta.case_id}, {t_meta.method_id})"
            )
        expected_breadth = breadth_by_transcript[b_rec.transcript_id]
        if b_rec.breadth != expected_breadth:
            raise ElaborationValidationError(
                f"Breadth record value ({b_rec.breadth}) does not match "
                f"coverage-derived breadth ({expected_breadth}) for {b_rec.transcript_id}"
            )

    missing_breadth_ids = set(transcript_lookup.keys()) - seen_breadth_transcripts
    if missing_breadth_ids:
        raise ElaborationValidationError(
            f"Missing breadth records for transcripts: {sorted(missing_breadth_ids)}"
        )

    all_transcript_metrics: list[TranscriptMetrics] = []
    for transcript in transcripts:
        t_id = transcript.transcript_id
        depth_counts = transcript_depth_counts[t_id]
        if sum(depth_counts.values()) != breadth_by_transcript[t_id]:
            raise ElaborationValidationError(
                f"Depth DAG count ({sum(depth_counts.values())}) does not match "
                f"breadth ({breadth_by_transcript[t_id]}) for {t_id}"
            )
        all_transcript_metrics.append(
            TranscriptMetrics(
                case_id=transcript.case_id,
                transcript_id=t_id,
                method_id=transcript.method_id,
                yield_count=yield_by_transcript[t_id],
                breadth=breadth_by_transcript[t_id],
                depth_counts=depth_counts,
            )
        )

    write_jsonl(elaboration_dir / "dags.jsonl", all_dags)

    depth_fieldnames = [
        "case_id",
        "transcript_id",
        "method_id",
        "cluster_id",
        "node_count",
        "edge_count",
        "depth",
    ]
    write_csv(
        elaboration_dir / "cluster_depths.csv",
        depth_fieldnames,
        [cd.model_dump() for cd in all_cluster_depths],
    )

    write_jsonl(
        elaboration_dir / "transcript_metrics.jsonl",
        all_transcript_metrics,
    )

    total_dags = len(all_dags)
    total_edges = sum(len(dag.edges) for dag in all_dags)
    summary: dict[str, Any] = {
        "total_transcripts": len(transcripts),
        "total_coverage_units": len(sorted_coverage),
        "total_dags": total_dags,
        "total_edges": total_edges,
        "methods": {},
    }

    for method in config.methods:
        method_metrics = [
            m for m in all_transcript_metrics if m.method_id == method
        ]
        yield_values = [m.yield_count for m in method_metrics]
        breadth_values = [m.breadth for m in method_metrics]
        method_depth_counts: dict[str, int] = {}
        for metric in method_metrics:
            for depth, count in metric.depth_counts.items():
                method_depth_counts[depth] = method_depth_counts.get(depth, 0) + count

        summary["methods"][method] = {
            "mean_yield": (
                round(float(statistics.mean(yield_values)), 4)
                if yield_values
                else 0.0
            ),
            "mean_breadth": (
                round(float(statistics.mean(breadth_values)), 4)
                if breadth_values
                else 0.0
            ),
            "depth_counts": dict(
                sorted(method_depth_counts.items(), key=lambda item: int(item[0]))
            ),
            "total_covered_clusters": sum(method_depth_counts.values()),
        }

    write_json(elaboration_dir / "summary.json", summary)
    write_jsonl(errors_path, [])
