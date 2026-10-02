import csv
import json
import os
from pathlib import Path
import tempfile
from typing import Any
from pydantic import BaseModel


def atomic_write_json(file_path: Path | str, data: Any, indent: int = 2) -> None:
    target_path = Path(file_path).resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(data, BaseModel):
        dumped_data = data.model_dump(mode="json")
    else:
        dumped_data = data

    serialized = json.dumps(dumped_data, ensure_ascii=False, indent=indent)

    temp_file = tempfile.NamedTemporaryFile(
        mode="w",
        dir=target_path.parent,
        encoding="utf-8",
        delete=False,
        suffix=".tmp",
    )
    temp_path = Path(temp_file.name)
    success = False
    try:
        try:
            temp_file.write(serialized)
            temp_file.flush()
        finally:
            temp_file.close()
        os.replace(temp_path, target_path)
        success = True
    finally:
        if not success and temp_path.exists():
            temp_path.unlink()


def read_json(file_path: Path | str) -> Any:
    resolved_path = Path(file_path).resolve()
    with open(resolved_path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_jsonl(file_path: Path | str) -> list[dict[str, Any]]:
    resolved_path = Path(file_path).resolve()
    records: list[dict[str, Any]] = []
    with open(resolved_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def write_csv(
    file_path: Path | str,
    rows: list[dict[str, Any]],
    fieldnames: list[str],
) -> None:
    target_path = Path(file_path).resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)

    temp_file = tempfile.NamedTemporaryFile(
        mode="w",
        dir=target_path.parent,
        encoding="utf-8-sig",
        newline="",
        delete=False,
        suffix=".tmp",
    )
    temp_path = Path(temp_file.name)
    success = False
    try:
        try:
            writer = csv.DictWriter(
                temp_file,
                fieldnames=fieldnames,
                lineterminator="\n",
                quoting=csv.QUOTE_MINIMAL,
            )
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
            temp_file.flush()
        finally:
            temp_file.close()
        os.replace(temp_path, target_path)
        success = True
    finally:
        if not success and temp_path.exists():
            temp_path.unlink()


def read_csv(file_path: Path | str) -> list[dict[str, str]]:
    resolved_path = Path(file_path).resolve()
    with open(resolved_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)
