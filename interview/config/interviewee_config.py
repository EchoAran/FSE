"""Interviewee Agent configuration schema and loader."""

import os
from pathlib import Path
from typing import Any, Dict, Optional, Union
import yaml
from pydantic import BaseModel, Field


class IntervieweeModelConfig(BaseModel):
    """Model endpoint and inference parameters for the interviewee agent."""

    api_url: str = Field(
        default="https://api.openai.com/v1/chat/completions",
        description="Full URL of the Chat Completions endpoint or base URL.",
    )
    model_name: str = Field(
        default="gpt-4o-mini",
        description="Target model identifier.",
    )
    api_key_env: str = Field(
        default="INTERVIEWEE_API_KEY",
        description="Primary environment variable name to retrieve the API key.",
    )
    api_key: str = Field(
        default="",
        description="Explicit API key string. Preferred to use environment variable.",
    )
    temperature: float = Field(
        default=0.5,
        ge=0.0,
        le=2.0,
        description="Sampling temperature for the interviewee LLM.",
    )
    timeout_seconds: float = Field(
        default=60.0,
        gt=0.0,
        description="Network request timeout in seconds.",
    )
    max_retries: int = Field(
        default=3,
        ge=0,
        description="Maximum request retry attempts upon transient failure.",
    )

    def get_effective_api_key(self) -> str:
        """Resolve API key using direct key, primary env var, or fallback env vars."""
        if self.api_key and self.api_key.strip():
            return self.api_key.strip()
        env_val = os.getenv(self.api_key_env, "").strip()
        if env_val:
            return env_val
        for fallback in ("OPENAI_API_KEY", "LLM_API_KEY"):
            fb_val = os.getenv(fallback, "").strip()
            if fb_val:
                return fb_val
        return ""

    def sanitized_dict(self) -> Dict[str, Any]:
        """Return dictionary representation with sensitive API keys redacted."""
        data = self.model_dump()
        data["api_key"] = ""
        return data


class IntervieweeConfig(BaseModel):
    """Top-level configuration for the simulated interviewee agent."""

    model: IntervieweeModelConfig = Field(default_factory=IntervieweeModelConfig)
    history_window_pairs: int = Field(
        default=6,
        ge=1,
        le=50,
        description="Number of recent dialogue turn pairs retained in context.",
    )
    prompt_path: Optional[str] = Field(
        default=None,
        description="Path to prompt.txt template file. Defaults to interview/interviewee/prompt.txt if None.",
    )

    @classmethod
    def load_from_yaml(cls, path: Union[str, Path]) -> "IntervieweeConfig":
        """Load and validate interviewee configuration from a YAML file."""
        config_path = Path(path)
        if not config_path.is_file():
            raise FileNotFoundError(f"Interviewee configuration file not found: {config_path}")

        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        return cls(**data)

    def sanitized_dict(self) -> Dict[str, Any]:
        """Return configuration dictionary without API credentials."""
        data = self.model_dump()
        data["model"]["api_key"] = ""
        return data


