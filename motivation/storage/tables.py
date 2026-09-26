"""Atomic writer for result tables."""

from __future__ import annotations

import csv
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any


def write_rows(path: Path, fieldnames: Sequence[str], rows: Iterable[dict[str, Any]]) -> Path:
    """Write CSV rows, replacing the target only on success."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(path.name + ".tmp")
    with temp_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        writer.writerows(rows)
    temp_path.replace(path)
    return path