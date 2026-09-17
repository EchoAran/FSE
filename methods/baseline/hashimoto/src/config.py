"""Configuration schema and loader for the Hashimoto interview engine."""

from pathlib import Path
from typing import Any
from pydantic import BaseModel, Field
import yaml


class InterviewConfig(BaseModel):
    """Runtime configuration parameters for Hashimoto Dynamic Slot + Abduction."""

    api_key: str = Field(default="", repr=False, description="API key for the OpenAI-compatible endpoint.")
    base_url: str | None = Field(default=None, description="Optional OpenAI-compatible API base URL.")
    model: str = Field(default="gpt-4o", description="Model identifier for the LLM API.")
    temperature: float = Field(default=0.1, ge=0.0, le=2.0, description="Sampling temperature.")
    max_tokens: int = Field(default=1024, gt=0, description="Maximum tokens per LLM completion.")
    max_turns: int = Field(default=20, gt=0, description="Maximum allowed interview dialogue turns.")
    fill_rate_threshold: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Slot filling rate threshold to trigger early completion.",
    )
    initial_slots_path: str = Field(
        default="config/re_initial_slots.yaml",
        description="Path to the initial requirement slots configuration file.",
    )
    prompts_dir: str = Field(
        default="prompts_re",
        description="Directory containing stage prompt templates.",
    )
    runs_dir: str = Field(
        default="runs",
        description="Directory storing session runs and execution artifacts.",
    )

    @classmethod
    def from_yaml(cls, yaml_path: str | Path) -> "InterviewConfig":
        """Load configuration options from a YAML file."""
        path = Path(yaml_path)
        if not path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            data: dict[str, Any] = yaml.safe_load(f) or {}

        return cls(**data)
