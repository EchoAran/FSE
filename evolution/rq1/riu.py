"""Requirement Information Unit (RIU) extraction and deduplication module."""

from __future__ import annotations

import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Callable, NamedTuple

from evolution.rq1.config import RQ1Config
from evolution.rq1.llm_client import ChatCompletionClient
from evolution.rq1.models import (
    DeduplicationBatchUnit,
    DeduplicationGroup,
    DeduplicationOutput,
    DeduplicationUnit,
    ExtractedRIU,
    ExtractionOutput,
    ExtractionUnit,
    ResponseRecord,
    RIUProvenance,
    TranscriptRecord,
    UniqueRIU,
)
from evolution.rq1.storage import append_jsonl, read_jsonl, write_json, write_jsonl


class RIUProcessingError(Exception):
    """Base exception for RIU extraction and deduplication errors."""


class ExtractionError(RIUProcessingError):
    """Exception raised when response extraction output fails validation."""


class EvidenceMismatchError(ExtractionError):
    """Exception raised when evidence text does not match the answer substring."""


class PartitionError(RIUProcessingError):
    """Exception raised when deduplication groups fail partition validation."""


class CheckpointError(RIUProcessingError):
    """Exception raised when an intermediate checkpoint record fails integrity validation."""


def _print_progress(stage: str, completed: int, total: int) -> None:
    """Print bounded progress updates for a long-running stage."""
    if completed == total or completed % 10 == 0:
        print(f"[{stage}] {completed}/{total} completed", flush=True)


class EvidenceSegment(NamedTuple):
    """Exact answer slice offered to the language model for evidence selection."""

    segment_id: int
    start: int
    end: int
    text: str


def build_evidence_segments(answer: str) -> list[EvidenceSegment]:
    """Split an answer at clause boundaries while preserving source offsets."""
    spans: list[tuple[int, int]] = []
    start = 0
    for match in re.finditer(r"[,;:!?\u3002\uff0c\uff01\uff1f\uff1b\uff1a]|\.(?=\s|$)|\r?\n+", answer):
        end = match.start() if match.group().startswith(("\r", "\n")) else match.end()
        spans.append((start, end))
        start = match.end()
    spans.append((start, len(answer)))

    segments: list[EvidenceSegment] = []
    for raw_start, raw_end in spans:
        segment_start = raw_start
        segment_end = raw_end
        while segment_start < segment_end and answer[segment_start].isspace():
            segment_start += 1
        while segment_end > segment_start and answer[segment_end - 1].isspace():
            segment_end -= 1
        if segment_start == segment_end:
            continue
        segments.append(
            EvidenceSegment(
                segment_id=len(segments) + 1,
                start=segment_start,
                end=segment_end,
                text=answer[segment_start:segment_end],
            )
        )
    return segments


def extract_response(
    response: ResponseRecord,
    prompt: str,
    client: ChatCompletionClient,
) -> ExtractionUnit:
    """Extract Requirement Information Units from a single response using LLM."""
    evidence_segments = build_evidence_segments(response.answer)
    user_payload = {
        "context_question": response.context_question,
        "evidence_segments": [
            {"segment_id": segment.segment_id, "text": segment.text}
            for segment in evidence_segments
        ],
    }

    raw_output = client.complete_json(prompt, user_payload)
    output = ExtractionOutput.model_validate(raw_output)

    rius_with_id: list[ExtractedRIU] = []
    for idx, riu in enumerate(output.rius, start=1):
        if riu.ordinal != idx:
            raise ExtractionError(
                f"Ordinal mismatch in {response.response_id}: expected {idx}, got {riu.ordinal}"
            )

        start_segment_id = riu.evidence_start_segment_id
        end_segment_id = riu.evidence_end_segment_id
        if start_segment_id > end_segment_id:
            raise EvidenceMismatchError(
                f"Evidence segment range is reversed in {response.response_id}, "
                f"RIU {riu.ordinal}: {start_segment_id}-{end_segment_id}"
            )
        if start_segment_id < 1 or end_segment_id > len(evidence_segments):
            raise EvidenceMismatchError(
                f"Unknown evidence segment ID in {response.response_id}, "
                f"RIU {riu.ordinal}: {start_segment_id}-{end_segment_id}"
            )
        first_segment = evidence_segments[start_segment_id - 1]
        last_segment = evidence_segments[end_segment_id - 1]
        start = first_segment.start
        end = last_segment.end
        evidence_text = response.answer[start:end]

        riu_id = f"{response.response_id}::U{riu.ordinal:02d}"
        rius_with_id.append(
            ExtractedRIU(
                ordinal=riu.ordinal,
                statement=riu.statement,
                evidence_text=evidence_text,
                evidence_start=start,
                evidence_end=end,
                riu_id=riu_id,
            )
        )

    return ExtractionUnit(
        response_id=response.response_id,
        transcript_id=response.transcript_id,
        case_id=response.case_id,
        method_id=response.method_id,
        turn_index=response.turn_index,
        rius=rius_with_id,
    )


