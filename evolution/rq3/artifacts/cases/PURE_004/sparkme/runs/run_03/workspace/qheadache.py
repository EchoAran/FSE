#!/usr/bin/env python3
import json
import os
import random
import shutil
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path

SAVE_DIR = Path.home() / '.qheadache'
SAVE_FILE = SAVE_DIR / 'save.json'
EXPORT_FILE = SAVE_DIR / 'stats_export.json'


def now():
    return int(time.time())


def safe_int(v, default=0):
    try:
        return int(v)
    except Exception:
        return default


def board_to_str(board):
    return '\n'.join(' '.join(row) for row in board)


def solved_board(size):
    nums = [str(i) for i in range(1, size * size)] + [' ']
    return [nums[i:i+size] for i in range(0, len(nums), size)]


def serialize_board(board):
    return [''.join(cell if cell != ' ' else '_' for cell in row) for row in board]


def deserialize_board(rows):
    return [[ch if ch != '_' else ' ' for ch in row] for row in rows]


def find_blank(board):
    for r, row in enumerate(board):
        for c, v in enumerate(row):
            if v == ' ':
                return r, c
    return None


def is_solved(board):
    return board == solved_board(len(board))


def neighbors(size, r, c):
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < size and 0 <= nc < size:
            yield nr, nc


def shuffle_board(size):
    board = solved_board(size)
    blank = (size - 1, size - 1)
    prev = None
    for _ in range(size * size * 20):
        opts = list(neighbors(size, *blank))
        if prev in opts and len(opts) > 1:
            opts.remove(prev)
        nxt = random.choice(opts)
        br, bc = blank
        nr, nc = nxt
        board[br][bc], board[nr][nc] = board[nr][nc], board[br][bc]
        prev, blank = blank, nxt
    return board


@dataclass
class Session:
    size: int
    board: list
    initial_board: list
    move_count: int = 0
    completed: bool = False
    started_at: int = 0
    updated_at: int = 0
    history: list = None
    message: str = ''

    def __post_init__(self):
        self.history = self.history or []


def load_state():
    if not SAVE_FILE.exists():
        return None, None
    try:
        data = json.loads(SAVE_FILE.read_text())
        if not isinstance(data, dict):
            raise ValueError('bad save')
        session = data.get('session')
        stats = data.get('stats', {})
        if not session or 'board' not in session:
            raise ValueError('missing session')
        s = Session(
            size=safe_int(session.get('size'), 3),
            board=deserialize_board(session['board']),
            initial_board=deserialize_board(session.get('initial_board', session['board'])),
            move_count=safe_int(session.get('move_count'), 0),
            completed=bool(session.get('completed', False)),
            started_at=safe_int(session.get('started_at'), now()),
            updated_at=safe_int(session.get('updated_at'), now()),
            history=session.get('history', []),
            message='Recovered last safe state.' if session.get('interrupted') else '',
        )
        return s, stats
    except Exception:
        bad = SAVE_FILE.with_suffix('.corrupt.json')
        try:
            shutil.move(str(SAVE_FILE), str(bad))
        except Exception:
            pass
        return None, {'warning': 'Save data was unreadable and was quarantined.'}


def save_state(session, stats, interrupted=False, allow_fail_message=True):
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        'session': {
            'size': session.size,
            'board': serialize_board(session.board),
            'initial_board': serialize_board(session.initial_board),
            'move_count': session.move_count,
            'completed': session.completed,
            'started_at': session.started_at,
            'updated_at': now(),
            'history': session.history[-100:],
            'interrupted': interrupted,
        },
        'stats': stats,
    }
    tmp = SAVE_FILE.with_suffix('.tmp')
    try:
        tmp.write_text(json.dumps(payload, indent=2))
        tmp.replace(SAVE_FILE)
        return True, 'Saved.'
    except Exception as e:
        if allow_fail_message:
            return False, f'Save failed: {e}'
        return False, ''


def default_stats():
    return {
        'puzzles_completed': 0,
        'sessions_started': 0,
        'best_moves': None,
        'best_time': None,
        'completed_records': [],
        'last_export': None,
    }


def merge_stats(stats):
    base = default_stats()
    base.update(stats or {})
    return base


def export_stats(stats, include_records=False):
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        'puzzles_completed': stats['puzzles_completed'],
        'sessions_started': stats['sessions_started'],
        'best_moves': stats['best_moves'],
        'best_time': stats['best_time'],
        'exported_at': now(),
    }
    if include_records:
        data['completed_records'] = stats.get('completed_records', [])
    EXPORT_FILE.write_text(json.dumps(data, indent=2))
    return EXPORT_FILE


