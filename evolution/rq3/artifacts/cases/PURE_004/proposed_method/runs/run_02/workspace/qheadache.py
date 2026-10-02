#!/usr/bin/env python3
import json
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

APP_NAME = "Qheadache"
DATA_DIR = Path.home() / ".qheadache"
PROFILES_DIR = DATA_DIR / "profiles"
DEFAULT_PROFILE = "player"

MOVE_DELTAS = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}

PUZZLES = {
    "1": {
        "name": "Starter",
        "width": 4,
        "height": 4,
        "board": [
            ["A", "A", ".", "."],
            ["B", ".", ".", "."],
            ["B", ".", "C", "C"],
            [".", ".", ".", "."],
        ],
        "goal": [
            [".", ".", ".", "."],
            [".", ".", ".", "."],
            [".", ".", "C", "C"],
            ["A", "A", "B", "B"],
        ],
    },
    "2": {
        "name": "Route",
        "width": 4,
        "height": 4,
        "board": [
            ["D", "D", ".", "."],
            [".", "E", "E", "."],
            [".", ".", ".", "."],
            [".", ".", "F", "F"],
        ],
        "goal": [
            [".", ".", ".", "."],
            ["D", "D", ".", "."],
            [".", "E", "E", "."],
            [".", ".", "F", "F"],
        ],
    },
}


def now_ts() -> float:
    return time.time()


def ensure_dirs() -> None:
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)


def board_to_key(board: List[List[str]]) -> str:
    return "\n".join("".join(row) for row in board)


def clone_board(board: List[List[str]]) -> List[List[str]]:
    return [row[:] for row in board]


def serialize_attempt(attempt: Dict) -> Dict:
    data = dict(attempt)
    data["board"] = attempt["board"]
    data["goal"] = attempt["goal"]
    return data


def load_json(path: Path, default):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except Exception:
        return default


def atomic_write_json(path: Path, payload: Dict) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        os.replace(tmp, path)
        return True
    except Exception:
        return False


@dataclass
class Attempt:
    profile: str
    puzzle_id: str
    board: List[List[str]]
    goal: List[List[str]]
    started_at: float = field(default_factory=now_ts)
    moves: int = 0
    rejected: int = 0
    score: int = 0
    undo_used: bool = False
    completed: bool = False
    strict_sequence: bool = False
    sequence_index: int = 0
    history: List[Dict] = field(default_factory=list)
    resumed: bool = False

    def puzzle_name(self) -> str:
        return PUZZLES[self.puzzle_id]["name"]

    def board_text(self) -> str:
        lines = []
        for row in self.board:
            lines.append(" ".join(cell if cell != "." else "." for cell in row))
        return "\n".join(lines)

    def elapsed(self) -> int:
        return int(now_ts() - self.started_at)

    def goal_reached(self) -> bool:
        return self.board == self.goal

    def legal_positions(self, piece: str) -> List[Tuple[int, int]]:
        positions = []
        for r, row in enumerate(self.board):
            for c, cell in enumerate(row):
                if cell == piece:
                    positions.append((r, c))
        return positions

    def move_piece(self, piece: str, direction: str) -> Tuple[bool, str]:
        if direction not in MOVE_DELTAS:
            return False, "Unknown direction."
        positions = self.legal_positions(piece)
        if not positions:
            return False, "That block does not exist."
        dr, dc = MOVE_DELTAS[direction]
        target_positions = [(r + dr, c + dc) for r, c in positions]
        h = len(self.board)
        w = len(self.board[0])
        for r, c in target_positions:
            if r < 0 or c < 0 or r >= h or c >= w:
                return False, "Illegal move: outside board."
            occupant = self.board[r][c]
            if occupant not in (".", piece):
                return False, "Illegal move: another block is in the way."
        self.history.append({"board": clone_board(self.board), "moves": self.moves, "score": self.score, "undo_used": self.undo_used, "sequence_index": self.sequence_index})
        new_board = clone_board(self.board)
        for r, c in positions:
            new_board[r][c] = "."
        for r, c in target_positions:
            new_board[r][c] = piece
        self.board = new_board
        self.moves += 1
        self.score = max(0, 1000 - self.moves * 10 - self.elapsed())
        return True, "Moved."

    def undo(self) -> Tuple[bool, str]:
        if not self.history:
            return False, "Nothing to undo."
        prev = self.history.pop()
        self.board = prev["board"]
        self.moves = prev["moves"]
        self.score = prev["score"]
        self.undo_used = True
        self.sequence_index = prev["sequence_index"]
        return True, "Undone."


class ProfileStore:
    def __init__(self, name: str):
        self.name = name
        self.path = PROFILES_DIR / f"{name}.json"
        self.data = load_json(self.path, {
            "name": name,
            "settings": {"font_size": "normal"},
            "progress": {},
            "results": [],
        })

    def save(self) -> bool:
        return atomic_write_json(self.path, self.data)

    def get_progress(self, puzzle_id: str):
        return self.data.get("progress", {}).get(puzzle_id)

    def set_progress(self, puzzle_id: str, attempt: Attempt):
        self.data.setdefault("progress", {})[puzzle_id] = {
            "profile": attempt.profile,
            "puzzle_id": attempt.puzzle_id,
            "board": attempt.board,
            "goal": attempt.goal,
            "started_at": attempt.started_at,
            "moves": attempt.moves,
            "rejected": attempt.rejected,
            "score": attempt.score,
            "undo_used": attempt.undo_used,
            "completed": attempt.completed,
            "strict_sequence": attempt.strict_sequence,
            "sequence_index": attempt.sequence_index,
            "resumed": attempt.resumed,
        }

    def clear_progress(self, puzzle_id: str):
        self.data.get("progress", {}).pop(puzzle_id, None)

    def add_result(self, result: Dict):
        self.data.setdefault("results", []).append(result)


