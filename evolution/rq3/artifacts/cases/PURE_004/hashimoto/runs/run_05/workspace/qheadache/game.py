from __future__ import annotations

import json
import os
import shutil
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Tuple, Optional

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
STATE_FILE = DATA_DIR / "state.json"
ARCHIVE_FILE = DATA_DIR / "archive.jsonl"

DEFAULT_STATE = {
    "pending_config": None,
    "active_config": {
        "board_width": 5,
        "board_height": 5,
        "start": [0, 0],
        "goal": [4, 4],
        "blocks": [[1, 1], [1, 2], [2, 1]],
        "beginner_puzzles": ["default"],
        "advanced_puzzles": ["default"],
        "difficulty": "normal",
        "small_settings": {"sound": True},
    },
    "players": {},
    "results": [],
}


def ensure_data_dir():
    DATA_DIR.mkdir(exist_ok=True)


def load_state():
    ensure_data_dir()
    if not STATE_FILE.exists():
        save_state(DEFAULT_STATE)
    with STATE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    ensure_data_dir()
    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)


def archive_record(record):
    ensure_data_dir()
    with ARCHIVE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def apply_pending_config(state):
    pending = state.get("pending_config")
    if pending:
        active = state["active_config"]
        for key, value in pending.items():
            if key == "small_settings":
                active.setdefault("small_settings", {}).update(value)
            else:
                active[key] = value
        state["pending_config"] = None


def board_repr(width, height, player, goal, blocks):
    out = []
    for y in range(height):
        row = []
        for x in range(width):
            pos = [x, y]
            if pos == player:
                row.append("P")
            elif pos == goal:
                row.append("G")
            elif pos in blocks:
                row.append("#")
            else:
                row.append(".")
        out.append(" ".join(row))
    return "\n".join(out)


def play(player_name: str):
    state = load_state()
    apply_pending_config(state)
    save_state(state)
    cfg = state["active_config"]
    player = cfg["start"][:]
    goal = cfg["goal"][:]
    blocks = [b[:] for b in cfg["blocks"]]
    width = cfg["board_width"]
    height = cfg["board_height"]
    actions = 0
    start = time.time()
    print("Qheadache - puzzle game")
    print("Enter moves with WASD, q to quit.")
    while True:
        print(board_repr(width, height, player, goal, blocks))
        if player == goal:
            elapsed = round(time.time() - start, 2)
            score = max(0, 1000 - actions * 10 - int(elapsed * 5))
            record = {
                "player": player_name,
                "time_seconds": elapsed,
                "actions": actions,
                "score": score,
                "won": True,
                "timestamp": time.time(),
            }
            state["results"].append(record)
            state.setdefault("players", {}).setdefault(player_name, {"plays": 0, "best_score": None})
            state["players"][player_name]["plays"] += 1
            best = state["players"][player_name]["best_score"]
            state["players"][player_name]["best_score"] = score if best is None else max(best, score)
            save_state(state)
            archive_record(record)
            print(f"Solved! time={elapsed}s actions={actions} score={score}")
            return 0
        cmd = input("move> ").strip().lower()
        if cmd == "q":
            print("Quit. Progress saved.")
            return 0
        dx, dy = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}.get(cmd, (0, 0))
        if (dx, dy) == (0, 0):
            print("Invalid move")
            continue
        nx, ny = player[0] + dx, player[1] + dy
        if not (0 <= nx < width and 0 <= ny < height):
            print("Blocked by wall")
            continue
        if [nx, ny] in blocks:
            print("Blocked by block")
            continue
        player = [nx, ny]
        actions += 1


def admin(args: List[str]):
    state = load_state()
    if not args:
        print(json.dumps(state, indent=2))
        return 0
    cmd = args[0]
    if cmd == "set-board" and len(args) == 3:
        w, h = int(args[1]), int(args[2])
        state["pending_config"] = state.get("pending_config") or {}
        state["pending_config"].update({"board_width": w, "board_height": h})
    elif cmd == "set-goal" and len(args) == 3:
        x, y = int(args[1]), int(args[2])
        state["pending_config"] = state.get("pending_config") or {}
        state["pending_config"].update({"goal": [x, y]})
    elif cmd == "set-start" and len(args) == 3:
        x, y = int(args[1]), int(args[2])
        state["pending_config"] = state.get("pending_config") or {}
        state["pending_config"].update({"start": [x, y]})
    elif cmd == "set-blocks":
        blocks = []
        for item in args[1:]:
            x, y = item.split(",")
            blocks.append([int(x), int(y)])
        state["pending_config"] = state.get("pending_config") or {}
        state["pending_config"].update({"blocks": blocks})
    elif cmd == "set-difficulty" and len(args) == 2:
        state["active_config"]["difficulty"] = args[1]
    elif cmd == "show-results":
        print(json.dumps(state["results"], indent=2))
        return 0
    elif cmd == "clear-results":
        state["results"] = []
        state["players"] = {}
    elif cmd == "archive-results":
        for r in state["results"]:
            archive_record(r)
        state["results"] = []
        state["players"] = {}
    else:
        print("Unknown admin command")
        return 1
    save_state(state)
    print("Admin update saved; changes marked for next start if applicable.")
    return 0


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: qheadache play <name> | admin <command> ...")
        return 1
    if argv[0] == "play":
        return play(argv[1] if len(argv) > 1 else "player")
    if argv[0] == "admin":
        return admin(argv[1:])
    print("Unknown mode")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
