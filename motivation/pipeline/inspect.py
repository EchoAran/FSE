"""Inspect stage: read-only provenance report of one analyzed conversation."""

from __future__ import annotations

from collections.abc import Sequence
from enum import Enum

from motivation.config.config import MotivationConfig
from motivation.models.analysis import (
    AnalysisIssue,
    ResolvedConversationAnalysis,
    ResolvedLaterInformationUnit,
)
from motivation.models.dataset import ConversationRecord
from motivation.pipeline.analyze import (
    ANALYSIS_DIR,
    CONVERSATION_ANALYSIS_FILE,
    ERRORS_FILE,
)
from motivation.pipeline.prepare import CONVERSATIONS_FILE
from motivation.pipeline.validation import (
    ConversationIndex,
    SpanSource,
    locate_in_turn,
    turn_body,
)
from motivation.storage.jsonl import iter_jsonl


def _label(value: object) -> str:
    """Render an optional enum member or plain value as report text."""
    if value is None:
        return "-"
    return value.value if isinstance(value, Enum) else str(value)


def _flag(value: bool) -> str:
    """Render a boolean as yes or no."""
    return "yes" if value else "no"


def _join(values: Sequence[str]) -> str:
    """Render a list of turn ids as one comma separated field."""
    return ", ".join(values) if values else "-"


def _located(sources: Sequence[SpanSource], key: str, span: str) -> str:
    """Report whether a stored span still occurs once in the source it names."""
    return "located" if locate_in_turn(key, span, sources) is not None else "not located"


def _conversation(config: MotivationConfig, conversation_id: str) -> ConversationRecord:
    """Read one derived conversation record, or reject an id the prepare stage never wrote."""
    path = config.derived_dir / CONVERSATIONS_FILE
    if not path.is_file():
        raise FileNotFoundError("derived artifacts not found, run prepare first")
    for payload in iter_jsonl(path):
        if payload["conversation_id"] == conversation_id:
            return ConversationRecord(**payload)
    raise ValueError(f"not a derived conversation: {conversation_id}")


def _analysis(
    config: MotivationConfig, conversation_id: str
) -> ResolvedConversationAnalysis | None:
    """Read the analysis record of one conversation, absent until the analyze stage wrote it."""
    path = config.results_dir / ANALYSIS_DIR / CONVERSATION_ANALYSIS_FILE
    if not path.is_file():
        return None
    for payload in iter_jsonl(path):
        if payload["conversation_id"] == conversation_id:
            return ResolvedConversationAnalysis(**payload)
    return None


def _issues(config: MotivationConfig, conversation_id: str) -> list[AnalysisIssue]:
    """Read the ledger records the analyze stage wrote for one conversation."""
    path = config.results_dir / ANALYSIS_DIR / ERRORS_FILE
    if not path.is_file():
        return []
    return [
        AnalysisIssue(**payload)
        for payload in iter_jsonl(path)
        if payload["conversation_id"] == conversation_id
    ]


def _context_lines(record: ConversationRecord) -> list[str]:
    """Describe the artifact contexts injected into the analysis of one conversation."""
    lines: list[str] = []
    for mention in record.mentions:
        lines.append(
            f"artifact {mention.artifact_id}: {mention.source_type} "
            f"{_label(mention.repo_name)}#{_label(mention.number)}"
        )
        lines.append(f"  temporal status: {mention.temporal_status}")
        lines.append(f"  mentioned property: {_label(mention.mentioned_property)}")
        lines.append(f"  title: {_label(mention.title)}")
        lines.append(f"  body: {_label(mention.body)}")
    return lines


def _turn_lines(record: ConversationRecord) -> list[str]:
    """Index every turn of the conversation with its role and rendered body size."""
    return [
        f"turn {turn.turn_id} {turn.role} chars={len(turn_body(turn))}"
        for turn in record.turns
    ]


