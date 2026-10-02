from __future__ import annotations

import json
import os
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

from flask import Flask, flash, redirect, render_template, request, url_for

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("QHEADACHE_DATA_DIR", APP_DIR / "data"))
DB_PATH = DATA_DIR / "qheadache.sqlite3"

DEFAULT_PUZZLES = [
    {
        "name": "Starter Cross",
        "rows": 3,
        "cols": 3,
        "goal": {"1": [0, 0], "2": [1, 0], "3": [2, 0], "4": [0, 1], "5": [1, 1], "6": [2, 1]},
        "start": {"1": [2, 2], "2": [1, 2], "3": [0, 2], "4": [2, 1], "5": [1, 1], "6": [0, 1]},
        "beginners": 1,
        "difficulty": 1,
    },
    {
        "name": "Tricky Shuffle",
        "rows": 4,
        "cols": 4,
        "goal": {"1": [0, 0], "2": [1, 0], "3": [2, 0], "4": [3, 0], "5": [0, 1], "6": [1, 1], "7": [2, 1], "8": [3, 1]},
        "start": {"1": [3, 3], "2": [2, 3], "3": [1, 3], "4": [0, 3], "5": [3, 2], "6": [2, 2], "7": [1, 2], "8": [0, 2]},
        "beginners": 0,
        "difficulty": 3,
    },
]

app = Flask(__name__)
app.secret_key = "qheadache-secret"


