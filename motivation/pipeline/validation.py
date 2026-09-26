"""Turn text, phrase location, window resolution, prior aggregation and LSRI derivation."""

from __future__ import annotations

import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass

from motivation.models.analysis import (
    AnalysisErrorCode,
    LsriUnit,
    PriorArtifactEvidence,
    PriorInformation,
    ResolvedConversationAnalysis,
    ResolvedLaterInformationUnit,
    UnitDraft,
)
from motivation.models.dataset import ConversationRecord, TurnRecord

ASSISTANT = "assistant"
DEVELOPER = "developer"
ABSENT = "Absent"
PRESENT = "Present"
UNCLEAR = "Unclear"
ARTIFACT_CONFIRMED_PRIOR = "confirmed_prior"
SEMANTIC_FIELDS = ("requirement_type", "introduction_mode", "eeo", "eeo_reason", "response_uptake")


@dataclass(frozen=True)
class IndexedText:
    """Text prepared for phrase matching, with a map back to the original characters."""

    original: str
    normalized: str
    offsets: list[int]

    @classmethod
    def build(cls, original: str) -> IndexedText:
        """Normalize one text through NFKC forms and collapsed whitespace."""
        chars: list[str] = []
        offsets: list[int] = []
        for index, char in enumerate(original):
            piece = unicodedata.normalize("NFKC", char)
            if not piece:
                continue
            if piece.isspace():
                if chars and chars[-1] != " ":
                    chars.append(" ")
                    offsets.append(index)
                continue
            for normalized_char in piece:
                chars.append(normalized_char)
                offsets.append(index)
        while chars and chars[-1] == " ":
            chars.pop()
            offsets.pop()
        return cls(original, "".join(chars), offsets)

    def occurrences(self, phrase: str) -> list[str]:
        """Return every occurrence of a phrase as the original text that carries it."""
        needle = IndexedText.build(phrase).normalized
        if not needle:
            return []
        found: list[str] = []
        start = self.normalized.find(needle)
        while start != -1:
            last = start + len(needle) - 1
            found.append(self.original[self.offsets[start] : self.offsets[last] + 1])
            start = self.normalized.find(needle, start + 1)
        return found


@dataclass(frozen=True)
class SpanSource:
    """One text that a phrase may be located in."""

    key: str
    text: IndexedText


@dataclass(frozen=True)
class LocatedSpan:
    """A phrase located in one source, written back as the original text."""

    key: str
    text: str


@dataclass(frozen=True)
class AnchorLocation:
    """The solution anchor the model named, with the span it copied when that span is locatable.

    ``span_rejection`` explains a span that could not be located in the named turn. The anchor
    itself still stands, so the rejection is a recorded degradation rather than a retry.
    """

    turn_id: str
    span: str | None
    span_rejection: str | None = None


def locate_in_turn(
    turn_id: str, phrase: str, sources: Sequence[SpanSource]
) -> LocatedSpan | None:
    """Return the phrase inside the named source, or None when it cannot be located.

    The named source is the only candidate, so a phrase that also occurs in other sources is no
    longer ambiguous. Inside the named source the phrase must still occur exactly once, which
    keeps every accepted span unambiguous.
    """
    for source in sources:
        if source.key == turn_id:
            occurrences = source.text.occurrences(phrase)
            return LocatedSpan(source.key, occurrences[0]) if len(occurrences) == 1 else None
    return None


def location_rejection(
    turn_id: str, phrase: str, sources: Sequence[SpanSource], subject: str
) -> str:
    """Explain why a phrase could not be located in the turn the model named."""
    named = next((source for source in sources if source.key == turn_id), None)
    if named is None:
        return f"{subject} {phrase!r} names {turn_id}, which may not carry it"
    occurrences = named.text.occurrences(phrase)
    if occurrences:
        return (
            f"{subject} {phrase!r} appears {len(occurrences)} times in {turn_id}: "
            "extend it with the adjacent words of the same sentence until it appears once"
        )
    elsewhere = [source.key for source in sources if source.text.occurrences(phrase)]
    hint = f"; it does appear in {', '.join(elsewhere)}" if elsewhere else ""
    return (
        f"{subject} {phrase!r} does not appear in {turn_id}: "
        f"copy a fragment of {turn_id} character for character{hint}"
    )


def turn_body(turn: TurnRecord) -> str:
    """Render the body of one turn as both the model input and the phrase search see it."""
    parts = [turn.content]
    for position, block in enumerate(turn.code_blocks, start=1):
        label = block.replace_string or f"[CODE_BLOCK_{position - 1}]"
        language = f" ({block.type})" if block.type else ""
        parts.append(f"code block {label}{language}:\n{block.content}")
    return "\n\n".join(parts)


