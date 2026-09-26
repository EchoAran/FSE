"""Structural screening of conversations before semantic analysis."""

from __future__ import annotations

from motivation.models.dataset import ConversationRecord, ScreeningRecord


def screen(record: ConversationRecord) -> ScreeningRecord:
    """Decide deterministically whether a conversation enters the Analyzer queue."""
    developer_prompt_count = sum(1 for turn in record.turns if turn.role == "developer")
    exclusion_codes: list[str] = []
    if record.status != 200:
        exclusion_codes.append("STATUS_NOT_200")
    if not record.turns:
        exclusion_codes.append("EMPTY_CONVERSATION")
    if developer_prompt_count < 2:
        exclusion_codes.append("LESS_THAN_TWO_DEVELOPER_PROMPTS")
    if any(not turn.content.strip() for turn in record.turns):
        exclusion_codes.append("MALFORMED_TURN")
    return ScreeningRecord(
        conversation_id=record.conversation_id,
        status_ok=record.status == 200,
        has_conversations=bool(record.turns),
        developer_prompt_count=developer_prompt_count,
        structural_eligible=not exclusion_codes,
        exclusion_codes=exclusion_codes,
    )