#!/usr/bin/env python3
import argparse
import json
import os
import random
import shutil
import sys
import tempfile
import time
from dataclasses import dataclass, asdict
from pathlib import Path

APP_NAME = 'Qheadache'
SAVE_VERSION = 1
DEFAULT_SAVE_PATH = Path.home() / '.qheadache_save.json'
DEFAULT_EXPORT_PATH = Path.cwd() / 'qheadache_stats_export.json'


def now() -> float:
    return time.time()


class SaveError(Exception):
    pass


@dataclass
class PuzzleState:
    size: int = 3
    tiles: list = None
    moves: int = 0
    completed: bool = False
    started_at: float = 0.0
    last_safe_at: float = 0.0
    history: list = None
    undo_stack: list = None

    def __post_init__(self):
        if self.tiles is None:
            self.tiles = list(range(1, self.size * self.size)) + [0]
        if self.history is None:
            self.history = []
        if self.undo_stack is None:
            self.undo_stack = []
        if not self.started_at:
            self.started_at = now()
        if not self.last_safe_at:
            self.last_safe_at = self.started_at

    def clone(self):
        return PuzzleState(
            size=self.size,
            tiles=list(self.tiles),
            moves=self.moves,
            completed=self.completed,
            started_at=self.started_at,
            last_safe_at=self.last_safe_at,
            history=list(self.history),
            undo_stack=[list(x) for x in self.undo_stack],
        )

    def is_solved(self):
        return self.tiles == list(range(1, self.size * self.size)) + [0]

    def find_zero(self):
        return self.tiles.index(0)

    def legal_moves(self):
        z = self.find_zero()
        r, c = divmod(z, self.size)
        moves = {}
        if r > 0:
            moves['up'] = z - self.size
        if r < self.size - 1:
            moves['down'] = z + self.size
        if c > 0:
            moves['left'] = z - 1
        if c < self.size - 1:
            moves['right'] = z + 1
        return moves

    def apply_move(self, direction):
        moves = self.legal_moves()
        if direction not in moves:
            return False, f'Invalid move: cannot move {direction}.'
        self.undo_stack.append(list(self.tiles))
        swap_idx = moves[direction]
        z = self.find_zero()
        self.tiles[z], self.tiles[swap_idx] = self.tiles[swap_idx], self.tiles[z]
        self.moves += 1
        self.history.append({'action': 'move', 'direction': direction, 'ts': now()})
        return True, 'Moved.'

    def undo(self):
        if not self.undo_stack:
            return False, 'Nothing to undo.'
        self.tiles = self.undo_stack.pop()
        self.moves = max(0, self.moves - 1)
        self.history.append({'action': 'undo', 'ts': now()})
        return True, 'Undid last move.'


class Storage:
    def __init__(self, path: Path):
        self.path = path

    def load(self):
        if not self.path.exists():
            return None
        try:
            raw = self.path.read_text(encoding='utf-8')
            data = json.loads(raw)
            if data.get('version') != SAVE_VERSION:
                raise SaveError('Unsupported save version.')
            return data
        except Exception as e:
            quarantine = self.path.with_suffix(self.path.suffix + '.corrupt')
            try:
                shutil.copy2(self.path, quarantine)
            except Exception:
                pass
            raise SaveError(f'Could not read save file: {e}')

    def atomic_write(self, data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + '.tmp')
        tmp.write_text(json.dumps(data, indent=2, sort_keys=True), encoding='utf-8')
        os.replace(tmp, self.path)


