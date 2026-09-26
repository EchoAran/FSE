"""Prepare stage: DevGPT expansion, deduplication, screening and derived artifacts."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from motivation.config.config import MotivationConfig, display_path
from motivation.models.dataset import (
    ConversationRecord,
    ParseErrorRecord,
    ScreeningRecord,
)
from motivation.pipeline.dedup import deduplicate
from motivation.pipeline.expand import Expansion, expand_source
from motivation.pipeline.ingest import discover_source_file, load_records
from motivation.pipeline.screening import screen
from motivation.storage.jsonl import iter_jsonl, write_jsonl
from motivation.storage.manifest import build_manifest, write_manifest
from motivation.storage.tables import write_rows

CONVERSATIONS_FILE = "conversations.jsonl"
MENTIONS_FILE = "mentions.jsonl"
SCREENING_FILE = "screening.jsonl"
STRUCTURAL_CANDIDATES_FILE = "structural_candidates.jsonl"
PARSE_ERRORS_FILE = "parse_errors.jsonl"
SCREENING_TABLE = "screening_structural.csv"


@dataclass
class PrepareResult:
    """Artifacts and counts produced by one prepare run."""

    input_files: dict[str, str]
    counts: dict[str, int]
    table_path: Path
    manifest_path: Path


@dataclass
class DerivedCounts:
    """Counts recomputed from the derived conversation artifacts."""

    unique_conversations: int
    payload_conflicts: int
    structural_candidates: int
    exclusion_codes: dict[str, int]
    temporal_status: dict[str, int]
    confirmed_prior_edited_after_conversation: int


def _snapshot_dir(config: MotivationConfig) -> Path:
    snapshot_dir = config.dataset.root / config.dataset.snapshot
    if not snapshot_dir.is_dir():
        raise FileNotFoundError(f"snapshot directory not found: {snapshot_dir}")
    return snapshot_dir


def _load_sources(config: MotivationConfig) -> tuple[dict[str, str], list[Expansion]]:
    """Discover and expand every configured source file."""
    snapshot_dir = _snapshot_dir(config)
    input_files: dict[str, str] = {}
    expansions: list[Expansion] = []
    ordinal = 0
    for source in config.dataset.sources:
        source_file = discover_source_file(snapshot_dir, source)
        input_files[source] = display_path(source_file)
        expansion = expand_source(load_records(source_file), source, ordinal)
        ordinal += len(expansion.candidates)
        expansions.append(expansion)
    return input_files, expansions


def _count_rows(
    sources: list[str],
    expansions: list[Expansion],
    conversations: list[ConversationRecord],
    screening: list[ScreeningRecord],
    parse_errors: list[ParseErrorRecord],
) -> dict[str, int]:
    """Collect the screening flow counts of the prepare stage."""
    rows = {
        f"raw_{source}_records": expansion.record_count
        for source, expansion in zip(sources, expansions)
    }
    rows.update(
        {
            "chatgpt_sharings": sum(item.sharing_count for item in expansions),
            "invalid_shared_url": sum(
                item.code == "INVALID_SHARED_URL" for item in parse_errors
            ),
            "malformed_turn": sum(item.code == "MALFORMED_TURN" for item in parse_errors),
            "unique_conversations": len(conversations),
            "status_200": sum(item.status == 200 for item in conversations),
            "nonempty_conversations": sum(bool(item.turns) for item in conversations),
            "multiturn_structural_candidates": sum(
                item.structural_eligible for item in screening
            ),
            "payload_conflict_conversations": sum(
                item.payload_conflict for item in conversations
            ),
            "parse_error_records": len(parse_errors),
        }
    )
    return rows


def _write_derived(
    config: MotivationConfig,
    conversations: list[ConversationRecord],
    screening: list[ScreeningRecord],
    parse_errors: list[ParseErrorRecord],
) -> None:
    """Write the derived conversation artifacts of the prepare stage."""
    derived = config.derived_dir
    write_jsonl(derived / CONVERSATIONS_FILE, conversations)
    write_jsonl(
        derived / MENTIONS_FILE,
        (mention for record in conversations for mention in record.mentions),
    )
    write_jsonl(derived / SCREENING_FILE, screening)
    write_jsonl(
        derived / STRUCTURAL_CANDIDATES_FILE,
        (
            {"conversation_id": record.conversation_id}
            for record in screening
            if record.structural_eligible
        ),
    )
    write_jsonl(derived / PARSE_ERRORS_FILE, parse_errors)


def prepare(config: MotivationConfig) -> PrepareResult:
    """Run the prepare stage and return the produced paths and counts."""
    input_files, expansions = _load_sources(config)
    candidates = [item for expansion in expansions for item in expansion.candidates]
    parse_errors = [item for expansion in expansions for item in expansion.parse_errors]
    conversations = deduplicate(candidates)
    screening = [screen(record) for record in conversations]

    _write_derived(config, conversations, screening, parse_errors)
    counts = _count_rows(
        config.dataset.sources, expansions, conversations, screening, parse_errors
    )
    table_path = write_rows(
        config.results_dir / "tables" / SCREENING_TABLE,
        ("stage", "count"),
        [{"stage": stage, "count": count} for stage, count in counts.items()],
    )
    manifest_path = write_manifest(
        config.results_dir, build_manifest(config, input_files)
    )
    return PrepareResult(
        input_files=input_files,
        counts=counts,
        table_path=table_path,
        manifest_path=manifest_path,
    )


def _timestamp(value: str) -> datetime:
    """Parse a serialized ISO 8601 timestamp from a derived record."""
    return datetime.fromisoformat(value)


def read_derived_counts(config: MotivationConfig) -> DerivedCounts:
    """Recount deduplication, screening and temporal visibility from derived files."""
    derived = config.derived_dir
    conversations_path = derived / CONVERSATIONS_FILE
    if not conversations_path.is_file():
        raise FileNotFoundError("derived artifacts not found, run prepare first")

    conversation_count = 0
    conflict_count = 0
    for record in iter_jsonl(conversations_path):
        conversation_count += 1
        conflict_count += int(record["payload_conflict"])

    exclusion_counts: Counter[str] = Counter()
    candidate_count = 0
    for record in iter_jsonl(derived / SCREENING_FILE):
        exclusion_counts.update(record["exclusion_codes"])
        candidate_count += int(record["structural_eligible"])

    temporal_counts: Counter[str] = Counter()
    edited_prior_count = 0
    for record in iter_jsonl(derived / MENTIONS_FILE):
        temporal_counts[record["temporal_status"]] += 1
        updated_at = record["updated_at"]
        if (
            record["temporal_status"] == "confirmed_prior"
            and updated_at is not None
            and _timestamp(updated_at) > _timestamp(record["conversation_at"])
        ):
            edited_prior_count += 1

    return DerivedCounts(
        unique_conversations=conversation_count,
        payload_conflicts=conflict_count,
        structural_candidates=candidate_count,
        exclusion_codes=dict(sorted(exclusion_counts.items())),
        temporal_status={
            status: temporal_counts[status]
            for status in ("confirmed_prior", "unclear", "not_available")
        },
        confirmed_prior_edited_after_conversation=edited_prior_count,
    )