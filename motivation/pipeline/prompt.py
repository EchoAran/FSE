"""User message construction and input slicing for the four analysis steps."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from motivation.models.dataset import ConversationRecord, MentionRecord, TurnRecord
from motivation.pipeline.validation import (
    ARTIFACT_CONFIRMED_PRIOR,
    ASSISTANT,
    DEVELOPER,
    ConversationIndex,
    LocatedUnit,
    turn_body,
)

WINDOW_SIZE = 10
PRIOR_BLOCK_SIZE = 10
CONTEXT_ASSISTANTS = 2
PROMPT_FILES = ("screen", "anchor", "units", "prior")


@dataclass(frozen=True)
class PromptSet:
    """The four step prompts that drive one analysis run."""

    screen: str
    anchor: str
    units: str
    prior: str

    @classmethod
    def load(cls, prompt_dir: Path) -> PromptSet:
        """Read the four step prompts from their directory."""
        texts = {
            name: (prompt_dir / f"{name}.txt").read_text(encoding="utf-8")
            for name in PROMPT_FILES
        }
        return cls(**texts)


@dataclass(frozen=True)
class UnitWindow:
    """One window of turns after the anchor whose developer turns are extracted for units."""

    turn_ids: list[str]
    developer_turn_ids: list[str]
    context_turn_ids: list[str]

    def scope(self) -> str:
        """Label the window in the ledger scope of the units step."""
        return f"{self.turn_ids[0]}-{self.turn_ids[-1]}"


@dataclass(frozen=True)
class PriorSource:
    """One prior context that the prior step consults on its own."""

    key: str
    confirmed: bool
    turn_ids: list[str] = field(default_factory=list)
    mention: MentionRecord | None = None


def _chunks(items: Sequence[str], size: int) -> Iterator[list[str]]:
    """Split items into consecutive blocks of one fixed size."""
    for start in range(0, len(items), size):
        yield list(items[start : start + size])


def unit_windows(index: ConversationIndex, anchor_position: int) -> list[UnitWindow]:
    """Split the region after the anchor into consecutive windows of developer turns."""
    region = [turn_id for turn_id in index.order if index.position[turn_id] > anchor_position]
    windows: list[UnitWindow] = []
    for block in _chunks(region, WINDOW_SIZE):
        developer_ids = [turn_id for turn_id in block if index.roles[turn_id] == DEVELOPER]
        if not developer_ids:
            continue
        windows.append(
            UnitWindow(
                turn_ids=block,
                developer_turn_ids=developer_ids,
                context_turn_ids=_window_context(index, block, anchor_position),
            )
        )
    return windows


def _window_context(
    index: ConversationIndex, block: Sequence[str], anchor_position: int
) -> list[str]:
    """Return the assistant turns that surround one window for reading context."""
    start = index.position[block[0]]
    end = index.position[block[-1]]
    leading = index.turns(role=ASSISTANT, after=anchor_position, before=start)[-1:]
    trailing = index.turns(role=ASSISTANT, after=end)[:CONTEXT_ASSISTANTS]
    return leading + trailing


def prior_sources(
    record: ConversationRecord, index: ConversationIndex, anchor_position: int
) -> list[PriorSource]:
    """Split the prior context of one conversation into the sources it is consulted by."""
    before = index.turns(role=DEVELOPER, before=anchor_position)
    sources = [
        PriorSource(key=f"{block[0]}-{block[-1]}", confirmed=True, turn_ids=block)
        for block in _chunks(before, PRIOR_BLOCK_SIZE)
    ]
    mentions = {mention.artifact_id: mention for mention in record.mentions}
    for artifact_id in index.artifact_ids():
        sources.append(
            PriorSource(
                key=artifact_id,
                confirmed=index.artifact_status[artifact_id] == {ARTIFACT_CONFIRMED_PRIOR},
                mention=mentions[artifact_id],
            )
        )
    return sources


def _turn_map(record: ConversationRecord) -> dict[str, TurnRecord]:
    """Return the turns of one conversation by turn id."""
    return {turn.turn_id: turn for turn in record.turns}


def initial_task(record: ConversationRecord) -> TurnRecord:
    """Return the first developer turn, which states the initial task."""
    return next(turn for turn in record.turns if turn.role == DEVELOPER)


def _render_turn(turn: TurnRecord) -> str:
    """Render one turn with its turn id and its role for the model input."""
    return f"[{turn.turn_id} {turn.role}]\n{turn_body(turn)}"


def _render_turns(turns: Sequence[TurnRecord]) -> str:
    """Render turns in the given order."""
    return "\n\n".join(_render_turn(turn) for turn in turns)


def _render_artifact(mention: MentionRecord) -> str:
    """Render one artifact context with its identity and its text."""
    reference = mention.source_type
    if mention.repo_name:
        reference = f"{reference} {mention.repo_name}"
    if mention.number is not None:
        reference = f"{reference}#{mention.number}"
    header = f"ARTIFACT [{mention.artifact_id}] source={reference}"
    if mention.mentioned_property:
        header = f"{header} property={mention.mentioned_property}"
    fields = []
    if mention.title:
        fields.append(f"title: {mention.title}")
    if mention.body:
        fields.append(f"body: {mention.body}")
    return f"{header}\n" + "\n".join(fields)


def screen_user_prompt(record: ConversationRecord) -> str:
    """Build the S1 user message: every turn of the conversation."""
    return f"CONVERSATION TURNS\n\n{_render_turns(record.turns)}"


def anchor_user_prompt(record: ConversationRecord, index: ConversationIndex) -> str:
    """Build the S2 user message: the initial task and every assistant answer."""
    turns = _turn_map(record)
    answers = [turns[turn_id] for turn_id in index.turns(role=ASSISTANT)]
    return (
        f"INITIAL TASK\n\n{_render_turn(initial_task(record))}\n\n"
        f"ASSISTANT ANSWERS\n\n{_render_turns(answers)}"
    )


def units_user_prompt(
    record: ConversationRecord,
    index: ConversationIndex,
    window: UnitWindow,
    anchor_turn_id: str,
) -> str:
    """Build the S3 user message: initial task, anchor turn, one turn window and its context."""
    turns = _turn_map(record)
    window_ids = sorted(window.turn_ids, key=index.position.__getitem__)
    context_ids = sorted(window.context_turn_ids, key=index.position.__getitem__)
    return (
        f"INITIAL TASK\n\n{_render_turn(initial_task(record))}\n\n"
        f"SOLUTION ANCHOR\n\n{_render_turn(turns[anchor_turn_id])}\n\n"
        f"TURN WINDOW\n\n{_render_turns([turns[turn_id] for turn_id in window_ids])}\n\n"
        f"SURROUNDING ASSISTANT TURNS\n\n"
        f"{_render_turns([turns[turn_id] for turn_id in context_ids])}"
    )


def prior_user_prompt(
    record: ConversationRecord, source: PriorSource, units: Sequence[LocatedUnit]
) -> str:
    """Build the S4 user message: one prior source and the numbered unit list."""
    if source.mention is not None:
        rendered = _render_artifact(source.mention)
    else:
        turns = _turn_map(record)
        rendered = _render_turns([turns[turn_id] for turn_id in source.turn_ids])
    unit_lines = "\n".join(
        f"unit {number}: {unit.draft.statement} | {unit.evidence_span}"
        for number, unit in enumerate(units, start=1)
    )
    return f"PRIOR SOURCE\n\n{rendered}\n\nUNITS\n\n{unit_lines}"