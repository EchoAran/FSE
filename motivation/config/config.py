"""Motivation Study configuration models and loading entry point."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, field_validator

MOTIVATION_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = MOTIVATION_ROOT.parent


def _resolve(path: Path) -> Path:
    """Resolve relative paths against the repository root."""
    return path if path.is_absolute() else REPO_ROOT / path


def display_path(path: Path) -> str:
    """Render a path relative to the repository root when it is inside it."""
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


class DatasetConfig(BaseModel):
    """Location settings of the DevGPT snapshot."""

    model_config = ConfigDict(extra="forbid")

    root: Path
    snapshot: str = "snapshot_20240514"
    sources: list[Literal["issue", "pr"]] = ["issue", "pr"]

    @field_validator("root")
    @classmethod
    def _resolve_root(cls, value: Path) -> Path:
        return _resolve(value)


class AnalyzerModelConfig(BaseModel):
    """Endpoint and inference parameters of the LLM Analyzer."""

    model_config = ConfigDict(extra="forbid")

    api_url: str
    api_key: str
    model_name: str
    temperature: float = 0.0
    timeout_seconds: float = 120.0
    max_retries: int = 2
    concurrency: int = 4


class MotivationConfig(BaseModel):
    """Top-level configuration of the Motivation Study pipeline."""

    model_config = ConfigDict(extra="forbid")

    dataset: DatasetConfig
    analyzer: AnalyzerModelConfig
    prompt_dir: Path
    derived_dir: Path = Path("motivation/data/derived")
    results_dir: Path = Path("motivation/results")

    @field_validator("prompt_dir", "derived_dir", "results_dir")
    @classmethod
    def _resolve_field(cls, value: Path) -> Path:
        return _resolve(value)


def load_config(path: str | Path) -> MotivationConfig:
    """Load the YAML configuration of one run."""
    config_path = Path(path)
    if not config_path.is_file():
        raise FileNotFoundError(f"configuration file not found: {config_path}")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return MotivationConfig(**data)