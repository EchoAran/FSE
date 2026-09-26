"""Step orchestration: run the four analysis steps of one conversation and assemble its record."""

from __future__ import annotations

from dataclasses import dataclass

from motivation.models.analysis import (
    AnalysisErrorCode,
    AnalysisIssue,
    AnalysisStage,
    AnchorAnswer,
    PriorSourceAnswer,
    ResolvedConversationAnalysis,
    ResolvedLaterInformationUnit,
    ScreenAnswer,
    UnitsAnswer,
)
from motivation.models.dataset import ConversationRecord
from motivation.pipeline.analyzer import (
    Inspect,
    Inspection,
    StepFailure,
    StepOutcome,
    StepRunner,
)
from motivation.pipeline.prompt import (
    PriorSource,
    PromptSet,
    UnitWindow,
    anchor_user_prompt,
    prior_sources,
    prior_user_prompt,
    screen_user_prompt,
    unit_windows,
    units_user_prompt,
)
from motivation.pipeline.validation import (
    ASSISTANT,
    AnchorLocation,
    ConversationIndex,
    Defect,
    LocatedUnit,
    PriorVerdict,
    SourceMatch,
    SourceResolution,
    UnitDefect,
    WindowResolution,
    locate_in_turn,
    location_rejection,
    resolve_unit_record,
    resolve_window,
    summarize_prior,
)

CONVERSATION_SCOPE = "conversation"


@dataclass(frozen=True)
class PipelineOutcome:
    """The resolved record of one conversation and the parts of it that were degraded."""

    conversation_id: str
    analysis: ResolvedConversationAnalysis | None
    issues: list[AnalysisIssue]