class Game:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.data = self._fresh_data()
        self.pending_notice = None

    def _fresh_data(self):
        return {
            'version': SAVE_VERSION,
            'best_moves': None,
            'best_time': None,
            'completed': 0,
            'attempts': [],
            'current': PuzzleState(),
            'last_export': None,
            'last_update_check': None,
        }

    def load(self):
        try:
            loaded = self.storage.load()
        except SaveError as e:
            self.data = self._fresh_data()
            self.pending_notice = str(e)
            return
        if not loaded:
            return
        current = loaded.get('current') or {}
        state = PuzzleState(
            size=current.get('size', 3),
            tiles=current.get('tiles') or list(range(1, 9)) + [0],
            moves=current.get('moves', 0),
            completed=current.get('completed', False),
            started_at=current.get('started_at', now()),
            last_safe_at=current.get('last_safe_at', now()),
            history=current.get('history', []),
            undo_stack=current.get('undo_stack', []),
        )
        self.data = loaded
        self.data['current'] = state

    def save(self, safe_only=True):
        current = self.data['current']
        if safe_only:
            current.last_safe_at = now()
        serializable = dict(self.data)
        serializable['current'] = asdict(current)
        self.storage.atomic_write(serializable)

    def new_session(self, size=3):
        self.data['current'] = PuzzleState(size=size)
        self.pending_notice = 'Started a new session.'
        self.save()

    def restart(self):
        size = self.data['current'].size
        self.new_session(size=size)

    def move(self, direction):
        state = self.data['current']
        ok, msg = state.apply_move(direction)
        if not ok:
            return False, msg
        if state.is_solved():
            state.completed = True
            elapsed = max(0.0, now() - state.started_at)
            self.data['completed'] = int(self.data.get('completed', 0)) + 1
            self.data['attempts'].append({'moves': state.moves, 'elapsed': elapsed, 'completed': True, 'ts': now()})
            best_moves = self.data.get('best_moves')
            if best_moves is None or state.moves < best_moves:
                self.data['best_moves'] = state.moves
            best_time = self.data.get('best_time')
            if best_time is None or elapsed < best_time:
                self.data['best_time'] = elapsed
            self.pending_notice = 'Puzzle solved and progress saved.'
            self.save()
            return True, 'Solved!'
        self.save()
        return True, msg

    def undo(self):
        ok, msg = self.data['current'].undo()
        if ok:
            self.save()
        return ok, msg

    def stats(self):
        current = self.data['current']
        elapsed = now() - current.started_at
        return {
            'completed': self.data.get('completed', 0),
            'current_moves': current.moves,
            'current_time_seconds': round(elapsed, 2),
            'best_moves': self.data.get('best_moves'),
            'best_time_seconds': None if self.data.get('best_time') is None else round(self.data['best_time'], 2),
        }

    def export_stats(self, path: Path, include_details=False):
        payload = {
            'app': APP_NAME,
            'exported_at': now(),
            'basic_stats': self.stats(),
        }
        if include_details:
            payload['session_records'] = self.data.get('attempts', [])
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding='utf-8')
        self.data['last_export'] = str(path)
        self.save()
        return path


def print_board(state: PuzzleState):
    for r in range(state.size):
        row = []
        for c in range(state.size):
            v = state.tiles[r * state.size + c]
            row.append('  ' if v == 0 else f'{v:2d}')
        print(' '.join(row))


def main(argv=None):
    parser = argparse.ArgumentParser(prog='qheadache', description='Qheadache puzzle game')
    parser.add_argument('--save-file', default=str(DEFAULT_SAVE_PATH))
    parser.add_argument('--export-file', default=str(DEFAULT_EXPORT_PATH))
    sub = parser.add_subparsers(dest='cmd', required=True)
    sub.add_parser('start')
    sub.add_parser('show')
    mv = sub.add_parser('move')
    mv.add_argument('direction', choices=['up', 'down', 'left', 'right'])
    sub.add_parser('undo')
    sub.add_parser('restart')
    sub.add_parser('stats')
    ex = sub.add_parser('export')
    ex.add_argument('--details', action='store_true')
    sub.add_parser('recover')
    args = parser.parse_args(argv)

    storage = Storage(Path(args.save_file))
    game = Game(storage)
    game.load()
    if game.pending_notice:
        print(game.pending_notice)

    if args.cmd == 'start':
        game.new_session()
        print('New puzzle started.')
        print_board(game.data['current'])
        return 0
    if args.cmd == 'show':
        print_board(game.data['current'])
        return 0
    if args.cmd == 'move':
        ok, msg = game.move(args.direction)
        print(msg)
        print_board(game.data['current'])
        return 0 if ok else 1
    if args.cmd == 'undo':
        ok, msg = game.undo()
        print(msg)
        print_board(game.data['current'])
        return 0 if ok else 1
    if args.cmd == 'restart':
        game.restart()
        print('Restarted.')
        print_board(game.data['current'])
        return 0
    if args.cmd == 'stats':
        st = game.stats()
        for k, v in st.items():
            print(f'{k}: {v}')
        return 0
    if args.cmd == 'export':
        path = Path(args.export_file)
        try:
            out = game.export_stats(path, include_details=args.details)
        except Exception as e:
            print(f'Export failed: {e}')
            return 1
        print(f'Stats exported successfully to {out}')
        return 0
    if args.cmd == 'recover':
        game.load()
        print('Recovery complete. Game is available.')
        print_board(game.data['current'])
        return 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
