#!/usr/bin/env python3
import json
import os
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

APP_NAME = "Qheadache"
SAVE_DIR = Path.home() / ".qheadache"
PROFILE_FILE = SAVE_DIR / "profiles.json"

PUZZLES = [
    {
        "id": "easy-1",
        "name": "First Push",
        "grid": [
            "#####",
            "#.@ #",
            "# $ #",
            "# . #",
            "#####",
        ],
    },
    {
        "id": "easy-2",
        "name": "Two Blocks",
        "grid": [
            "######",
            "#.@  #",
            "# $$ #",
            "# .. #",
            "######",
        ],
    },
]


def now() -> float:
    return time.time()


def clamp_score(moves: int, seconds: float) -> int:
    return max(0, 1000 - moves * 10 - int(seconds))


@dataclass
class Attempt:
    puzzle_id: str
    started_at: float
    moves: int = 0
    undo_used: bool = False
    completed: bool = False
    finished_at: Optional[float] = None
    invalidated: bool = False

    def elapsed(self) -> float:
        end = self.finished_at or now()
        return max(0.0, end - self.started_at)


@dataclass
class ProfileData:
    name: str
    best_times: Dict[str, float]
    best_moves: Dict[str, int]
    history: List[dict]
    current_attempt: Optional[dict]


def ensure_save_dir():
    SAVE_DIR.mkdir(parents=True, exist_ok=True)


def load_profiles() -> Dict[str, ProfileData]:
    if not PROFILE_FILE.exists():
        return {}
    try:
        raw = json.loads(PROFILE_FILE.read_text())
        out = {}
        for name, pdata in raw.items():
            out[name] = ProfileData(
                name=name,
                best_times=pdata.get("best_times", {}),
                best_moves=pdata.get("best_moves", {}),
                history=pdata.get("history", []),
                current_attempt=pdata.get("current_attempt"),
            )
        return out
    except Exception:
        return {}


def save_profiles(profiles: Dict[str, ProfileData]) -> bool:
    try:
        ensure_save_dir()
        tmp = PROFILE_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps({k: asdict(v) for k, v in profiles.items()}, indent=2))
        tmp.replace(PROFILE_FILE)
        return True
    except Exception:
        return False


def parse_grid(grid: List[str]):
    walls = set()
    goals = set()
    boxes = set()
    player = None
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == '#':
                walls.add((x, y))
            elif ch == '.':
                goals.add((x, y))
            elif ch == '$':
                boxes.add((x, y))
            elif ch == '@':
                player = (x, y)
            elif ch == '*':
                goals.add((x, y)); boxes.add((x, y))
            elif ch == '+':
                goals.add((x, y)); player = (x, y)
    return walls, goals, boxes, player


def render(grid: List[str], player, boxes, goals):
    rows = [list(r) for r in grid]
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if (x, y) in walls_global:
                row[x] = '#'
            else:
                row[x] = ' '
    for x, y in goals:
        rows[y][x] = '.'
    for x, y in boxes:
        rows[y][x] = '*' if (x, y) in goals else '$'
    px, py = player
    rows[py][px] = '+' if (px, py) in goals else '@'
    return "\n".join("".join(r) for r in rows)


def is_completed(boxes, goals):
    return boxes == goals or goals.issuperset(boxes) and len(boxes) == len(goals) and all(b in goals for b in boxes)


def move_state(player, boxes, walls, goals, direction):
    dx, dy = direction
    nx, ny = player[0] + dx, player[1] + dy
    if (nx, ny) in walls:
        return None
    if (nx, ny) in boxes:
        bx, by = nx + dx, ny + dy
        if (bx, by) in walls or (bx, by) in boxes:
            return None
        new_boxes = set(boxes)
        new_boxes.remove((nx, ny))
        new_boxes.add((bx, by))
        return (nx, ny), new_boxes
    return (nx, ny), set(boxes)


def select_profile(profiles):
    print(APP_NAME)
    print("Profiles:")
    names = list(profiles.keys()) or ["Player1"]
    for i, n in enumerate(names, 1):
        print(f"  {i}. {n}")
    print("  N. New profile")
    choice = input("Select profile: ").strip().lower()
    if choice == 'n' or not profiles:
        name = input("Enter new profile name: ").strip() or "Player1"
        profiles.setdefault(name, ProfileData(name=name, best_times={}, best_moves={}, history=[], current_attempt=None))
        return name
    try:
        return names[int(choice) - 1]
    except Exception:
        return names[0]


def main():
    profiles = load_profiles()
    profile_name = select_profile(profiles)
    profile = profiles[profile_name]
    while True:
        print("\nMain menu: [P]lay [R]esults [Q]uit")
        cmd = input("> ").strip().lower()
        if cmd == 'q':
            save_profiles(profiles)
            return 0
        if cmd == 'r':
            print("Results:")
            for pid, t in profile.best_times.items():
                print(f"  {pid}: best time {t:.1f}s, best moves {profile.best_moves.get(pid, '-')}")
            continue
        if cmd != 'p':
            continue
        for puzzle in PUZZLES:
            play_puzzle(profile, puzzle)
        save_profiles(profiles)


def play_puzzle(profile, puzzle):
    global walls_global
    walls, goals, boxes, player = parse_grid(puzzle['grid'])
    walls_global = walls
    attempt = Attempt(puzzle_id=puzzle['id'], started_at=now())
    print(f"\nPuzzle: {puzzle['name']}")
    print("Use W A S D to move, U undo, R restart, C continue, M menu")
    if profile.current_attempt and profile.current_attempt.get('puzzle_id') == puzzle['id']:
        at = profile.current_attempt
        attempt.moves = at.get('moves', 0)
        attempt.undo_used = at.get('undo_used', False)
    move_history = []
    while True:
        print(render(puzzle['grid'], player, boxes, goals))
        print(f"Moves: {attempt.moves} Time: {attempt.elapsed():.1f}s Score: {clamp_score(attempt.moves, attempt.elapsed())}")
        if is_completed(boxes, goals):
            attempt.completed = True
            attempt.finished_at = now()
            sec = attempt.elapsed()
            profile.history.append({
                'puzzle_id': puzzle['id'],
                'completed': True,
                'moves': attempt.moves,
                'seconds': sec,
                'undo_used': attempt.undo_used,
            })
            best_t = profile.best_times.get(puzzle['id'])
            best_m = profile.best_moves.get(puzzle['id'])
            if best_t is None or sec < best_t:
                profile.best_times[puzzle['id']] = sec
            if best_m is None or attempt.moves < best_m:
                profile.best_moves[puzzle['id']] = attempt.moves
            profile.current_attempt = None
            print("Completed!")
            return
        key = input("Move: ").strip().lower()
        if key == 'm':
            profile.current_attempt = {'puzzle_id': puzzle['id'], 'moves': attempt.moves, 'undo_used': attempt.undo_used}
            return
        if key == 'r':
            profile.history.append({'puzzle_id': puzzle['id'], 'completed': False, 'abandoned': True, 'moves': attempt.moves, 'seconds': attempt.elapsed(), 'undo_used': attempt.undo_used})
            return play_puzzle(profile, puzzle)
        if key == 'u' and move_history:
            player, boxes = move_history.pop()
            attempt.undo_used = True
            continue
        dir_map = {'w': (0, -1), 's': (0, 1), 'a': (-1, 0), 'd': (1, 0)}
        if key not in dir_map:
            continue
        res = move_state(player, boxes, walls, goals, dir_map[key])
        if res is None:
            continue
        move_history.append((player, set(boxes)))
        player, boxes = res
        attempt.moves += 1


if __name__ == '__main__':
    raise SystemExit(main())