def extract_all(
    config: RQ1Config,
    responses: list[ResponseRecord],
    prompt: str,
    client: ChatCompletionClient,
) -> list[ExtractionUnit]:
    """Extract raw RIUs for all responses concurrently, supporting resumption."""
    artifacts_dir = config.paths.artifacts_root / "riu"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    extraction_units_path = artifacts_dir / "extraction_units.jsonl"
    raw_rius_path = artifacts_dir / "raw_rius.jsonl"
    errors_path = artifacts_dir / "errors.jsonl"

    completed_units: dict[str, ExtractionUnit] = {}
    expected_responses_map = {r.response_id: r for r in responses}

    if extraction_units_path.is_file():
        existing_rows = read_jsonl(extraction_units_path)
        seen_response_ids: set[str] = set()
        for row in existing_rows:
            unit = ExtractionUnit.model_validate(row)
            if unit.response_id in seen_response_ids:
                raise CheckpointError(
                    f"Duplicate response checkpoint for '{unit.response_id}' in {extraction_units_path}"
                )
            seen_response_ids.add(unit.response_id)

            if unit.response_id not in expected_responses_map:
                raise CheckpointError(
                    f"Unknown response checkpoint '{unit.response_id}' not in expected responses"
                )

            expected_resp = expected_responses_map[unit.response_id]
            if (
                unit.case_id != expected_resp.case_id
                or unit.method_id != expected_resp.method_id
                or unit.turn_index != expected_resp.turn_index
                or unit.transcript_id != expected_resp.transcript_id
            ):
                raise CheckpointError(
                    f"Metadata mismatch in extraction checkpoint for '{unit.response_id}'"
                )

            answer_len = len(expected_resp.answer)
            for idx, riu in enumerate(unit.rius, start=1):
                if riu.ordinal != idx:
                    raise CheckpointError(
                        f"Ordinal mismatch in checkpoint for '{unit.response_id}': expected {idx}, got {riu.ordinal}"
                    )
                expected_riu_id = f"{unit.response_id}::U{riu.ordinal:02d}"
                if riu.riu_id != expected_riu_id:
                    raise CheckpointError(
                        f"RIU ID mismatch in checkpoint: expected '{expected_riu_id}', got '{riu.riu_id}'"
                    )
                if riu.evidence_start < 0 or riu.evidence_end > answer_len or riu.evidence_start >= riu.evidence_end:
                    raise CheckpointError(
                        f"Invalid evidence offsets in checkpoint for '{unit.response_id}'"
                    )
                if expected_resp.answer[riu.evidence_start:riu.evidence_end] != riu.evidence_text:
                    raise CheckpointError(
                        f"Evidence text mismatch in checkpoint for '{unit.response_id}'"
                    )

            completed_units[unit.response_id] = unit

    pending_responses = [resp for resp in responses if resp.response_id not in completed_units]
    file_lock = threading.Lock()
    total_responses = len(responses)
    print(
        f"[extraction] starting with {len(completed_units)}/{total_responses} responses restored",
        flush=True,
    )

    if pending_responses:
        with ThreadPoolExecutor(max_workers=config.llm.concurrency) as executor:
            future_to_resp = {
                executor.submit(extract_response, resp, prompt, client): resp
                for resp in pending_responses
            }
            for future in as_completed(future_to_resp):
                resp = future_to_resp[future]
                try:
                    unit = future.result()
                    completed_units[resp.response_id] = unit
                    with file_lock:
                        append_jsonl(extraction_units_path, unit)
                    _print_progress(
                        "extraction", len(completed_units), total_responses
                    )
                except Exception as err:
                    with file_lock:
                        append_jsonl(
                            errors_path,
                            {
                                "stage": "extraction",
                                "response_id": resp.response_id,
                                "error_type": type(err).__name__,
                                "error_message": str(err),
                            },
                        )
                    for pending_future in future_to_resp:
                        pending_future.cancel()
                    raise

    ordered_units = [completed_units[resp.response_id] for resp in responses]

    all_raw_rius: list[ExtractedRIU] = []
    for unit in ordered_units:
        all_raw_rius.extend(unit.rius)

    write_jsonl(raw_rius_path, all_raw_rius)
    write_jsonl(errors_path, [])
    return ordered_units