class ConversationIndex:
    """Turn lookup, phrase location and artifact context text of one conversation record."""

    def __init__(self, record: ConversationRecord) -> None:
        self.order = [turn.turn_id for turn in record.turns]
        self.roles = {turn.turn_id: turn.role for turn in record.turns}
        self.position = {turn.turn_id: index for index, turn in enumerate(record.turns)}
        self._turn_text = {
            turn.turn_id: IndexedText.build(turn_body(turn)) for turn in record.turns
        }
        self.artifact_status: dict[str, set[str]] = {}
        artifact_parts: dict[str, list[str]] = {}
        for mention in record.mentions:
            self.artifact_status.setdefault(mention.artifact_id, set()).add(
                mention.temporal_status
            )
            parts = [part for part in (mention.title, mention.body) if part]
            if parts:
                artifact_parts.setdefault(mention.artifact_id, []).extend(parts)
        self._artifact_text = {
            artifact_id: IndexedText.build(" ".join(parts))
            for artifact_id, parts in artifact_parts.items()
        }

    def turns(
        self,
        role: str | None = None,
        after: int | None = None,
        before: int | None = None,
    ) -> list[str]:
        """Return the turn ids of one role, restricted to a position window when asked."""
        return [
            turn_id
            for turn_id in self.order
            if (role is None or self.roles[turn_id] == role)
            and (after is None or self.position[turn_id] > after)
            and (before is None or self.position[turn_id] < before)
        ]

    def span_sources(self, turn_ids: Sequence[str]) -> list[SpanSource]:
        """Return the turn texts a phrase may be located in."""
        return [SpanSource(turn_id, self._turn_text[turn_id]) for turn_id in turn_ids]

    def artifact_ids(self) -> list[str]:
        """Return the injected artifact contexts that carry text."""
        return list(self._artifact_text)

    def artifact_source(self, artifact_id: str) -> SpanSource:
        """Return the text of one injected artifact context."""
        return SpanSource(artifact_id, self._artifact_text[artifact_id])


@dataclass(frozen=True)
class Defect:
    """One rejected element of a step answer."""

    code: AnalysisErrorCode
    message: str


@dataclass(frozen=True)
class UnitDefect(Defect):
    """One unit of a window that could not be delivered."""

    position: int
    source_turn_id: str | None = None


@dataclass(frozen=True)
class LocatedUnit:
    """One extracted unit whose phrases were located in the window turns."""

    draft: UnitDraft
    evidence_span: str
    source_turn_id: str
    supporting_turn_ids: list[str]


@dataclass(frozen=True)
class WindowResolution:
    """Units located in one window and the units that window could not deliver."""

    units: list[LocatedUnit]
    defects: list[UnitDefect]


def _missing_semantic_fields(draft: UnitDraft) -> list[str]:
    """Return the semantic fields a requirement relevant unit has to carry."""
    if not draft.requirement_relevant:
        return []
    return [name for name in SEMANTIC_FIELDS if getattr(draft, name) is None]


def resolve_window(
    drafts: Sequence[UnitDraft],
    index: ConversationIndex,
    window_turn_ids: Sequence[str],
    context_turn_ids: Sequence[str],
) -> WindowResolution:
    """Locate the phrases of one window and report the units it cannot deliver."""
    unit_turn_ids = [turn_id for turn_id in window_turn_ids if index.roles[turn_id] == DEVELOPER]
    uptake_turn_ids = [
        turn_id
        for turn_id in [*window_turn_ids, *context_turn_ids]
        if index.roles[turn_id] == ASSISTANT
    ]
    unit_sources = index.span_sources(unit_turn_ids)
    units: list[LocatedUnit] = []
    defects: list[UnitDefect] = []
    for position, draft in enumerate(drafts, start=1):
        source = locate_in_turn(draft.unit.turn_id, draft.unit.phrase, unit_sources)
        if source is None:
            defects.append(
                UnitDefect(
                    AnalysisErrorCode.EVIDENCE_SPAN_MISMATCH,
                    location_rejection(
                        draft.unit.turn_id,
                        draft.unit.phrase,
                        unit_sources,
                        f"unit {position} phrase",
                    ),
                    position,
                    draft.unit.turn_id,
                )
            )
            continue
        missing = _missing_semantic_fields(draft)
        if missing:
            defects.append(
                UnitDefect(
                    AnalysisErrorCode.MISSING_LSRI_FIELDS,
                    f"unit {position} misses {', '.join(missing)}",
                    position,
                    source.key,
                )
            )
            continue
        supporting_turn_ids: list[str] = []
        if draft.uptake is not None:
            after = index.position[source.key]
            candidates = [
                turn_id for turn_id in uptake_turn_ids if index.position[turn_id] > after
            ]
            uptake_sources = index.span_sources(candidates)
            uptake = locate_in_turn(
                draft.uptake.turn_id, draft.uptake.phrase, uptake_sources
            )
            if uptake is None:
                defects.append(
                    UnitDefect(
                        AnalysisErrorCode.EVIDENCE_SPAN_MISMATCH,
                        location_rejection(
                            draft.uptake.turn_id,
                            draft.uptake.phrase,
                            uptake_sources,
                            f"unit {position} uptake phrase",
                        ),
                        position,
                        source.key,
                    )
                )
                continue
            supporting_turn_ids = [uptake.key]
        units.append(LocatedUnit(draft, source.text, source.key, supporting_turn_ids))
    return WindowResolution(units, defects)


