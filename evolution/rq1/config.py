"""Configuration models and loading routines for RQ1 evaluation."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field


class PathsConfig(BaseModel):
    """Filesystem paths for evaluation inputs and generated artifacts."""

    model_config = ConfigDict(extra="forbid")

    results_root: Path
    artifacts_root: Path


class LLMConfig(BaseModel):
    """Configuration for chat completions endpoint."""

    model_config = ConfigDict(extra="forbid")

    api_url: str
    model_name: str
    api_key: str = ""
    api_key_env: str = ""
    temperature: float = Field(ge=0.0, default=0.0)
    timeout_seconds: float = Field(gt=0.0, default=120.0)
    max_retries: int = Field(ge=0, default=3)
    concurrency: int = Field(gt=0, default=4)
    deduplication_batch_size: int = Field(gt=0, default=50)

    def resolve_api_key(self) -> str:
        """Resolve API key from direct config, environment variable, or fallback env vars."""
        if self.api_key and self.api_key.strip():
            return self.api_key.strip()
        if self.api_key_env and self.api_key_env.strip():
            if self.api_key_env.strip().startswith("sk-"):
                return self.api_key_env.strip()
            env_val = os.environ.get(self.api_key_env.strip())
            if env_val and env_val.strip():
                return env_val.strip()
        for fallback in ("OPENAI_API_KEY", "LLM_API_KEY"):
            fb_val = os.environ.get(fallback, "").strip()
            if fb_val:
                return fb_val
        raise ValueError(
            "API key is not configured. Please specify 'api_key' in the config YAML "
            f"or set environment variable '{self.api_key_env or 'OPENAI_API_KEY'}'."
        )


class EmbeddingConfig(BaseModel):
    """Configuration for text embedding endpoint."""

    model_config = ConfigDict(extra="forbid")

    api_url: str
    model_name: str
    api_key: str = ""
    api_key_env: str = ""
    dimensions: int = Field(gt=0, default=3072)
    batch_size: int = Field(gt=0, default=64)
    timeout_seconds: float = Field(gt=0.0, default=120.0)

    def resolve_api_key(self) -> str:
        """Resolve API key from direct config, environment variable, or fallback env vars."""
        if self.api_key and self.api_key.strip():
            return self.api_key.strip()
        if self.api_key_env and self.api_key_env.strip():
            if self.api_key_env.strip().startswith("sk-"):
                return self.api_key_env.strip()
            env_val = os.environ.get(self.api_key_env.strip())
            if env_val and env_val.strip():
                return env_val.strip()
        for fallback in ("OPENAI_API_KEY", "EMBEDDING_API_KEY", "LLM_API_KEY"):
            fb_val = os.environ.get(fallback, "").strip()
            if fb_val:
                return fb_val
        raise ValueError(
            "API key is not configured. Please specify 'api_key' in the config YAML "
            f"or set environment variable '{self.api_key_env or 'OPENAI_API_KEY'}'."
        )


class ClusteringConfig(BaseModel):
    """Hierarchical clustering parameters for breadth calculation."""

    model_config = ConfigDict(extra="forbid")

    distance_threshold: float = Field(gt=0.0, default=0.5)
    sensitivity_thresholds: list[float] = Field(default_factory=lambda: [0.45, 0.55])


class ElaborationConfig(BaseModel):
    """Pairwise elaboration judgment parameters for depth calculation."""

    model_config = ConfigDict(extra="forbid")

    pair_batch_size: int = Field(gt=0, default=100)


class AuditConfig(BaseModel):
    """Sampling configuration for human audit review sheets."""

    model_config = ConfigDict(extra="forbid")

    random_seed: int = 31017
    case_count: int = Field(gt=0, default=7)


class StatisticsConfig(BaseModel):
    """Parameters for descriptive and paired comparative statistics."""

    model_config = ConfigDict(extra="forbid")

    random_seed: int = 31017
    bootstrap_repeats: int = Field(gt=0, default=10000)
    tokenizer_encoding: str = "cl100k_base"


class RQ1Config(BaseModel):
    """Unified configuration container for RQ1 evaluation workflow."""

    model_config = ConfigDict(extra="forbid")

    paths: PathsConfig
    methods: list[str]
    llm: LLMConfig
    embedding: EmbeddingConfig
    clustering: ClusteringConfig
    elaboration: ElaborationConfig
    audit: AuditConfig
    statistics: StatisticsConfig


def find_repository_root(start_path: Path | None = None) -> Path:
    """Find repository root by looking for pyproject.toml upwards."""
    current = (start_path or Path.cwd()).resolve()
    for directory in [current, *current.parents]:
        if (directory / "pyproject.toml").is_file():
            return directory
    return current


def load_config(path: str | Path, repo_root: Path | None = None) -> RQ1Config:
    """Load and validate RQ1 configuration from YAML file, resolving relative paths."""
    config_path = Path(path).resolve()
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        raw_data: dict[str, Any] = yaml.safe_load(file)

    root = repo_root or find_repository_root(config_path)

    paths_section = raw_data.get("paths", {})
    if "results_root" in paths_section:
        results_root = Path(paths_section["results_root"])
        if not results_root.is_absolute():
            paths_section["results_root"] = (root / results_root).resolve()

    if "artifacts_root" in paths_section:
        artifacts_root = Path(paths_section["artifacts_root"])
        if not artifacts_root.is_absolute():
            paths_section["artifacts_root"] = (root / artifacts_root).resolve()

    return RQ1Config.model_validate(raw_data)
