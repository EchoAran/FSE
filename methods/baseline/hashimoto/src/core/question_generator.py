"""Question generation module targeting unfilled slots and abduction hypotheses."""

import json
import re
from src.client.base import BaseLLMClient
from src.models import AbductionRecord, Message, Slot


class QuestionGenerator:
    """Generates targeted follow-up interview questions based on unfilled slots."""

    def __init__(self, prompt_template: str, llm_client: BaseLLMClient) -> None:
        """Initialize the question generator with prompt template and LLM client."""
        self._prompt_template = prompt_template
        self._llm_client = llm_client

    def _extract_target_slots_and_question(self, raw_text: str) -> tuple[list[str], str]:
        """Parse target slots and question text from Target-Slot JSON object or raw text."""
        cleaned = raw_text.strip()
        code_block = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
        if code_block:
            cleaned = code_block.group(1).strip()

        candidates = [cleaned]
        json_match = re.search(r"(\{[\s\S]*\})", cleaned)
        if json_match and json_match.group(1) != cleaned:
            candidates.append(json_match.group(1).strip())

        for text_to_try in candidates:
            try:
                parsed = json.loads(text_to_try)
                if isinstance(parsed, dict):
                    raw_target = (
                        parsed.get("Target Slot S")
                        or parsed.get("target_slot")
                        or parsed.get("target_slots")
                        or parsed.get("Target Slot")
                    )
                    target_slots: list[str] = []

                    if isinstance(raw_target, dict):
                        target_slots = [str(k).strip() for k in raw_target.keys() if str(k).strip()]
                    elif isinstance(raw_target, list):
                        for item in raw_target:
                            if isinstance(item, dict):
                                name = item.get("name") or item.get("slot") or item.get("slot_name")
                                if name:
                                    target_slots.append(str(name).strip())
                            elif str(item).strip():
                                target_slots.append(str(item).strip())
                    elif isinstance(raw_target, str) and raw_target.strip():
                        target_slots = [raw_target.strip()]

                    q_val = (
                        parsed.get("Question")
                        or parsed.get("question")
                        or parsed.get("interview_question")
                        or parsed.get("formulated_question")
                    )
                    if q_val:
                        return target_slots, str(q_val).strip()
            except (json.JSONDecodeError, TypeError):
                continue

        return [], cleaned.strip('"').strip("'")


    def generate_question(
        self,
        current_slots: dict[str, Slot],
        dialogue_history: list[Message],
        initial_requirements: str,
        latest_abduction: AbductionRecord | None,
        model: str,
        temperature: float = 0.1,
        max_tokens: int = 1024,
    ) -> tuple[list[str], str]:
        """Formulate targeted slots and a single focused question."""
        unfilled_slots = [
            {"name": s.name, "category": s.category}
            for s in current_slots.values()
            if not s.is_filled
        ]
        filled_slots = [
            {"name": s.name, "category": s.category, "value": s.value}
            for s in current_slots.values()
            if s.is_filled
        ]

        system_message = Message(
            role="system",
            content=self._prompt_template,
        )

        context_parts = [
            f"Project Background Context:\n{initial_requirements.strip()}\n",
            f"Unfilled Target Slots (Priority):\n{json.dumps(unfilled_slots, indent=2)}\n",
            f"Already Filled Slots:\n{json.dumps(filled_slots, indent=2)}\n",
        ]

        if latest_abduction:
            context_parts.append(
                f"Latest Abduction Focus:\n"
                f"- Observed Fact C: {latest_abduction.surprising_fact}\n"
                f"- Suspected Reason A: {latest_abduction.suspected_reason}\n"
                f"- Target Probing Slot: {latest_abduction.new_slot}\n"
            )

        history_text = "\n".join(
            [f"{m.role.capitalize()}: {m.content}" for m in dialogue_history if m.role != "system"]
        )
        context_parts.append(f"Conversation History:\n{history_text}")

        user_message = Message(
            role="user",
            content="\n\n".join(context_parts),
        )

        response_text = self._llm_client.generate(
            messages=[system_message, user_message],
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return self._extract_target_slots_and_question(response_text)
