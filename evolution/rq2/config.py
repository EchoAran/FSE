from pathlib import Path
from typing import Any
import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StrictConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PathsConfig(StrictConfigModel):
    cases_file: Path
    results_root: Path
    artifacts_root: Path


class JudgeConfig(StrictConfigModel):
    api_url: str
    model_name: str
    api_key: str
    temperature: float | None = 0.0
    timeout_seconds: float = 180.0
    max_retries: int = 3
    concurrency: int = 2

    @field_validator("api_url", "model_name", "api_key")
    @classmethod
    def validate_non_empty_strings(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field must not be empty.")
        return v.strip()

    @field_validator("timeout_seconds")
    @classmethod
    def validate_timeout(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("timeout_seconds must be positive.")
        return v

    @field_validator("max_retries")
    @classmethod
    def validate_max_retries(cls, v: int) -> int:
        if v < 0:
            raise ValueError("max_retries must be non-negative.")
        return v

    @field_validator("concurrency")
    @classmethod
    def validate_concurrency(cls, v: int) -> int:
        if v < 1:
            raise ValueError("concurrency must be at least 1.")
        return v


class StatisticsConfig(StrictConfigModel):
    random_seed: int = 31017
    bootstrap_repeats: int = 10000

    @field_validator("bootstrap_repeats")
    @classmethod
    def validate_bootstrap_repeats(cls, v: int) -> int:
        if v < 1:
            raise ValueError("bootstrap_repeats must be a positive integer.")
        return v


class RQ2Config(StrictConfigModel):
    paths: PathsConfig
    methods: list[str] = Field(min_length=1)
    judges: dict[str, JudgeConfig]
    statistics: StatisticsConfig

    @model_validator(mode="after")
    def validate_judges_keys(self) -> "RQ2Config":
        required_judges = {"llm_expert_1", "llm_expert_2"}
        if set(self.judges.keys()) != required_judges:
            raise ValueError(
                f"Judges must contain exactly {required_judges}, got {set(self.judges.keys())}"
            )
        return self


def load_config(
    config_path: str | Path,
    repo_root: Path | None = None,
) -> RQ2Config:
    resolved_path = Path(config_path).resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f"Config file not found: {resolved_path}")

    with open(resolved_path, "r", encoding="utf-8") as f:
        data: Any = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Config file at {resolved_path} must be a YAML mapping.")

    base_dir = repo_root.resolve() if repo_root is not None else Path(__file__).resolve().parents[2]

    paths_data = data.get("paths")
    if isinstance(paths_data, dict):
        for key in ("cases_file", "results_root", "artifacts_root"):
            val = paths_data.get(key)
            if val is not None:
                p = Path(val)
                if not p.is_absolute():
                    paths_data[key] = (base_dir / p).resolve()

    return RQ2Config.model_validate(data)
