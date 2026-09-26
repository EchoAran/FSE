"""Summarize stage: deterministic aggregation of the validated analysis into paper tables.

Every table reads the stored analysis artifacts and the derived conversations, so a rerun over
an unchanged input reproduces the same files. Two denominators are defined once and reused:
the analyzed conversations and the core LSRI units. A conversation counts as analyzed when the
LLM judged it implementation oriented, found a solution anchor, and the conversation carries a
developer turn after that anchor.
"""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from motivation.config.config import MotivationConfig
from motivation.models.analysis import (
    ElicitationOpportunity,
    IntroductionMode,
    LsriUnit,
    RequirementType,
    ResolvedConversationAnalysis,
    ResolvedLaterInformationUnit,
    ResponseUptake,
)
from motivation.models.dataset import ConversationRecord
from motivation.pipeline.analyze import (
    ANALYSIS_DIR,
    CONVERSATION_ANALYSIS_FILE,
    LSRI_FILE,
)
from motivation.pipeline.prepare import (
    CONVERSATIONS_FILE,
    SCREENING_TABLE,
    STRUCTURAL_CANDIDATES_FILE,
)
from motivation.storage.jsonl import iter_jsonl, write_json
from motivation.storage.tables import write_rows

TABLES_DIR = "tables"
CASES_DIR = "cases"
SCREENING_FLOW_FILE = "screening_flow.csv"
SCREENING_FLOW_JSON_FILE = "screening_flow.json"
CONVERSATION_SUMMARY_FILE = "conversation_summary.csv"
PRIOR_CONTEXT_FILE = "prior_context_visibility.csv"
CANDIDATE_CASES_FILE = "candidate_cases.csv"
SUMMARY_FILE = "summary.json"

DEVELOPER = "developer"
CONFIRMED_PRIOR_PRESENT = "confirmed_prior_present"
UNCLEAR_ONLY = "unclear_only"
NO_ARTIFACT_CONTEXT = "no_artifact_context"

DIMENSIONS: tuple[tuple[str, type], ...] = (
    ("requirement_type", RequirementType),
    ("introduction_mode", IntroductionMode),
    ("eeo", ElicitationOpportunity),
    ("response_uptake", ResponseUptake),
)
CROSS_DIMENSIONS: tuple[tuple[str, str], ...] = (
    ("requirement_type", "eeo"),
    ("introduction_mode", "eeo"),
    ("eeo", "response_uptake"),
)
PRIOR_CATEGORIES = (CONFIRMED_PRIOR_PRESENT, UNCLEAR_ONLY, NO_ARTIFACT_CONTEXT)

FLOW_FIELDS = ("stage", "count")
CATEGORY_FIELDS = ("category", "count", "percentage")
SUMMARY_FIELDS = (
    "conversation_id",
    "source_types",
    "repo_name_count",
    "developer_prompt_count",
    "solution_anchor_turn",
    "artifact_context_confirmed_count",
    "artifact_context_unclear_count",
    "later_unit_count",
    "lsri_count",
    "eeo_yes_count",
    "eeo_uncertain_count",
    "eeo_no_count",
    "revised_count",
    "extended_count",
    "no_uptake_count",
    "insufficient_evidence_count",
)
CASE_FIELDS = (
    "conversation_id",
    "shared_url",
    "source_types",
    "solution_anchor_turn",
    "lsri_count",
    "eeo_yes_count",
    "uptake_positive_count",
    "turn_count",
    "evidence_complete",
)


@dataclass
class SummarizeResult:
    """Counts and paths produced by one summarize run."""

    analyzed_conversations: int
    lsri_units: int
    lsri_conversations: int
    candidate_cases: int
    flow_path: Path
    summary_path: Path
    tables_dir: Path
    cases_dir: Path


def _percentage(count: int, denominator: int) -> float:
    """Report one share of a denominator, rounded to two decimals."""
    return round(count * 100 / denominator, 2) if denominator else 0.0


def _label_count(units: list[LsriUnit], field: str, value: Any) -> int:
    """Count the LSRI units that carry one semantic label."""
    return sum(getattr(unit, field) == value for unit in units)


