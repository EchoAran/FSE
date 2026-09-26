"""Canonical URL deduplication and payload selection."""

from __future__ import annotations

from motivation.models.dataset import ConversationRecord
from motivation.pipeline.expand import SharingCandidate
from motivation.pipeline.normalize import conversation_id


def _selection_key(candidate: SharingCandidate) -> tuple[int, int, int, int]:
    """Rank competing payloads of one shared URL."""
    return (
        1 if candidate.status == 200 else 0,
        1 if candidate.turns else 0,
        candidate.number_of_prompts or 0,
        -candidate.ordinal,
    )


def deduplicate(candidates: list[SharingCandidate]) -> list[ConversationRecord]:
    """Merge mentions per canonical URL and keep the most complete payload."""
    grouped: dict[str, list[SharingCandidate]] = {}
    for candidate in candidates:
        grouped.setdefault(candidate.canonical_url, []).append(candidate)

    conversations: list[ConversationRecord] = []
    for canonical_url in sorted(grouped):
        group = grouped[canonical_url]
        chosen = max(group, key=_selection_key)
        mentions = [
            candidate.mention for candidate in sorted(group, key=lambda item: item.ordinal)
        ]
        conversations.append(
            ConversationRecord(
                conversation_id=conversation_id(canonical_url),
                shared_url=canonical_url,
                status=chosen.status,
                date_of_conversation=chosen.date_of_conversation,
                conversation_at=chosen.conversation_at,
                model=chosen.model,
                number_of_prompts=chosen.number_of_prompts,
                mentions=mentions,
                turns=chosen.turns,
                payload_hash=chosen.payload_hash,
                payload_conflict=len({item.payload_hash for item in group}) > 1,
                confirmed_prior_artifact_count=sum(
                    mention.temporal_status == "confirmed_prior" for mention in mentions
                ),
                unclear_artifact_count=sum(
                    mention.temporal_status == "unclear" for mention in mentions
                ),
            )
        )
    return conversations