from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CaseRecord(StrictBaseModel):
    case_id: str
    project_name: str
    initial_requirements: str


class MessageRecord(StrictBaseModel):
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
    messages: list[MessageRecord]


class InputItem(StrictBaseModel):
    case_id: str
    method_id: str
    source_status: str
    completed_turns: int | str
    prepare_status: Literal["ready", "source_incomplete", "input_error", "not_prepared"]
    reason: str

    def to_row(self) -> dict[str, str]:
        return {
            "case_id": self.case_id,
            "method_id": self.method_id,
            "source_status": self.source_status,
            "completed_turns": str(self.completed_turns) if self.completed_turns != "" else "",
            "prepare_status": self.prepare_status,
            "reason": self.reason,
        }


class SourceEvidence(StrictBaseModel):
    source_kind: Literal["initial_requirement", "interview_turn"]
    source_id: str
    evidence_span: str


class SRSItem(StrictBaseModel):
    requirement_id: str
    type: Literal[
        "scope_context",
        "stakeholder_actor",
        "functional_requirement",
        "business_rule_constraint",
        "data_external_interface",
        "quality_requirement",
        "exception_boundary",
        "unresolved_information",
    ]
    statement: str
    status: Literal["stated", "conditional", "unresolved"]
    source_evidence: list[SourceEvidence] = Field(default_factory=list)


class SRSRecord(StrictBaseModel):
    case_id: str
    method_id: str
    project_name: str
    items: list[SRSItem] = Field(default_factory=list)


class ValidationIssue(StrictBaseModel):
    requirement_id: str | None = None
    field: str
    issue_type: str
    message: str


class SRSGenerationResult(StrictBaseModel):
    status: Literal["success", "failed"]
    draft: SRSRecord | None = None
    request: dict[str, Any]
    raw_response: dict[str, Any] | str | None = None
    usage: dict[str, Any] | None = None
    error: str | None = None


class SRSReviewDecision(StrictBaseModel):
    requirement_id: str
    type: str
    statement: str
    status: str
    evidence_summary: str = ""
    decision: Literal["accept", "revise", "delete", "regenerate_document", ""] = ""
    revised_type: str = ""
    revised_statement: str = ""
    revised_status: str = ""
    revised_evidence_json: str = ""
    notes: str = ""

    def to_row(self) -> dict[str, str]:
        return {
            "requirement_id": self.requirement_id,
            "type": self.type,
            "statement": self.statement,
            "status": self.status,
            "evidence_summary": self.evidence_summary,
            "decision": self.decision,
            "revised_type": self.revised_type,
            "revised_statement": self.revised_statement,
            "revised_status": self.revised_status,
            "revised_evidence_json": self.revised_evidence_json,
            "notes": self.notes,
        }


class ReviewedSRSResult(StrictBaseModel):
    status: Literal["reviewed", "needs_regeneration", "review_incomplete"]
    reviewed_srs: SRSRecord | None = None
    errors: list[str] = Field(default_factory=list)


class ScenarioRecord(StrictBaseModel):
    requirement_id: str
    evaluation_scope: Literal["required", "context_only", "unresolved"]
    is_core: bool
    scenario_id: str
    setup: str
    action: str
    expected_observation: str

    def to_row(self) -> dict[str, str]:
        return {
            "requirement_id": self.requirement_id,
            "evaluation_scope": self.evaluation_scope,
            "is_core": "true" if self.is_core else "false",
            "scenario_id": self.scenario_id,
            "setup": self.setup,
            "action": self.action,
            "expected_observation": self.expected_observation,
        }


class CodingTask(StrictBaseModel):
    task_id: str
    case_id: str
    method_id: str
    run_index: int
    srs_file: str
    artifacts_root: str
    run_dir: str
    workspace_dir: str


class CommandResult(StrictBaseModel):
    command: str
    output: str
    returncode: int
    timed_out: bool = False


