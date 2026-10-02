from __future__ import annotations

import json
import os
import random
import shutil
import sys
import tempfile
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple, Optional

APP_DIR = Path.home() / ".qheadache"
SAVE_PATH = APP_DIR / "save.json"
EXPORT_DIR = APP_DIR / "exports"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass
class Puzzle:
    width: int
    height: int
    target: Tuple[int, int]
    player: Tuple[int, int]
    obstacles: List[Tuple[int, int]] = field(default_factory=list)
    solved: bool = False

    def clone(self) -> "Puzzle":
        return Puzzle(self.width, self.height, self.target, self.player, list(self.obstacles), self.solved)

    def to_dict(self):
        d = asdict(self)
        d["target"] = list(self.target)
        d["player"] = list(self.player)
        d["obstacles"] = [list(x) for x in self.obstacles]
        return d

    @classmethod
    def from_dict(cls, d):
        return cls(
            width=d["width"],
            height=d["height"],
            target=tuple(d["target"]),
            player=tuple(d["player"]),
            obstacles=[tuple(x) for x in d.get("obstacles", [])],
            solved=d.get("solved", False),
        )

    def in_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def blocked(self, pos):
        return pos in self.obstacles

    def valid_move(self, dest):
        if not self.in_bounds(dest):
            return False, "Move is outside the board."
        if self.blocked(dest):
            return False, "That square is blocked."
        px, py = self.player
        dx = abs(dest[0] - px)
        dy = abs(dest[1] - py)
        if dx + dy != 1:
            return False, "You can only move one step at a time."
        return True, ""

    def move(self, dest):
        ok, msg = self.valid_move(dest)
        if not ok:
            return False, msg
        self.player = dest
        self.solved = self.player == self.target
        return True, "Solved!" if self.solved else "Moved."


@dataclass
class Session:
    puzzle: Puzzle
    moves: int = 0
    started_at: str = field(default_factory=now_iso)
    finished_at: Optional[str] = None
    completed: bool = False
    history: List[Tuple[int, int]] = field(default_factory=list)
    undo_stack: List[Tuple[int, int]] = field(default_factory=list)
    score: int = 0
    hint_used: bool = False

    def to_dict(self):
        d = asdict(self)
        d["puzzle"] = self.puzzle.to_dict()
        d["history"] = [list(x) for x in self.history]
        d["undo_stack"] = [list(x) for x in self.undo_stack]
        return d

    @classmethod
    def from_dict(cls, d):
        return cls(
            puzzle=Puzzle.from_dict(d["puzzle"]),
            moves=d.get("moves", 0),
            started_at=d.get("started_at", now_iso()),
            finished_at=d.get("finished_at"),
            completed=d.get("completed", False),
            history=[tuple(x) for x in d.get("history", [])],
            undo_stack=[tuple(x) for x in d.get("undo_stack", [])],
            score=d.get("score", 0),
            hint_used=d.get("hint_used", False),
        )


class Store:
    def __init__(self, save_path: Path = SAVE_PATH):
        self.save_path = save_path
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
        EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    def load(self) -> Optional[Session]:
        if not self.save_path.exists():
            return None
        try:
            data = json.loads(self.save_path.read_text())
            return Session.from_dict(data)
        except Exception:
            bad = self.save_path.with_suffix(".corrupt.json")
            try:
                shutil.move(str(self.save_path), str(bad))
            except Exception:
                pass
            return None

    def atomic_write(self, payload: dict):
        tmp = self.save_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, indent=2))
        os.replace(tmp, self.save_path)

    def save(self, session: Session):
        self.atomic_write(session.to_dict())

    def export_stats(self, session: Session, include_detail: bool = False) -> Path:
        EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"qheadache_stats_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        path = EXPORT_DIR / filename
        payload = {
            "exported_at": now_iso(),
            "moves": session.moves,
            "completed": session.completed,
            "score": session.score,
            "started_at": session.started_at,
        }
        if include_detail:
            payload["session"] = session.to_dict()
        path.write_text(json.dumps(payload, indent=2))
        return path


def make_new_session(seed: Optional[int] = None) -> Session:
    rng = random.Random(seed)
    width = 4
    height = 4
    target = (width - 1, height - 1)
    obstacles = [(1, 1), (2, 1)] if rng.random() < 0.5 else [(1, 2)]
    puzzle = Puzzle(width, height, target, (0, 0), obstacles)
    return Session(puzzle=puzzle)


def render(session: Session) -> str:
    p = session.puzzle
    rows = []
    for y in range(p.height):
        row = []
        for x in range(p.width):
            pos = (x, y)
            if pos == p.player:
                row.append("P")
            elif pos == p.target:
                row.append("T")
            elif pos in p.obstacles:
                row.append("#")
            else:
                row.append(".")
        rows.append(" ".join(row))
    return "\n".join(rows)


def score(session: Session) -> int:
    base = 100
    return max(0, base - session.moves * 5 - (10 if session.hint_used else 0))


def play_cli():
    store = Store()
    session = store.load() or make_new_session()
    if session.completed:
        session = make_new_session()
    print("Qheadache - a small offline puzzle game")
    print("Commands: w/a/s/d move, u undo, r restart, h hint, p progress, e export, q quit")
    while True:
        session.score = score(session)
        print("\n" + render(session))
        print(f"Moves: {session.moves} Score: {session.score} Time: {session.started_at}")
        cmd = input("> ").strip().lower()
        if cmd == "q":
            store.save(session)
            print("Saved progress. Goodbye.")
            return
        if cmd == "p":
            print(f"Progress: completed={session.completed} moves={session.moves} score={session.score}")
            continue
        if cmd == "e":
            try:
                path = store.export_stats(session)
                print(f"Stats exported successfully to {path}")
            except Exception as exc:
                print(f"Stats export failed: {exc}")
            continue
        if cmd == "h":
            session.hint_used = True
            px, py = session.puzzle.player
            tx, ty = session.puzzle.target
            hint = "move right" if tx > px else "move left" if tx < px else "move down" if ty > py else "move up"
            print(f"Hint: try to {hint}.")
            continue
        if cmd == "u":
            if session.undo_stack:
                session.puzzle.player = session.undo_stack.pop()
                session.moves = max(0, session.moves - 1)
                session.puzzle.solved = False
                print("Undone.")
            else:
                print("Nothing to undo.")
            continue
        if cmd == "r":
            session = make_new_session()
            print("Restarted.")
            continue
        moves = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
        if cmd in moves:
            dx, dy = moves[cmd]
            dest = (session.puzzle.player[0] + dx, session.puzzle.player[1] + dy)
            session.undo_stack.append(session.puzzle.player)
            ok, msg = session.puzzle.move(dest)
            if ok:
                session.moves += 1
                print(msg)
                store.save(session)
                if session.puzzle.solved:
                    session.completed = True
                    session.finished_at = now_iso()
                    session.score = score(session)
                    store.save(session)
                    print("Puzzle solved! Progress saved.")
                    return
            else:
                session.undo_stack.pop()
                print(f"Invalid move: {msg}")
            continue
        print("Unknown command.")


def main(argv=None):
    argv = argv or sys.argv[1:]
    if argv and argv[0] == "--export-demo":
        s = make_new_session()
        print(Store().export_stats(s))
        return 0
    play_cli()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
