from pathlib import Path
from typing import Any

from evolution.rq3.config import RQ3Config
from evolution.rq3.models import CaseRecord, InputItem, MessageRecord, TranscriptRecord
from evolution.rq3.storage import atomic_write_json, read_csv, read_json, read_jsonl, write_csv

INVENTORY_FIELDNAMES = [
    "case_id",
    "method_id",
    "source_status",
    "completed_turns",
    "prepare_status",
    "reason",
]

INCOMPLETE_STATUSES = {"initialized", "running", "interrupted", "failed"}


def load_cases(cases_file: Path | str, case_ids: list[str] | None = None) -> list[CaseRecord]:
    """Load cases from a JSONL file, validating uniqueness and filtering if requested."""
    resolved_path = Path(cases_file).resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f"Cases file not found: {resolved_path}")

    raw_records = read_jsonl(resolved_path)
    cases: list[CaseRecord] = []
    seen_ids: set[str] = set()

    for idx, record in enumerate(raw_records, start=1):
        case = CaseRecord.model_validate(record)
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


def _validate_message_stream(
    raw_messages: list[Any],
    allow_trailing_question: bool,
) -> tuple[str | None, list[MessageRecord]]:
    """Validate message schema, alternation, non-empty content, and strict turn sequence.

    QA pairs follow the rule: question k, answer k+1.
    """
    if not allow_trailing_question and len(raw_messages) % 2 != 0:
        return f"Odd number of messages ({len(raw_messages)}) violates QA pair alternation", []

    transcript_messages: list[MessageRecord] = []
    for idx, raw_msg in enumerate(raw_messages, start=1):
        if not isinstance(raw_msg, dict):
            return f"Message at line {idx} is not a JSON object", []

        role = raw_msg.get("role")
        content = raw_msg.get("content")
        turn_index = raw_msg.get("turn_index")

        expected_role = "interviewer" if (idx % 2 == 1) else "interviewee"
        if role != expected_role:
            return f"Message {idx} role is '{role}', expected '{expected_role}'", []

        if not isinstance(content, str) or not content.strip():
            return f"Message {idx} content is empty or not a string", []

        if type(turn_index) is not int or isinstance(turn_index, bool) or turn_index < 0:
            return f"Message {idx} turn_index must be a non-negative integer, got {turn_index!r}", []

        pair_idx = (idx - 1) // 2
        expected_turn_index = pair_idx if (idx % 2 == 1) else (pair_idx + 1)
        if turn_index != expected_turn_index:
            return f"Message {idx} turn_index is {turn_index}, expected {expected_turn_index}", []

        message_id = f"T{idx:03d}"
        transcript_messages.append(
            MessageRecord(
                message_id=message_id,
                turn_index=turn_index,
                role=role,
                content=content,
            )
        )

    return None, transcript_messages