@dataclass(frozen=True)
class ConversationAggregate:
    """One analyzed conversation with the record and the LSRI units every table reads."""

    analysis: ResolvedConversationAnalysis
    record: ConversationRecord
    units: list[ResolvedLaterInformationUnit]
    lsri: list[LsriUnit]

    def source_types(self) -> str:
        """Render the artifact types that share this conversation."""
        return ";".join(sorted({mention.source_type for mention in self.record.mentions}))

    def summary_row(self) -> dict[str, Any]:
        """Build the conversation level row of the summary table."""
        return {
            "conversation_id": self.analysis.conversation_id,
            "source_types": self.source_types(),
            "repo_name_count": len(
                {mention.repo_name for mention in self.record.mentions if mention.repo_name}
            ),
            "developer_prompt_count": sum(
                turn.role == DEVELOPER for turn in self.record.turns
            ),
            "solution_anchor_turn": self.analysis.solution_anchor_turn,
            "artifact_context_confirmed_count": self.record.confirmed_prior_artifact_count,
            "artifact_context_unclear_count": self.record.unclear_artifact_count,
            "later_unit_count": len(self.units),
            "lsri_count": len(self.lsri),
            "eeo_yes_count": _label_count(self.lsri, "eeo", ElicitationOpportunity.YES),
            "eeo_uncertain_count": _label_count(
                self.lsri, "eeo", ElicitationOpportunity.UNCERTAIN
            ),
            "eeo_no_count": _label_count(self.lsri, "eeo", ElicitationOpportunity.NO),
            "revised_count": _label_count(self.lsri, "response_uptake", ResponseUptake.REVISED),
            "extended_count": _label_count(self.lsri, "response_uptake", ResponseUptake.EXTENDED),
            "no_uptake_count": _label_count(
                self.lsri, "response_uptake", ResponseUptake.NO_UPTAKE
            ),
            "insufficient_evidence_count": _label_count(
                self.lsri, "response_uptake", ResponseUptake.INSUFFICIENT
            ),
        }

    def prior_visibility(self) -> str:
        """Classify how visible the artifact prior context of this conversation is."""
        if self.record.confirmed_prior_artifact_count:
            return CONFIRMED_PRIOR_PRESENT
        if self.record.unclear_artifact_count:
            return UNCLEAR_ONLY
        return NO_ARTIFACT_CONTEXT

    def evidence_complete(self) -> bool:
        """Report whether the displayed anchor and LSRI evidence are all locatable spans."""
        return bool(self.analysis.solution_anchor_evidence) and all(
            unit.evidence_span for unit in self.lsri
        )

    def candidate_row(self) -> dict[str, Any]:
        """Build the shortlist row of one conversation."""
        return {
            "conversation_id": self.analysis.conversation_id,
            "shared_url": self.record.shared_url,
            "source_types": self.source_types(),
            "solution_anchor_turn": self.analysis.solution_anchor_turn,
            "lsri_count": len(self.lsri),
            "eeo_yes_count": _label_count(self.lsri, "eeo", ElicitationOpportunity.YES),
            "uptake_positive_count": _label_count(
                self.lsri, "response_uptake", ResponseUptake.REVISED
            )
            + _label_count(self.lsri, "response_uptake", ResponseUptake.EXTENDED),
            "turn_count": len(self.record.turns),
            "evidence_complete": self.evidence_complete(),
        }


def _read_analyses(config: MotivationConfig) -> list[ResolvedConversationAnalysis]:
    """Read the validated conversation analyses in stored order."""
    path = config.results_dir / ANALYSIS_DIR / CONVERSATION_ANALYSIS_FILE
    if not path.is_file():
        raise FileNotFoundError("conversation analysis not found, run analyze first")
    return [ResolvedConversationAnalysis(**payload) for payload in iter_jsonl(path)]


def _read_lsri_units(config: MotivationConfig) -> dict[str, list[LsriUnit]]:
    """Read the core LSRI units grouped by conversation."""
    path = config.results_dir / ANALYSIS_DIR / LSRI_FILE
    if not path.is_file():
        raise FileNotFoundError("lsri units not found, run analyze first")
    grouped: dict[str, list[LsriUnit]] = {}
    for payload in iter_jsonl(path):
        unit = LsriUnit(**payload)
        grouped.setdefault(unit.conversation_id, []).append(unit)
    return grouped


def _read_conversations(config: MotivationConfig) -> dict[str, ConversationRecord]:
    """Read the derived conversations by conversation id."""
    path = config.derived_dir / CONVERSATIONS_FILE
    if not path.is_file():
        raise FileNotFoundError("derived artifacts not found, run prepare first")
    return {
        payload["conversation_id"]: ConversationRecord(**payload)
        for payload in iter_jsonl(path)
    }


