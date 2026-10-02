from pathlib import Path
from typing import Any
import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PathsConfig(StrictConfigModel):
    cases_file: Path
    results_root: Path
    artifacts_root: Path


class ArtifactProcessorConfig(StrictConfigModel):
    api_url: str
    model_name: str
    api_key: str
    timeout_seconds: float = 120.0

    @field_validator("timeout_seconds")
    @classmethod
    def validate_timeout(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("timeout_seconds must be positive.")
        return v

    def validate_executable(self) -> None:
        """Validate that configuration has real values, not placeholders or empty strings."""
        if not self.api_url or not self.api_url.strip() or self.api_url.startswith("YOUR_"):
            raise ValueError(f"artifact_processor.api_url must be configured, got {self.api_url!r}.")
        if not self.model_name or not self.model_name.strip() or self.model_name.startswith("YOUR_"):
            raise ValueError(f"artifact_processor.model_name must be configured, got {self.model_name!r}.")
        if not self.api_key or not self.api_key.strip() or self.api_key.startswith("YOUR_"):
            raise ValueError(f"artifact_processor.api_key must be configured, got {self.api_key!r}.")

        # Parse and assign normalized values
        self.api_url = self.api_url.strip()
        self.model_name = self.model_name.strip()
        self.api_key = self.api_key.strip()


class CodingConfig(StrictConfigModel):
    api_url: str
    model_name: str
    api_key: str
    agent_python: str
    image: str = "rq3-coding"
    runs_per_srs: int = 5
    step_limit: int | str
    wall_time_seconds: int | str
    cost_limit: float | str
    command_timeout_seconds: float = 60.0
    network: str = "none"
    concurrency: int = 1

    @field_validator("runs_per_srs")
    @classmethod
    def validate_runs(cls, v: int) -> int:
        if v < 1:
            raise ValueError("runs_per_srs must be at least 1.")
        return v

    @field_validator("command_timeout_seconds")
    @classmethod
    def validate_cmd_timeout(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("command_timeout_seconds must be positive.")
        return v

    @field_validator("concurrency")
    @classmethod
    def validate_concurrency(cls, v: int) -> int:
        if v < 1:
            raise ValueError("concurrency must be at least 1.")
        return v

    def validate_executable(self) -> None:
        """Validate that all coding configuration values are concrete and valid."""
        if not self.api_url or not self.api_url.strip() or self.api_url.startswith("YOUR_"):
            raise ValueError(f"coding.api_url must be configured, got {self.api_url!r}.")
        if not self.model_name or not self.model_name.strip() or self.model_name.startswith("YOUR_"):
            raise ValueError(f"coding.model_name must be configured, got {self.model_name!r}.")
        if not self.api_key or not self.api_key.strip() or self.api_key.startswith("YOUR_"):
            raise ValueError(f"coding.api_key must be configured, got {self.api_key!r}.")
        if not self.agent_python or not self.agent_python.strip() or self.agent_python.startswith("YOUR_"):
            raise ValueError(f"coding.agent_python must be configured, got {self.agent_python!r}.")
        if not self.image or not self.image.strip() or self.image.startswith("YOUR_"):
            raise ValueError(f"coding.image must be configured, got {self.image!r}.")

        # Validate step_limit
        if isinstance(self.step_limit, str):
            try:
                step_limit_int = int(self.step_limit)
            except ValueError:
                raise ValueError(f"coding.step_limit must be a positive integer, got {self.step_limit!r}.")
        else:
            step_limit_int = self.step_limit
        if step_limit_int <= 0:
            raise ValueError(f"coding.step_limit must be positive, got {step_limit_int}.")

        # Validate wall_time_seconds
        if isinstance(self.wall_time_seconds, str):
            try:
                wall_time_int = int(self.wall_time_seconds)
            except ValueError:
                raise ValueError(f"coding.wall_time_seconds must be a positive integer, got {self.wall_time_seconds!r}.")
        else:
            wall_time_int = self.wall_time_seconds
        if wall_time_int <= 0:
            raise ValueError(f"coding.wall_time_seconds must be positive, got {wall_time_int}.")

        # Validate cost_limit
        if isinstance(self.cost_limit, str):
            try:
                cost_limit_float = float(self.cost_limit)
            except ValueError:
                raise ValueError(f"coding.cost_limit must be a positive number, got {self.cost_limit!r}.")
        else:
            cost_limit_float = float(self.cost_limit)
        if cost_limit_float <= 0:
            raise ValueError(f"coding.cost_limit must be positive, got {cost_limit_float}.")

        # Parse and assign normalized values
        self.image = self.image.strip()
        self.api_url = self.api_url.strip()
        self.model_name = self.model_name.strip()
        self.api_key = self.api_key.strip()
        self.agent_python = self.agent_python.strip()
        self.step_limit = step_limit_int
        self.wall_time_seconds = wall_time_int
        self.cost_limit = cost_limit_float

    def validate_container_settings(self) -> None:
        """Validate the image and network that container work shares with coding."""
        if not self.image or not self.image.strip() or self.image.startswith("YOUR_"):
            raise ValueError(f"coding.image must be configured, got {self.image!r}.")
        if not self.network or not self.network.strip() or self.network.startswith("YOUR_"):
            raise ValueError(f"coding.network must be configured, got {self.network!r}.")
        self.image = self.image.strip()
        self.network = self.network.strip()


class EvaluatorConfig(StrictConfigModel):
    api_url: str
    model_name: str
    api_key: str
    timeout_seconds: float = 120.0

    @field_validator("timeout_seconds")
    @classmethod
    def validate_timeout(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("timeout_seconds must be positive.")
        return v

    def validate_executable(self) -> None:
        """Validate that evaluation configuration has valid values."""
        if not self.api_url or not self.api_url.strip() or self.api_url.startswith("YOUR_"):
            raise ValueError(f"implementation_evaluator.api_url must be configured, got {self.api_url!r}.")
        if not self.model_name or not self.model_name.strip() or self.model_name.startswith("YOUR_"):
            raise ValueError(f"implementation_evaluator.model_name must be configured, got {self.model_name!r}.")
        if not self.api_key or not self.api_key.strip() or self.api_key.startswith("YOUR_"):
            raise ValueError(f"implementation_evaluator.api_key must be configured, got {self.api_key!r}.")

        # Parse and assign normalized values
        self.api_url = self.api_url.strip()
        self.model_name = self.model_name.strip()
        self.api_key = self.api_key.strip()


class RQ3Config(StrictConfigModel):
    paths: PathsConfig
    methods: list[str] = Field(min_length=1)
    artifact_processor: ArtifactProcessorConfig | None = None
    coding: CodingConfig | None = None
    implementation_evaluator: EvaluatorConfig | None = None

    def validate_for_prepare(self) -> None:
        """Ensure configurations needed for input preparation are present."""
        if not self.methods:
            raise ValueError("Configuration 'methods' must not be empty.")

    def validate_for_srs(self) -> None:
        """Ensure configurations needed for SRS generation are present and valid."""
        self.validate_for_prepare()
        if self.artifact_processor is None:
            raise ValueError("Missing 'artifact_processor' configuration for SRS generation.")
        self.artifact_processor.validate_executable()

    def validate_for_coding(self) -> None:
        """Ensure configurations needed for coding tasks are present and valid."""
        self.validate_for_prepare()
        if self.coding is None:
            raise ValueError("Missing 'coding' configuration for implementation execution.")
        self.coding.validate_executable()

    def validate_for_evaluation(self) -> None:
        """Ensure configurations needed for evaluation are present and valid."""
        self.validate_for_prepare()
        if self.implementation_evaluator is None:
            raise ValueError("Missing 'implementation_evaluator' configuration for requirement evaluation.")
        self.implementation_evaluator.validate_executable()

    def validate_for_evidence(self) -> None:
        """Ensure the container settings needed for evidence collection are present.

        Evidence collection shares the image and network of the coding containers, but
        it starts no model work, so it does not require the coding model or its key.
        """
        self.validate_for_prepare()
        if self.coding is None:
            raise ValueError("Missing 'coding' configuration for evidence collection.")
        self.coding.validate_container_settings()


def load_config(
    config_path: str | Path,
    repo_root: Path | None = None,
) -> RQ3Config:
    """Load and parse the RQ3 configuration YAML file."""
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

    return RQ3Config.model_validate(data)