def inspect_single_input(
    case: CaseRecord,
    method_id: str,
    results_root: Path,
) -> tuple[InputItem, TranscriptRecord | None]:
    """Inspect the interview outputs for a single case-method combination."""
    case_dir = results_root / method_id / case.case_id
    manifest_path = case_dir / "manifest.json"
    conv_path = case_dir / "conversation.jsonl"

    if not manifest_path.exists():
        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="",
                completed_turns="",
                prepare_status="input_error",
                reason=f"Missing manifest.json at {manifest_path}",
            ),
            None,
        )

    try:
        manifest = read_json(manifest_path)
    except Exception as exc:
        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="",
                completed_turns="",
                prepare_status="input_error",
                reason=f"Failed to parse manifest.json: {exc}",
            ),
            None,
        )

    if not isinstance(manifest, dict):
        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="",
                completed_turns="",
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

    if manifest_case_id != case.case_id:
        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status=str(source_status) if isinstance(source_status, str) else "",
                completed_turns=completed_turns if (type(completed_turns) is int and not isinstance(completed_turns, bool)) else "",
                prepare_status="input_error",
                reason=f"Manifest case_id '{manifest_case_id}' does not match expected '{case.case_id}'",
            ),
            None,
        )

    if manifest_method_id != method_id:
        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status=str(source_status) if isinstance(source_status, str) else "",
                completed_turns=completed_turns if (type(completed_turns) is int and not isinstance(completed_turns, bool)) else "",
                prepare_status="input_error",
                reason=f"Manifest method_id '{manifest_method_id}' does not match expected '{method_id}'",
            ),
            None,
        )

    if manifest_project_name != case.project_name:
        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status=str(source_status) if isinstance(source_status, str) else "",
                completed_turns=completed_turns if (type(completed_turns) is int and not isinstance(completed_turns, bool)) else "",
                prepare_status="input_error",
                reason=f"Manifest project_name '{manifest_project_name}' does not match case record '{case.project_name}'",
            ),
            None,
        )

    if not isinstance(source_status, str) or not source_status.strip():
        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="",
                completed_turns="",
                prepare_status="input_error",
                reason=f"Manifest 'status' must be a non-empty string, got {type(source_status).__name__}",
            ),
            None,
        )

    if source_status in INCOMPLETE_STATUSES:
        if completed_turns is not None and (
            type(completed_turns) is not int or isinstance(completed_turns, bool) or completed_turns < 0
        ):
            return (
                InputItem(
                    case_id=case.case_id,
                    method_id=method_id,
                    source_status=source_status,
                    completed_turns="",
                    prepare_status="input_error",
                    reason=f"Manifest 'completed_turns' must be null or a non-negative integer, got {completed_turns!r}",
                ),
                None,
            )

        if not conv_path.exists():
            if completed_turns is None or completed_turns == 0:
                return (
                    InputItem(
                        case_id=case.case_id,
                        method_id=method_id,
                        source_status=source_status,
                        completed_turns=0,
                        prepare_status="source_incomplete",
                        reason=f"Source interview is incomplete with status '{source_status}'",
                    ),
                    None,
                )
            return (
                InputItem(
                    case_id=case.case_id,
                    method_id=method_id,
                    source_status=source_status,
                    completed_turns=completed_turns,
                    prepare_status="input_error",
                    reason=f"Missing conversation.jsonl for interview claiming {completed_turns} completed turns at {conv_path}",
                ),
                None,
            )

        try:
            raw_messages = read_jsonl(conv_path)
        except Exception as exc:
            return (
                InputItem(
                    case_id=case.case_id,
                    method_id=method_id,
                    source_status=source_status,
                    completed_turns=completed_turns if completed_turns is not None else "",
                    prepare_status="input_error",
                    reason=f"Failed to parse conversation.jsonl: {exc}",
                ),
                None,
            )

        if not raw_messages:
            if completed_turns is not None and completed_turns > 0:
                return (
                    InputItem(
                        case_id=case.case_id,
                        method_id=method_id,
                        source_status=source_status,
                        completed_turns=completed_turns,
                        prepare_status="input_error",
                        reason=f"Conversation file is empty but completed_turns is {completed_turns}",
                    ),
                    None,
                )
            return (
                InputItem(
                    case_id=case.case_id,
                    method_id=method_id,
                    source_status=source_status,
                    completed_turns=0,
                    prepare_status="source_incomplete",
                    reason=f"Source interview is incomplete with status '{source_status}'",
                ),
                None,
            )

        error_reason, _ = _validate_message_stream(raw_messages, allow_trailing_question=True)
        if error_reason is not None:
            return (
                InputItem(
                    case_id=case.case_id,
                    method_id=method_id,
                    source_status=source_status,
                    completed_turns=completed_turns if completed_turns is not None else "",
                    prepare_status="input_error",
                    reason=error_reason,
                ),
                None,
            )

        actual_completed_pairs = len(raw_messages) // 2
        if completed_turns is not None and completed_turns != actual_completed_pairs:
            return (
                InputItem(
                    case_id=case.case_id,
                    method_id=method_id,
                    source_status=source_status,
                    completed_turns=completed_turns,
                    prepare_status="input_error",
                    reason=f"Conversation QA pairs count ({actual_completed_pairs}) does not match manifest completed_turns ({completed_turns})",
                ),
                None,
            )

        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status=source_status,
                completed_turns=completed_turns if completed_turns is not None else actual_completed_pairs,
                prepare_status="source_incomplete",
                reason=f"Source interview is incomplete with status '{source_status}'",
            ),
            None,
        )

    if source_status != "method_finished":
        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status=source_status,
                completed_turns="",
                prepare_status="input_error",
                reason=f"Unknown source status '{source_status}' in manifest",
            ),
            None,
        )

    if type(completed_turns) is not int or isinstance(completed_turns, bool) or completed_turns <= 0:
        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="method_finished",
                completed_turns="",
                prepare_status="input_error",
                reason=f"Completed interview has invalid completed_turns: {completed_turns!r}",
            ),
            None,
        )

    if not conv_path.exists():
        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="method_finished",
                completed_turns=completed_turns,
                prepare_status="input_error",
                reason=f"Missing conversation.jsonl at {conv_path}",
            ),
            None,
        )

    try:
        raw_messages = read_jsonl(conv_path)
    except Exception as exc:
        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="method_finished",
                completed_turns=completed_turns,
                prepare_status="input_error",
                reason=f"Failed to parse conversation.jsonl: {exc}",
            ),
            None,
        )

    if not raw_messages:
        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="method_finished",
                completed_turns=completed_turns,
                prepare_status="input_error",
                reason="Conversation file contains no messages",
            ),
            None,
        )

    error_reason, transcript_messages = _validate_message_stream(raw_messages, allow_trailing_question=False)
    if error_reason is not None:
        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="method_finished",
                completed_turns=completed_turns,
                prepare_status="input_error",
                reason=error_reason,
            ),
            None,
        )

    qa_pairs_count = len(raw_messages) // 2
    if qa_pairs_count != completed_turns:
        return (
            InputItem(
                case_id=case.case_id,
                method_id=method_id,
                source_status="method_finished",
                completed_turns=completed_turns,
                prepare_status="input_error",
                reason=f"Conversation QA pairs count ({qa_pairs_count}) does not match manifest completed_turns ({completed_turns})",
            ),
            None,
        )

    transcript = TranscriptRecord(
        case_id=case.case_id,
        method_id=method_id,
        project_name=case.project_name,
        initial_requirements=case.initial_requirements,
        source_status=source_status,
        completed_turns=completed_turns,
        messages=transcript_messages,
    )

    return (
        InputItem(
            case_id=case.case_id,
            method_id=method_id,
            source_status=source_status,
            completed_turns=completed_turns,
            prepare_status="ready",
            reason="Transcript validated successfully",
        ),
        transcript,
    )


