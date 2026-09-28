"""Per-turn token usage accounting for method LLM calls in interview runs."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class TokenUsage:
    """Cumulative token counters for a method's LLM calls within one run."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    def to_dict(self) -> Dict[str, int]:
        """Serialize token counters to a plain dictionary."""
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenUsage":
        """Rebuild token counters from a dictionary representation."""
        return cls(
            prompt_tokens=int(data["prompt_tokens"]),
            completion_tokens=int(data["completion_tokens"]),
            total_tokens=int(data["total_tokens"]),
        )

    def __add__(self, other: "TokenUsage") -> "TokenUsage":
        return TokenUsage(
            prompt_tokens=self.prompt_tokens + other.prompt_tokens,
            completion_tokens=self.completion_tokens + other.completion_tokens,
            total_tokens=self.total_tokens + other.total_tokens,
        )

    def __sub__(self, other: "TokenUsage") -> "TokenUsage":
        return TokenUsage(
            prompt_tokens=self.prompt_tokens - other.prompt_tokens,
            completion_tokens=self.completion_tokens - other.completion_tokens,
            total_tokens=self.total_tokens - other.total_tokens,
        )


class TokenUsageLog:
    """Appends and reads per-turn method token usage records in tokens.jsonl."""

    FILENAME = "tokens.jsonl"

    @classmethod
    def get_path(cls, results_dir: Path) -> Path:
        """Return the path to tokens.jsonl in the results directory."""
        return results_dir / cls.FILENAME

    @classmethod
    def load(cls, results_dir: Path) -> List[Dict[str, Any]]:
        """Load recorded per-turn token usage rows from tokens.jsonl."""
        path = cls.get_path(results_dir)
        if not path.is_file():
            return []

        records: List[Dict[str, Any]] = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    records.append(json.loads(stripped))
        return records

    @classmethod
    def sync(cls, results_dir: Path, turn_count: int, cumulative: TokenUsage) -> None:
        """Ensure tokens.jsonl holds one row per completed turn, deriving each row's delta from the running total."""
        records = cls.load(results_dir)
        accounted = TokenUsage(0, 0, 0)
        for record in records:
            accounted = accounted + TokenUsage.from_dict(record)

        while len(records) < turn_count + 1:
            turn_index = len(records)
            delta = cumulative - accounted
            row = {
                "turn_index": turn_index,
                "phase": "initialization" if turn_index == 0 else "dialogue",
                **delta.to_dict(),
            }
            cls._append(results_dir, row)
            records.append(row)
            accounted = accounted + delta

    @classmethod
    def _append(cls, results_dir: Path, row: Dict[str, Any]) -> None:
        """Append a single token usage row to tokens.jsonl."""
        results_dir.mkdir(parents=True, exist_ok=True)
        path = cls.get_path(results_dir)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")