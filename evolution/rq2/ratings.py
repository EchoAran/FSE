import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, StrictInt, model_validator

from evolution.rq2.config import RQ2Config
from evolution.rq2.evaluate import build_user_payload, load_evaluation_prompt
from evolution.rq2.llm_client import build_chat_request_payload
from evolution.rq2.models import EvaluationRecord, TranscriptRecord
from evolution.rq2.storage import read_csv, read_json, write_csv

RATING_FIELDNAMES = [
    "case_id",
    "method_id",
    "rater_id",
    "dimension",
    "status",
    "score",
]

ALLOWED_DIMENSIONS: tuple[str, ...] = (
    "local_coherence",
    "transition_quality",
    "contingent_responsiveness",
)

ALLOWED_RATERS: tuple[str, ...] = (
    "llm_expert_1",
    "llm_expert_2",
    "human_expert_1",
    "human_expert_2",
)


class RatingRow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    case_id: str
    method_id: str
    rater_id: str
    dimension: Literal["local_coherence", "transition_quality", "contingent_responsiveness"]
    status: Literal["scored", ""]
    score: StrictInt | None = None

    @model_validator(mode="after")
    def validate_row_logic(self) -> "RatingRow":
        if self.status == "":
            if self.score is not None:
                raise ValueError("Score must be null when status is empty.")
        else:
            if self.score is None:
                raise ValueError("Score is required when status is 'scored'.")
            if not (1 <= self.score <= 5):
                raise ValueError(f"Score must be an integer between 1 and 5, got {self.score}.")
        return self

    def to_csv_dict(self) -> dict[str, str]:
        return {
            "case_id": self.case_id,
            "method_id": self.method_id,
            "rater_id": self.rater_id,
            "dimension": self.dimension,
            "status": self.status,
            "score": str(self.score) if self.score is not None else "",
        }


@dataclass(frozen=True)
class TemplateExportSummary:
    llm_expert_1_rows: int
    llm_expert_2_rows: int
    human_expert_1_existing_rows: int
    human_expert_1_added_rows: int
    human_expert_2_existing_rows: int
    human_expert_2_added_rows: int


def parse_and_validate_csv_row(
    row: dict[str, str],
    expected_rater_id: str,
    file_path: Path,
    line_number: int,
) -> RatingRow:
    missing_fields = set(RATING_FIELDNAMES) - set(row.keys())
    if missing_fields:
        raise ValueError(
            f"File '{file_path}' line {line_number} is missing columns: {sorted(missing_fields)}"
        )

    case_id = row.get("case_id", "").strip()
    method_id = row.get("method_id", "").strip()
    rater_id = row.get("rater_id", "").strip()
    dimension = row.get("dimension", "").strip()
    status = row.get("status", "").strip()
    score_str = row.get("score", "").strip()

    if not case_id or not method_id:
        raise ValueError(f"File '{file_path}' line {line_number} has empty case_id or method_id.")

    if rater_id != expected_rater_id:
        raise ValueError(
            f"File '{file_path}' line {line_number} has rater_id '{rater_id}', expected '{expected_rater_id}'."
        )

    if dimension not in ALLOWED_DIMENSIONS:
        raise ValueError(
            f"File '{file_path}' line {line_number} has invalid dimension '{dimension}'."
        )

    score_val: int | None = None
    if score_str != "":
        try:
            score_val = int(score_str)
        except ValueError:
            raise ValueError(
                f"File '{file_path}' line {line_number} has non-integer score: '{score_str}'."
            )

    try:
        return RatingRow(
            case_id=case_id,
            method_id=method_id,
            rater_id=rater_id,
            dimension=dimension,  # type: ignore[arg-type]
            status=status,  # type: ignore[arg-type]
            score=score_val,
        )
    except Exception as exc:
        raise ValueError(f"File '{file_path}' line {line_number} failed validation: {exc}") from exc


