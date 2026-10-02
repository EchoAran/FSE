import json
from pathlib import Path
import re
from typing import Any

from evolution.rq3.config import ArtifactProcessorConfig
from evolution.rq3.llm_client import LLMClient, LLMClientError
from evolution.rq3.models import (
    SRSRecord,
    SRSItem,
    SourceEvidence,
    TranscriptRecord,
    ValidationIssue,
    SRSGenerationResult,
)
from evolution.rq3.storage import atomic_write_json, atomic_write_text

SECTION_TYPE_MAP = [
    ("1. Scope and Context", "scope_context"),
    ("2. Actors", "stakeholder_actor"),
    ("3. Functional Requirements", "functional_requirement"),
    ("4. Business Rules and Constraints", "business_rule_constraint"),
    ("5. Data and External Interfaces", "data_external_interface"),
    ("6. Quality Requirements", "quality_requirement"),
    ("7. Exceptions and Boundary Conditions", "exception_boundary"),
    ("8. Unresolved Information", "unresolved_information"),
]

VALID_TYPES = {t for _, t in SECTION_TYPE_MAP}
VALID_STATUSES = {"stated", "conditional", "unresolved"}


def load_system_prompt() -> str:
    """Load the system prompt for SRS generation."""
    prompt_path = Path(__file__).resolve().parent / "prompts" / "build_srs.txt"
    return prompt_path.read_text(encoding="utf-8")


def build_srs_user_prompt(transcript: TranscriptRecord) -> str:
    """Construct the user prompt containing initial requirements and interview messages."""
    lines: list[str] = [
        f"Project: {transcript.project_name}",
        f"Case ID: {transcript.case_id}",
        "",
        "=== Initial Requirements [INITIAL_REQUIREMENTS] ===",
        transcript.initial_requirements,
        "",
        "=== Interview Transcript ===",
    ]
    for msg in transcript.messages:
        lines.append(f"[{msg.message_id}] ({msg.role}):")
        lines.append(msg.content)
        lines.append("")

    return "\n".join(lines)


def _strip_markdown_code_fences(text: str) -> str:
    """Strip markdown code fence blocks if wrapped around JSON."""
    cleaned = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if match:
        return match.group(1).strip()
    return cleaned


def parse_srs_response(
    content: str,
    transcript: TranscriptRecord,
) -> SRSRecord:
    """Parse selected source IDs and attach their complete original content."""
    cleaned = _strip_markdown_code_fences(content)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to parse model response as JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("Model response JSON root must be an object")

    raw_items = data.get("items")
    if not isinstance(raw_items, list):
        raise ValueError("Model response must contain an 'items' array")

    source_contents = {"INITIAL_REQUIREMENTS": transcript.initial_requirements}
    source_contents.update({msg.message_id: msg.content for msg in transcript.messages})
    items: list[SRSItem] = []
    for idx, raw_item in enumerate(raw_items, start=1):
        if not isinstance(raw_item, dict):
            raise ValueError(f"Item at index {idx} is not an object")
        if "source_evidence" in raw_item:
            raise ValueError(f"Item at index {idx} must select source_ids, not supply source_evidence")
        source_ids = raw_item.pop("source_ids", None)
        if not isinstance(source_ids, list) or any(not isinstance(source_id, str) for source_id in source_ids):
            raise ValueError(f"Item at index {idx} must contain a source_ids array of strings")
        source_evidence: list[SourceEvidence] = []
        for source_id in source_ids:
            if source_id not in source_contents:
                raise ValueError(f"Item at index {idx} references unknown source_id '{source_id}'")
            source_evidence.append(
                SourceEvidence(
                    source_kind="initial_requirement" if source_id == "INITIAL_REQUIREMENTS" else "interview_turn",
                    source_id=source_id,
                    evidence_span=source_contents[source_id],
                )
            )
        raw_item["source_evidence"] = source_evidence
        item = SRSItem.model_validate(raw_item)
        items.append(item)

    return SRSRecord(
        case_id=transcript.case_id,
        method_id=transcript.method_id,
        project_name=transcript.project_name,
        items=items,
    )


