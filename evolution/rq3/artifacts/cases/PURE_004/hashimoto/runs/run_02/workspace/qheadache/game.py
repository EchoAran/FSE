from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

APP_DIR = Path(os.environ.get("QHEADACHE_DATA_DIR", Path.home() / ".qheadache"))
CONFIG_FILE = APP_DIR / "config.json"
RESULTS_FILE = APP_DIR / "results.json"
ARCHIVE_FILE = APP_DIR / "archive.json"

DEFAULT_CONFIG = {
    "board_width": 4,
    "board_height": 4,
    "difficulty": "normal",
    "beginner_levels": ["easy"],
    "advanced_levels": ["normal", "hard"],
    "puzzles": [
        {"id": "easy", "title": "Swap the blocks", "type": "swap", "size": 4},
        {"id": "normal", "title": "Reverse the row", "type": "reverse", "size": 4},
        {"id": "hard", "title": "Sort numbers", "type": "sort", "size": 5},
    ],
}


def ensure_storage():
    APP_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")
    for p in (RESULTS_FILE, ARCHIVE_FILE):
        if not p.exists():
            p.write_text(json.dumps([], indent=2), encoding="utf-8")


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


@dataclass
class Result:
    puzzle_id: str
    time_seconds: float
    actions: int
    score: int
    completed: bool
    timestamp: float


class Store:
    def __init__(self):
        ensure_storage()

    def config(self) -> Dict[str, Any]:
        return load_json(CONFIG_FILE, DEFAULT_CONFIG)

    def save_config(self, config: Dict[str, Any]):
        save_json(CONFIG_FILE, config)

    def results(self) -> List[Dict[str, Any]]:
        return load_json(RESULTS_FILE, [])

    def archive(self) -> List[Dict[str, Any]]:
        return load_json(ARCHIVE_FILE, [])

    def add_result(self, result: Result):
        results = self.results()
        results.append(asdict(result))
        save_json(RESULTS_FILE, results)

    def clear_results(self):
        save_json(RESULTS_FILE, [])

    def archive_results(self):
        archived = self.archive()
        archived.extend(self.results())
        save_json(ARCHIVE_FILE, archived)
        self.clear_results()


class Puzzle:
    def __init__(self, puzzle_def: Dict[str, Any]):
        self.defn = puzzle_def
        size = puzzle_def["size"]
        if puzzle_def["type"] == "swap":
            self.start = [2, 1] + list(range(3, size + 1))
            self.goal = [1, 2] + list(range(3, size + 1))
        elif puzzle_def["type"] == "reverse":
            self.start = list(range(1, size + 1))
            self.goal = list(reversed(self.start))
        else:
            self.start = [3, 1, 2] + list(range(4, size + 1))
            self.goal = list(range(1, size + 1))

    def solved(self, state: List[int]) -> bool:
        return state == self.goal

    def move(self, state: List[int], action: str) -> List[int]:
        new_state = state[:]
        if self.defn["type"] == "swap" and action in ("1", "2"):
            i = int(action) - 1
            j = 1 - i
            new_state[i], new_state[j] = new_state[j], new_state[i]
        elif self.defn["type"] == "reverse" and action == "r":
            new_state = list(reversed(new_state))
        elif self.defn["type"] == "sort" and action == "s":
            new_state = sorted(new_state)
        return new_state


def score_for(time_seconds: float, actions: int, solved: bool) -> int:
    if not solved:
        return 0
    base = 1000
    penalty = int(time_seconds * 5) + actions * 10
    return max(100, base - penalty)


def choose_puzzle(config: Dict[str, Any]) -> Dict[str, Any]:
    level = input("Choose level (beginner/advanced): ").strip().lower() or "beginner"
    available = config["beginner_levels"] if level.startswith("b") else config["advanced_levels"]
    puzzles = [p for p in config["puzzles"] if p["id"] in available]
    print("Available puzzles:")
    for idx, p in enumerate(puzzles, 1):
        print(f"{idx}. {p['title']} ({p['id']})")
    choice = int(input("Select puzzle number: ").strip())
    return puzzles[choice - 1]


def play(store: Store):
    config = store.config()
    puzzle_def = choose_puzzle(config)
    puzzle = Puzzle(puzzle_def)
    state = puzzle.start[:]
    actions = 0
    start = time.time()
    print(f"Board: {state}")
    print("Enter actions: for swap use 1 or 2; for reverse use r; for sort use s; q to quit")
    while True:
        if puzzle.solved(state):
            break
        action = input("> ").strip().lower()
        if action == "q":
            break
        new_state = puzzle.move(state, action)
        if new_state != state:
            actions += 1
            state = new_state
        print(f"Board: {state}")
    elapsed = time.time() - start
    solved = puzzle.solved(state)
    score = score_for(elapsed, actions, solved)
    result = Result(puzzle_id=puzzle_def["id"], time_seconds=round(elapsed, 2), actions=actions, score=score, completed=solved, timestamp=time.time())
    store.add_result(result)
    print("Solved!" if solved else "Not solved.")
    print(f"Time: {result.time_seconds}s Actions: {actions} Score: {score}")


def admin(store: Store):
    config = store.config()
    print("Admin menu: 1) Show config 2) Set board size 3) Set difficulty 4) Control beginner puzzles 5) Show results 6) Clear results 7) Archive results 8) Save and exit")
    dirty = False
    while True:
        choice = input("admin> ").strip()
        if choice == "1":
            print(json.dumps(config, indent=2))
        elif choice == "2":
            config["board_width"] = int(input("Width: "))
            config["board_height"] = int(input("Height: "))
            dirty = True
        elif choice == "3":
            config["difficulty"] = input("Difficulty: ").strip()
            dirty = True
        elif choice == "4":
            raw = input("Beginner puzzle ids comma-separated: ")
            config["beginner_levels"] = [x.strip() for x in raw.split(",") if x.strip()]
            dirty = True
        elif choice == "5":
            print(json.dumps(store.results(), indent=2))
        elif choice == "6":
            store.clear_results()
            print("Results cleared")
        elif choice == "7":
            store.archive_results()
            print("Results archived")
        elif choice == "8":
            if dirty:
                store.save_config(config)
            print("Saved")
            return


def main():
    store = Store()
    while True:
        cmd = input("Qheadache: (p)lay, (a)dmin, (r)eport, (q)uit > ").strip().lower()
        if cmd == "p":
            play(store)
        elif cmd == "a":
            admin(store)
        elif cmd == "r":
            print(json.dumps(store.results(), indent=2))
        elif cmd == "q":
            return


if __name__ == "__main__":
    main()
