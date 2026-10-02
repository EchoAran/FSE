"""Structured filesystem storage helpers for JSON, JSONL, and CSV artifacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable

from pydantic import BaseModel


def _serialize_value(value: Any) -> Any:
    """Serialize model objects or collections to JSON-serializable primitives."""
    if isinstance(value, BaseModel):
        return value.model_dump(by_alias=True, mode="json")
    return value


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON file into a Python dictionary."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(path: Path, value: Any, indent: int = 2) -> None:
    """Write an object to a formatted JSON file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = _serialize_value(value)
    with path.open("w", encoding="utf-8") as file:
        json.dump(serialized, file, ensure_ascii=False, indent=indent)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read a JSON Lines file into a list of dictionaries."""
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def write_jsonl(path: Path, rows: Iterable[Any]) -> None:
    """Write an iterable of items to a JSON Lines file, creating parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            serialized = _serialize_value(row)
            file.write(json.dumps(serialized, ensure_ascii=False) + "\n")


def append_jsonl(path: Path, row: Any) -> None:
    """Append a single record to a JSON Lines file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = _serialize_value(row)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(serialized, ensure_ascii=False) + "\n")


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    """Write row dictionaries to a CSV file with specified column names."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="raise")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
