"""Slot filling module updating existing slot values based on conversation history and background context."""

import json
import re
from src.client.base import BaseLLMClient
from src.models import Message, Slot


class SlotFiller:
    """Updates the values of existing information slots from dialogue turns and context."""

    def __init__(self, prompt_template: str, llm_client: BaseLLMClient) -> None:
        """Initialize the slot filler with its prompt template and LLM client."""
        self._prompt_template = prompt_template
        self._llm_client = llm_client

    def _extract_json(self, raw_text: str) -> dict | list:
        """Extract and parse JSON object or list from LLM response text."""
        cleaned = raw_text.strip()
        code_block = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
        if code_block:
            cleaned = code_block.group(1).strip()

        return json.loads(cleaned)

    def fill_slots(
        self,
        current_slots: dict[str, Slot],
        dialogue_history: list[Message],
        initial_requirements: str,
        model: str,
        temperature: float = 0.1,
        max_tokens: int = 1024,
    ) -> dict[str, Slot]:
        """Execute slot filling to update existing slot values without adding or deleting keys."""
        slots_payload = [
            {"name": s.name, "category": s.category, "value": s.value}
            for s in current_slots.values()
        ]

        history_lines = [
            f"{m.role.capitalize()}: {m.content}"
            for m in dialogue_history
            if m.role != "system"
        ]

        system_message = Message(
            role="system",
            content=self._prompt_template,
        )
        user_message = Message(
            role="user",
            content=(
                f"Project Background Context:\n{initial_requirements.strip()}\n\n"
                f"Current Slots:\n{json.dumps(slots_payload, indent=2)}\n\n"
                f"Dialogue History:\n" + "\n".join(history_lines)
            ),
        )

        response_text = self._llm_client.generate(
            messages=[system_message, user_message],
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        updated_slots = {k: Slot(name=v.name, category=v.category, value=v.value) for k, v in current_slots.items()}

        try:
            parsed = self._extract_json(response_text)
        except (json.JSONDecodeError, KeyError, TypeError):
            return updated_slots

        # Format 1: Direct dictionary mapping {slot_name: value} or {slot_name: {"category": "...", "value": ...}}
        if isinstance(parsed, dict) and "slots" not in parsed:
            for name, item_payload in parsed.items():
                if name in updated_slots:
                    if isinstance(item_payload, dict):
                        new_value = item_payload.get("value")
                    else:
                        new_value = item_payload

                    if new_value is not None:
                        cleaned_val = str(new_value).strip()
                        updated_slots[name].value = cleaned_val if cleaned_val else None
            return updated_slots

        # Format 2: Object with "slots" array or raw list of slot objects
        slot_list = parsed.get("slots", []) if isinstance(parsed, dict) else parsed
        if isinstance(slot_list, list):
            for item in slot_list:
                if isinstance(item, dict):
                    name = item.get("name")
                    new_value = item.get("value")
                    if name in updated_slots and new_value is not None:
                        cleaned_val = str(new_value).strip()
                        updated_slots[name].value = cleaned_val if cleaned_val else None

        return updated_slots
