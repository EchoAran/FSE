"""Analyze stage: batch LLM analysis of the structural candidates."""

from __future__ import annotations

from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

from motivation.config.config import MotivationConfig
from motivation.models.analysis import (
    AnalysisIssue,
    LsriUnit,
    ResolvedConversationAnalysis,
)
from motivation.models.dataset import ConversationRecord
from motivation.pipeline.analyzer import CompletionClient, StepRunner
from motivation.pipeline.pipeline import ConversationPipeline, PipelineOutcome
from motivation.pipeline.prepare import CONVERSATIONS_FILE, STRUCTURAL_CANDIDATES_FILE
from motivation.pipeline.prompt import PromptSet
from motivation.pipeline.validation import derive_lsri
from motivation.storage.jsonl import append_jsonl, iter_jsonl, write_jsonl

ANALYSIS_DIR = "analysis"
CONVERSATION_ANALYSIS_FILE = "conversation_analysis.jsonl"
LSRI_FILE = "lsri.jsonl"
ERRORS_FILE = "errors.jsonl"


@dataclass
class AnalysisResult:
    """Counts and paths produced by one analyze run."""

    analyzed: int
    skipped: int
    failed: int
    degraded: int
    lsri_units: int
    error_codes: dict[str, int]
    analysis_path: Path
    lsri_path: Path
    errors_path: Path


@dataclass(frozen=True)
class PreviousRun:
    """Analyses and ledger records a previous run left behind."""

    analyses: dict[str, ResolvedConversationAnalysis]
    issues: list[AnalysisIssue]

    def degraded_ids(self) -> set[str]:
        """Return the conversations the ledger marks as degraded."""
        return {issue.conversation_id for issue in self.issues}


def _issue_order(issue: AnalysisIssue) -> tuple[str, str, str]:
    """Sort ledger records by conversation, step and scope."""
    return (issue.conversation_id, issue.stage.value, issue.scope)


class AnalysisStore:
    """Persists analyses, LSRI units and ledger records while a run is in progress.

    Every finished conversation is appended immediately, so an interrupted run keeps
    the work it already did. ``rewrite`` restores a deterministic order afterwards.
    A rerun replaces the stored outcome of every conversation it analyzes, so a run
    never mixes results produced under different prompts.
    """

    def __init__(self, analysis_path: Path, lsri_path: Path, errors_path: Path) -> None:
        self._analysis_path = analysis_path
        self._lsri_path = lsri_path
        self._errors_path = errors_path
        self._analyses: dict[str, ResolvedConversationAnalysis] = {}
        self._issues: list[AnalysisIssue] = []

    def reset(self, previous: PreviousRun, rerun: set[str]) -> None:
        """Start from the records of the conversations this run does not touch."""
        self._analyses = {
            key: value for key, value in previous.analyses.items() if key not in rerun
        }
        self._issues = [item for item in previous.issues if item.conversation_id not in rerun]
        self.rewrite()

    def add(self, outcome: PipelineOutcome) -> None:
        """Store one finished conversation, replacing the record it supersedes."""
        if outcome.analysis is not None:
            self._analyses[outcome.conversation_id] = outcome.analysis
            append_jsonl(self._analysis_path, outcome.analysis)
            for unit in derive_lsri(outcome.analysis):
                append_jsonl(self._lsri_path, unit)
        for issue in outcome.issues:
            append_jsonl(self._errors_path, issue)
        self._issues.extend(outcome.issues)

    def rewrite(self) -> None:
        """Rewrite the artifacts in a deterministic order."""
        write_jsonl(self._analysis_path, (self._analyses[key] for key in sorted(self._analyses)))
        write_jsonl(self._lsri_path, self.lsri_units())
        write_jsonl(self._errors_path, sorted(self._issues, key=_issue_order))

    def lsri_units(self) -> list[LsriUnit]:
        """Derive the LSRI units of every stored analysis."""
        return [
            unit
            for key in sorted(self._analyses)
            for unit in derive_lsri(self._analyses[key])
        ]

    def error_codes(self) -> dict[str, int]:
        """Count the ledger records of every stored issue."""
        return dict(sorted(Counter(item.error_code.value for item in self._issues).items()))


class ProgressReporter:
    """Prints one console line per finished conversation."""

    def __init__(self, total: int) -> None:
        self._total = total
        self._done = 0

    def start(self) -> None:
        """Announce the size of the run before the first request."""
        print(f"analyzing {self._total} conversations", flush=True)

    def report(self, outcome: PipelineOutcome) -> None:
        """Report the state of one finished conversation."""
        self._done += 1
        print(
            f"[{self._done}/{self._total}] {outcome.conversation_id}: {_summary(outcome)}",
            flush=True,
        )


