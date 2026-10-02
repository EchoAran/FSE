"""Interview conversation ingestion and question-answer pairing module."""

from __future__ import annotations

import statistics
from pathlib import Path
from typing import Any

from evolution.rq1.case_artifacts import discover_case_ids
from evolution.rq1.config import RQ1Config
from evolution.rq1.models import (
    ConversationTurn,
    ManifestRecord,
    ResponseRecord,
    TranscriptRecord,
)
from evolution.rq1.storage import read_json, read_jsonl, write_json, write_jsonl


class IngestionError(Exception):
    """Base exception for transcript ingestion errors."""


class ConversationStructureError(IngestionError):
    """Exception raised when conversation turns violate strict turn taking contracts."""


def load_manifest(path: Path) -> ManifestRecord:
    """Load and validate an interview execution manifest."""
    raw = read_json(path)
    return ManifestRecord.model_validate(raw)


def load_conversation(path: Path) -> list[ConversationTurn]:
    """Load and validate turns from a conversation JSON Lines file."""
    rows = read_jsonl(path)
    return [ConversationTurn.model_validate(row) for row in rows]


def pair_responses(
    transcript_id: str,
    case_id: str,
    method_id: str,
    turns: list[ConversationTurn],
) -> list[ResponseRecord]:
    """Pair each interviewer question with its subsequent interviewee answer."""
    if not turns:
        raise ConversationStructureError(f"Conversation has no turns: {transcript_id}")

    pending_question: ConversationTurn | None = None
    paired: list[ResponseRecord] = []

    for turn in turns:
        content = turn.content.strip()
        if not content:
            raise ConversationStructureError(
                f"Empty turn content encountered in {transcript_id}, turn {turn.turn_index}, role {turn.role}"
            )

        if turn.role == "interviewer":
            if pending_question is not None:
                raise ConversationStructureError(
                    f"Consecutive interviewer questions without interviewee response in {transcript_id}, turn {turn.turn_index}"
                )
            pending_question = turn

        elif turn.role == "interviewee":
            if pending_question is None:
                raise ConversationStructureError(
                    f"Interviewee response without preceding interviewer question in {transcript_id}, turn {turn.turn_index}"
                )
            response_id = f"{case_id}::{method_id}::A{turn.turn_index:03d}"
            paired.append(
                ResponseRecord(
                    response_id=response_id,
                    transcript_id=transcript_id,
                    case_id=case_id,
                    method_id=method_id,
                    turn_index=turn.turn_index,
                    context_question=pending_question.content,
                    answer=turn.content,
                )
            )
            pending_question = None
        else:
            raise ConversationStructureError(
                f"Unknown conversation role '{turn.role}' in {transcript_id}, turn {turn.turn_index}"
            )

    if pending_question is not None:
        raise ConversationStructureError(
            f"Conversation ended with an unanswered question in {transcript_id}, turn {pending_question.turn_index}"
        )

    return paired


def ingest_results(
    config: RQ1Config,
    case_ids: list[str] | None = None,
) -> tuple[list[TranscriptRecord], list[ResponseRecord]]:
    """Validate source conversations and export artifacts for selected Cases."""
    results_root = config.paths.results_root
    if not results_root.is_dir():
        raise IngestionError(f"Results directory does not exist: {results_root}")

    selected_cases = discover_case_ids(config) if case_ids is None else case_ids

    all_transcripts: list[TranscriptRecord] = []
    all_responses: list[ResponseRecord] = []
    responses_per_transcript: dict[str, list[int]] = {m: [] for m in config.methods}

    for case_id in selected_cases:
        for method_id in config.methods:
            case_dir = results_root / method_id / case_id
            manifest_path = case_dir / "manifest.json"
            conversation_path = case_dir / "conversation.jsonl"

            if not manifest_path.is_file():
                raise IngestionError(f"Missing manifest file: {manifest_path}")
            if not conversation_path.is_file():
                raise IngestionError(f"Missing conversation file: {conversation_path}")

            manifest = load_manifest(manifest_path)
            if manifest.case_id != case_id or manifest.method_id != method_id:
                raise IngestionError(
                    f"Manifest metadata mismatch in {case_dir}: "
                    f"expected ({case_id}, {method_id}), found ({manifest.case_id}, {manifest.method_id})"
                )

            turns = load_conversation(conversation_path)
            transcript_id = f"{case_id}::{method_id}"
            responses = pair_responses(transcript_id, case_id, method_id, turns)

            if len(responses) != manifest.completed_turns:
                raise IngestionError(
                    f"Response count ({len(responses)}) does not match manifest completed_turns "
                    f"({manifest.completed_turns}) in {transcript_id}"
                )

            transcript = TranscriptRecord(
                transcript_id=transcript_id,
                case_id=case_id,
                method_id=method_id,
                completed_turns=manifest.completed_turns,
            )
            all_transcripts.append(transcript)
            all_responses.extend(responses)
            responses_per_transcript[method_id].append(len(responses))

    ingestion_dir = config.paths.artifacts_root / "ingestion"
    write_jsonl(ingestion_dir / "transcripts.jsonl", all_transcripts)
    write_jsonl(ingestion_dir / "responses.jsonl", all_responses)

    summary: dict[str, Any] = {
        "total_cases": len(selected_cases),
        "total_transcripts": len(all_transcripts),
        "total_responses": len(all_responses),
        "methods": {},
    }

    for method_id in config.methods:
        counts = responses_per_transcript[method_id]
        summary["methods"][method_id] = {
            "transcript_count": len(counts),
            "response_count": sum(counts),
            "min_responses_per_transcript": min(counts) if counts else 0,
            "median_responses_per_transcript": float(statistics.median(counts)) if counts else 0.0,
            "max_responses_per_transcript": max(counts) if counts else 0,
        }

    write_json(ingestion_dir / "summary.json", summary)

    return all_transcripts, all_responses