class ImageBuildResult(StrictBaseModel):
    status: Literal["success", "failed"]
    image: str
    log: str
    error: str | None = None


class CodingResult(StrictBaseModel):
    task_id: str
    case_id: str
    method_id: str
    run_index: int
    status: Literal[
        "planned",
        "running",
        "completed",
        "limits_exceeded",
        "infrastructure_failed",
        "interrupted",
    ]
    reason: str | None = None
    workspace_dir: str | None = None
    trajectory_path: str | None = None
    process_log: str | None = None
    exit_status: str = ""
    model_calls: int = 0
    cost: float = 0.0
    usage: dict[str, int] | None = None


class DeliverySpec(StrictBaseModel):
    build_command: str = ""
    test_command: str = ""
    run_command: str = ""
    interface_type: Literal["http", "cli", "gui", "file"]
    local_url: str = ""
    known_limitations: list[str] = Field(default_factory=list)


class SourceLocation(StrictBaseModel):
    path: str
    line: int
    snippet: str


class CommandLog(StrictBaseModel):
    command: str
    working_directory: str
    returncode: int
    timed_out: bool
    stdout_path: str
    stderr_path: str


class EvidenceRecord(StrictBaseModel):
    evidence_id: str
    case_id: str
    method_id: str
    run_index: int
    scenario_id: str
    evidence_type: Literal["source_code", "command_log", "http_response", "ui_capture", "file_output", "observation_limit"]
    relative_path: str
    summary: str


class VerificationResult(StrictBaseModel):
    case_id: str
    method_id: str
    run_index: int
    status: Literal["collected", "entry_missing", "infrastructure_failed"]
    build: CommandLog | None = None
    run: CommandLog | None = None
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    error: str | None = None


class CliInvocation(StrictBaseModel):
    command: str
    stdin: str = ""


class HttpRequest(StrictBaseModel):
    url: str
    method: str = "GET"
    request_body: str = ""
    headers: dict[str, str] = Field(default_factory=dict)
    capture: dict[str, str] = Field(default_factory=dict)


class HttpInvocation(HttpRequest):
    start_command: str
    wait_seconds: float = 2.0
    setup: list[HttpRequest] = Field(default_factory=list)
    actions: list[HttpRequest] = Field(default_factory=list)


class UnavailableInvocation(StrictBaseModel):
    reason: str = Field(min_length=1)


class UiStep(StrictBaseModel):
    action: Literal["click", "type", "key", "wait"]
    value: str = ""
    seconds: float = 0.0


class UiInvocation(StrictBaseModel):
    target: Literal["browser", "desktop"]
    url: str = ""
    start_command: str = ""
    wait_seconds: float = 2.0
    steps: list[UiStep] = Field(default_factory=list)
    screenshot_name: str = "capture.png"

    @model_validator(mode="after")
    def validate_target_payload(self) -> "UiInvocation":
        if self.target == "browser" and not self.url:
            raise ValueError("A browser UI invocation requires 'url'.")
        if self.target == "desktop" and not self.start_command:
            raise ValueError("A desktop UI invocation requires 'start_command'.")
        return self


class FileInvocation(StrictBaseModel):
    command: str
    output_files: list[str] = Field(default_factory=list)
    inspect_pdf: bool = False


class InvocationSpec(StrictBaseModel):
    case_id: str
    method_id: str
    run_index: int
    scenario_id: str
    interface_type: Literal["cli", "http", "ui", "file", "unavailable"]
    working_directory: str = ""
    timeout_seconds: float
    cli: CliInvocation | None = None
    http: HttpInvocation | None = None
    ui: UiInvocation | None = None
    file: FileInvocation | None = None
    unavailable: UnavailableInvocation | None = None

    @model_validator(mode="after")
    def validate_interface_payload(self) -> "InvocationSpec":
        provided = [
            name
            for name in ("cli", "http", "ui", "file", "unavailable")
            if getattr(self, name) is not None
        ]
        if provided != [self.interface_type]:
            raise ValueError(
                f"interface_type '{self.interface_type}' requires exactly the '{self.interface_type}' "
                f"payload, got {provided or 'none'}."
            )
        return self


