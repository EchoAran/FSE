"""Construction, run status and atomic writing of the prepared input manifest."""

from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any

from motivation.config.config import MotivationConfig

STUDY = "devgpt_motivation"
DATASET_DOI = "10.5281/zenodo.16392320"
MANIFEST_FILENAME = "manifest.json"


class ManifestStatus(str, Enum):
    """Run status of the Motivation Study, advanced by every stage."""

    PREPARED = "prepared"
    ANALYZING = "analyzing"
    ANALYZED = "analyzed"
    SUMMARIZED = "summarized"


def build_manifest(config: MotivationConfig, input_files: dict[str, str]) -> dict[str, Any]:
    """Describe the DevGPT input set used by the current prepare run."""
    return {
        "study": STUDY,
        "dataset_doi": DATASET_DOI,
        "snapshot": config.dataset.snapshot,
        "source_types": list(config.dataset.sources),
        "input_files": input_files,
        "status": ManifestStatus.PREPARED.value,
    }


def write_manifest(results_dir: Path, manifest: dict[str, Any]) -> Path:
    """Write the manifest atomically."""
    results_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = results_dir / MANIFEST_FILENAME
    temp_path = manifest_path.with_name(manifest_path.name + ".tmp")
    temp_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp_path.replace(manifest_path)
    return manifest_path


def read_manifest(results_dir: Path) -> dict[str, Any] | None:
    """Read the manifest, or None when prepare has not run yet."""
    manifest_path = results_dir / MANIFEST_FILENAME
    if not manifest_path.is_file():
        return None
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def update_status(results_dir: Path, status: ManifestStatus) -> Path:
    """Record the status of one stage run in the manifest."""
    manifest = read_manifest(results_dir)
    if manifest is None:
        raise FileNotFoundError("manifest not found, run prepare first")
    manifest["status"] = status.value
    return write_manifest(results_dir, manifest)