def _candidate_ids(config: MotivationConfig) -> list[str]:
    """Read the structural candidate conversation ids in derived order."""
    path = config.derived_dir / STRUCTURAL_CANDIDATES_FILE
    if not path.is_file():
        raise FileNotFoundError("structural candidates not found, run prepare first")
    return [record["conversation_id"] for record in iter_jsonl(path)]


def _screening_counts(config: MotivationConfig) -> dict[str, int]:
    """Read the screening counts a prepare run wrote."""
    path = config.results_dir / TABLES_DIR / SCREENING_TABLE
    if not path.is_file():
        raise FileNotFoundError("screening table not found, run prepare first")
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["stage"]: int(row["count"]) for row in csv.DictReader(handle)}


def _is_analyzed(analysis: ResolvedConversationAnalysis, record: ConversationRecord) -> bool:
    """Report whether one conversation reached the region after its solution anchor."""
    if not analysis.implementation_oriented or analysis.solution_anchor_turn is None:
        return False
    order = [turn.turn_id for turn in record.turns]
    if analysis.solution_anchor_turn not in order:
        return False
    roles = {turn.turn_id: turn.role for turn in record.turns}
    after = order[order.index(analysis.solution_anchor_turn) + 1 :]
    return any(roles[turn_id] == DEVELOPER for turn_id in after)


def _aggregates(
    analyses: list[ResolvedConversationAnalysis],
    conversations: dict[str, ConversationRecord],
    lsri_units: dict[str, list[LsriUnit]],
) -> list[ConversationAggregate]:
    """Build the conversation level aggregates of the analyzed set, in stored order."""
    return [
        ConversationAggregate(
            analysis=analysis,
            record=conversations[analysis.conversation_id],
            units=analysis.later_information_units,
            lsri=lsri_units.get(analysis.conversation_id, []),
        )
        for analysis in analyses
        if _is_analyzed(analysis, conversations[analysis.conversation_id])
    ]


def _screening_flow(
    config: MotivationConfig,
    candidate_ids: list[str],
    analyses: list[ResolvedConversationAnalysis],
    aggregates: list[ConversationAggregate],
) -> dict[str, int]:
    """Merge the structural screening counts with the counts the analysis adds."""
    flow = _screening_counts(config)
    flow["implementation_conversations"] = sum(
        analysis.implementation_oriented for analysis in analyses
    )
    flow["anchored_conversations"] = sum(
        analysis.implementation_oriented and analysis.solution_anchor_turn is not None
        for analysis in analyses
    )
    flow["analyzed_conversations"] = len(aggregates)
    flow["lsri_conversations"] = sum(bool(item.lsri) for item in aggregates)
    flow["analysis_failed"] = len(candidate_ids) - len(analyses)
    return flow


def _values(field: str) -> list[str]:
    """Return the labels of one semantic dimension in their declared order."""
    return [value.value for value in dict(DIMENSIONS)[field]]


def _distribution(units: list[LsriUnit], field: str) -> dict[str, int]:
    """Count the LSRI units of every label of one semantic dimension."""
    counts = Counter(getattr(unit, field).value for unit in units)
    return {label: counts[label] for label in _values(field)}


def _cross_table(
    units: list[LsriUnit], first_field: str, second_field: str
) -> tuple[list[str], list[dict[str, Any]], dict[str, dict[str, int]]]:
    """Count the units of every combination of two semantic dimensions."""
    counts = Counter(
        (getattr(unit, first_field).value, getattr(unit, second_field).value)
        for unit in units
    )
    rows_labels = _values(first_field)
    columns_labels = _values(second_field)
    fields = [first_field, *(f"{second_field}={label}" for label in columns_labels)]
    rows = [
        {
            first_field: row,
            **{
                f"{second_field}={column}": counts[(row, column)]
                for column in columns_labels
            },
        }
        for row in rows_labels
    ]
    document = {
        row: {column: counts[(row, column)] for column in columns_labels}
        for row in rows_labels
    }
    return fields, rows, document


def _prior_visibility(aggregates: list[ConversationAggregate]) -> dict[str, int]:
    """Classify the analyzed conversations by the visibility of their artifact context."""
    counts = Counter(item.prior_visibility() for item in aggregates)
    return {category: counts[category] for category in PRIOR_CATEGORIES}


