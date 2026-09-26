"""Expansion of DevGPT artifacts and shared conversations into candidate records."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from motivation.models.dataset import (
    CodeBlock,
    MentionRecord,
    ParseErrorRecord,
    TurnRecord,
)
from motivation.pipeline.normalize import canonicalize_shared_url, conversation_id
from motivation.pipeline.temporal import artifact_temporal_status

MISSING_TOKEN = "none"


def _optional_text(value: Any) -> str | None:
    """Normalize a text field, mapping empty values and the "None" token to None."""
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() == MISSING_TOKEN:
        return None
    return text


def _optional_int(value: Any) -> int | None:
    """Normalize numeric fields that DevGPT stores as strings."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    try:
        return int(str(value).strip())
    except ValueError:
        return None


def _parse_conversation_date(value: Any) -> datetime | None:
    """Parse the day-only conversation date into midnight UTC."""
    text = _optional_text(value)
    if text is None:
        return None
    return datetime.strptime(text, "%B %d, %Y").replace(tzinfo=timezone.utc)


def _parse_timestamp(value: Any) -> datetime | None:
    """Parse a GitHub ISO 8601 timestamp."""
    text = _optional_text(value)
    if text is None:
        return None
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def _artifact_id(source_type: str, source_url: str) -> str:
    """Derive a machine independent artifact identifier."""
    return hashlib.sha256(f"{source_type}:{source_url}".encode()).hexdigest()[:16]


def _code_blocks(raw: Any) -> list[CodeBlock]:
    """Convert the DevGPT ListOfCode field into assistant code blocks."""
    if not isinstance(raw, list):
        return []
    return [
        CodeBlock(
            replace_string=_optional_text(item.get("ReplaceString")),
            type=_optional_text(item.get("Type")),
            content=item.get("Content") or "",
        )
        for item in raw
        if isinstance(item, dict)
    ]


def _build_turns(pairs: Any) -> tuple[list[TurnRecord], list[str]]:
    """Expand prompt/answer pairs into ordered turns keyed by pair index and role."""
    if not isinstance(pairs, list):
        return [], []
    turns: list[TurnRecord] = []
    problems: list[str] = []
    for pair_index, pair in enumerate(pairs, start=1):
        prompt = pair.get("Prompt") if isinstance(pair, dict) else None
        answer = pair.get("Answer") if isinstance(pair, dict) else None
        if not isinstance(prompt, str) or not prompt.strip():
            problems.append(f"pair {pair_index} developer prompt missing")
            prompt = ""
        if not isinstance(answer, str) or not answer.strip():
            problems.append(f"pair {pair_index} assistant answer missing")
            answer = ""
        turns.append(
            TurnRecord(
                turn_id=f"D{pair_index:04d}",
                pair_index=pair_index,
                role="developer",
                content=prompt,
            )
        )
        turns.append(
            TurnRecord(
                turn_id=f"A{pair_index:04d}",
                pair_index=pair_index,
                role="assistant",
                content=answer,
                code_blocks=_code_blocks(pair.get("ListOfCode")),
            )
        )
    return turns, problems


def _payload_signature(pairs: Any) -> str:
    """Hash the prompt/answer content of a shared conversation payload."""
    payload = (
        [{"Prompt": pair.get("Prompt"), "Answer": pair.get("Answer")} for pair in pairs]
        if isinstance(pairs, list)
        else []
    )
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()


@dataclass
class SharingCandidate:
    """One expanded ChatgptSharing with its conversation payload and artifact provenance."""

    ordinal: int
    canonical_url: str
    status: int | None
    date_of_conversation: str | None
    conversation_at: datetime | None
    model: str | None
    number_of_prompts: int | None
    turns: list[TurnRecord]
    payload_hash: str
    mention: MentionRecord


@dataclass
class Expansion:
    """Expansion result of a single DevGPT source file."""

    candidates: list[SharingCandidate]
    parse_errors: list[ParseErrorRecord]
    record_count: int
    sharing_count: int


def expand_source(
    records: list[dict[str, Any]], source_type: str, start_ordinal: int = 0
) -> Expansion:
    """Expand every record and ChatgptSharing of one source file."""
    candidates: list[SharingCandidate] = []
    parse_errors: list[ParseErrorRecord] = []
    sharing_count = 0
    ordinal = start_ordinal
    for record in records:
        source_url = str(record.get("URL") or "")
        source_id = _artifact_id(source_type, source_url)
        title = _optional_text(record.get("Title"))
        body = _optional_text(record.get("Body"))
        created_at = _parse_timestamp(record.get("CreatedAt"))
        updated_at = _parse_timestamp(record.get("UpdatedAt"))
        for sharing in record.get("ChatgptSharing") or []:
            sharing_count += 1
            shared_url = str(sharing.get("URL") or "")
            try:
                canonical_url = canonicalize_shared_url(shared_url)
            except ValueError as error:
                parse_errors.append(
                    ParseErrorRecord(
                        code="INVALID_SHARED_URL",
                        source_type=source_type,
                        artifact_id=source_id,
                        source_url=source_url,
                        shared_url=shared_url,
                        detail=str(error),
                    )
                )
                continue

            ordinal += 1
            shared_conversation_id = conversation_id(canonical_url)
            turns, problems = _build_turns(sharing.get("Conversations"))
            for problem in problems:
                parse_errors.append(
                    ParseErrorRecord(
                        code="MALFORMED_TURN",
                        source_type=source_type,
                        artifact_id=source_id,
                        source_url=source_url,
                        shared_url=shared_url,
                        conversation_id=shared_conversation_id,
                        detail=problem,
                    )
                )

            conversation_at = _parse_conversation_date(sharing.get("DateOfConversation"))
            raw_mention = sharing.get("Mention") or {}
            mention = MentionRecord(
                conversation_id=shared_conversation_id,
                artifact_id=source_id,
                source_type=source_type,
                source_url=source_url,
                repo_name=_optional_text(record.get("RepoName")),
                number=_optional_int(record.get("Number")),
                title=title,
                body=body,
                created_at=created_at,
                updated_at=updated_at,
                mentioned_text=_optional_text(raw_mention.get("MentionedText")),
                mentioned_property=_optional_text(raw_mention.get("MentionedProperty")),
                conversation_at=conversation_at,
                temporal_status=artifact_temporal_status(
                    created_at, conversation_at, bool(title or body)
                ),
            )
            candidates.append(
                SharingCandidate(
                    ordinal=ordinal,
                    canonical_url=canonical_url,
                    status=_optional_int(sharing.get("Status")),
                    date_of_conversation=_optional_text(sharing.get("DateOfConversation")),
                    conversation_at=conversation_at,
                    model=_optional_text(sharing.get("Model")),
                    number_of_prompts=_optional_int(sharing.get("NumberOfPrompts")),
                    turns=turns,
                    payload_hash=_payload_signature(sharing.get("Conversations")),
                    mention=mention,
                )
            )
    return Expansion(
        candidates=candidates,
        parse_errors=parse_errors,
        record_count=len(records),
        sharing_count=sharing_count,
    )