def validate_partition(
    expected_ids: set[str],
    groups: list[DeduplicationGroup],
    expected_transcript_id: str | None = None,
) -> None:
    """Validate that groups form a valid mathematical partition of expected RIU IDs without crossing transcripts."""
    seen_ids: set[str] = set()

    for group in groups:
        member_set = set(group.member_riu_ids)
        if group.representative_riu_id not in member_set:
            raise PartitionError(
                f"Representative '{group.representative_riu_id}' is not in group members {group.member_riu_ids}"
            )

        if len(group.member_riu_ids) != len(member_set):
            raise PartitionError(
                f"Duplicate members within group for representative '{group.representative_riu_id}'"
            )

        if expected_transcript_id is not None:
            expected_prefix = f"{expected_transcript_id}::"
            for mid in group.member_riu_ids:
                if not mid.startswith(expected_prefix):
                    raise PartitionError(
                        f"Group member '{mid}' does not match expected transcript '{expected_transcript_id}'"
                    )
        else:
            prefixes = {mid.split("::A")[0] for mid in group.member_riu_ids}
            if len(prefixes) > 1:
                raise PartitionError(
                    f"Group crosses multiple transcripts: {sorted(prefixes)}"
                )

        overlap = seen_ids & member_set
        if overlap:
            raise PartitionError(f"Duplicate raw RIU IDs found across groups: {sorted(overlap)}")

        seen_ids.update(member_set)

    unknown_ids = seen_ids - expected_ids
    if unknown_ids:
        raise PartitionError(f"Unknown RIU IDs in deduplication groups: {sorted(unknown_ids)}")

    missing_ids = expected_ids - seen_ids
    if missing_ids:
        raise PartitionError(f"Missing raw RIU IDs in deduplication groups: {sorted(missing_ids)}")