class ScenarioEvidence(StrictBaseModel):
    run_index: int
    scenarios: list[ScenarioRecord] = Field(default_factory=list)
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    captured_text: dict[str, str] = Field(default_factory=dict)


class RequirementJudgment(StrictBaseModel):
    requirement_id: str
    run_index: int
    status: Literal[
        "observed_satisfied",
        "observed_partial",
        "observed_unsatisfied",
        "not_observable",
        "coding_failure",
    ]
    evidence_ids: list[str] = Field(default_factory=list)
    rationale: str
    limitation: str = ""


class RequirementEvaluation(StrictBaseModel):
    status: Literal["success", "failed"]
    judgment: RequirementJudgment | None = None
    request: dict[str, Any]
    raw_response: dict[str, Any] | str | None = None
    usage: dict[str, Any] | None = None
    error: str | None = None


class ConsistencyConclusion(StrictBaseModel):
    case_id: str
    method_id: str
    dimension: Literal["build_run", "core_requirement", "boundary_constraint", "observable_behavior"]
    consistency_status: Literal[
        "consistent_positive",
        "consistent_negative",
        "mixed",
        "evidence_limited",
        "not_applicable",
    ]
    run_indices: list[int] = Field(default_factory=list)
    requirement_ids: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    rationale: str
    limitation: str = ""


class CrossRunMatrixRow(StrictBaseModel):
    requirement_id: str
    dimension: Literal["core_requirement", "boundary_constraint", "observable_behavior"]
    statuses: list[str | None]


class CrossRunMatrix(StrictBaseModel):
    case_id: str
    method_id: str
    run_indices: list[int]
    build: list[str | None]
    run: list[str | None]
    rows: list[CrossRunMatrixRow] = Field(default_factory=list)


class EnvironmentRecord(StrictBaseModel):
    cases_file: str
    results_root: str
    artifacts_root: str
    methods: list[str] = Field(default_factory=list)
    runs_per_srs: int = 0
    artifact_processor_model: str = ""
    coding_model: str = ""
    implementation_evaluator_model: str = ""
    container_image: str = ""
    container_network: str = ""


class SRSInventoryEntry(StrictBaseModel):
    case_id: str
    method_id: str
    project_name: str = ""
    srs_status: Literal["reviewed", "draft", "missing"]
    item_count: int = 0
    requirement_ids: list[str] = Field(default_factory=list)
    scenario_count: int = 0
    pending_scenario_fields: list[str] = Field(default_factory=list)
    unresolved_reviews: int = 0


class RunCoverage(StrictBaseModel):
    case_id: str
    method_id: str
    run_index: int
    coding_status: str = "missing"
    evidence_count: int = 0
    judgment_count: int = 0


class EvidenceIndexEntry(StrictBaseModel):
    case_id: str
    method_id: str
    run_index: int
    scenario_id: str
    evidence_id: str
    evidence_type: str
    relative_path: str
    status: Literal["recorded", "artifact_missing", "collection_incomplete"]
    detail: str = ""


class CoverageReport(StrictBaseModel):
    environment: EnvironmentRecord
    input_items: list[InputItem] = Field(default_factory=list)
    srs_inventory: list[SRSInventoryEntry] = Field(default_factory=list)
    runs: list[RunCoverage] = Field(default_factory=list)
    evidence: list[EvidenceIndexEntry] = Field(default_factory=list)


class ReportResult(StrictBaseModel):
    output_dir: str
    files: list[str] = Field(default_factory=list)
    pending_conclusions: int = 0
    evidence_limitations: int = 0


class VerificationIssue(StrictBaseModel):
    issue_type: str
    message: str
    case_id: str = ""
    method_id: str = ""
    run_index: int | None = None
