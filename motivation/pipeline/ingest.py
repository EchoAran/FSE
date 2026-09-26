"""Discovery and top-level parsing of the DevGPT input files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SOURCE_PATTERNS: dict[str, tuple[str, ...]] = {
    "issue": ("*_issue_sharing.json", "*_issue_sharings.json"),
    "pr": ("*_pr_sharing.json", "*_pr_sharings.json"),
}


def discover_source_file(snapshot_dir: Path, source: str) -> Path:
    """Find the single source file of one snapshot source type."""
    matches = sorted(
        {path for pattern in SOURCE_PATTERNS[source] for path in snapshot_dir.glob(pattern)}
    )
    if len(matches) != 1:
        candidates = [str(path) for path in matches]
        raise ValueError(
            f"{source} input discovery failed, {len(matches)} candidates: {candidates}"
        )
    return matches[0]


def load_records(path: Path) -> list[dict[str, Any]]:
    """Parse a DevGPT JSON file rooted either at a list or at an object with Sources."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("Sources"), list):
        return payload["Sources"]
    raise ValueError(f"unsupported DevGPT JSON root structure: {path}")