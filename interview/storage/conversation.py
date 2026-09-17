"""Logger and parser for conversation.jsonl public dialogue records."""

import json
from pathlib import Path
from typing import Dict, List, Optional

from interview.storage.models import DialogueMessage


class ConversationLogger:
    """Handles appending and reading dialogue turns in conversation.jsonl."""

    FILENAME = "conversation.jsonl"

    @classmethod
    def get_conversation_path(cls, results_dir: Path) -> Path:
        """Return the path to conversation.jsonl in the results directory."""
        return results_dir / cls.FILENAME

    @classmethod
    def append_message(
        cls,
        results_dir: Path,
        turn_index: int,
        role: str,
        content: str,
    ) -> DialogueMessage:
        """Append a single dialogue message to conversation.jsonl without timestamps."""
        results_dir.mkdir(parents=True, exist_ok=True)
        message = DialogueMessage(
            turn_index=turn_index,
            role=role,
            content=content,
        )
        file_path = cls.get_conversation_path(results_dir)
        with file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(message.to_dict(), ensure_ascii=False) + "\n")

        return message

    @classmethod
    def load_messages(cls, results_dir: Path) -> List[DialogueMessage]:
        """Load all recorded dialogue messages from conversation.jsonl."""
        file_path = cls.get_conversation_path(results_dir)
        if not file_path.is_file():
            return []

        messages: List[DialogueMessage] = []
        with file_path.open("r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    data = json.loads(stripped)
                    messages.append(
                        DialogueMessage(
                            turn_index=data["turn_index"],
                            role=data["role"],
                            content=data["content"],
                        )
                    )
        return messages

    @classmethod
    def get_recent_dialogue_pairs(
        cls,
        results_dir: Path,
        window_size: int = 6,
    ) -> List[Dict[str, str]]:
        """Reconstruct completed (interviewer_question, interviewee_answer) pairs from conversation."""
        messages = cls.load_messages(results_dir)
        pairs: List[Dict[str, str]] = []

        last_question: Optional[str] = None
        for msg in messages:
            if msg.role == "interviewer":
                last_question = msg.content
            elif msg.role == "interviewee" and last_question is not None:
                pairs.append({
                    "interviewer": last_question,
                    "interviewee": msg.content,
                })

        if window_size > 0:
            return pairs[-window_size:]
        return pairs

    @classmethod
    def get_latest_question(cls, results_dir: Path) -> Optional[str]:
        """Return the most recent interviewer question recorded in the dialogue."""
        messages = cls.load_messages(results_dir)
        for msg in reversed(messages):
            if msg.role == "interviewer":
                return msg.content
        return None