def deduplicate_transcript(
    transcript: TranscriptRecord,
    raw_rius: list[ExtractedRIU],
    provenance_map: dict[str, RIUProvenance],
    prompt: str,
    client: ChatCompletionClient,
    batch_size: int,
    batch_checkpoint: DeduplicationBatchUnit | None = None,
    checkpoint_callback: Callable[[DeduplicationBatchUnit], None] | None = None,
) -> tuple[list[DeduplicationGroup], list[UniqueRIU]]:
    """Deduplicate raw RIUs within one transcript into unique canonical units."""
    expected_prefix = f"{transcript.transcript_id}::"
    for riu in raw_rius:
        if not riu.riu_id:
            raise RIUProcessingError(
                f"Raw RIU missing required riu_id in transcript {transcript.transcript_id}: {riu}"
            )
        if not riu.riu_id.startswith(expected_prefix):
            raise RIUProcessingError(
                f"Raw RIU ID '{riu.riu_id}' does not belong to transcript '{transcript.transcript_id}'"
            )
        if riu.riu_id not in provenance_map:
            raise RIUProcessingError(
                f"Missing provenance mapping for raw RIU '{riu.riu_id}' in transcript '{transcript.transcript_id}'"
            )
        prov = provenance_map[riu.riu_id]
        if prov.riu_id != riu.riu_id:
            raise RIUProcessingError(
                f"Provenance riu_id '{prov.riu_id}' does not match raw RIU ID '{riu.riu_id}'"
            )
        if not prov.response_id.startswith(expected_prefix):
            raise RIUProcessingError(
                f"Provenance response_id '{prov.response_id}' does not belong to transcript '{transcript.transcript_id}'"
            )

    if not raw_rius:
        return [], []

    expected_ids = {riu.riu_id for riu in raw_rius}
    position_map = {riu.riu_id: idx for idx, riu in enumerate(raw_rius)}

    raw_riu_map = {riu.riu_id: riu for riu in raw_rius}
    if batch_checkpoint is None:
        group_members: list[list[ExtractedRIU]] = []
        processed_riu_count = 0
    else:
        group_members = [
            [raw_riu_map[riu_id] for riu_id in member_ids]
            for member_ids in batch_checkpoint.group_member_riu_ids
        ]
        processed_riu_count = batch_checkpoint.processed_riu_count
        print(
            f"[deduplication][{transcript.transcript_id}] restored "
            f"{processed_riu_count}/{len(raw_rius)} RIUs",
            flush=True,
        )

    total_batches = (len(raw_rius) + batch_size - 1) // batch_size
    for batch_number, batch_start in enumerate(
        range(processed_riu_count, len(raw_rius), batch_size),
        start=processed_riu_count // batch_size + 1,
    ):
        batch = raw_rius[batch_start : batch_start + batch_size]
        existing_group_count = len(group_members)
        user_payload = {
            "transcript_id": transcript.transcript_id,
            "existing_groups": [
                {
                    "group_id": group_id,
                    "representative_statement": members[0].statement,
                    "member_item_indices": [
                        position_map[member.riu_id] + 1 for member in members
                    ],
                }
                for group_id, members in enumerate(group_members, start=1)
            ],
            "new_rius": [
                {
                    "item_index": batch_start + offset,
                    "turn_index": provenance_map[riu.riu_id].turn_index,
                    "statement": riu.statement,
                }
                for offset, riu in enumerate(batch, start=1)
            ],
        }

        raw_output = client.complete_json(prompt, user_payload)
        output = DeduplicationOutput.model_validate(raw_output)
        first_new_index = batch_start + 1
        last_new_index = batch_start + len(batch)
        nodes = [members.copy() for members in group_members]
        nodes.extend([riu] for riu in batch)
        previous_item_nodes = {
            position_map[member.riu_id] + 1: group_node
            for group_node, members in enumerate(group_members)
            for member in members
        }
        parents = list(range(len(nodes)))

        def find(node: int) -> int:
            while parents[node] != node:
                parents[node] = parents[parents[node]]
                node = parents[node]
            return node

        def union(left: int, right: int) -> None:
            left_root = find(left)
            right_root = find(right)
            if left_root != right_root:
                parents[right_root] = left_root

        for match in output.duplicate_matches:
            source_index = match.new_item_index
            if source_index < first_new_index or source_index > last_new_index:
                raise PartitionError(
                    f"Deduplication batch {batch_number}/{total_batches} returned unknown "
                    f"new item {source_index} in transcript {transcript.transcript_id}"
                )
            source_node = existing_group_count + source_index - first_new_index

            if match.target_type == "existing_group":
                if match.target_id < 1 or match.target_id > existing_group_count:
                    raise PartitionError(
                        f"Deduplication batch {batch_number}/{total_batches} returned unknown "
                        f"existing group {match.target_id} in transcript {transcript.transcript_id}"
                    )
                target_node = match.target_id - 1
            else:
                if (
                    match.target_id < 1
                    or match.target_id > last_new_index
                ):
                    raise PartitionError(
                        f"Deduplication batch {batch_number}/{total_batches} returned invalid "
                        f"new item {match.target_id} for item {source_index} in "
                        f"transcript {transcript.transcript_id}"
                    )
                if match.target_id < first_new_index:
                    target_node = previous_item_nodes[match.target_id]
                else:
                    target_node = existing_group_count + match.target_id - first_new_index
            union(source_node, target_node)

        merged_members: dict[int, list[ExtractedRIU]] = {}
        for node, members in enumerate(nodes):
            merged_members.setdefault(find(node), []).extend(members)
        group_members = list(merged_members.values())
        if checkpoint_callback is not None:
            checkpoint_callback(
                DeduplicationBatchUnit(
                    transcript_id=transcript.transcript_id,
                    case_id=transcript.case_id,
                    method_id=transcript.method_id,
                    processed_riu_count=min(batch_start + batch_size, len(raw_rius)),
                    group_member_riu_ids=[
                        [member.riu_id for member in members]
                        for members in group_members
                    ],
                )
            )
        print(
            f"[deduplication][{transcript.transcript_id}] batch "
            f"{batch_number}/{total_batches} completed "
            f"({min(batch_start + batch_size, len(raw_rius))}/{len(raw_rius)} RIUs)",
            flush=True,
        )

    groups: list[DeduplicationGroup] = []
    for members in group_members:
        representative = members[0]
        member_ids = [member.riu_id for member in members]
        groups.append(
            DeduplicationGroup(
                representative_riu_id=representative.riu_id,
                member_riu_ids=member_ids,
                statement=representative.statement,
            )
        )

    validate_partition(expected_ids, groups, expected_transcript_id=transcript.transcript_id)

    sorted_groups = sorted(
        groups,
        key=lambda grp: min(position_map[mid] for mid in grp.member_riu_ids),
    )

    unique_rius: list[UniqueRIU] = []
    for idx, group in enumerate(sorted_groups, start=1):
        first_pos = min(position_map[mid] for mid in group.member_riu_ids)
        unique_riu_id = f"{transcript.transcript_id}::R{idx:03d}"
        group_provenance = [provenance_map[mid] for mid in group.member_riu_ids]

        unique_rius.append(
            UniqueRIU(
                transcript_riu_id=unique_riu_id,
                transcript_id=transcript.transcript_id,
                case_id=transcript.case_id,
                method_id=transcript.method_id,
                statement=group.statement,
                member_riu_ids=group.member_riu_ids,
                first_position=first_pos,
                provenance=group_provenance,
            )
        )

    return sorted_groups, unique_rius


