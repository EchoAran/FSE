"""Artifact prior context temporal classification."""

from __future__ import annotations

from datetime import datetime


def artifact_temporal_status(
    created_at: datetime | None,
    conversation_at: datetime | None,
    has_content: bool,
) -> str:
    """Classify how far an artifact context can support a prior information judgement.

    An artifact counts as confirmed prior once its creation predates the conversation
    and the conversation date is known. DevGPT captures no artifact edit history, so
    the update timestamp is recorded on the mention but never disqualifies a context.
    """
    if not has_content:
        return "not_available"
    if conversation_at is None or created_at is None:
        return "unclear"
    return "confirmed_prior" if created_at <= conversation_at else "unclear"