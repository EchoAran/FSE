"""Domain models for software requirement cases, dialogue turns, and public transcripts."""

from pydantic import BaseModel, Field


class RequirementCase(BaseModel):
    """Specification of a software requirements elicitation case."""

    case_id: str = Field(description="Unique identifier for the requirement case.")
    project_name: str = Field(description="Name of the software project under elicitation.")
    initial_requirements: str = Field(description="Initial background requirements or problem statement.")


class DialogueTurn(BaseModel):
    """A single clean dialogue turn in the public conversation transcript."""

    turn_id: int = Field(description="1-based index of the interview dialogue turn.")
    interviewer_utterance: str = Field(description="Question formulated by the interviewer.")
    interviewee_utterance: str = Field(description="Answer provided by the stakeholder.")


class InterviewTranscript(BaseModel):
    """Clean public record of the requirements elicitation interview."""

    case_id: str = Field(description="Identifier of the elicited requirement case.")
    project_name: str = Field(description="Name of the software project.")
    initial_requirements: str = Field(default="", description="Initial requirements context provided.")
    turns: list[DialogueTurn] = Field(default_factory=list, description="Sequence of completed interview dialogue turns.")
    is_completed: bool = Field(default=False, description="Flag indicating if the interview reached completion.")