def read_rating_csv(
    file_path: Path | str,
    expected_rater_id: str,
) -> list[RatingRow]:
    resolved_path = Path(file_path).resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f"Rating file not found: {resolved_path}")

    with open(resolved_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or list(reader.fieldnames) != RATING_FIELDNAMES:
            raise ValueError(
                f"File '{resolved_path}' header mismatch: expected {RATING_FIELDNAMES}, got {reader.fieldnames}"
            )

        rows: list[RatingRow] = []
        seen_keys: set[tuple[str, str, str, str]] = set()

        for raw_row in reader:
            line_no = reader.line_num
            rating_row = parse_and_validate_csv_row(
                row=raw_row,
                expected_rater_id=expected_rater_id,
                file_path=resolved_path,
                line_number=line_no,
            )

            row_key = (
                rating_row.case_id,
                rating_row.method_id,
                rating_row.rater_id,
                rating_row.dimension,
            )
            if row_key in seen_keys:
                raise ValueError(
                    f"File '{resolved_path}' line {line_no} contains duplicate row key: {row_key}"
                )
            seen_keys.add(row_key)
            rows.append(rating_row)

    return rows


def export_llm_ratings(
    config: RQ2Config,
    rater_id: str,
    prompt_path: Path | None = None,
) -> int:
    if rater_id not in config.judges:
        raise ValueError(f"Unknown LLM rater_id: {rater_id}")

    artifacts_root = config.paths.artifacts_root
    inventory_path = artifacts_root / "input_inventory.csv"
    if not inventory_path.exists():
        raise FileNotFoundError(f"Inventory file not found: {inventory_path}")

    inventory_rows = read_csv(inventory_path)
    ready_items = [r for r in inventory_rows if r.get("prepare_status") == "ready"]

    judge_config = config.judges[rater_id]
    system_prompt = load_evaluation_prompt(prompt_path)

    csv_rows: list[dict[str, str]] = []

    for item in ready_items:
        c_id = item["case_id"]
        m_id = item["method_id"]
        record_path = artifacts_root / "cases" / c_id / m_id / f"{rater_id}.json"
        transcript_path = artifacts_root / "cases" / c_id / m_id / "transcript.json"

        if not record_path.exists() or not transcript_path.exists():
            continue

        try:
            record_data = read_json(record_path)
            record = EvaluationRecord.model_validate(record_data)
        except Exception as exc:
            raise ValueError(f"Corrupt evaluation record at {record_path}: {exc}") from exc

        if record.status != "completed" or record.evaluation is None:
            continue

        try:
            transcript_data = read_json(transcript_path)
            transcript = TranscriptRecord.model_validate(transcript_data)
        except Exception as exc:
            raise ValueError(f"Corrupt transcript artifact at {transcript_path}: {exc}") from exc

        user_payload = build_user_payload(transcript)
        current_request = build_chat_request_payload(
            model_name=judge_config.model_name,
            system_prompt=system_prompt,
            user_payload=user_payload,
            temperature=judge_config.temperature,
        )

        if record.call.request != current_request:
            continue

        flow_eval = record.evaluation
        dimension_map = {
            "local_coherence": flow_eval.local_coherence,
            "transition_quality": flow_eval.transition_quality,
            "contingent_responsiveness": flow_eval.contingent_responsiveness,
        }

        for dim_name in ALLOWED_DIMENSIONS:
            row_obj = RatingRow(
                case_id=c_id,
                method_id=m_id,
                rater_id=rater_id,
                dimension=dim_name,  # type: ignore[arg-type]
                status="scored",
                score=dimension_map[dim_name],
            )
            csv_rows.append(row_obj.to_csv_dict())

    dim_order = {dim: i for i, dim in enumerate(ALLOWED_DIMENSIONS)}
    csv_rows.sort(key=lambda r: (r["case_id"], r["method_id"], dim_order.get(r["dimension"], 99)))

    output_csv_path = artifacts_root / "ratings" / f"{rater_id}.csv"
    write_csv(output_csv_path, csv_rows, fieldnames=RATING_FIELDNAMES)
    return len(csv_rows)


def export_human_template(config: RQ2Config, rater_id: str) -> tuple[int, int]:
    if not rater_id.startswith("human_"):
        raise ValueError(f"Invalid human rater_id: {rater_id}")

    artifacts_root = config.paths.artifacts_root
    inventory_path = artifacts_root / "input_inventory.csv"
    if not inventory_path.exists():
        raise FileNotFoundError(f"Inventory file not found: {inventory_path}")

    inventory_rows = read_csv(inventory_path)
    known_inventory_keys = {(r["case_id"], r["method_id"]) for r in inventory_rows}
    ready_items = [r for r in inventory_rows if r.get("prepare_status") == "ready"]

    target_csv = artifacts_root / "ratings" / f"{rater_id}.csv"

    existing_rows_map: dict[tuple[str, str, str], dict[str, str]] = {}
    existing_count = 0

    if target_csv.exists():
        existing_ratings = read_rating_csv(
            target_csv,
            expected_rater_id=rater_id,
        )
        existing_count = len(existing_ratings)
        for r in existing_ratings:
            if (r.case_id, r.method_id) not in known_inventory_keys:
                raise ValueError(
                    f"File '{target_csv}' contains unknown case/method key {(r.case_id, r.method_id)} not present in inventory."
                )
            key = (r.case_id, r.method_id, r.dimension)
            existing_rows_map[key] = r.to_csv_dict()

    added_count = 0
    merged_rows_map: dict[tuple[str, str, str], dict[str, str]] = dict(existing_rows_map)

    for item in ready_items:
        c_id = item["case_id"]
        m_id = item["method_id"]
        for dim_name in ALLOWED_DIMENSIONS:
            key = (c_id, m_id, dim_name)
            if key not in merged_rows_map:
                empty_row = RatingRow(
                    case_id=c_id,
                    method_id=m_id,
                    rater_id=rater_id,
                    dimension=dim_name,  # type: ignore[arg-type]
                    status="",
                    score=None,
                )
                merged_rows_map[key] = empty_row.to_csv_dict()
                added_count += 1

    dim_order = {dim: i for i, dim in enumerate(ALLOWED_DIMENSIONS)}
    sorted_keys = sorted(
        merged_rows_map.keys(),
        key=lambda k: (k[0], k[1], dim_order.get(k[2], 99)),
    )
    output_rows = [merged_rows_map[k] for k in sorted_keys]

    write_csv(target_csv, output_rows, fieldnames=RATING_FIELDNAMES)
    return existing_count, added_count


def export_templates(
    config: RQ2Config,
    prompt_path: Path | None = None,
) -> TemplateExportSummary:
    llm1_rows = export_llm_ratings(config, "llm_expert_1", prompt_path=prompt_path)
    llm2_rows = export_llm_ratings(config, "llm_expert_2", prompt_path=prompt_path)

    h1_existing, h1_added = export_human_template(config, "human_expert_1")
    h2_existing, h2_added = export_human_template(config, "human_expert_2")

    return TemplateExportSummary(
        llm_expert_1_rows=llm1_rows,
        llm_expert_2_rows=llm2_rows,
        human_expert_1_existing_rows=h1_existing,
        human_expert_1_added_rows=h1_added,
        human_expert_2_existing_rows=h2_existing,
        human_expert_2_added_rows=h2_added,
    )
