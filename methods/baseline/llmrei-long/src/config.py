"""Configuration schema and loader for the interview runner."""

from pathlib import Path
from typing import Any
from pydantic import BaseModel, Field
import yaml


class InterviewConfig(BaseModel):
    """Runtime configuration parameters for LLMREI-long."""

    api_key: str = Field(default="", repr=False, description="API key for the OpenAI-compatible endpoint.")
    base_url: str | None = Field(default=None, description="Optional OpenAI-compatible API base URL.")
    model: str = Field(default="gpt-4o", description="Model identifier for the LLM API.")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0, description="Sampling temperature.")
    max_tokens: int = Field(default=1024, gt=0, description="Maximum response tokens per turn.")
    max_turns: int = Field(default=20, gt=0, description="Maximum number of interview dialogue turns.")
    prompt_path: str = Field(
        default="vendor/long_prompt.txt",
        description="Path to the official long prompt text template.",
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