def connect() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS puzzles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                rows INTEGER NOT NULL,
                cols INTEGER NOT NULL,
                goal_json TEXT NOT NULL,
                start_json TEXT NOT NULL,
                beginners INTEGER NOT NULL DEFAULT 0,
                difficulty INTEGER NOT NULL DEFAULT 1,
                active INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT NOT NULL,
                puzzle_id INTEGER NOT NULL,
                moves INTEGER NOT NULL,
                elapsed_seconds REAL NOT NULL,
                score INTEGER NOT NULL,
                completed_at TEXT NOT NULL
            );
            """
        )
        cur = conn.execute("SELECT COUNT(*) AS c FROM puzzles")
        if cur.fetchone()["c"] == 0:
            for p in DEFAULT_PUZZLES:
                conn.execute(
                    "INSERT INTO puzzles (name, rows, cols, goal_json, start_json, beginners, difficulty, active) VALUES (?, ?, ?, ?, ?, ?, ?, 1)",
                    (
                        p["name"],
                        p["rows"],
                        p["cols"],
                        json.dumps(p["goal"]),
                        json.dumps(p["start"]),
                        p["beginners"],
                        p["difficulty"],
                    ),
                )
        defaults = {"beginner_mode": "1", "board_title": "Qheadache"}
        for k, v in defaults.items():
            conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))


@app.before_request
def _ensure_db() -> None:
    init_db()


def get_settings() -> Dict[str, str]:
    with connect() as conn:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
    return {r["key"]: r["value"] for r in rows}


def set_setting(key: str, value: str) -> None:
    with connect() as conn:
        conn.execute("REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))


def list_puzzles(admin_view: bool = False) -> List[sqlite3.Row]:
    with connect() as conn:
        if admin_view:
            return conn.execute("SELECT * FROM puzzles ORDER BY id").fetchall()
        settings = get_settings()
        beginner_mode = settings.get("beginner_mode", "1") == "1"
        if beginner_mode:
            return conn.execute("SELECT * FROM puzzles WHERE active = 1 AND beginners = 1 ORDER BY difficulty, id").fetchall()
        return conn.execute("SELECT * FROM puzzles WHERE active = 1 ORDER BY difficulty, id").fetchall()


def get_puzzle(puzzle_id: int) -> sqlite3.Row | None:
    with connect() as conn:
        return conn.execute("SELECT * FROM puzzles WHERE id = ?", (puzzle_id,)).fetchone()


def load_grid(puzzle: sqlite3.Row) -> Tuple[List[List[str]], Dict[str, List[int]], Dict[str, List[int]]]:
    start = json.loads(puzzle["start_json"])
    goal = json.loads(puzzle["goal_json"])
    grid = [["" for _ in range(puzzle["cols"])] for _ in range(puzzle["rows"])]
    for token, (x, y) in start.items():
        grid[y][x] = token
    return grid, start, goal


def is_solved(board: Dict[str, List[int]], goal: Dict[str, List[int]]) -> bool:
    return all(board.get(k) == v for k, v in goal.items())


@app.route("/")
def index():
    puzzles = list_puzzles()
    settings = get_settings()
    return render_template("index.html", puzzles=puzzles, settings=settings)


@app.route("/play/<int:puzzle_id>", methods=["GET", "POST"])
def play(puzzle_id: int):
    puzzle = get_puzzle(puzzle_id)
    if not puzzle:
        return "Puzzle not found", 404
    if request.method == "POST":
        data = request.form
        player = data.get("player", "Guest").strip() or "Guest"
        moves = int(data.get("moves", "0"))
        elapsed = float(data.get("elapsed", "0"))
        board = json.loads(data.get("board", "{}"))
        goal = json.loads(puzzle["goal_json"])
        if is_solved(board, goal):
            score = max(0, int(1000 - moves * 10 - elapsed))
            with connect() as conn:
                conn.execute(
                    "INSERT INTO progress (player, puzzle_id, moves, elapsed_seconds, score, completed_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (player, puzzle_id, moves, elapsed, score, time.strftime("%Y-%m-%d %H:%M:%S")),
                )
            flash("Puzzle solved! Progress saved.")
            return redirect(url_for("results"))
        flash("That board is not solved yet.")
    grid, start, goal = load_grid(puzzle)
    return render_template("play.html", puzzle=puzzle, grid=grid, start=start, goal=goal)


@app.route("/results")
def results():
    with connect() as conn:
        rows = conn.execute("SELECT * FROM progress ORDER BY id DESC").fetchall()
    return render_template("results.html", rows=rows)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "settings":
            set_setting("beginner_mode", "1" if request.form.get("beginner_mode") == "1" else "0")
            set_setting("board_title", request.form.get("board_title", "Qheadache"))
            flash("Settings updated.")
        elif action == "add_puzzle":
            name = request.form["name"]
            rows = int(request.form["rows"])
            cols = int(request.form["cols"])
            goal = json.loads(request.form["goal_json"])
            start = json.loads(request.form["start_json"])
            beginners = 1 if request.form.get("beginners") == "1" else 0
            difficulty = int(request.form.get("difficulty", "1"))
            with connect() as conn:
                conn.execute(
                    "INSERT INTO puzzles (name, rows, cols, goal_json, start_json, beginners, difficulty, active) VALUES (?, ?, ?, ?, ?, ?, ?, 1)",
                    (name, rows, cols, json.dumps(goal), json.dumps(start), beginners, difficulty),
                )
            flash("Puzzle added.")
        elif action == "toggle":
            pid = int(request.form["puzzle_id"])
            active = 0 if request.form.get("active") == "1" else 1
            with connect() as conn:
                conn.execute("UPDATE puzzles SET active = ? WHERE id = ?", (active, pid))
            flash("Puzzle updated.")
        elif action == "clear_progress":
            with connect() as conn:
                conn.execute("DELETE FROM progress")
            flash("Progress cleared.")
        elif action == "archive_progress":
            with connect() as conn:
                rows = conn.execute("SELECT * FROM progress").fetchall()
                archive = DATA_DIR / f"archive_{int(time.time())}.json"
                archive.write_text(json.dumps([dict(r) for r in rows], indent=2))
                conn.execute("DELETE FROM progress")
            flash(f"Progress archived to {archive.name}.")
        return redirect(url_for("admin"))
    puzzles = list_puzzles(admin_view=True)
    settings = get_settings()
    with connect() as conn:
        progress_count = conn.execute("SELECT COUNT(*) AS c FROM progress").fetchone()["c"]
    return render_template("admin.html", puzzles=puzzles, settings=settings, progress_count=progress_count)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000, debug=False)