def deduplicate_all(
    config: RQ1Config,
    transcripts: list[TranscriptRecord],
    responses: list[ResponseRecord],
    extraction_units: list[ExtractionUnit],
    prompt: str,
    client: ChatCompletionClient,
) -> list[UniqueRIU]:
    """Perform within-transcript deduplication across all transcripts concurrently with checkpointing."""
    artifacts_dir = config.paths.artifacts_root / "riu"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_units_path = artifacts_dir / "deduplication_units.jsonl"
    batch_checkpoints_path = artifacts_dir / "deduplication_batches.jsonl"
    groups_path = artifacts_dir / "deduplication_groups.jsonl"
    unique_rius_path = artifacts_dir / "unique_rius.jsonl"
    summary_path = artifacts_dir / "summary.json"
    errors_path = artifacts_dir / "errors.jsonl"

    response_map = {r.response_id: r for r in responses}
    provenance_map: dict[str, RIUProvenance] = {}
    rius_by_transcript: dict[str, list[ExtractedRIU]] = {t.transcript_id: [] for t in transcripts}

    for unit in extraction_units:
        resp = response_map[unit.response_id]
        for riu in unit.rius:
            if not riu.riu_id:
                raise RIUProcessingError(
                    f"Encountered raw RIU without riu_id in response {unit.response_id}: {riu}"
                )
            provenance = RIUProvenance(
                riu_id=riu.riu_id,
                response_id=unit.response_id,
                turn_index=unit.turn_index,
                evidence_text=riu.evidence_text,
                evidence_start=riu.evidence_start,
                evidence_end=riu.evidence_end,
                context_question=resp.context_question,
            )
            provenance_map[riu.riu_id] = provenance
            rius_by_transcript[unit.transcript_id].append(riu)

    completed_units: dict[str, DeduplicationUnit] = {}
    expected_transcripts_map = {t.transcript_id: t for t in transcripts}

    if checkpoint_units_path.is_file():
        existing_rows = read_jsonl(checkpoint_units_path)
        seen_checkpoint_ids: set[str] = set()
        for row in existing_rows:
            unit = DeduplicationUnit.model_validate(row)
            if unit.transcript_id in seen_checkpoint_ids:
                raise CheckpointError(
                    f"Duplicate transcript checkpoint found for '{unit.transcript_id}' in {checkpoint_units_path}"
                )
            seen_checkpoint_ids.add(unit.transcript_id)

            if unit.transcript_id not in expected_transcripts_map:
                raise CheckpointError(
                    f"Unknown transcript checkpoint '{unit.transcript_id}' not in expected transcripts"
                )

            expected_t = expected_transcripts_map[unit.transcript_id]
            if unit.case_id != expected_t.case_id or unit.method_id != expected_t.method_id:
                raise CheckpointError(
                    f"Metadata mismatch in checkpoint for '{unit.transcript_id}': "
                    f"expected ({expected_t.case_id}, {expected_t.method_id}), "
                    f"got ({unit.case_id}, {unit.method_id})"
                )

            transcript_raw_rius = rius_by_transcript[unit.transcript_id]
            expected_raw_ids = {r.riu_id for r in transcript_raw_rius}
            validate_partition(expected_raw_ids, unit.groups, expected_transcript_id=unit.transcript_id)

            position_map = {riu.riu_id: idx for idx, riu in enumerate(transcript_raw_rius)}
            sorted_groups = sorted(
                unit.groups,
                key=lambda grp: min(position_map[mid] for mid in grp.member_riu_ids),
            )

            if len(unit.unique_rius) != len(sorted_groups):
                raise CheckpointError(
                    f"Unique RIU count ({len(unit.unique_rius)}) does not match group count ({len(sorted_groups)}) in checkpoint for '{unit.transcript_id}'"
                )

            all_unique_members: set[str] = set()
            for idx, (group, u) in enumerate(zip(sorted_groups, unit.unique_rius), start=1):
                expected_u_id = f"{unit.transcript_id}::R{idx:03d}"
                if u.transcript_riu_id != expected_u_id:
                    raise CheckpointError(
                        f"Unique RIU ID mismatch in checkpoint for '{unit.transcript_id}': expected '{expected_u_id}', got '{u.transcript_riu_id}'"
                    )

                if (
                    u.transcript_id != unit.transcript_id
                    or u.case_id != unit.case_id
                    or u.method_id != unit.method_id
                ):
                    raise CheckpointError(
                        f"Transcript metadata mismatch in unique RIU '{u.transcript_riu_id}': "
                        f"expected ({unit.case_id}, {unit.method_id}, {unit.transcript_id}), "
                        f"got ({u.case_id}, {u.method_id}, {u.transcript_id})"
                    )

                if u.statement != group.statement:
                    raise CheckpointError(
                        f"Statement mismatch between unique RIU '{u.transcript_riu_id}' and group: "
                        f"expected '{group.statement}', got '{u.statement}'"
                    )

                if u.member_riu_ids != group.member_riu_ids:
                    raise CheckpointError(
                        f"Member RIU IDs mismatch in unique RIU '{u.transcript_riu_id}': "
                        f"expected {group.member_riu_ids}, got {u.member_riu_ids}"
                    )

                expected_first_pos = min(position_map[mid] for mid in group.member_riu_ids)
                if u.first_position != expected_first_pos:
                    raise CheckpointError(
                        f"First position mismatch in unique RIU '{u.transcript_riu_id}': "
                        f"expected {expected_first_pos}, got {u.first_position}"
                    )

                expected_provenance = [provenance_map[mid] for mid in group.member_riu_ids]
                if len(u.provenance) != len(expected_provenance):
                    raise CheckpointError(
                        f"Provenance count mismatch in unique RIU '{u.transcript_riu_id}': "
                        f"expected {len(expected_provenance)}, got {len(u.provenance)}"
                    )

                for p_act, p_exp in zip(u.provenance, expected_provenance):
                    if p_act.model_dump() != p_exp.model_dump():
                        raise CheckpointError(
                            f"Provenance mismatch in unique RIU '{u.transcript_riu_id}' for member '{p_exp.riu_id}'"
                        )

                all_unique_members.update(u.member_riu_ids)

            if all_unique_members != expected_raw_ids:
                raise CheckpointError(
                    f"Unique RIU members union {all_unique_members} does not match expected raw RIU IDs {expected_raw_ids} in '{unit.transcript_id}'"
                )

            completed_units[unit.transcript_id] = unit

    batch_checkpoints: dict[str, DeduplicationBatchUnit] = {}
    if batch_checkpoints_path.is_file():
        previous_counts: dict[str, int] = {}
        for row in read_jsonl(batch_checkpoints_path):
            checkpoint = DeduplicationBatchUnit.model_validate(row)
            if checkpoint.transcript_id not in expected_transcripts_map:
                raise CheckpointError(
                    f"Unknown batch checkpoint transcript '{checkpoint.transcript_id}'"
                )
            expected_t = expected_transcripts_map[checkpoint.transcript_id]
            if (
                checkpoint.case_id != expected_t.case_id
                or checkpoint.method_id != expected_t.method_id
            ):
                raise CheckpointError(
                    f"Metadata mismatch in batch checkpoint for '{checkpoint.transcript_id}'"
                )

            transcript_rius = rius_by_transcript[checkpoint.transcript_id]
            count = checkpoint.processed_riu_count
            if count < 1 or count > len(transcript_rius):
                raise CheckpointError(
                    f"Invalid processed RIU count {count} in batch checkpoint for "
                    f"'{checkpoint.transcript_id}'"
                )
            if count < len(transcript_rius) and count % config.llm.deduplication_batch_size != 0:
                raise CheckpointError(
                    f"Processed RIU count {count} is not aligned with batch size in "
                    f"checkpoint for '{checkpoint.transcript_id}'"
                )
            if count <= previous_counts.get(checkpoint.transcript_id, 0):
                raise CheckpointError(
                    f"Batch checkpoints are not strictly increasing for "
                    f"'{checkpoint.transcript_id}'"
                )

            flattened_ids = [
                riu_id
                for member_ids in checkpoint.group_member_riu_ids
                for riu_id in member_ids
            ]
            if any(not member_ids for member_ids in checkpoint.group_member_riu_ids):
                raise CheckpointError(
                    f"Empty group in batch checkpoint for '{checkpoint.transcript_id}'"
                )
            if len(flattened_ids) != len(set(flattened_ids)):
                raise CheckpointError(
                    f"Duplicate RIU IDs in batch checkpoint for '{checkpoint.transcript_id}'"
                )
            expected_prefix_ids = {
                riu.riu_id for riu in transcript_rius[:count]
            }
            if set(flattened_ids) != expected_prefix_ids:
                raise CheckpointError(
                    f"Batch checkpoint does not partition the processed RIU prefix for "
                    f"'{checkpoint.transcript_id}'"
                )

            previous_counts[checkpoint.transcript_id] = count
            batch_checkpoints[checkpoint.transcript_id] = checkpoint

    pending_transcripts = [
        t for t in transcripts if t.transcript_id not in completed_units
    ]
    file_lock = threading.Lock()
    total_transcripts = len(transcripts)
    print(
        f"[deduplication] starting with {len(completed_units)}/{total_transcripts} transcripts restored",
        flush=True,
    )

    def deduplicate_and_checkpoint(transcript: TranscriptRecord) -> DeduplicationUnit:
        def save_batch_checkpoint(checkpoint: DeduplicationBatchUnit) -> None:
            with file_lock:
                append_jsonl(batch_checkpoints_path, checkpoint)

        groups, unique_list = deduplicate_transcript(
            transcript,
            rius_by_transcript[transcript.transcript_id],
            provenance_map,
            prompt,
            client,
            config.llm.deduplication_batch_size,
            batch_checkpoints.get(transcript.transcript_id),
            save_batch_checkpoint,
        )
        unit = DeduplicationUnit(
            transcript_id=transcript.transcript_id,
            case_id=transcript.case_id,
            method_id=transcript.method_id,
            groups=groups,
            unique_rius=unique_list,
        )
        with file_lock:
            append_jsonl(checkpoint_units_path, unit)
        return unit

    if pending_transcripts:
        with ThreadPoolExecutor(max_workers=config.llm.concurrency) as executor:
            future_to_transcript = {
                executor.submit(deduplicate_and_checkpoint, t): t
                for t in pending_transcripts
            }
            for future in as_completed(future_to_transcript):
                t = future_to_transcript[future]
                try:
                    unit = future.result()
                    completed_units[t.transcript_id] = unit
                    print(
                        f"[deduplication] {len(completed_units)}/{total_transcripts} completed",
                        flush=True,
                    )
                except Exception as err:
                    with file_lock:
                        append_jsonl(
                            errors_path,
                            {
                                "stage": "deduplication",
                                "transcript_id": t.transcript_id,
                                "error_type": type(err).__name__,
                                "error_message": str(err),
                            },
                        )
                    for pending_future in future_to_transcript:
                        pending_future.cancel()
                    raise

    all_unique_rius: list[UniqueRIU] = []
    all_groups: list[DeduplicationGroup] = []
    for t in transcripts:
        unit = completed_units[t.transcript_id]
        all_unique_rius.extend(unit.unique_rius)
        all_groups.extend(unit.groups)

    write_jsonl(unique_rius_path, all_unique_rius)
    write_jsonl(groups_path, all_groups)

    total_raw = sum(len(rius_by_transcript[t.transcript_id]) for t in transcripts)
    total_unique = len(all_unique_rius)
    dedup_ratio = (total_raw - total_unique) / total_raw if total_raw > 0 else 0.0

    summary: dict[str, Any] = {
        "total_transcripts": len(transcripts),
        "total_raw_rius": total_raw,
        "total_unique_rius": total_unique,
        "deduplication_reduction_ratio": dedup_ratio,
        "methods": {},
    }

    for method in config.methods:
        method_raw = sum(
            len(rius_by_transcript[t.transcript_id])
            for t in transcripts
            if t.method_id == method
        )
        method_unique = sum(
            len(completed_units[t.transcript_id].unique_rius)
            for t in transcripts
            if t.method_id == method
        )
        summary["methods"][method] = {
            "raw_rius": method_raw,
            "unique_rius": method_unique,
            "reduction_ratio": (
                (method_raw - method_unique) / method_raw if method_raw > 0 else 0.0
            ),
        }

    write_json(summary_path, summary)
    write_jsonl(batch_checkpoints_path, [])
    write_jsonl(errors_path, [])
    return all_unique_rius