class ConversationPipeline:
    """Runs the four analysis steps of one conversation and assembles its resolved record."""

    def __init__(self, runner: StepRunner, prompts: PromptSet) -> None:
        self._runner = runner
        self._prompts = prompts

    def analyze(self, record: ConversationRecord) -> PipelineOutcome:
        """Analyze one conversation and report the parts its steps could not deliver."""
        index = ConversationIndex(record)
        screen = self._runner.run(
            self._prompts.screen, screen_user_prompt(record), ScreenAnswer
        )
        if screen.failure is not None:
            issue = self._failure_issue(
                record, AnalysisStage.SCREEN, CONVERSATION_SCOPE, screen.failure
            )
            return PipelineOutcome(record.conversation_id, None, [issue])
        if not screen.answer.implementation_oriented:
            return PipelineOutcome(
                record.conversation_id, self._record(record, screen.answer, None, []), []
            )
        issues: list[AnalysisIssue] = []
        anchor = self._anchor(record, index)
        if anchor.failure is not None or anchor.retry_reasons:
            issues.append(self._anchor_issue(record, anchor))
            return PipelineOutcome(record.conversation_id, None, issues)
        anchored = anchor.report
        if anchored is None:
            return PipelineOutcome(
                record.conversation_id, self._record(record, screen.answer, None, []), []
            )
        if anchored.span_rejection is not None:
            issues.append(
                self._anchor_span_issue(record, anchored.span_rejection, anchor.retry_count)
            )
        units = self._units(record, index, anchored.turn_id, issues)
        verdicts = self._prior(record, index, anchored.turn_id, units, issues)
        resolved = [
            resolve_unit_record(unit, f"U{number}", verdict)
            for number, (unit, verdict) in enumerate(zip(units, verdicts), start=1)
        ]
        return PipelineOutcome(
            record.conversation_id,
            self._record(record, screen.answer, anchored, resolved),
            issues,
        )

    @staticmethod
    def _record(
        record: ConversationRecord,
        screen: ScreenAnswer,
        anchor: AnchorLocation | None,
        units: list[ResolvedLaterInformationUnit],
    ) -> ResolvedConversationAnalysis:
        """Assemble the resolved record of one conversation."""
        return ResolvedConversationAnalysis(
            conversation_id=record.conversation_id,
            implementation_oriented=screen.implementation_oriented,
            implementation_reason=screen.implementation_reason,
            solution_anchor_turn=anchor.turn_id if anchor is not None else None,
            solution_anchor_evidence=anchor.span if anchor is not None else None,
            later_information_units=units,
        )

    def _anchor(
        self, record: ConversationRecord, index: ConversationIndex
    ) -> StepOutcome[AnchorAnswer, AnchorLocation | None]:
        """Locate the assistant turn that first carries a concrete solution.

        The turn id is what the anchor asserts, so the conversation continues with that turn
        even when the copied phrase cannot be located: the span is a record field, not the
        anchor itself. A miss is carried out as a degradation, not as a retry reason.
        """
        sources = index.span_sources(index.turns(role=ASSISTANT))

        def inspect(answer: AnchorAnswer) -> Inspection[AnchorLocation | None]:
            reference = answer.solution_anchor
            if reference is None:
                return Inspection([], None)
            if not any(source.key == reference.turn_id for source in sources):
                return Inspection(
                    [
                        location_rejection(
                            reference.turn_id, reference.phrase, sources, "the anchor phrase"
                        )
                    ],
                    None,
                )
            located = locate_in_turn(reference.turn_id, reference.phrase, sources)
            if located is None:
                return Inspection(
                    [],
                    AnchorLocation(
                        reference.turn_id,
                        None,
                        location_rejection(
                            reference.turn_id, reference.phrase, sources, "the anchor phrase"
                        ),
                    ),
                )
            return Inspection([], AnchorLocation(reference.turn_id, located.text))

        return self._runner.run(
            self._prompts.anchor, anchor_user_prompt(record, index), AnchorAnswer, inspect
        )

    def _units(
        self,
        record: ConversationRecord,
        index: ConversationIndex,
        anchor_turn_id: str,
        issues: list[AnalysisIssue],
    ) -> list[LocatedUnit]:
        """Extract the information units of every window after the anchor."""
        located: list[LocatedUnit] = []
        for window in unit_windows(index, index.position[anchor_turn_id]):
            outcome = self._runner.run(
                self._prompts.units,
                units_user_prompt(record, index, window, anchor_turn_id),
                UnitsAnswer,
                self._window_inspector(index, window),
            )
            if outcome.failure is not None:
                scope = f"window {window.scope()}"
                issues.append(self._failure_issue(record, AnalysisStage.UNITS, scope, outcome.failure))
                continue
            resolution: WindowResolution = outcome.report
            issues.extend(
                self._unit_issues(record, window, resolution.defects, outcome.retry_count)
            )
            located.extend(resolution.units)
        located.sort(key=lambda unit: index.position[unit.source_turn_id])
        return located

    def _window_inspector(
        self, index: ConversationIndex, window: UnitWindow
    ) -> Inspect[UnitsAnswer, WindowResolution]:
        """Return the validation pass of the units step for one window."""

        def inspect(answer: UnitsAnswer) -> Inspection[WindowResolution]:
            resolution = resolve_window(
                answer.units, index, window.turn_ids, window.context_turn_ids
            )
            return Inspection([defect.message for defect in resolution.defects], resolution)

        return inspect

    def _prior(
        self,
        record: ConversationRecord,
        index: ConversationIndex,
        anchor_turn_id: str,
        units: list[LocatedUnit],
        issues: list[AnalysisIssue],
    ) -> list[PriorVerdict]:
        """Judge every prior source of the conversation against its units."""
        if not units:
            return []
        resolutions: list[SourceResolution] = []
        for source in prior_sources(record, index, index.position[anchor_turn_id]):
            outcome = self._runner.run(
                self._prompts.prior,
                prior_user_prompt(record, source, units),
                PriorSourceAnswer,
                self._source_inspector(index, source, len(units)),
            )
            scope = f"source {source.key}"
            if outcome.failure is not None:
                resolutions.append(self._failed_source(source, outcome.failure))
                issues.append(self._failure_issue(record, AnalysisStage.PRIOR, scope, outcome.failure))
                continue
            resolutions.append(outcome.report)
            if outcome.report.defects:
                issues.append(
                    self._source_issue(record, scope, outcome.report, outcome.retry_count)
                )
        return summarize_prior(len(units), resolutions)

    def _source_inspector(
        self, index: ConversationIndex, source: PriorSource, unit_count: int
    ) -> Inspect[PriorSourceAnswer, SourceResolution]:
        """Return the validation pass of the prior step for one source."""
        span_sources = (
            [index.artifact_source(source.key)]
            if source.mention is not None
            else index.span_sources(source.turn_ids)
        )

        def inspect(answer: PriorSourceAnswer) -> Inspection[SourceResolution]:
            matches: list[SourceMatch] = []
            defects: list[Defect] = []
            for match in answer.matches:
                if not 1 <= match.unit_index <= unit_count:
                    defects.append(
                        Defect(
                            AnalysisErrorCode.EVIDENCE_SPAN_MISMATCH,
                            f"unit index {match.unit_index} is outside the unit list",
                        )
                    )
                    continue
                located = locate_in_turn(match.prior.turn_id, match.prior.phrase, span_sources)
                if located is None:
                    defects.append(
                        Defect(
                            AnalysisErrorCode.EVIDENCE_SPAN_MISMATCH,
                            location_rejection(
                                match.prior.turn_id,
                                match.prior.phrase,
                                span_sources,
                                f"the phrase of unit {match.unit_index}",
                            ),
                        )
                    )
                    continue
                turn_id = None if source.mention is not None else located.key
                matches.append(SourceMatch(match.unit_index, located.text, turn_id))
            resolution = SourceResolution(
                key=source.key,
                confirmed=source.confirmed,
                matches=matches,
                defects=defects,
            )
            return Inspection([defect.message for defect in defects], resolution)

        return inspect

    @staticmethod
    def _anchor_span_issue(
        record: ConversationRecord, message: str, retry_count: int
    ) -> AnalysisIssue:
        """Record an anchor turn that could not give back the phrase the model copied from it."""
        return AnalysisIssue(
            conversation_id=record.conversation_id,
            stage=AnalysisStage.ANCHOR,
            scope=CONVERSATION_SCOPE,
            error_code=AnalysisErrorCode.EVIDENCE_SPAN_MISMATCH,
            message=message,
            retry_count=retry_count,
        )

    def _anchor_issue(
        self, record: ConversationRecord, outcome: StepOutcome
    ) -> AnalysisIssue:
        """Record an anchor step that could not settle on a solution turn."""
        if outcome.failure is not None:
            return self._failure_issue(
                record, AnalysisStage.ANCHOR, CONVERSATION_SCOPE, outcome.failure
            )
        return AnalysisIssue(
            conversation_id=record.conversation_id,
            stage=AnalysisStage.ANCHOR,
            scope=CONVERSATION_SCOPE,
            error_code=AnalysisErrorCode.EVIDENCE_SPAN_MISMATCH,
            message="; ".join(outcome.retry_reasons),
            retry_count=outcome.retry_count,
        )

    def _unit_issues(
        self,
        record: ConversationRecord,
        window: UnitWindow,
        defects: list[UnitDefect],
        retry_count: int,
    ) -> list[AnalysisIssue]:
        """Record the units one window could not deliver."""
        return [
            AnalysisIssue(
                conversation_id=record.conversation_id,
                stage=AnalysisStage.UNITS,
                scope=f"unit {defect.source_turn_id or window.scope()}#{defect.position}",
                error_code=defect.code,
                message=defect.message,
                retry_count=retry_count,
            )
            for defect in defects
        ]

    def _source_issue(
        self, record: ConversationRecord, scope: str, resolution: SourceResolution, retry_count: int
    ) -> AnalysisIssue:
        """Record a prior source that could not be consulted completely."""
        return AnalysisIssue(
            conversation_id=record.conversation_id,
            stage=AnalysisStage.PRIOR,
            scope=scope,
            error_code=resolution.defects[0].code,
            message="; ".join(defect.message for defect in resolution.defects),
            retry_count=retry_count,
        )

    @staticmethod
    def _failed_source(source: PriorSource, failure: StepFailure) -> SourceResolution:
        """Report one prior source whose call returned no usable answer."""
        return SourceResolution(
            key=source.key,
            confirmed=source.confirmed,
            matches=[],
            defects=[Defect(failure.error_code, failure.message)],
        )

    @staticmethod
    def _failure_issue(
        record: ConversationRecord, stage: AnalysisStage, scope: str, failure: StepFailure
    ) -> AnalysisIssue:
        """Record one step that returned no usable answer."""
        return AnalysisIssue(
            conversation_id=record.conversation_id,
            stage=stage,
            scope=scope,
            error_code=failure.error_code,
            message=failure.message,
            retry_count=failure.retry_count,
        )