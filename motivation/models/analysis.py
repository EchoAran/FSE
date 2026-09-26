"""Semantic analysis models: the four step contracts, the assembled records and the ledger.

Each step answers with semantic labels and with the short phrase it selected, together with the
turn it read that phrase from. Naming the turn is what makes a phrase unambiguous, so the program
verifies the phrase inside the named turn instead of requiring it to be unique in the whole
candidate set. Numbering, timing and derivation stay pipeline duties.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel

PriorInformation = Literal["Absent", "Present", "Unclear"]


class RequirementType(str, Enum):
    """Category of requirement knowledge a later information unit carries."""

    FUNCTIONAL_BEHAVIOR = "Functional Behavior"
    ACTOR_PERMISSION = "Actor & Permission"
    BUSINESS_RULE = "Business Rule"
    DATA = "Data"
    INTERFACE = "Interface"
    CONSTRAINT_ENVIRONMENT = "Constraint & Environment"
    EXCEPTION_BOUNDARY = "Exception & Boundary"
    QUALITY = "Quality"


class IntroductionMode(str, Enum):
    """Whether the developer raised the information on their own initiative."""

    DEVELOPER_INITIATED = "Developer-initiated"
    ASSISTANT_ELICITED = "Assistant-elicited"
    UNCLEAR = "Unclear"


class ElicitationOpportunity(str, Enum):
    """Whether earlier elicitation had a reasonable chance to ask for the information."""

    YES = "Yes"
    UNCERTAIN = "Uncertain"
    NO = "No"


class ResponseUptake(str, Enum):
    """How the assistant answers after the unit reacted to the information."""

    REVISED = "Revised"
    EXTENDED = "Extended"
    NO_UPTAKE = "No Uptake"
    INSUFFICIENT = "Insufficient Evidence"


class ScreenAnswer(BaseModel):
    """S1 contract: whether the conversation asks for an implementation task."""

    implementation_oriented: bool
    implementation_reason: str


class TurnPhrase(BaseModel):
    """A phrase and the turn the model copied it from."""

    turn_id: str
    phrase: str


class AnchorAnswer(BaseModel):
    """S2 contract: the first assistant turn that holds a solution, identified by a phrase."""

    solution_anchor: TurnPhrase | None = None


class UnitDraft(BaseModel):
    """S3 contract: one later information unit as the model states it."""

    statement: str
    unit: TurnPhrase
    requirement_relevant: bool
    response_uptake: ResponseUptake | None = None
    requirement_type: RequirementType | None = None
    introduction_mode: IntroductionMode | None = None
    eeo: ElicitationOpportunity | None = None
    eeo_reason: str | None = None
    uptake: TurnPhrase | None = None


class UnitsAnswer(BaseModel):
    """S3 contract: the units the model extracted from one turn window."""

    units: list[UnitDraft] = []


class PriorMatch(BaseModel):
    """S4 contract: one unit whose meaning a prior source already expresses."""

    unit_index: int
    prior: TurnPhrase


class PriorSourceAnswer(BaseModel):
    """S4 contract: the matches found in one prior source."""

    matches: list[PriorMatch] = []


class PriorArtifactEvidence(BaseModel):
    """An artifact context span that carries the prior meaning of a unit."""

    artifact_id: str
    evidence_span: str


class LaterInformationUnit(BaseModel):
    """One information increment a developer states after the solution anchor."""

    statement: str
    evidence_span: str
    requirement_relevant: bool
    prior_information: PriorInformation
    prior_evidence_spans: list[str] = []
    prior_artifact_evidence: list[PriorArtifactEvidence] = []
    requirement_type: RequirementType | None = None
    introduction_mode: IntroductionMode | None = None
    eeo: ElicitationOpportunity | None = None
    eeo_reason: str | None = None
    response_uptake: ResponseUptake | None = None

    def is_lsri(self) -> bool:
        """Report whether the program derives this unit as a core LSRI."""
        return self.requirement_relevant and self.prior_information == "Absent"


class ResolvedLaterInformationUnit(LaterInformationUnit):
    """A later information unit whose phrases were located in the conversation turns."""

    unit_id: str
    source_turn_id: str
    prior_evidence_turn_ids: list[str] = []
    supporting_turn_ids: list[str] = []


class ResolvedConversationAnalysis(BaseModel):
    """The analysis of one conversation whose phrases were located and numbered."""

    conversation_id: str
    implementation_oriented: bool
    implementation_reason: str
    solution_anchor_turn: str | None = None
    solution_anchor_evidence: str | None = None
    later_information_units: list[ResolvedLaterInformationUnit] = []


class LsriUnit(ResolvedLaterInformationUnit):
    """A resolved unit the program derived as a core LSRI."""

    conversation_id: str


class AnalysisErrorCode(str, Enum):
    """Fixed error codes of the analyze stage."""

    EVIDENCE_SPAN_MISMATCH = "EVIDENCE_SPAN_MISMATCH"
    MISSING_LSRI_FIELDS = "MISSING_LSRI_FIELDS"
    LLM_SCHEMA_ERROR = "LLM_SCHEMA_ERROR"
    LLM_TRANSPORT_ERROR = "LLM_TRANSPORT_ERROR"


class AnalysisStage(str, Enum):
    """Pipeline step that owns a ledger record."""

    SCREEN = "screen"
    ANCHOR = "anchor"
    UNITS = "units"
    PRIOR = "prior"


class AnalysisIssue(BaseModel):
    """One piece of analysis a step could not produce, and why."""

    conversation_id: str
    stage: AnalysisStage
    scope: str
    error_code: AnalysisErrorCode
    message: str
    retry_count: int = 0