def _anchor_lines(
    analysis: ResolvedConversationAnalysis, index: ConversationIndex
) -> list[str]:
    """Describe the solution anchor and locate the evidence span it names."""
    turn_id = analysis.solution_anchor_turn
    if turn_id is None:
        return ["solution anchor: -"]
    span = analysis.solution_anchor_evidence
    if span is None:
        return [f"solution anchor: {turn_id}", "  evidence: -"]
    status = _located(index.span_sources([turn_id]), turn_id, span)
    return [f"solution anchor: {turn_id}", f"  evidence: {span} ({status} in {turn_id})"]


def _unit_lines(unit: ResolvedLaterInformationUnit, index: ConversationIndex) -> list[str]:
    """Describe one later information unit with its prior evidence and derived labels."""
    evidence_status = _located(
        index.span_sources([unit.source_turn_id]), unit.source_turn_id, unit.evidence_span
    )
    lines = [
        f"unit {unit.unit_id}",
        f"  source turn: {unit.source_turn_id}",
        f"  statement: {unit.statement}",
        f"  evidence span: {unit.evidence_span} ({evidence_status} in {unit.source_turn_id})",
        f"  requirement relevant: {_flag(unit.requirement_relevant)}",
        f"  prior information: {unit.prior_information}",
    ]
    for turn_id, span in zip(unit.prior_evidence_turn_ids, unit.prior_evidence_spans):
        status = _located(index.span_sources([turn_id]), turn_id, span)
        lines.append(f"  prior evidence: {span} ({status} in {turn_id})")
    for item in unit.prior_artifact_evidence:
        sources = [index.artifact_source(item.artifact_id)]
        status = _located(sources, item.artifact_id, item.evidence_span)
        lines.append(
            f"  prior artifact evidence: {item.evidence_span} "
            f"({status} in {item.artifact_id})"
        )
    lines += [
        f"  requirement type: {_label(unit.requirement_type)}",
        f"  introduction mode: {_label(unit.introduction_mode)}",
        f"  eeo: {_label(unit.eeo)}",
        f"  eeo reason: {_label(unit.eeo_reason)}",
        f"  response uptake: {_label(unit.response_uptake)}",
        f"  supporting turns: {_join(unit.supporting_turn_ids)}",
        f"  core lsri: {_flag(unit.is_lsri())}",
    ]
    return lines


def _analysis_lines(
    analysis: ResolvedConversationAnalysis | None, index: ConversationIndex
) -> list[str]:
    """Describe the analysis record of one conversation, or report that it is pending."""
    if analysis is None:
        return ["analysis: pending"]
    lines = [
        f"implementation oriented: {_flag(analysis.implementation_oriented)}",
        f"implementation reason: {analysis.implementation_reason}",
    ]
    lines += _anchor_lines(analysis, index)
    for unit in analysis.later_information_units:
        lines += _unit_lines(unit, index)
    return lines


def _issue_lines(issues: Sequence[AnalysisIssue]) -> list[str]:
    """Describe the ledger records of one conversation."""
    return [
        f"ledger {issue.stage.value} {issue.scope} {issue.error_code.value} "
        f"retries={issue.retry_count}: {issue.message}"
        for issue in issues
    ]


def _validation_status(
    analysis: ResolvedConversationAnalysis | None, issues: Sequence[AnalysisIssue]
) -> str:
    """Summarize the analysis record and its ledger into the state of one conversation."""
    if analysis is None:
        return "failed" if issues else "pending"
    return "degraded" if issues else "analyzed"


def conversation_report(config: MotivationConfig, conversation_id: str) -> list[str]:
    """Report the full provenance trace of one conversation without writing anything."""
    record = _conversation(config, conversation_id)
    index = ConversationIndex(record)
    analysis = _analysis(config, conversation_id)
    issues = _issues(config, conversation_id)
    lines = [
        f"conversation: {record.conversation_id}",
        f"shared url: {record.shared_url}",
        f"status: {_label(record.status)}",
        f"model: {_label(record.model)}",
    ]
    lines += _context_lines(record)
    lines += _turn_lines(record)
    lines += _analysis_lines(analysis, index)
    lines += _issue_lines(issues)
    lines.append(f"validation: {_validation_status(analysis, issues)}")
    return lines