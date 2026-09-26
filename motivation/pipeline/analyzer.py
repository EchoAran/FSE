"""Transport of the analysis steps: one request, one parse and retries after rejected output."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

from pydantic import BaseModel, ValidationError

from motivation.llm.client import CompletionError
from motivation.models.analysis import AnalysisErrorCode

ATTEMPTS = 3

AnswerT = TypeVar("AnswerT", bound=BaseModel)
ReportT = TypeVar("ReportT")


class CompletionClient(Protocol):
    """Transport that returns the assistant message of one request."""

    def complete(self, system_prompt: str, user_prompt: str) -> str: ...


@dataclass(frozen=True)
class StepFailure:
    """Why one step could not return a usable answer."""

    error_code: AnalysisErrorCode
    message: str
    retry_count: int


@dataclass(frozen=True)
class Inspection(Generic[ReportT]):
    """Verdict of one validation pass over a parsed answer."""

    reasons: list[str]
    report: ReportT


Inspect = Callable[[AnswerT], Inspection[ReportT]]


@dataclass(frozen=True)
class StepOutcome(Generic[AnswerT, ReportT]):
    """Answer of one step together with the verdict of its last validation pass."""

    answer: AnswerT | None
    report: ReportT | None
    retry_reasons: list[str]
    failure: StepFailure | None
    retry_count: int


def extract_json_object(raw: str) -> str:
    """Strip an optional markdown fence around the returned JSON object."""
    text = raw.strip()
    if not text.startswith("```"):
        return text
    lines = text.splitlines()
    body = lines[1:] if lines and lines[0].startswith("```") else lines
    if body and body[-1].strip() == "```":
        body = body[:-1]
    return "\n".join(body).strip()


def retry_prompt(user_prompt: str, reasons: list[str]) -> str:
    """Append the rejection reasons so the retry can repair the previous answer."""
    details = "\n".join(f"- {reason}" for reason in reasons)
    return (
        f"{user_prompt}\n\nPREVIOUS ATTEMPT WAS REJECTED\n\n{details}\n\n"
        "Return a corrected JSON object that satisfies the rules."
    )


class StepRunner:
    """Performs one validated model call on behalf of a pipeline step."""

    def __init__(self, client: CompletionClient, attempts: int = ATTEMPTS) -> None:
        self._client = client
        self._attempts = attempts

    def run(
        self,
        system_prompt: str,
        user_prompt: str,
        answer_type: type[AnswerT],
        inspect: Inspect[AnswerT, ReportT] | None = None,
    ) -> StepOutcome[AnswerT, ReportT]:
        """Request one step answer, retrying when its output is rejected."""
        answer: AnswerT | None = None
        report: ReportT | None = None
        reasons: list[str] = []
        for attempt in range(self._attempts):
            prompt = user_prompt if attempt == 0 else retry_prompt(user_prompt, reasons)
            try:
                raw = self._client.complete(system_prompt, prompt)
            except CompletionError as error:
                failure = StepFailure(AnalysisErrorCode.LLM_TRANSPORT_ERROR, str(error), attempt)
                return StepOutcome(None, None, [], failure, attempt)
            try:
                answer = answer_type(**json.loads(extract_json_object(raw)))
            except (TypeError, ValueError, ValidationError) as error:
                answer = None
                report = None
                reasons = [f"{AnalysisErrorCode.LLM_SCHEMA_ERROR.value}: {error}"]
                continue
            if inspect is None:
                return StepOutcome(answer, None, [], None, attempt)
            inspection = inspect(answer)
            report = inspection.report
            reasons = inspection.reasons
            if not reasons:
                return StepOutcome(answer, report, [], None, attempt)
        if answer is None:
            failure = StepFailure(
                AnalysisErrorCode.LLM_SCHEMA_ERROR, "; ".join(reasons), self._attempts - 1
            )
            return StepOutcome(None, None, reasons, failure, self._attempts - 1)
        return StepOutcome(answer, report, reasons, None, self._attempts - 1)