"""JSONL streaming readers and atomic writers."""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

from pydantic import BaseModel


def write_jsonl(path: Path, records: Iterable[BaseModel | dict[str, Any]]) -> Path:
    """Stream records into a JSONL file, replacing the target only on success."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(path.name + ".tmp")
    with temp_path.open("w", encoding="utf-8") as handle:
        for record in records:
            payload = record.model_dump(mode="json") if isinstance(record, BaseModel) else record
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
    temp_path.replace(path)
    return path


def append_jsonl(path: Path, record: BaseModel | dict[str, Any]) -> Path:
    """Append one record to a JSONL file and flush it for crash-safe progress."""
    payload = record.model_dump(mode="json") if isinstance(record, BaseModel) else record
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
        handle.flush()
    return path


def iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    """Yield JSONL records one by one."""
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def write_json(path: Path, payload: Any) -> Path:
    """Write one JSON document, replacing the target only on success."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(path.name + ".tmp")
    temp_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temp_path.replace(path)
    return path