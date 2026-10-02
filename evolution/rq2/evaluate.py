from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Literal
import pydantic

from evolution.rq2.config import RQ2Config
from evolution.rq2.llm_client import ChatCompletionClient, LLMClientError
from evolution.rq2.models import EvaluationRecord, FlowEvaluation, LLMCallDetails, TranscriptRecord
from evolution.rq2.storage import atomic_write_json, read_csv, read_json

CODE_FENCE = "```"


@dataclass(frozen=True)
class EvaluateTaskResult:
    case_id: str
    method_id: str
    rater_id: str
    status: Literal["completed", "failed", "skipped"]
    record: EvaluationRecord | None
    error_message: str | None = None


@dataclass(frozen=True)
class EvaluateSummary:
    rater_id: str
    total_tasks: int
    completed_count: int
    failed_count: int
    skipped_count: int
    has_failures: bool
    results: list[EvaluateTaskResult]


def load_evaluation_prompt(prompt_path: Path | None = None) -> str:
    if prompt_path is None:
        prompt_path = Path(__file__).resolve().parent / "prompts" / "evaluate.txt"

    if not prompt_path.exists():
        raise FileNotFoundError(f"Evaluation prompt file not found: {prompt_path}")

    return prompt_path.read_text(encoding="utf-8")


def build_user_payload(transcript: TranscriptRecord) -> dict[str, Any]:
    return {
        "project_name": transcript.project_name,
        "initial_requirements": transcript.initial_requirements,
        "messages": [
            {
                "message_id": msg.message_id,
                "role": msg.role,
                "content": msg.content,
            }
            for msg in transcript.messages
        ],
    }


def parse_and_validate_flow_evaluation(
    raw_content: str | None,
    finish_reason: str | None,
) -> FlowEvaluation:
    if finish_reason == "length":
        raise ValueError("Generation truncated due to token limit (finish_reason=length).")

    if not raw_content or not raw_content.strip():
        raise ValueError("Empty or whitespace LLM response content.")

    # Some models wrap the JSON document in a Markdown code fence.
    content = raw_content.strip()
    if content.startswith(CODE_FENCE):
        content = content[len(CODE_FENCE):]
        if content.startswith("json"):
            content = content[len("json"):]
        content = content.strip()
        if content.endswith(CODE_FENCE):
            content = content[: -len(CODE_FENCE)].strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to decode LLM response as JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"LLM JSON root must be a mapping, got {type(data).__name__}.")

    try:
        return FlowEvaluation.model_validate(data)
    except pydantic.ValidationError as exc:
        raise ValueError(f"LLM output violated FlowEvaluation schema: {exc}") from exc


def _execute_single_task(
    case_id: str,
    method_id: str,
    rater_id: str,
    transcript: TranscriptRecord,
    client: ChatCompletionClient,
    system_prompt: str,
    artifacts_root: Path,
    rerun: bool,
) -> EvaluateTaskResult:
    record_path = artifacts_root / "cases" / case_id / method_id / f"{rater_id}.json"
    user_payload = build_user_payload(transcript)
    current_request = client._build_request_payload(system_prompt, user_payload)

    if record_path.exists() and not rerun:
        try:
            existing_data = read_json(record_path)
            existing_record = EvaluationRecord.model_validate(existing_data)
        except Exception as exc:
            err_msg = f"Failed to load existing record at {record_path}: {exc}"
            return EvaluateTaskResult(
                case_id=case_id,
                method_id=method_id,
                rater_id=rater_id,
                status="failed",
                record=None,
                error_message=err_msg,
            )

        if existing_record.status == "completed":
            if existing_record.call.request == current_request:
                return EvaluateTaskResult(
                    case_id=case_id,
                    method_id=method_id,
                    rater_id=rater_id,
                    status="skipped",
                    record=existing_record,
                )

            err_msg = (
                f"Existing completed record at {record_path} has mismatched inputs or configuration. "
                "Explicit --rerun is required to re-evaluate."
            )
            return EvaluateTaskResult(
                case_id=case_id,
                method_id=method_id,
                rater_id=rater_id,
                status="failed",
                record=existing_record,
                error_message=err_msg,
            )

    call_details: LLMCallDetails
    evaluation_record: EvaluationRecord

    try:
        response = client.complete(system_prompt, user_payload)
        call_details = LLMCallDetails(request=response.request_payload)
        try:
            flow_eval = parse_and_validate_flow_evaluation(
                raw_content=response.content,
                finish_reason=response.finish_reason,
            )
            evaluation_record = EvaluationRecord(
                case_id=case_id,
                method_id=method_id,
                rater_id=rater_id,
                status="completed",
                call=call_details,
                evaluation=flow_eval,
                error=None,
            )
        except Exception as eval_exc:
            evaluation_record = EvaluationRecord(
                case_id=case_id,
                method_id=method_id,
                rater_id=rater_id,
                status="failed",
                call=call_details,
                evaluation=None,
                error=str(eval_exc),
            )
    except LLMClientError as client_exc:
        call_details = LLMCallDetails(
            request=client_exc.request_payload or current_request,
        )
        evaluation_record = EvaluationRecord(
            case_id=case_id,
            method_id=method_id,
            rater_id=rater_id,
            status="failed",
            call=call_details,
            evaluation=None,
            error=str(client_exc),
        )
    except Exception as call_exc:
        call_details = LLMCallDetails(request=current_request)
        evaluation_record = EvaluationRecord(
            case_id=case_id,
            method_id=method_id,
            rater_id=rater_id,
            status="failed",
            call=call_details,
            evaluation=None,
            error=str(call_exc),
        )

    try:
        atomic_write_json(record_path, evaluation_record)
    except Exception as persist_exc:
        err_msg = f"Failed to persist evaluation record to {record_path}: {persist_exc}"
        return EvaluateTaskResult(
            case_id=case_id,
            method_id=method_id,
            rater_id=rater_id,
            status="failed",
            record=None,
            error_message=err_msg,
        )

    if evaluation_record.status == "completed":
        return EvaluateTaskResult(
            case_id=case_id,
            method_id=method_id,
            rater_id=rater_id,
            status="completed",
            record=evaluation_record,
        )
    else:
        return EvaluateTaskResult(
            case_id=case_id,
            method_id=method_id,
            rater_id=rater_id,
            status="failed",
            record=evaluation_record,
            error_message=evaluation_record.error,
        )


