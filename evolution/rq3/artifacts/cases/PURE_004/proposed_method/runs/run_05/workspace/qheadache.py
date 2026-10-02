#!/usr/bin/env python3
import json
import os
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

APP_NAME = "Qheadache"
DATA_DIR = Path.home() / ".qheadache"
PROFILES_DIR = DATA_DIR / "profiles"
DEFAULT_PROFILE = "player1"

PUZZLES = {
    "1": {
        "name": "Simple Slide",
        "description": "Move A to the right edge, then place B and C as shown.",
        "strict_sequence": False,
        "board_size": (4, 4),
        "goal": {"A": (3, 0), "B": (1, 1), "C": (2, 2)},
        "start": {"A": (0, 0), "B": (1, 1), "C": (2, 2)},
        "blocks": ["A", "B", "C"],
    },
    "2": {
        "name": "Strict Order",
        "description": "Follow the order A then B then C. This level is strict.",
        "strict_sequence": True,
        "sequence": ["A", "B", "C"],
        "board_size": (4, 4),
        "goal": {"A": (3, 0), "B": (3, 1), "C": (3, 2)},
        "start": {"A": (0, 0), "B": (0, 1), "C": (0, 2)},
        "blocks": ["A", "B", "C"],
    },
}


@dataclass
class Attempt:
    puzzle_id: str
    start_time: float
    end_time: Optional[float] = None
    moves: int = 0
    score: int = 0
    completed: bool = False
    undo_used: bool = False
    abandoned: bool = False
    valid_for_best: bool = True
    current_state: Optional[Dict[str, Tuple[int, int]]] = None


@dataclass
class ProfileData:
    name: str
    completed: Dict[str, Dict[str, object]]
    active_attempt: Optional[Dict[str, object]] = None


