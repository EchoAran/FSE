from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field

from evolution.rq2.config import RQ2Config
from evolution.rq2.models import TranscriptMessage, TranscriptRecord
from evolution.rq2.storage import atomic_write_json, read_csv, read_json, read_jsonl, write_csv

INVENTORY_FIELDNAMES = [
    "case_id",
    "method_id",
    "source_status",
    "completed_turns",
    "method_max_turns",
    "ending_observation",
    "prepare_status",
    "reason",
]


class CaseMeta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    case_id: str
    project_name: str
    initial_requirements: str


class InventoryItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    case_id: str
    method_id: str
    source_status: str
    completed_turns: int | str
    method_max_turns: int | str
    ending_observation: str
    prepare_status: Literal["ready", "source_incomplete", "input_error"]
    reason: str

    def to_row(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "method_id": self.method_id,
            "source_status": self.source_status,
            "completed_turns": str(self.completed_turns) if self.completed_turns != "" else "",
            "method_max_turns": str(self.method_max_turns) if self.method_max_turns != "" else "",
            "ending_observation": self.ending_observation,
            "prepare_status": self.prepare_status,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class IngestSummary:
    total_cases: int
    total_items: int
    ready_count: int
    incomplete_count: int
    error_count: int
    has_errors: bool
    inventory: list[InventoryItem]


def load_cases(cases_file: Path | str, case_ids: list[str] | None = None) -> list[CaseMeta]:
    resolved_path = Path(cases_file).resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f"Cases file not found: {resolved_path}")

    raw_records = read_jsonl(resolved_path)
    cases: list[CaseMeta] = []
    seen_ids: set[str] = set()

    for idx, record in enumerate(raw_records, start=1):
        case = CaseMeta.model_validate(record)
        if case.case_id in seen_ids:
            raise ValueError(f"Duplicate case_id '{case.case_id}' in cases file at line {idx}.")
        seen_ids.add(case.case_id)
        cases.append(case)

    if case_ids is not None:
        selected_set = set(case_ids)
        missing_ids = selected_set - seen_ids
        if missing_ids:
            raise ValueError(f"Specified case_id(s) not found in cases file: {sorted(missing_ids)}")
        cases = [c for c in cases if c.case_id in selected_set]

    return cases


