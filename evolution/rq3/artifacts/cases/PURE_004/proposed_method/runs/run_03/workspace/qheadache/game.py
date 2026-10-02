from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

BOARD_WIDTH = 5
BOARD_HEIGHT = 5
SAVE_VERSION = 1


@dataclass
class Puzzle:
    puzzle_id: str
    name: str
    width: int
    height: int
    blocks: Dict[str, Tuple[int, int]]
    goal: Dict[str, Tuple[int, int]]
    strict_sequence: Optional[List[str]] = None


@dataclass
class AttemptStats:
    moves: int = 0
    time_seconds: int = 0
    score: int = 0
    undo_used: bool = False
    completed: bool = False
    abandoned: bool = False


class SaveError(Exception):
    pass


class Game:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.profiles_dir = data_dir / "profiles"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.puzzles = self._load_puzzles()

    def _load_puzzles(self) -> Dict[str, Puzzle]:
        return {
            "p1": Puzzle(
                puzzle_id="p1",
                name="Warm-up",
                width=BOARD_WIDTH,
                height=BOARD_HEIGHT,
                blocks={"A": (0, 0), "B": (2, 0), "C": (4, 4)},
                goal={"A": (1, 1), "B": (3, 0), "C": (4, 3)},
            ),
            "p2": Puzzle(
                puzzle_id="p2",
                name="Sequence",
                width=BOARD_WIDTH,
                height=BOARD_HEIGHT,
                blocks={"A": (0, 4), "B": (1, 4)},
                goal={"A": (3, 4), "B": (4, 4)},
                strict_sequence=["A", "B"],
            ),
        }

    def profile_path(self, profile: str) -> Path:
        return self.profiles_dir / f"{profile}.json"

    def list_profiles(self) -> List[str]:
        return sorted(p.stem for p in self.profiles_dir.glob("*.json"))

    def load_profile(self, profile: str) -> dict:
        path = self.profile_path(profile)
        if not path.exists():
            return {"profile": profile, "results": [], "attempt": None}
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def save_profile(self, profile: str, payload: dict) -> None:
        path = self.profile_path(profile)
        tmp = path.with_suffix(".json.tmp")
        with tmp.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
        os.replace(tmp, path)

    def new_attempt(self, puzzle_id: str) -> dict:
        puzzle = self.puzzles[puzzle_id]
        return {
            "puzzle_id": puzzle_id,
            "state": {k: list(v) for k, v in puzzle.blocks.items()},
            "initial_state": {k: list(v) for k, v in puzzle.blocks.items()},
            "attempt_stats": asdict(AttemptStats()),
            "history": [],
            "sequence_index": 0,
        }

    def is_goal(self, puzzle_id: str, state: Dict[str, List[int]]) -> bool:
        puzzle = self.puzzles[puzzle_id]
        return all(tuple(state[b]) == goal for b, goal in puzzle.goal.items())

    def legal_move(self, puzzle_id: str, state: Dict[str, List[int]], block: str, dx: int, dy: int) -> Tuple[bool, str]:
        puzzle = self.puzzles[puzzle_id]
        if block not in state:
            return False, "Unknown block."
        if abs(dx) + abs(dy) != 1:
            return False, "Moves must be one step up, down, left, or right."
        x, y = state[block]
        nx, ny = x + dx, y + dy
        if not (0 <= nx < puzzle.width and 0 <= ny < puzzle.height):
            return False, "That move leaves the board."
        occupied = {k: tuple(v) for k, v in state.items() if k != block}
        if (nx, ny) in occupied.values():
            return False, "That space is already occupied."
        if puzzle.strict_sequence:
            expected = puzzle.strict_sequence[min(len(puzzle.strict_sequence) - 1, self._sequence_index(state))]
            if block != expected:
                return False, f"This level requires moving {expected} next."
        return True, "OK"

    def _sequence_index(self, state: Dict[str, List[int]]) -> int:
        return int(state.get("__seq", 0)) if isinstance(state.get("__seq", 0), int) else 0

    def apply_move(self, attempt: dict, block: str, dx: int, dy: int) -> Tuple[bool, str]:
        puzzle_id = attempt["puzzle_id"]
        state = attempt["state"]
        ok, msg = self.legal_move(puzzle_id, state, block, dx, dy)
        if not ok:
            return False, msg
        attempt["history"].append({"block": block, "dx": dx, "dy": dy})
        x, y = state[block]
        state[block] = [x + dx, y + dy]
        attempt["attempt_stats"]["moves"] += 1
        if self.puzzles[puzzle_id].strict_sequence:
            idx = attempt["sequence_index"]
            if idx < len(self.puzzles[puzzle_id].strict_sequence) and block == self.puzzles[puzzle_id].strict_sequence[idx]:
                attempt["sequence_index"] += 1
        if self.is_goal(puzzle_id, state):
            attempt["attempt_stats"]["completed"] = True
            attempt["attempt_stats"]["score"] = max(0, 1000 - attempt["attempt_stats"]["moves"] * 10 - attempt["attempt_stats"]["time_seconds"])
            return True, "Puzzle completed!"
        return True, "Move accepted."

    def restart_attempt(self, attempt: dict) -> dict:
        attempt["attempt_stats"]["abandoned"] = True
        return self.new_attempt(attempt["puzzle_id"])

    def finish_attempt(self, profile_data: dict, attempt: dict) -> dict:
        stats = attempt["attempt_stats"]
        if stats["completed"]:
            result = {
                "puzzle_id": attempt["puzzle_id"],
                "moves": stats["moves"],
                "time_seconds": stats["time_seconds"],
                "score": stats["score"],
                "undo_used": stats["undo_used"],
            }
            profile_data["results"].append(result)
        profile_data["attempt"] = attempt
        return profile_data
