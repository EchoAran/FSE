from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, StrictInt, model_validator


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TranscriptMessage(StrictBaseModel):
    message_id: str
    turn_index: int
    role: Literal["interviewer", "interviewee"]
    content: str


class TranscriptRecord(StrictBaseModel):
    case_id: str
    method_id: str
    project_name: str
    initial_requirements: str
    source_status: str
    completed_turns: int
    method_max_turns: int | None = None
    finish_message: str | None = None
    ending_observation: Literal["turn_limit_reached", "unknown"]
    messages: list[TranscriptMessage]


class FlowEvaluation(StrictBaseModel):
    local_coherence: StrictInt
    transition_quality: StrictInt
    contingent_responsiveness: StrictInt

    @model_validator(mode="after")
    def validate_scores(self) -> "FlowEvaluation":
        for name in ("local_coherence", "transition_quality", "contingent_responsiveness"):
            value = getattr(self, name)
            if not (1 <= value <= 5):
                raise ValueError(f"{name} must be an integer between 1 and 5, got {value}.")
        return self


class LLMCallDetails(StrictBaseModel):
    request: dict[str, Any]


class EvaluationRecord(StrictBaseModel):
    case_id: str
    method_id: str
    rater_id: str
    status: Literal["completed", "failed"]
    call: LLMCallDetails
    evaluation: FlowEvaluation | None = None
    error: str | None = None

    @model_validator(mode="after")
    def validate_status_integrity(self) -> "EvaluationRecord":
        if self.status == "completed":
            if self.evaluation is None:
                raise ValueError("Evaluation must be present when status is 'completed'.")
            if self.error is not None:
                raise ValueError("Error must be null when status is 'completed'.")
        elif self.status == "failed":
            if self.evaluation is not None:
                raise ValueError("Evaluation must be null when status is 'failed'.")
            if not self.error or not self.error.strip():
                raise ValueError("Error description is required when status is 'failed'.")
        return self
