"""Structured recording of LLM API calls with latency and token usage auditing."""

from pathlib import Path
from pydantic import BaseModel, Field


class LLMCallRecord(BaseModel):
    """A single LLM API call capturing its inputs, outputs, latency, and token usage."""

    model: str = Field(description="Model identifier used for the call.")
    temperature: float = Field(description="Sampling temperature used for the call.")
    max_tokens: int = Field(description="Maximum completion tokens requested.")
    messages: list[dict[str, str]] = Field(description="Message payload sent to the API.")
    output: str | None = Field(default=None, description="Assistant response text, or null on failure.")
    latency_ms: float = Field(description="Wall-clock latency of the call in milliseconds.")
    prompt_tokens: int = Field(default=0, description="Number of input tokens consumed.")
    completion_tokens: int = Field(default=0, description="Number of output tokens produced.")
    total_tokens: int = Field(default=0, description="Sum of input and output tokens.")
    status: str = Field(description="Outcome of the call: 'ok' or 'error'.")
    error_message: str | None = Field(default=None, description="Failure reason when status is 'error'.")


class LLMCallLogger:
    """Appends LLMCallRecord entries to llm_calls.jsonl under the active project directory."""

    def __init__(self, runs_dir: Path | str) -> None:
        """Initialize the logger with the root directory storing project run artifacts."""
        self._runs_dir = Path(runs_dir)
        self._project_id: str | None = None

    def set_project(self, project_id: str) -> None:
        """Bind subsequent records to the given project's log file."""
        self._project_id = project_id

    def record_call(
        self,
        model: str,
        temperature: float,
        max_tokens: int,
        messages: list[dict[str, str]],
        output: str | None,
        latency_ms: float,
        prompt_tokens: int,
        completion_tokens: int,
        status: str = "ok",
        error_message: str | None = None,
    ) -> None:
        """Build the call record and append it to the project JSONL log."""
        record = LLMCallRecord(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=messages,
            output=output,
            latency_ms=latency_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            status=status,
            error_message=error_message,
        )

        log_file = self._runs_dir / self._project_id / "llm_calls.jsonl"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as f:
            f.write(record.model_dump_json() + "\n")