def show_progress(stats, session=None):
    print('\n== Progress ==')
    print(f"Puzzles completed: {stats['puzzles_completed']}")
    if session:
        elapsed = max(0, now() - session.started_at)
        print(f'Current time on active puzzle: {elapsed}s')
        print(f'Moves made: {session.move_count}')
    print(f"Best moves: {stats['best_moves'] if stats['best_moves'] is not None else 'n/a'}")
    print(f"Best time: {stats['best_time'] if stats['best_time'] is not None else 'n/a'}")


def print_help():
    print('\nCommands:')
    print('  swap r1 c1 r2 c2   swap adjacent tiles using 1-based coordinates')
    print('  undo               undo last move')
    print('  restart            restart puzzle')
    print('  hint               show a subtle hint')
    print('  progress           show progress/stats')
    print('  export             export stats to a local JSON file')
    print('  quit               save and exit')


def main():
    stats = default_stats()
    session, loaded_stats = load_state()
    stats = merge_stats(loaded_stats if loaded_stats else stats)
    if session is None:
        session = Session(size=3, board=shuffle_board(3), initial_board=[], started_at=now())
        session.initial_board = [row[:] for row in session.board]
        stats['sessions_started'] += 1
        save_state(session, stats)
        print('New puzzle started.')
    else:
        print(session.message or 'Loaded saved puzzle.')
    print('Qheadache - lightweight sliding puzzle')
    print_help()

    while True:
        print('\n' + board_to_str(session.board))
        if is_solved(session.board) and not session.completed:
            session.completed = True
            stats['puzzles_completed'] += 1
            duration = now() - session.started_at
            if stats['best_moves'] is None or session.move_count < stats['best_moves']:
                stats['best_moves'] = session.move_count
            if stats['best_time'] is None or duration < stats['best_time']:
                stats['best_time'] = duration
            stats['completed_records'].append({'moves': session.move_count, 'time': duration, 'at': now()})
            msg = f'Puzzle solved in {session.move_count} moves and {duration}s.'
            ok, save_msg = save_state(session, stats)
            print(msg)
            print(save_msg)
            print('Type restart for a new puzzle or quit to exit.')

        cmd = input('\n> ').strip().lower()
        if not cmd:
            continue
        if cmd == 'quit':
            ok, msg = save_state(session, stats, interrupted=True)
            print(msg if ok else 'Unable to save before exit.')
            return 0
        if cmd == 'progress':
            show_progress(stats, session)
            continue
        if cmd == 'export':
            try:
                path = export_stats(stats, include_records=False)
                stats['last_export'] = str(path)
                save_state(session, stats)
                print(f'Stats exported successfully to {path}')
            except Exception as e:
                print(f'Export failed: {e}. The game will keep running.')
            continue
        if cmd == 'hint':
            br, bc = find_blank(session.board)
            options = list(neighbors(session.size, br, bc))
            r, c = options[0]
            print(f'Hint: a tile next to the blank at row {r+1}, col {c+1} can move.')
            continue
        if cmd == 'restart':
            session.board = [row[:] for row in session.initial_board]
            session.move_count = 0
            session.completed = False
            session.started_at = now()
            session.history = []
            print('Puzzle restarted.')
            save_state(session, stats)
            continue
        if cmd == 'undo':
            if not session.history:
                print('Nothing to undo.')
                continue
            session.board = session.history.pop()
            session.move_count = max(0, session.move_count - 1)
            print('Move undone.')
            save_state(session, stats)
            continue
        parts = cmd.split()
        if parts and parts[0] == 'swap' and len(parts) == 5:
            try:
                r1, c1, r2, c2 = map(lambda x: safe_int(x) - 1, parts[1:])
                if any(v < 0 or v >= session.size for v in [r1, c1, r2, c2]):
                    raise ValueError
                if abs(r1 - r2) + abs(c1 - c2) != 1:
                    print('Invalid move: tiles must be adjacent.')
                    continue
                session.history.append([row[:] for row in session.board])
                session.board[r1][c1], session.board[r2][c2] = session.board[r2][c2], session.board[r1][c1]
                session.move_count += 1
                session.completed = False
                ok, msg = save_state(session, stats)
                if not ok:
                    print(msg)
                else:
                    print('Move accepted.')
            except Exception:
                print('Invalid move syntax. Use: swap r1 c1 r2 c2')
            continue
        print('Unknown command. Type help?')


if __name__ == '__main__':
    raise SystemExit(main())