def _summary(outcome: PipelineOutcome) -> str:
    """Describe the outcome of one conversation."""
    if outcome.analysis is None:
        return f"failed error={outcome.issues[0].error_code.value}"
    units = outcome.analysis.later_information_units
    state = "degraded" if outcome.issues else "analyzed"
    summary = f"{state} units={len(units)} lsri={sum(unit.is_lsri() for unit in units)}"
    return f"{summary} issues={len(outcome.issues)}" if outcome.issues else summary


def _candidate_ids(config: MotivationConfig) -> list[str]:
    """Read the structural candidate conversation ids in derived order."""
    path = config.derived_dir / STRUCTURAL_CANDIDATES_FILE
    if not path.is_file():
        raise FileNotFoundError("structural candidates not found, run prepare first")
    return [record["conversation_id"] for record in iter_jsonl(path)]


def _candidate_records(
    config: MotivationConfig, candidate_ids: list[str]
) -> dict[str, ConversationRecord]:
    """Read the conversation records of the structural candidates."""
    wanted = set(candidate_ids)
    records: dict[str, ConversationRecord] = {}
    for payload in iter_jsonl(config.derived_dir / CONVERSATIONS_FILE):
        if payload["conversation_id"] in wanted:
            records[payload["conversation_id"]] = ConversationRecord(**payload)
    return records


def _read_previous(analysis_path: Path, errors_path: Path) -> PreviousRun:
    """Read the analyses and the ledger records of a previous run."""
    analyses: dict[str, ResolvedConversationAnalysis] = {}
    if analysis_path.is_file():
        for payload in iter_jsonl(analysis_path):
            analyses[payload["conversation_id"]] = ResolvedConversationAnalysis(**payload)
    issues: list[AnalysisIssue] = []
    if errors_path.is_file():
        issues = [AnalysisIssue(**payload) for payload in iter_jsonl(errors_path)]
    return PreviousRun(analyses, issues)


def _selected_ids(
    candidate_ids: list[str], conversation_ids: list[str] | None
) -> list[str]:
    """Restrict the candidate ids to the conversations named on the command line."""
    if not conversation_ids:
        return candidate_ids
    unknown = [item for item in conversation_ids if item not in set(candidate_ids)]
    if unknown:
        raise ValueError(f"not a structural candidate: {', '.join(unknown)}")
    wanted = set(conversation_ids)
    return [item for item in candidate_ids if item in wanted]


def _target_ids(
    selected: list[str],
    previous: PreviousRun,
    limit: int | None,
    force: bool,
) -> tuple[list[str], int]:
    """Choose the conversations to analyze and count the ones a previous run holds."""
    pending = list(selected) if force else _pending_ids(selected, previous)
    skipped = len(selected) - len(pending)
    if limit is not None:
        pending = pending[:limit]
    return pending, skipped


def _pending_ids(selected: list[str], previous: PreviousRun) -> list[str]:
    """Order one run: conversations never analyzed first, the reruns of the ledger afterwards."""
    degraded = previous.degraded_ids()
    untouched = [
        item for item in selected if item not in previous.analyses and item not in degraded
    ]
    rerun = [item for item in selected if item in degraded]
    return untouched + rerun


def analyze(
    config: MotivationConfig,
    client: CompletionClient,
    conversation_ids: list[str] | None = None,
    limit: int | None = None,
    force: bool = False,
) -> AnalysisResult:
    """Run the analysis steps over the structural candidates and write the artifacts."""
    candidate_ids = _candidate_ids(config)
    analysis_path = config.results_dir / ANALYSIS_DIR / CONVERSATION_ANALYSIS_FILE
    lsri_path = config.results_dir / ANALYSIS_DIR / LSRI_FILE
    errors_path = config.results_dir / ANALYSIS_DIR / ERRORS_FILE
    previous = _read_previous(analysis_path, errors_path)
    selected = _selected_ids(candidate_ids, conversation_ids)
    targets, skipped = _target_ids(selected, previous, limit, force)
    records = _candidate_records(config, candidate_ids)
    pipeline = ConversationPipeline(StepRunner(client), PromptSet.load(config.prompt_dir))
    store = AnalysisStore(analysis_path, lsri_path, errors_path)
    store.reset(previous, set(targets))
    reporter = ProgressReporter(len(targets))
    reporter.start()

    outcomes: list[PipelineOutcome] = []
    with ThreadPoolExecutor(max_workers=config.analyzer.concurrency) as pool:
        futures = [pool.submit(pipeline.analyze, records[item]) for item in targets]
        for future in as_completed(futures):
            outcome = future.result()
            store.add(outcome)
            reporter.report(outcome)
            outcomes.append(outcome)
    store.rewrite()

    return AnalysisResult(
        analyzed=len(targets),
        skipped=skipped,
        failed=sum(outcome.analysis is None for outcome in outcomes),
        degraded=sum(
            outcome.analysis is not None and bool(outcome.issues) for outcome in outcomes
        ),
        lsri_units=len(store.lsri_units()),
        error_codes=store.error_codes(),
        analysis_path=analysis_path,
        lsri_path=lsri_path,
        errors_path=errors_path,
    )