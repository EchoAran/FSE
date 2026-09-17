"""Simulated interviewee agent driven by LLM and prompt.txt template."""

import re
from typing import Any, Dict, List
import openai

from interview.cases.models import CaseRecord
from interview.config.interviewee_config import IntervieweeConfig
from interview.interviewee.exceptions import (
    IntervieweeEmptyAnswerError,
    IntervieweeLLMError,
)
from interview.interviewee.prompts import build_system_prompt


class IntervieweeAgent:
    """Simulates a stakeholder answering requirements elicitation questions."""

    def __init__(self, config: IntervieweeConfig) -> None:
        self.config = config

        api_key = self.config.model.get_effective_api_key()
        if not api_key:
            raise ValueError(
                f"Missing API key for interviewee agent. Set environment variable "
                f"'{self.config.model.api_key_env}' or configure 'model.api_key'."
            )

        api_url = self.config.model.api_url.strip()
        if api_url.endswith("/chat/completions"):
            base_url = api_url[: -len("/chat/completions")]
        else:
            base_url = api_url

        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=self.config.model.timeout_seconds,
            max_retries=self.config.model.max_retries,
        )

    def build_messages(
        self,
        case: CaseRecord,
        current_question: str,
        recent_dialogue: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        """Construct the prompt messages array including system prompt and recent dialogue turns."""
        system_prompt = build_system_prompt(
            case=case,
            template_path=self.config.prompt_path,
        )

        messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

        window_size = self.config.history_window_pairs
        history_slice = recent_dialogue[-window_size:] if window_size > 0 else []

        for pair in history_slice:
            q_text = pair.get("interviewer", "").strip()
            a_text = pair.get("interviewee", "").strip()
            if q_text:
                messages.append({"role": "user", "content": q_text})
            if a_text:
                cleaned_a = "\n".join(line.strip() for line in a_text.splitlines() if line.strip())
                messages.append({"role": "assistant", "content": cleaned_a})

        messages.append({"role": "user", "content": current_question.strip()})
        return messages

    def respond(
        self,
        case: CaseRecord,
        current_question: str,
        recent_dialogue: List[Dict[str, str]],
    ) -> str:
        """Call the interviewee LLM to generate an answer for the current interview question."""
        if not current_question or not current_question.strip():
            raise ValueError("Current question cannot be empty.")

        messages = self.build_messages(case, current_question, recent_dialogue)

        try:
            response = self.client.chat.completions.create(
                model=self.config.model.model_name,
                messages=messages,
                temperature=self.config.model.temperature,
            )
            raw_answer = response.choices[0].message.content
        except Exception as exc:
            raise IntervieweeLLMError(f"Interviewee LLM API call failed: {exc}") from exc

        if not raw_answer or not raw_answer.strip():
            raise IntervieweeEmptyAnswerError("Interviewee LLM returned an empty or whitespace-only answer.")

        return self.clean_conversational_response(raw_answer)

    @staticmethod
    def clean_conversational_response(text: str) -> str:
        """Strip markdown syntax and eliminate empty lines for compact spoken output."""
        cleaned = text.strip()
        # Strip markdown headers (e.g. "### Summary" -> "Summary")
        cleaned = re.sub(r"^#{1,6}\s*", "", cleaned, flags=re.MULTILINE)
        # Strip bold and italic markdown markers
        cleaned = re.sub(r"\*\*([^*]+)\*\*", r"\1", cleaned)
        cleaned = re.sub(r"\*([^*]+)\*", r"\1", cleaned)
        # Strip list bullets (e.g. "- item" or "* item" or "1. item") from start of lines
        cleaned = re.sub(r"^\s*[-*•]\s+", "", cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r"^\s*\d+\.\s+", "", cleaned, flags=re.MULTILINE)
        # Remove empty lines (blank lines containing only whitespace) to save tokens
        lines = [line.strip() for line in cleaned.splitlines()]
        return "\n".join(line for line in lines if line)
