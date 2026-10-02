"""Case-scoped artifact paths and cross-case artifact loading."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from evolution.rq1.config import RQ1Config
from evolution.rq1.storage import read_jsonl


class CaseArtifactError(Exception):
    """Exception raised when Case-scoped artifacts are incomplete or inconsistent."""


def discover_case_ids(config: RQ1Config) -> list[str]:
    """Return the common ordered Case set across all configured methods."""
    cases_by_method: dict[str, set[str]] = {}
    for method in config.methods:
        method_dir = config.paths.results_root / method
        if not method_dir.is_dir():
            raise CaseArtifactError(
                f"Directory for configured method '{method}' does not exist: {method_dir}"
            )
        cases_by_method[method] = {
            entry.name for entry in method_dir.iterdir() if entry.is_dir()
        }

    reference_method = config.methods[0]
    expected = cases_by_method[reference_method]
    if not expected:
        raise CaseArtifactError(
            f"No case directories found for method '{reference_method}'"
        )

    for method in config.methods[1:]:
        missing = expected - cases_by_method[method]
        extra = cases_by_method[method] - expected
        if missing or extra:
            raise CaseArtifactError(
                f"Case set mismatch in method '{method}': "
                f"missing={sorted(missing)}, extra={sorted(extra)}"
            )
    return sorted(expected)


def resolve_case_ids(config: RQ1Config, case_id: str | None) -> list[str]:
    """Resolve one requested Case or the complete configured Case set."""
    if case_id is None:
        return discover_case_ids(config)
    missing_methods = [
        method
        for method in config.methods
        if not (config.paths.results_root / method / case_id).is_dir()
    ]
    if missing_methods:
        raise CaseArtifactError(
            f"Case '{case_id}' is missing for methods: {missing_methods}"
        )
    return [case_id]


def case_artifacts_root(config: RQ1Config, case_id: str) -> Path:
    """Return the artifact root for one Case."""
    return config.paths.artifacts_root / "cases" / case_id


def case_config(config: RQ1Config, case_id: str) -> RQ1Config:
    """Return a configuration whose artifact root is scoped to one Case."""
    paths = config.paths.model_copy(
        update={"artifacts_root": case_artifacts_root(config, case_id)}
    )
    return config.model_copy(update={"paths": paths})


def require_case_file(config: RQ1Config, case_id: str, relative_path: str) -> Path:
    """Return a required Case artifact path or raise an explicit error."""
    path = case_artifacts_root(config, case_id) / relative_path
    if not path.is_file():
        raise CaseArtifactError(
            f"Required artifact for case '{case_id}' not found: {path}"
        )
    return path


def read_case_jsonl(
    config: RQ1Config,
    relative_path: str,
    case_ids: list[str],
) -> list[dict[str, Any]]:
    """Read and concatenate one JSONL artifact from ordered Case directories."""
    rows: list[dict[str, Any]] = []
    for case_id in case_ids:
        rows.extend(read_jsonl(require_case_file(config, case_id, relative_path)))
    return rows


def read_case_csv(
    config: RQ1Config,
    relative_path: str,
    case_ids: list[str],
) -> list[dict[str, str]]:
    """Read and concatenate one CSV artifact from ordered Case directories."""
    rows: list[dict[str, str]] = []
    for case_id in case_ids:
        path = require_case_file(config, case_id, relative_path)
        with path.open("r", encoding="utf-8", newline="") as file:
            rows.extend(csv.DictReader(file))
    return rows
