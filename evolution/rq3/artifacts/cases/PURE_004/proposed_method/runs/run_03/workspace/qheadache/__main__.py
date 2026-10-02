from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from qheadache.game import Game, SaveError


def render_board(state, width, height):
    grid = [["." for _ in range(width)] for _ in range(height)]
    for block, (x, y) in state.items():
        if block.startswith("__"):
            continue
        grid[y][x] = block
    return "\n".join(" ".join(row) for row in grid)


def main():
    parser = argparse.ArgumentParser(prog="qheadache")
    parser.add_argument("--data-dir", default=str(Path.home() / ".qheadache"))
    args = parser.parse_args()

    game = Game(Path(args.data_dir))
    print("Qheadache")
    profile = input("Profile name: ").strip() or "default"
    data = game.load_profile(profile)
    if data.get("attempt"):
        resume = input("Resume existing attempt? [y/N] ").strip().lower() == "y"
        attempt = data["attempt"] if resume else game.new_attempt(data["attempt"]["puzzle_id"])
    else:
        print("Available puzzles:")
        for pid, puzzle in game.puzzles.items():
            print(f"  {pid}: {puzzle.name}")
        puzzle_id = input("Select puzzle: ").strip() or "p1"
        attempt = game.new_attempt(puzzle_id)

    while True:
        puzzle = game.puzzles[attempt["puzzle_id"]]
        print("\nBoard:\n" + render_board(attempt["state"], puzzle.width, puzzle.height))
        print(f"Moves: {attempt['attempt_stats']['moves']}  Time: {attempt['attempt_stats']['time_seconds']}  Score: {attempt['attempt_stats']['score']}")
        if puzzle.strict_sequence:
            print(f"Strict order: {' -> '.join(puzzle.strict_sequence)}")
        cmd = input("Command (move A up/down/left/right, restart, save, results, quit): ").strip().lower()
        if cmd == "quit":
            data = game.finish_attempt(data, attempt)
            game.save_profile(profile, data)
            print("Saved.")
            return
        if cmd == "results":
            print(json.dumps(data.get("results", []), indent=2))
            continue
        if cmd == "restart":
            attempt = game.restart_attempt(attempt)
            continue
        if cmd == "save":
            data = game.finish_attempt(data, attempt)
            game.save_profile(profile, data)
            print("Saved.")
            continue
        parts = cmd.split()
        if len(parts) != 3 or parts[0] != "move":
            print("Unknown command.")
            continue
        block = parts[1].upper()
        dirs = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
        if parts[2] not in dirs:
            print("Use up, down, left, or right.")
            continue
        ok, msg = game.apply_move(attempt, block, *dirs[parts[2]])
        print(msg)
        if ok and attempt["attempt_stats"]["completed"]:
            data = game.finish_attempt(data, attempt)
            game.save_profile(profile, data)
            print("Completed and saved.")
            return


if __name__ == "__main__":
    main()