def prepare_transcript(
    case: CaseRecord,
    method_id: str,
    results_root: Path | str,
) -> TranscriptRecord:
    """Validate and generate a standardized TranscriptRecord for a case-method pair."""
    root_path = Path(results_root).resolve()
    item, transcript = inspect_single_input(case, method_id, root_path)
    if item.prepare_status != "ready" or transcript is None:
        raise ValueError(
            f"Cannot prepare transcript for case '{case.case_id}' and method '{method_id}': "
            f"[{item.prepare_status}] {item.reason}"
        )
    return transcript


def inspect_inputs(
    config: RQ3Config,
    case_ids: list[str] | None = None,
    method_ids: list[str] | None = None,
) -> list[InputItem]:
    """Inspect all configured case and method combinations and return status items."""
    config.validate_for_prepare()
    cases = load_cases(config.paths.cases_file, case_ids=case_ids)

    selected_methods = config.methods
    if method_ids is not None:
        selected_set = set(method_ids)
        configured_set = set(config.methods)
        missing = selected_set - configured_set
        if missing:
            raise ValueError(f"Specified method_id(s) not in configured methods: {sorted(missing)}")
        selected_methods = [m for m in config.methods if m in selected_set]

    items: list[InputItem] = []
    for case in cases:
        for method_id in selected_methods:
            item, _ = inspect_single_input(case, method_id, config.paths.results_root)
            items.append(item)

    return items


def collect_transcripts(
    config: RQ3Config,
    case_ids: list[str] | None = None,
    method_ids: list[str] | None = None,
) -> tuple[list[InputItem], list[TranscriptRecord]]:
    """Inspect all combinations and return status items alongside ready transcripts."""
    config.validate_for_prepare()
    cases = load_cases(config.paths.cases_file, case_ids=case_ids)

    selected_methods = config.methods
    if method_ids is not None:
        selected_set = set(method_ids)
        configured_set = set(config.methods)
        missing = selected_set - configured_set
        if missing:
            raise ValueError(f"Specified method_id(s) not in configured methods: {sorted(missing)}")
        selected_methods = [m for m in config.methods if m in selected_set]

    items: list[InputItem] = []
    transcripts: list[TranscriptRecord] = []

    for case in cases:
        for method_id in selected_methods:
            item, transcript = inspect_single_input(case, method_id, config.paths.results_root)
            items.append(item)
            if transcript is not None:
                transcripts.append(transcript)

    return items, transcripts


def write_input_artifacts(
    items: list[InputItem],
    transcripts: list[TranscriptRecord],
    artifacts_root: Path | str,
) -> None:
    """Write the inventory summary CSV and the standardized transcript files.

    The inventory is updated for the Case and method entries that this call inspects,
    so preparing a subset replaces those rows only and keeps the recorded state of the
    entries outside the selection.
    """
    root_path = Path(artifacts_root).resolve()
    root_path.mkdir(parents=True, exist_ok=True)

    inventory_path = root_path / "input_inventory.csv"
    write_csv(inventory_path, _updated_inventory_rows(items, inventory_path), INVENTORY_FIELDNAMES)

    for transcript in transcripts:
        case_dir = root_path / "cases" / transcript.case_id / transcript.method_id
        transcript_path = case_dir / "transcript.json"
        atomic_write_json(transcript_path, transcript)


def _updated_inventory_rows(items: list[InputItem], inventory_path: Path) -> list[dict[str, str]]:
    """Update the recorded inventory rows of the inspected Case and method entries."""
    inspected = {(item.case_id, item.method_id): item for item in items}
    rows: list[dict[str, str]] = []
    for row in read_csv(inventory_path) if inventory_path.exists() else []:
        key = (row.get("case_id", "").strip(), row.get("method_id", "").strip())
        item = inspected.pop(key, None)
        if item is not None:
            rows.append(item.to_row())
        else:
            rows.append({name: row.get(name, "") or "" for name in INVENTORY_FIELDNAMES})
    rows.extend(item.to_row() for item in inspected.values())
    return rows
