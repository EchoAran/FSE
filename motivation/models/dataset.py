"""Data models for DevGPT raw records and normalized conversations."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class CodeBlock(BaseModel):
    """A code block attached to an assistant answer."""

    replace_string: str | None = None
    type: str | None = None
    content: str


class TurnRecord(BaseModel):
    """A single expanded conversation turn."""

    turn_id: str
    pair_index: int
    role: Literal["developer", "assistant"]
    content: str
    code_blocks: list[CodeBlock] = []


class MentionRecord(BaseModel):
    """A conversation reference in an Issue/PR together with its prior context."""

    conversation_id: str
    artifact_id: str
    source_type: Literal["issue", "pr"]
    source_url: str
    repo_name: str | None = None
    number: int | None = None
    title: str | None = None
    body: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    mentioned_text: str | None = None
    mentioned_property: str | None = None
    conversation_at: datetime | None = None
    temporal_status: Literal["confirmed_prior", "unclear", "not_available"]


class ConversationRecord(BaseModel):
    """A deduplicated conversation shared by one or more artifacts."""

    conversation_id: str
    shared_url: str
    status: int | None
    date_of_conversation: str | None
    conversation_at: datetime | None
    model: str | None
    number_of_prompts: int | None
    mentions: list[MentionRecord]
    turns: list[TurnRecord]
    payload_hash: str
    payload_conflict: bool
    confirmed_prior_artifact_count: int
    unclear_artifact_count: int


class ScreeningRecord(BaseModel):
    """Structural screening outcome of a single conversation."""

    conversation_id: str
    status_ok: bool
    has_conversations: bool
    developer_prompt_count: int
    structural_eligible: bool
    exclusion_codes: list[str]


class ParseErrorRecord(BaseModel):
    """A sharing that cannot enter the normal conversation flow."""

    code: Literal["INVALID_SHARED_URL", "MALFORMED_TURN"]
    source_type: Literal["issue", "pr"]
    artifact_id: str
    source_url: str
    shared_url: str
    conversation_id: str | None = None
    detail: str