def _candidate_cases(aggregates: list[ConversationAggregate]) -> list[dict[str, Any]]:
    """Shortlist the conversations that carry a complete, visible LSRI story."""
    cases = [item.candidate_row() for item in aggregates]
    shortlist = [
        case
        for case in cases
        if case["lsri_count"]
        and case["eeo_yes_count"]
        and case["uptake_positive_count"]
        and case["evidence_complete"]
    ]
    shortlist.sort(key=lambda case: (case["turn_count"], case["conversation_id"]))
    return shortlist


def _conversation_level(aggregates: list[ConversationAggregate]) -> dict[str, Any]:
    """Report the conversation level figures the paper states."""
    analyzed = len(aggregates)
    lsri_conversations = sum(bool(item.lsri) for item in aggregates)
    eeo_yes_conversations = sum(
        bool(_label_count(item.lsri, "eeo", ElicitationOpportunity.YES))
        for item in aggregates
    )
    return {
        "analyzed_conversations": analyzed,
        "lsri_conversations": lsri_conversations,
        "lsri_conversation_ratio": _percentage(lsri_conversations, analyzed),
        "eeo_yes_conversations": eeo_yes_conversations,
        "eeo_yes_conversation_ratio": _percentage(eeo_yes_conversations, analyzed),
    }


def summarize(config: MotivationConfig) -> SummarizeResult:
    """Aggregate the validated analysis into the tables and the summary document."""
    candidate_ids = _candidate_ids(config)
    analyses = _read_analyses(config)
    conversations = _read_conversations(config)
    aggregates = _aggregates(analyses, conversations, _read_lsri_units(config))
    units = [unit for item in aggregates for unit in item.lsri]
    tables_dir = config.results_dir / TABLES_DIR
    cases_dir = config.results_dir / CASES_DIR

    flow = _screening_flow(config, candidate_ids, analyses, aggregates)
    flow_path = write_rows(
        tables_dir / SCREENING_FLOW_FILE,
        FLOW_FIELDS,
        [{"stage": stage, "count": count} for stage, count in flow.items()],
    )
    write_json(tables_dir / SCREENING_FLOW_JSON_FILE, flow)

    write_rows(
        tables_dir / CONVERSATION_SUMMARY_FILE,
        SUMMARY_FIELDS,
        (item.summary_row() for item in aggregates),
    )

    visibility = _prior_visibility(aggregates)
    write_rows(
        tables_dir / PRIOR_CONTEXT_FILE,
        CATEGORY_FIELDS,
        [
            {
                "category": category,
                "count": count,
                "percentage": _percentage(count, len(aggregates)),
            }
            for category, count in visibility.items()
        ],
    )

    distributions = {name: _distribution(units, name) for name, _ in DIMENSIONS}
    for name, counts in distributions.items():
        write_rows(
            tables_dir / f"{name}.csv",
            CATEGORY_FIELDS,
            [
                {
                    "category": category,
                    "count": count,
                    "percentage": _percentage(count, len(units)),
                }
                for category, count in counts.items()
            ],
        )

    cross_tables = {
        f"{first}_x_{second}": _cross_table(units, first, second)
        for first, second in CROSS_DIMENSIONS
    }
    for name, (fields, rows, _) in cross_tables.items():
        write_rows(tables_dir / f"{name}.csv", fields, rows)

    cases = _candidate_cases(aggregates)
    write_rows(cases_dir / CANDIDATE_CASES_FILE, CASE_FIELDS, cases)

    summary_path = write_json(
        config.results_dir / SUMMARY_FILE,
        {
            "screening": flow,
            "conversation_level": _conversation_level(aggregates),
            "prior_context_visibility": visibility,
            "lsri_total": len(units),
            **distributions,
            "cross_tables": {
                name: document for name, (_, _, document) in cross_tables.items()
            },
            "representative_case_id": None,
        },
    )
    return SummarizeResult(
        analyzed_conversations=len(aggregates),
        lsri_units=len(units),
        lsri_conversations=sum(bool(item.lsri) for item in aggregates),
        candidate_cases=len(cases),
        flow_path=flow_path,
        summary_path=summary_path,
        tables_dir=tables_dir,
        cases_dir=cases_dir,
    )