def evaluate_judge(
    config: RQ2Config,
    rater_id: str,
    case_ids: list[str] | None = None,
    rerun: bool = False,
    prompt_path: Path | None = None,
) -> EvaluateSummary:
    if rater_id not in config.judges:
        raise ValueError(
            f"Invalid rater_id '{rater_id}'. Configured judges are: {list(config.judges.keys())}"
        )

    judge_config = config.judges[rater_id]
    artifacts_root = config.paths.artifacts_root
    inventory_path = artifacts_root / "input_inventory.csv"

    if not inventory_path.exists():
        raise FileNotFoundError(
            f"Input inventory not found at {inventory_path}. Run input preparation first."
        )

    inventory_rows = read_csv(inventory_path)
    known_inventory_cases = {row.get("case_id") for row in inventory_rows if row.get("case_id")}

    if case_ids is not None:
        unknown_cases = set(case_ids) - known_inventory_cases
        if unknown_cases:
            raise ValueError(f"Unknown case_id(s) requested: {sorted(unknown_cases)}")

    ready_rows = [
        row for row in inventory_rows
        if row.get("prepare_status") == "ready"
    ]

    if case_ids is not None:
        target_case_set = set(case_ids)
        ready_rows = [row for row in ready_rows if row.get("case_id") in target_case_set]
        if not ready_rows:
            raise ValueError(f"No ready items found for requested case_id(s): {sorted(target_case_set)}")

    system_prompt = load_evaluation_prompt(prompt_path)
    client = ChatCompletionClient(judge_config)

    tasks: list[tuple[str, str, TranscriptRecord]] = []
    for row in ready_rows:
        c_id = row["case_id"]
        m_id = row["method_id"]
        transcript_path = artifacts_root / "cases" / c_id / m_id / "transcript.json"
        if not transcript_path.exists():
            raise FileNotFoundError(
                f"Transcript artifact missing for ready case '{c_id}', method '{m_id}' at {transcript_path}"
            )
        transcript_data = read_json(transcript_path)
        transcript = TranscriptRecord.model_validate(transcript_data)
        tasks.append((c_id, m_id, transcript))

    results: list[EvaluateTaskResult] = []

    with ThreadPoolExecutor(max_workers=judge_config.concurrency) as executor:
        future_to_task = {
            executor.submit(
                _execute_single_task,
                case_id=c_id,
                method_id=m_id,
                rater_id=rater_id,
                transcript=transcript,
                client=client,
                system_prompt=system_prompt,
                artifacts_root=artifacts_root,
                rerun=rerun,
            ): (c_id, m_id)
            for c_id, m_id, transcript in tasks
        }

        for future in as_completed(future_to_task):
            try:
                task_result = future.result()
            except Exception as future_exc:
                c_id, m_id = future_to_task[future]
                task_result = EvaluateTaskResult(
                    case_id=c_id,
                    method_id=m_id,
                    rater_id=rater_id,
                    status="failed",
                    record=None,
                    error_message=f"Task execution failed: {future_exc}",
                )
            results.append(task_result)

    completed_count = sum(1 for r in results if r.status == "completed")
    failed_count = sum(1 for r in results if r.status == "failed")
    skipped_count = sum(1 for r in results if r.status == "skipped")

    return EvaluateSummary(
        rater_id=rater_id,
        total_tasks=len(tasks),
        completed_count=completed_count,
        failed_count=failed_count,
        skipped_count=skipped_count,
        has_failures=failed_count > 0,
        results=results,
    )