def validate_srs(srs: SRSRecord, transcript: TranscriptRecord) -> list[ValidationIssue]:
    """Validate SRS structure, identifier uniqueness, and exact source evidence quotes."""
    issues: list[ValidationIssue] = []

    if srs.case_id != transcript.case_id:
        issues.append(
            ValidationIssue(
                field="case_id",
                issue_type="metadata_mismatch",
                message=f"SRS case_id '{srs.case_id}' does not match transcript '{transcript.case_id}'",
            )
        )

    if srs.method_id != transcript.method_id:
        issues.append(
            ValidationIssue(
                field="method_id",
                issue_type="metadata_mismatch",
                message=f"SRS method_id '{srs.method_id}' does not match transcript '{transcript.method_id}'",
            )
        )

    seen_req_ids: set[str] = set()
    message_lookup = {m.message_id: m.content for m in transcript.messages}
    message_roles = {m.message_id: m.role for m in transcript.messages}

    for item in srs.items:
        req_id = item.requirement_id
        if not req_id or not req_id.strip():
            issues.append(
                ValidationIssue(
                    requirement_id=req_id,
                    field="requirement_id",
                    issue_type="empty_identifier",
                    message="Requirement ID must not be empty",
                )
            )
        elif req_id in seen_req_ids:
            issues.append(
                ValidationIssue(
                    requirement_id=req_id,
                    field="requirement_id",
                    issue_type="duplicate_identifier",
                    message=f"Duplicate requirement ID '{req_id}' in SRS",
                )
            )
        seen_req_ids.add(req_id)

        if item.type not in VALID_TYPES:
            issues.append(
                ValidationIssue(
                    requirement_id=req_id,
                    field="type",
                    issue_type="invalid_type",
                    message=f"Requirement type '{item.type}' is not recognized",
                )
            )

        if item.status not in VALID_STATUSES:
            issues.append(
                ValidationIssue(
                    requirement_id=req_id,
                    field="status",
                    issue_type="invalid_status",
                    message=f"Requirement status '{item.status}' is not recognized",
                )
            )

        if item.status == "unresolved" and item.type != "unresolved_information":
            issues.append(
                ValidationIssue(
                    requirement_id=req_id,
                    field="status",
                    issue_type="status_type_mismatch",
                    message="Status 'unresolved' is only allowed for type 'unresolved_information'",
                )
            )

        if item.type == "unresolved_information" and item.status != "unresolved":
            issues.append(
                ValidationIssue(
                    requirement_id=req_id,
                    field="status",
                    issue_type="status_type_mismatch",
                    message="Type 'unresolved_information' must have status 'unresolved'",
                )
            )

        if not item.statement or not item.statement.strip():
            issues.append(
                ValidationIssue(
                    requirement_id=req_id,
                    field="statement",
                    issue_type="empty_statement",
                    message="Requirement statement must not be empty",
                )
            )

        if not item.source_evidence:
            issues.append(
                ValidationIssue(
                    requirement_id=req_id,
                    field="source_evidence",
                    issue_type="missing_evidence",
                    message=f"Requirement '{req_id}' has no source evidence",
                )
            )

        for ev_idx, ev in enumerate(item.source_evidence, start=1):
            if not ev.evidence_span or not ev.evidence_span.strip():
                issues.append(
                    ValidationIssue(
                        requirement_id=req_id,
                        field=f"source_evidence[{ev_idx}].evidence_span",
                        issue_type="empty_evidence_span",
                        message=f"Evidence span for requirement '{req_id}' must not be empty",
                    )
                )
                continue

            if ev.source_kind == "initial_requirement":
                if ev.source_id != "INITIAL_REQUIREMENTS":
                    issues.append(
                        ValidationIssue(
                            requirement_id=req_id,
                            field=f"source_evidence[{ev_idx}].source_id",
                            issue_type="invalid_source_id",
                            message=f"initial_requirement source_id must be 'INITIAL_REQUIREMENTS', got '{ev.source_id}'",
                        )
                    )
                if ev.evidence_span not in transcript.initial_requirements:
                    issues.append(
                        ValidationIssue(
                            requirement_id=req_id,
                            field=f"source_evidence[{ev_idx}].evidence_span",
                            issue_type="evidence_span_not_found",
                            message=f"Evidence span '{ev.evidence_span}' not found in initial_requirements",
                        )
                    )
            elif ev.source_kind == "interview_turn":
                if ev.source_id not in message_lookup:
                    issues.append(
                        ValidationIssue(
                            requirement_id=req_id,
                            field=f"source_evidence[{ev_idx}].source_id",
                            issue_type="source_message_not_found",
                            message=f"Evidence source_id '{ev.source_id}' not found in transcript messages",
                        )
                    )
                else:
                    msg_content = message_lookup[ev.source_id]
                    if ev.evidence_span not in msg_content:
                        issues.append(
                            ValidationIssue(
                                requirement_id=req_id,
                                field=f"source_evidence[{ev_idx}].evidence_span",
                                issue_type="evidence_span_not_found",
                                message=f"Evidence span '{ev.evidence_span}' not found in message '{ev.source_id}'",
                            )
                        )
            else:
                issues.append(
                    ValidationIssue(
                        requirement_id=req_id,
                        field=f"source_evidence[{ev_idx}].source_kind",
                        issue_type="invalid_source_kind",
                        message=f"Unknown source_kind '{ev.source_kind}'",
                    )
                )

        if item.status in ("stated", "conditional"):
            has_confirmed_source = any(
                ev.source_kind == "initial_requirement"
                or (ev.source_kind == "interview_turn" and message_roles.get(ev.source_id) == "interviewee")
                for ev in item.source_evidence
            )
            if not has_confirmed_source:
                issues.append(
                    ValidationIssue(
                        requirement_id=req_id,
                        field="source_evidence",
                        issue_type="unconfirmed_evidence",
                        message=f"Requirement '{req_id}' with status '{item.status}' must have at least one piece of evidence from initial requirements or an interviewee turn",
                    )
                )

    return issues