def print_board(attempt: Attempt):
    print(f"\nPuzzle: {attempt.puzzle_name()} | Moves: {attempt.moves} | Time: {attempt.elapsed()}s | Score: {attempt.score}")
    print(attempt.board_text())


def available_pieces(board: List[List[str]]) -> List[str]:
    pieces = sorted({cell for row in board for cell in row if cell != "."})
    return pieces


def complete_attempt(store: ProfileStore, attempt: Attempt):
    attempt.completed = True
    result = {
        "puzzle_id": attempt.puzzle_id,
        "puzzle_name": attempt.puzzle_name(),
        "completed_at": now_ts(),
        "time_seconds": attempt.elapsed(),
        "moves": attempt.moves,
        "score": attempt.score,
        "undo_used": attempt.undo_used,
        "resumed": attempt.resumed,
    }
    store.add_result(result)
    store.clear_progress(attempt.puzzle_id)
    if not store.save():
        print("Warning: could not save results locally.")
    print("\nPuzzle completed!")
    print(json.dumps(result, indent=2))


def start_attempt(profile: str, puzzle_id: str, resumed: bool = False) -> Attempt:
    puzzle = PUZZLES[puzzle_id]
    return Attempt(profile=profile, puzzle_id=puzzle_id, board=clone_board(puzzle["board"]), goal=clone_board(puzzle["goal"]), resumed=resumed)


def restore_attempt(profile: str, puzzle_id: str, payload: Dict) -> Optional[Attempt]:
    try:
        puzzle = PUZZLES[puzzle_id]
        attempt = Attempt(
            profile=profile,
            puzzle_id=puzzle_id,
            board=payload["board"],
            goal=payload.get("goal", clone_board(puzzle["goal"])),
            started_at=payload.get("started_at", now_ts()),
            moves=payload.get("moves", 0),
            rejected=payload.get("rejected", 0),
            score=payload.get("score", 0),
            undo_used=payload.get("undo_used", False),
            completed=payload.get("completed", False),
            strict_sequence=payload.get("strict_sequence", False),
            sequence_index=payload.get("sequence_index", 0),
            resumed=True,
        )
        if attempt.board != puzzle["board"] and attempt.goal != puzzle["goal"]:
            return attempt
        return attempt
    except Exception:
        return None


def help_text():
    print("Commands:")
    print("  puzzles               List puzzles")
    print("  start <id>            Start a puzzle")
    print("  resume <id>           Resume saved progress for a puzzle")
    print("  move <piece> <dir>    Move a block: up/down/left/right")
    print("  undo                  Undo the last move")
    print("  board                 Show the board")
    print("  save                  Save current progress locally")
    print("  results               Show saved results")
    print("  profiles              List profiles")
    print("  switch <name>         Switch profile")
    print("  restart               Restart current puzzle")
    print("  quit                  Exit")


def main():
    ensure_dirs()
    profile_name = os.environ.get("QHEADACHE_PROFILE", DEFAULT_PROFILE)
    store = ProfileStore(profile_name)
    current: Optional[Attempt] = None
    print(APP_NAME)
    print(f"Profile: {profile_name}")
    print("Type 'help' for commands.")
    while True:
        try:
            raw = input("> ").strip()
        except EOFError:
            print()
            break
        if not raw:
            continue
        parts = raw.split()
        cmd = parts[0].lower()
        args = parts[1:]
        if cmd == "help":
            help_text()
        elif cmd == "puzzles":
            for pid, p in PUZZLES.items():
                print(f"{pid}: {p['name']}")
        elif cmd == "start" and args:
            pid = args[0]
            if pid not in PUZZLES:
                print("Unknown puzzle.")
                continue
            current = start_attempt(store.name, pid)
            print_board(current)
        elif cmd == "resume" and args:
            pid = args[0]
            saved = store.get_progress(pid)
            if not saved:
                print("No saved progress for that puzzle.")
                continue
            current = restore_attempt(store.name, pid, saved)
            if current is None:
                print("Could not restore progress.")
                continue
            print("Resumed saved progress.")
            print_board(current)
        elif cmd == "board" and current:
            print_board(current)
        elif cmd == "move" and current and len(args) == 2:
            ok, msg = current.move_piece(args[0], args[1].lower())
            if not ok:
                current.rejected += 1
                print(msg)
            else:
                print(msg)
                if current.goal_reached():
                    complete_attempt(store, current)
                    current = None
                else:
                    if not store.get_progress(current.puzzle_id) and not store.save():
                        print("Warning: progress could not be saved.")
        elif cmd == "undo" and current:
            ok, msg = current.undo()
            print(msg)
        elif cmd == "save" and current:
            store.set_progress(current.puzzle_id, current)
            if store.save():
                print("Progress saved.")
            else:
                print("Could not save progress.")
        elif cmd == "results":
            for r in store.data.get("results", []):
                print(json.dumps(r, indent=2))
            if not store.data.get("results"):
                print("No results yet.")
        elif cmd == "profiles":
            profiles = sorted(p.stem for p in PROFILES_DIR.glob("*.json"))
            print("Profiles:")
            for p in profiles:
                print(f"  {p}")
        elif cmd == "switch" and args:
            profile_name = args[0]
            store = ProfileStore(profile_name)
            current = None
            print(f"Switched to profile {profile_name}.")
        elif cmd == "restart" and current:
            current = start_attempt(store.name, current.puzzle_id)
            print("Restarted current puzzle.")
            print_board(current)
        elif cmd == "quit":
            if current:
                store.set_progress(current.puzzle_id, current)
                store.save()
            break
        else:
            print("Unknown command or missing puzzle.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