@dataclass(frozen=True)
class SourceMatch:
    """One unit whose meaning a prior source already expresses."""

    unit_number: int
    evidence_span: str
    turn_id: str | None = None


@dataclass(frozen=True)
class SourceResolution:
    """Outcome of consulting one prior source."""

    key: str
    confirmed: bool
    matches: list[SourceMatch]
    defects: list[Defect]

    @property
    def complete(self) -> bool:
        """Report whether the source was consulted without a rejected match."""
        return not self.defects


@dataclass(frozen=True)
class PriorVerdict:
    """Aggregated prior information of one unit."""

    prior_information: PriorInformation
    evidence_spans: list[str]
    evidence_turn_ids: list[str]
    artifact_evidence: list[PriorArtifactEvidence]


def _verdict(label: PriorInformation, hits: Sequence[tuple[SourceResolution, SourceMatch]]) -> PriorVerdict:
    """Collect the evidence of the hits that carry one prior information label."""
    turn_hits = [match for _, match in hits if match.turn_id is not None]
    artifact_hits = [(resolution.key, match) for resolution, match in hits if match.turn_id is None]
    return PriorVerdict(
        prior_information=label,
        evidence_spans=[match.evidence_span for match in turn_hits],
        evidence_turn_ids=[match.turn_id for match in turn_hits if match.turn_id],
        artifact_evidence=[
            PriorArtifactEvidence(artifact_id=key, evidence_span=match.evidence_span)
            for key, match in artifact_hits
        ],
    )


def summarize_prior(
    unit_count: int, resolutions: Sequence[SourceResolution]
) -> list[PriorVerdict]:
    """Aggregate the matches of every source into the prior information of every unit."""
    verdicts: list[PriorVerdict] = []
    incomplete = any(not resolution.complete for resolution in resolutions)
    for number in range(1, unit_count + 1):
        hits = [
            (resolution, match)
            for resolution in resolutions
            for match in resolution.matches
            if match.unit_number == number
        ]
        confirmed_hits = [hit for hit in hits if hit[0].confirmed]
        if confirmed_hits:
            verdicts.append(_verdict(PRESENT, confirmed_hits))
            continue
        if hits or incomplete:
            verdicts.append(_verdict(UNCLEAR, hits))
            continue
        verdicts.append(_verdict(ABSENT, []))
    return verdicts


def resolve_unit_record(
    located: LocatedUnit, unit_id: str, verdict: PriorVerdict
) -> ResolvedLaterInformationUnit:
    """Combine one located unit with its aggregated prior verdict into a record."""
    draft = located.draft
    return ResolvedLaterInformationUnit(
        unit_id=unit_id,
        source_turn_id=located.source_turn_id,
        supporting_turn_ids=located.supporting_turn_ids,
        prior_evidence_turn_ids=verdict.evidence_turn_ids,
        statement=draft.statement,
        evidence_span=located.evidence_span,
        requirement_relevant=draft.requirement_relevant,
        prior_information=verdict.prior_information,
        prior_evidence_spans=verdict.evidence_spans,
        prior_artifact_evidence=verdict.artifact_evidence,
        requirement_type=draft.requirement_type,
        introduction_mode=draft.introduction_mode,
        eeo=draft.eeo,
        eeo_reason=draft.eeo_reason,
        response_uptake=draft.response_uptake,
    )


def derive_lsri(analysis: ResolvedConversationAnalysis) -> list[LsriUnit]:
    """Derive the core LSRI units of a resolved analysis."""
    return [
        LsriUnit(conversation_id=analysis.conversation_id, **unit.model_dump())
        for unit in analysis.later_information_units
        if unit.is_lsri()
    ]