def render_srs(srs: SRSRecord, include_evidence: bool = False) -> str:
    """Render SRS into Markdown.

    When include_evidence is False (for coding execution), hides method identities,
    turn IDs, raw quotes, and review opinions.
    """
    lines: list[str] = [
        f"# Software Requirements Specification: {srs.project_name}",
        "",
    ]

    items_by_type: dict[str, list[SRSItem]] = {t: [] for _, t in SECTION_TYPE_MAP}
    for item in srs.items:
        if item.type in items_by_type:
            items_by_type[item.type].append(item)

    for section_title, sec_type in SECTION_TYPE_MAP:
        lines.append(f"## {section_title}")
        lines.append("")
        sec_items = items_by_type[sec_type]

        if sec_type == "unresolved_information":
            if not sec_items:
                lines.append("No unresolved items identified.")
                lines.append("")
            else:
                lines.append(
                    "*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*"
                )
                lines.append("")
                for item in sec_items:
                    lines.append(f"### [{item.requirement_id}]")
                    lines.append(item.statement.strip())
                    lines.append("")
                    if include_evidence and item.source_evidence:
                        lines.append("**Source Evidence:**")
                        for ev in item.source_evidence:
                            lines.append(f"- `[{ev.source_kind}:{ev.source_id}]` \"{ev.evidence_span}\"")
                        lines.append("")
            continue

        if not sec_items:
            lines.append("None specified.")
            lines.append("")
            continue

        for item in sec_items:
            if include_evidence:
                lines.append(f"### [{item.requirement_id}] ({item.status})")
            else:
                lines.append(f"### [{item.requirement_id}]")
            lines.append(item.statement.strip())
            lines.append("")

            if include_evidence and item.source_evidence:
                lines.append("**Source Evidence:**")
                for ev in item.source_evidence:
                    lines.append(f"- `[{ev.source_kind}:{ev.source_id}]` \"{ev.evidence_span}\"")
                lines.append("")

    return "\n".join(lines)


def generate_srs(
    transcript: TranscriptRecord,
    processor_config: ArtifactProcessorConfig,
    client: LLMClient | None = None,
) -> SRSGenerationResult:
    """Generate a draft SRS using the configured LLM client and system prompt."""
    processor_config.validate_executable()

    if client is None:
        client = LLMClient(
            endpoint=processor_config.api_url,
            model_name=processor_config.model_name,
            api_key=processor_config.api_key,
            timeout_seconds=processor_config.timeout_seconds,
        )

    system_prompt = load_system_prompt()
    user_prompt = build_srs_user_prompt(transcript)
    request_payload = {
        "model": processor_config.model_name,
        "case_id": transcript.case_id,
        "method_id": transcript.method_id,
        "temperature": 0.0,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    try:
        response = client.complete(system_prompt, user_prompt, temperature=0.0)
    except LLMClientError as exc:
        return SRSGenerationResult(
            status="failed",
            request=request_payload,
            raw_response=exc.raw_response,
            error=str(exc),
        )
    except Exception as exc:
        return SRSGenerationResult(
            status="failed",
            request=request_payload,
            error=f"Unexpected generation failure: {exc}",
        )

    if not response.content or not response.content.strip():
        return SRSGenerationResult(
            status="failed",
            request=request_payload,
            raw_response=response.raw_response,
            usage=response.usage,
            error="Model returned empty response content",
        )

    try:
        draft = parse_srs_response(
            response.content,
            transcript,
        )
    except Exception as exc:
        return SRSGenerationResult(
            status="failed",
            request=request_payload,
            raw_response=response.raw_response,
            usage=response.usage,
            error=f"Failed to parse SRS JSON: {exc}",
        )

    issues = validate_srs(draft, transcript)
    if issues:
        error_details = "; ".join(f"{iss.field}: {iss.message}" for iss in issues[:5])
        if len(issues) > 5:
            error_details += f" (and {len(issues) - 5} more issues)"
        return SRSGenerationResult(
            status="failed",
            draft=draft,
            request=request_payload,
            raw_response=response.raw_response,
            usage=response.usage,
            error=f"Draft SRS validation failed: {error_details}",
        )

    return SRSGenerationResult(
        status="success",
        draft=draft,
        request=request_payload,
        raw_response=response.raw_response,
        usage=response.usage,
    )


def save_srs_generation(result: SRSGenerationResult, output_dir: Path | str) -> None:
    """Save generation artifacts including draft JSON, Markdown, and call record."""
    target_dir = Path(output_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    generation_data = {
        "status": result.status,
        "request": result.request,
        "raw_response": result.raw_response,
        "usage": result.usage,
        "error": result.error,
    }
    atomic_write_json(target_dir / "generation_record.json", generation_data)

    if result.draft is not None:
        atomic_write_json(target_dir / "draft_srs.json", result.draft)
        reading_markdown = render_srs(result.draft, include_evidence=True)
        atomic_write_text(target_dir / "draft_srs.md", reading_markdown)