def run_riu(
    config: RQ1Config,
    client: ChatCompletionClient | None = None,
) -> list[UniqueRIU]:
    """Execute end-to-end RIU extraction and deduplication pipeline."""
    artifacts_root = config.paths.artifacts_root
    transcripts_path = artifacts_root / "ingestion" / "transcripts.jsonl"
    responses_path = artifacts_root / "ingestion" / "responses.jsonl"

    if not transcripts_path.is_file():
        raise RIUProcessingError(f"Transcripts artifact not found: {transcripts_path}")
    if not responses_path.is_file():
        raise RIUProcessingError(f"Responses artifact not found: {responses_path}")

    transcripts = [
        TranscriptRecord.model_validate(row)
        for row in read_jsonl(transcripts_path)
    ]
    responses = [
        ResponseRecord.model_validate(row)
        for row in read_jsonl(responses_path)
    ]

    extract_prompt_path = Path(__file__).parent / "prompts" / "extract_riu.txt"
    dedup_prompt_path = Path(__file__).parent / "prompts" / "deduplicate_riu.txt"

    if not extract_prompt_path.is_file():
        raise RIUProcessingError(
            f"Extraction prompt file not found: {extract_prompt_path}"
        )
    if not dedup_prompt_path.is_file():
        raise RIUProcessingError(
            f"Deduplication prompt file not found: {dedup_prompt_path}"
        )

    extract_prompt = extract_prompt_path.read_text(encoding="utf-8")
    dedup_prompt = dedup_prompt_path.read_text(encoding="utf-8")

    def execute_with_client(active_client: ChatCompletionClient) -> list[UniqueRIU]:
        extraction_units = extract_all(
            config=config,
            responses=responses,
            prompt=extract_prompt,
            client=active_client,
        )
        return deduplicate_all(
            config=config,
            transcripts=transcripts,
            responses=responses,
            extraction_units=extraction_units,
            prompt=dedup_prompt,
            client=active_client,
        )

    if client is not None:
        return execute_with_client(client)
    with ChatCompletionClient(config.llm) as default_client:
        return execute_with_client(default_client)