def _inspect_and_prepare_transcript(
    case: CaseMeta,
    method_id: str,
    results_root: Path,
) -> tuple[InventoryItem, TranscriptRecord | None]:
    case_dir = results_root / method_id / case.case_id
    manifest_path = case_dir / "manifest.json"
    conv_path = case_dir / "conversation.jsonl"

    if not manifest_path.exists():
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="",
                completed_turns="",
                method_max_turns="",
                ending_observation="",
                prepare_status="input_error",
                reason=f"Missing manifest.json at {manifest_path}",
            ),
            None,
        )

    try:
        manifest = read_json(manifest_path)
    except Exception as exc:
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="",
                completed_turns="",
                method_max_turns="",
                ending_observation="",
                prepare_status="input_error",
                reason=f"Failed to parse manifest.json: {exc}",
            ),
            None,
        )

    if not isinstance(manifest, dict):
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="",
                completed_turns="",
                method_max_turns="",
                ending_observation="",
                prepare_status="input_error",
                reason="manifest.json root must be a JSON object",
            ),
            None,
        )

    manifest_case_id = manifest.get("case_id")
    manifest_method_id = manifest.get("method_id")
    manifest_project_name = manifest.get("project_name")
    source_status = manifest.get("status")
    completed_turns = manifest.get("completed_turns")
    method_max_turns = manifest.get("method_max_turns")
    finish_message = manifest.get("finish_message")

    if manifest_case_id != case.case_id:
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status=str(source_status) if isinstance(source_status, str) else "",
                completed_turns=completed_turns if (type(completed_turns) is int and not isinstance(completed_turns, bool)) else "",
                method_max_turns=method_max_turns if (type(method_max_turns) is int and not isinstance(method_max_turns, bool)) else "",
                ending_observation="",
                prepare_status="input_error",
                reason=f"Manifest case_id '{manifest_case_id}' does not match path/case '{case.case_id}'",
            ),
            None,
        )

    if manifest_method_id != method_id:
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status=str(source_status) if isinstance(source_status, str) else "",
                completed_turns=completed_turns if (type(completed_turns) is int and not isinstance(completed_turns, bool)) else "",
                method_max_turns=method_max_turns if (type(method_max_turns) is int and not isinstance(method_max_turns, bool)) else "",
                ending_observation="",
                prepare_status="input_error",
                reason=f"Manifest method_id '{manifest_method_id}' does not match method '{method_id}'",
            ),
            None,
        )

    if manifest_project_name != case.project_name:
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status=str(source_status) if isinstance(source_status, str) else "",
                completed_turns=completed_turns if (type(completed_turns) is int and not isinstance(completed_turns, bool)) else "",
                method_max_turns=method_max_turns if (type(method_max_turns) is int and not isinstance(method_max_turns, bool)) else "",
                ending_observation="",
                prepare_status="input_error",
                reason=f"Manifest project_name '{manifest_project_name}' does not match case file '{case.project_name}'",
            ),
            None,
        )

    if not isinstance(source_status, str) or not source_status.strip():
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="",
                completed_turns="",
                method_max_turns="",
                ending_observation="",
                prepare_status="input_error",
                reason=f"Manifest 'status' must be a non-empty string, got {type(source_status).__name__}",
            ),
            None,
        )

    if method_max_turns is not None:
        if type(method_max_turns) is not int or isinstance(method_max_turns, bool) or method_max_turns <= 0:
            return (
                InventoryItem(
                    case_id=case.case_id,
                    method_id=method_id,
                    source_status=source_status,
                    completed_turns="",
                    method_max_turns="",
                    ending_observation="",
                    prepare_status="input_error",
                    reason=f"Manifest 'method_max_turns' must be null or a positive integer, got {method_max_turns!r}",
                ),
                None,
            )

    if finish_message is not None and not isinstance(finish_message, str):
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status=source_status,
                completed_turns=completed_turns if (type(completed_turns) is int and not isinstance(completed_turns, bool)) else "",
                method_max_turns=method_max_turns if method_max_turns is not None else "",
                ending_observation="",
                prepare_status="input_error",
                reason=f"Manifest 'finish_message' must be null or a string, got {finish_message!r}",
            ),
            None,
        )

    valid_incomplete_statuses = {"initialized", "running", "interrupted", "failed"}
    if source_status in valid_incomplete_statuses:
        if completed_turns is not None and (
            type(completed_turns) is not int or isinstance(completed_turns, bool) or completed_turns < 0
        ):
            return (
                InventoryItem(
                    case_id=case.case_id,
                    method_id=method_id,
                    source_status=source_status,
                    completed_turns="",
                    method_max_turns=method_max_turns if method_max_turns is not None else "",
                    ending_observation="",
                    prepare_status="input_error",
                    reason=f"Manifest 'completed_turns' must be null or a non-negative integer, got {completed_turns!r}",
                ),
                None,
            )

        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status=source_status,
                completed_turns=completed_turns if completed_turns is not None else "",
                method_max_turns=method_max_turns if method_max_turns is not None else "",
                ending_observation="",
                prepare_status="source_incomplete",
                reason=f"Source interview is incomplete with status '{source_status}'",
            ),
            None,
        )

    if source_status != "method_finished":
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status=source_status,
                completed_turns="",
                method_max_turns=method_max_turns if method_max_turns is not None else "",
                ending_observation="",
                prepare_status="input_error",
                reason=f"Unknown source status '{source_status}' in manifest",
            ),
            None,
        )

    if type(completed_turns) is not int or isinstance(completed_turns, bool) or completed_turns <= 0:
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="method_finished",
                completed_turns="",
                method_max_turns=method_max_turns if method_max_turns is not None else "",
                ending_observation="",
                prepare_status="input_error",
                reason=f"Completed interview has invalid or non-positive completed_turns: {completed_turns!r}",
            ),
            None,
        )

    if not conv_path.exists():
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="method_finished",
                completed_turns=completed_turns,
                method_max_turns=method_max_turns if method_max_turns is not None else "",
                ending_observation="",
                prepare_status="input_error",
                reason=f"Missing conversation.jsonl at {conv_path}",
            ),
            None,
        )

    try:
        raw_messages = read_jsonl(conv_path)
    except Exception as exc:
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="method_finished",
                completed_turns=completed_turns,
                method_max_turns=method_max_turns if method_max_turns is not None else "",
                ending_observation="",
                prepare_status="input_error",
                reason=f"Failed to parse conversation.jsonl: {exc}",
            ),
            None,
        )

    if not raw_messages:
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="method_finished",
                completed_turns=completed_turns,
                method_max_turns=method_max_turns if method_max_turns is not None else "",
                ending_observation="",
                prepare_status="input_error",
                reason="Conversation file contains no messages",
            ),
            None,
        )

    if len(raw_messages) % 2 != 0:
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="method_finished",
                completed_turns=completed_turns,
                method_max_turns=method_max_turns if method_max_turns is not None else "",
                ending_observation="",
                prepare_status="input_error",
                reason=f"Odd number of messages ({len(raw_messages)}) violates QA pair alternation",
            ),
            None,
        )

    qa_pairs_count = len(raw_messages) // 2
    if qa_pairs_count != completed_turns:
        return (
            InventoryItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="method_finished",
                completed_turns=completed_turns,
                method_max_turns=method_max_turns if method_max_turns is not None else "",
                ending_observation="",
                prepare_status="input_error",
                reason=f"Conversation QA pairs count ({qa_pairs_count}) does not match manifest completed_turns ({completed_turns})",
            ),
            None,
        )

    transcript_messages: list[TranscriptMessage] = []
    for idx, raw_msg in enumerate(raw_messages, start=1):
        if not isinstance(raw_msg, dict):
            return (
                InventoryItem(
                    case_id=case.case_id,
                    method_id=method_id,
                    source_status="method_finished",
                    completed_turns=completed_turns,
                    method_max_turns=method_max_turns if method_max_turns is not None else "",
                    ending_observation="",
                    prepare_status="input_error",
                    reason=f"Message at index {idx} is not a valid JSON object",
                ),
                None,
            )

        role = raw_msg.get("role")
        content = raw_msg.get("content")
        turn_index = raw_msg.get("turn_index")

        expected_role = "interviewer" if (idx % 2 == 1) else "interviewee"
        if role != expected_role:
            return (
                InventoryItem(
                    case_id=case.case_id,
                    method_id=method_id,
                    source_status="method_finished",
                    completed_turns=completed_turns,
                    method_max_turns=method_max_turns if method_max_turns is not None else "",
                    ending_observation="",
                    prepare_status="input_error",
                    reason=f"Message {idx} role is '{role}', expected '{expected_role}'",
                ),
                None,
            )

        if not isinstance(content, str) or not content.strip():
            return (
                InventoryItem(
                    case_id=case.case_id,
                    method_id=method_id,
                    source_status="method_finished",
                    completed_turns=completed_turns,
                    method_max_turns=method_max_turns if method_max_turns is not None else "",
                    ending_observation="",
                    prepare_status="input_error",
                    reason=f"Message {idx} content is empty or not a string",
                ),
                None,
            )

        if type(turn_index) is not int or isinstance(turn_index, bool) or turn_index < 0:
            return (
                InventoryItem(
                    case_id=case.case_id,
                    method_id=method_id,
                    source_status="method_finished",
                    completed_turns=completed_turns,
                    method_max_turns=method_max_turns if method_max_turns is not None else "",
                    ending_observation="",
                    prepare_status="input_error",
                    reason=f"Message {idx} turn_index must be a non-negative integer, got {turn_index!r}",
                ),
                None,
            )

        msg_id = f"M{idx:03d}"
        transcript_messages.append(
            TranscriptMessage(
                message_id=msg_id,
                turn_index=turn_index,
                role=expected_role,
                content=content,
            )
        )

    ending_observation: Literal["turn_limit_reached", "unknown"]
    if method_max_turns is not None and completed_turns >= method_max_turns:
        ending_observation = "turn_limit_reached"
    else:
        ending_observation = "unknown"

    record = TranscriptRecord(
        case_id=case.case_id,
        method_id=method_id,
        project_name=case.project_name,
        initial_requirements=case.initial_requirements,
        source_status="method_finished",
        completed_turns=completed_turns,
        method_max_turns=method_max_turns,
        finish_message=finish_message,
        ending_observation=ending_observation,
        messages=transcript_messages,
    )

    item = InventoryItem(
        case_id=case.case_id,
        method_id=method_id,
        source_status="method_finished",
        completed_turns=completed_turns,
        method_max_turns=method_max_turns if method_max_turns is not None else "",
        ending_observation=ending_observation,
        prepare_status="ready",
        reason="",
    )

    return item, record


