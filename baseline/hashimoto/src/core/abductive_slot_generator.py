"""Abductive slot generator dynamically proposing candidate slots from inferred hypotheses."""

import json
import re
from src.client.base import BaseLLMClient
from src.models import AbductionRecord, Message, Slot


class AbductiveSlotGenerator:
    """Combines abductive reasoning and dynamic slot generation into a single unified step."""

    def __init__(self, prompt_template: str, llm_client: BaseLLMClient) -> None:
        """Initialize the generator with prompt template and LLM client."""
        self._prompt_template = prompt_template
        self._llm_client = llm_client

    def _extract_json(self, raw_text: str) -> dict:
        """Extract and parse JSON object from LLM response text."""
        cleaned = raw_text.strip()
        code_block = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
        if code_block:
            cleaned = code_block.group(1).strip()

        return json.loads(cleaned)

    def generate(
        self,
        current_slots: dict[str, Slot],
        dialogue_history: list[Message],
        abduction_history: list[AbductionRecord],
        initial_requirements: str,
        model: str,
        temperature: float = 0.1,
        max_tokens: int = 1024,
    ) -> tuple[AbductionRecord | None, list[Slot]]:
        """Perform abductive reasoning and generate at most 5 new candidate slots in total."""
        existing_names = set(current_slots.keys())
        slots_payload = [
            {"name": s.name, "category": s.category, "value": s.value}
            for s in current_slots.values()
        ]
        abduction_payload = [
            {
                "surprising_fact": rec.surprising_fact,
                "suspected_reason": rec.suspected_reason,
                "new_slot": rec.new_slot,
            }
            for rec in abduction_history
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
                f"Previous Abductions:\n{json.dumps(abduction_payload, indent=2)}\n\n"
                f"Dialogue History:\n" + "\n".join(history_lines)
            ),
        )

        response_text = self._llm_client.generate(
            messages=[system_message, user_message],
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        try:
            parsed = self._extract_json(response_text)
        except (json.JSONDecodeError, KeyError, TypeError):
            return None, []

        created_slots: list[Slot] = []

        # Extract new slots from either "New Slot" dict or "new_slots" list
        raw_new_slots = parsed.get("New Slot") or parsed.get("new_slots") or []

        if isinstance(raw_new_slots, dict):
            for name, meta in raw_new_slots.items():
                if len(created_slots) >= 5:
                    break
                if name and isinstance(name, str):
                    normalized_name = name.strip()
                    if normalized_name and normalized_name not in existing_names:
                        category = meta.get("category", "dynamic") if isinstance(meta, dict) else "dynamic"
                        created_slots.append(
                            Slot(name=normalized_name, category=str(category).strip(), value=None)
                        )
                        existing_names.add(normalized_name)
        elif isinstance(raw_new_slots, list):
            for item in raw_new_slots:
                if len(created_slots) >= 5:
                    break
                if isinstance(item, dict):
                    name = item.get("name")
                    category = item.get("category", "dynamic")
                    if name and isinstance(name, str):
                        normalized_name = name.strip()
                        if normalized_name and normalized_name not in existing_names:
                            created_slots.append(
                                Slot(name=normalized_name, category=str(category).strip(), value=None)
                            )
                            existing_names.add(normalized_name)

        # Extract Surprising Fact C and Reason to Suspect A
        surprising_fact = str(
            parsed.get("Surprising Fact C") or parsed.get("surprising_fact") or ""
        ).strip()
        suspected_reason = str(
            parsed.get("Reason to Suspect A") or parsed.get("suspected_reason") or ""
        ).strip()
        has_abduction_flag = parsed.get("has_abduction", bool(surprising_fact and suspected_reason))

        # Process abduction record with strict binding and deduplication
        abduction_record: AbductionRecord | None = None
        if has_abduction_flag and surprising_fact and suspected_reason and created_slots:
            is_duplicate = any(
                rec.surprising_fact.lower() == surprising_fact.lower()
                and rec.suspected_reason.lower() == suspected_reason.lower()
                for rec in abduction_history
            )

            if not is_duplicate:
                abduction_record = AbductionRecord(
                    surprising_fact=surprising_fact,
                    suspected_reason=suspected_reason,
                    new_slot=created_slots[0].name,
                )

        return abduction_record, created_slots