class Game:
    def __init__(self, profile_name: str):
        self.profile_name = profile_name
        self.profile_path = PROFILES_DIR / f"{profile_name}.json"
        self.profile = self.load_profile()
        self.attempt: Optional[Attempt] = self.restore_attempt()
        self.current_puzzle_id: Optional[str] = None
        if self.attempt:
            self.current_puzzle_id = self.attempt.puzzle_id

    def load_profile(self) -> ProfileData:
        PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        if self.profile_path.exists():
            with self.profile_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return ProfileData(name=data["name"], completed=data.get("completed", {}), active_attempt=data.get("active_attempt"))
        return ProfileData(name=self.profile_name, completed={})

    def save_profile(self) -> None:
        tmp = self.profile_path.with_suffix(".json.tmp")
        payload = asdict(self.profile)
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        tmp.replace(self.profile_path)

    def restore_attempt(self) -> Optional[Attempt]:
        a = self.profile.active_attempt
        if not a:
            return None
        return Attempt(**a)

    def save_attempt(self) -> None:
        self.profile.active_attempt = asdict(self.attempt) if self.attempt else None
        self.save_profile()

    def start_puzzle(self, puzzle_id: str) -> None:
        self.current_puzzle_id = puzzle_id
        puzzle = PUZZLES[puzzle_id]
        self.attempt = Attempt(puzzle_id=puzzle_id, start_time=time.time(), current_state=dict(puzzle["start"]))
        self.save_attempt()

    def restart(self) -> None:
        if self.current_puzzle_id:
            self.start_puzzle(self.current_puzzle_id)

    def current_state(self) -> Dict[str, Tuple[int, int]]:
        if self.attempt and self.attempt.current_state:
            return {k: tuple(v) for k, v in self.attempt.current_state.items()}
        return dict(PUZZLES[self.current_puzzle_id]["start"]) if self.current_puzzle_id else {}

    def board_str(self) -> str:
        pid = self.current_puzzle_id
        puzzle = PUZZLES[pid]
        w, h = puzzle["board_size"]
        grid = [["." for _ in range(w)] for _ in range(h)]
        for block, (x, y) in self.current_state().items():
            grid[y][x] = block
        return "\n".join(" ".join(row) for row in grid)

    def move(self, block: str, dx: int, dy: int) -> str:
        puzzle = PUZZLES[self.current_puzzle_id]
        state = self.current_state()
        if block not in state:
            return "Illegal move: unknown block."
        x, y = state[block]
        nx, ny = x + dx, y + dy
        w, h = puzzle["board_size"]
        if not (0 <= nx < w and 0 <= ny < h):
            return "Illegal move: outside board."
        if any(pos == (nx, ny) for b, pos in state.items() if b != block):
            return "Illegal move: blocked by another block."
        if puzzle.get("strict_sequence"):
            expected = puzzle["sequence"][min(self.attempt.moves, len(puzzle["sequence"]) - 1)]
            if block != expected:
                return f"Illegal move: strict sequence requires {expected}."
        state[block] = (nx, ny)
        self.attempt.current_state = state
        self.attempt.moves += 1
        self.attempt.score += 10
        self.save_attempt()
        if self.is_completed(state):
            return self.complete_attempt()
        return "Move accepted."

    def is_completed(self, state: Dict[str, Tuple[int, int]]) -> bool:
        goal = PUZZLES[self.current_puzzle_id]["goal"]
        return all(tuple(state.get(k, (-1, -1))) == tuple(v) for k, v in goal.items())

    def complete_attempt(self) -> str:
        self.attempt.completed = True
        self.attempt.end_time = time.time()
        self.attempt.valid_for_best = not self.attempt.abandoned
        result = {
            "time": round(self.attempt.end_time - self.attempt.start_time, 2),
            "moves": self.attempt.moves,
            "score": self.attempt.score,
            "undo_used": self.attempt.undo_used,
        }
        if self.attempt.valid_for_best:
            self.profile.completed.setdefault(self.current_puzzle_id, {})
            best = self.profile.completed[self.current_puzzle_id]
            if not best or result["time"] < best.get("best_time", float("inf")):
                best["best_time"] = result["time"]
            if not best or result["moves"] < best.get("fewest_moves", 10**9):
                best["fewest_moves"] = result["moves"]
            best["last_result"] = result
        self.profile.active_attempt = None
        self.attempt = None
        self.save_profile()
        return "Puzzle completed!"

    def show_results(self) -> str:
        lines = [f"Profile: {self.profile.name}"]
        if not self.profile.completed:
            lines.append("No completed puzzles yet.")
        for pid, rec in self.profile.completed.items():
            lines.append(f"Puzzle {pid} ({PUZZLES[pid]['name']}): best time={rec.get('best_time')}, fewest moves={rec.get('fewest_moves')}")
        return "\n".join(lines)


def main() -> int:
    profile = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PROFILE
    game = Game(profile)
    print(APP_NAME)
    while True:
        if not game.current_puzzle_id:
            print("\nMenu: [1] Simple Slide [2] Strict Order [R] Results [Q] Quit")
            choice = input("> ").strip().lower()
            if choice in PUZZLES:
                game.start_puzzle(choice)
                continue
            if choice == "r":
                print(game.show_results())
                continue
            if choice == "q":
                return 0
            continue
        print(f"\nPuzzle {game.current_puzzle_id}: {PUZZLES[game.current_puzzle_id]['name']}")
        print(game.board_str())
        print("Commands: move BLOCK DX DY | restart | results | menu | quit")
        cmd = input("> ").strip().split()
        if not cmd:
            continue
        if cmd[0] == "quit":
            return 0
        if cmd[0] == "menu":
            game.current_puzzle_id = None
            game.save_attempt()
            continue
        if cmd[0] == "results":
            print(game.show_results())
            continue
        if cmd[0] == "restart":
            game.restart()
            continue
        if cmd[0] == "move" and len(cmd) == 4:
            try:
                print(game.move(cmd[1], int(cmd[2]), int(cmd[3])))
            except ValueError:
                print("Invalid move command.")
            continue
        print("Unknown command.")


if __name__ == "__main__":
    raise SystemExit(main())