def prepare_inputs(
    config: RQ2Config,
    case_ids: list[str] | None = None,
) -> IngestSummary:
    artifacts_root = config.paths.artifacts_root
    inventory_path = artifacts_root / "input_inventory.csv"

    existing_rows_map: dict[tuple[str, str], dict[str, Any]] = {}
    if inventory_path.exists():
        raw_rows = read_csv(inventory_path)
        for row in raw_rows:
            key = (row.get("case_id", ""), row.get("method_id", ""))
            if key[0] and key[1]:
                existing_rows_map[key] = row

    cases = load_cases(config.paths.cases_file, case_ids=case_ids)

    new_inventory_items: dict[tuple[str, str], InventoryItem] = {}

    for case in cases:
        for method_id in config.methods:
            item, record = _inspect_and_prepare_transcript(
                case=case,
                method_id=method_id,
                results_root=config.paths.results_root,
            )
            key = (case.case_id, method_id)
            new_inventory_items[key] = item

            if item.prepare_status == "ready" and record is not None:
                transcript_path = artifacts_root / "cases" / case.case_id / method_id / "transcript.json"
                atomic_write_json(transcript_path, record)

    merged_rows_map: dict[tuple[str, str], dict[str, Any]] = dict(existing_rows_map)
    for key, item in new_inventory_items.items():
        merged_rows_map[key] = item.to_row()

    all_keys = sorted(merged_rows_map.keys())
    output_rows = [merged_rows_map[k] for k in all_keys]

    write_csv(inventory_path, output_rows, fieldnames=INVENTORY_FIELDNAMES)

    current_items = [
        InventoryItem.model_validate(merged_rows_map[k])
        for k in all_keys
        if case_ids is None or k[0] in {c.case_id for c in cases}
    ]

    ready_count = sum(1 for item in current_items if item.prepare_status == "ready")
    incomplete_count = sum(1 for item in current_items if item.prepare_status == "source_incomplete")
    error_count = sum(1 for item in current_items if item.prepare_status == "input_error")

    return IngestSummary(
        total_cases=len(cases),
        total_items=len(current_items),
        ready_count=ready_count,
        incomplete_count=incomplete_count,
        error_count=error_count,
        has_errors=error_count > 0,
        inventory=current_items,
    )
