#!/usr/bin/env python3
import argparse
import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Tuple

APP_DIR = Path.home() / '.qheadache'
PROFILES_DIR = APP_DIR / 'profiles'

MOVE_DELTAS = {
    'w': (-1, 0),
    's': (1, 0),
    'a': (0, -1),
    'd': (0, 1),
}

LEVELS = [
    {
        'name': 'Starter 1',
        'description': 'Move the block onto the goal.',
        'grid': [
            '#####',
            '#P.G#',
            '#...#',
            '#####',
        ],
        'strict_sequence': None,
    },
    {
        'name': 'Starter 2',
        'description': 'Two blocks need to be arranged on goals.',
        'grid': [
            '######',
            '#P.BG#',
            '#..G.#',
            '######',
        ],
        'strict_sequence': ['d', 'd', 's'],
    },
]

@dataclass
class AttemptResult:
    level_name: str
    completed: bool
    moves: int
    time_seconds: int
    score: int
    undo_used: bool = False
    strict_sequence_used: bool = False


def ensure_dirs():
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)


def profile_path(profile: str) -> Path:
    safe = ''.join(c for c in profile if c.isalnum() or c in ('-', '_')) or 'default'
    return PROFILES_DIR / f'{safe}.json'


def load_profile(profile: str) -> dict:
    ensure_dirs()
    path = profile_path(profile)
    if not path.exists():
        return {'profile': profile, 'results': [], 'settings': {}}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {'profile': profile, 'results': [], 'settings': {}, 'corrupted': True}


def save_profile(profile: str, data: dict) -> bool:
    ensure_dirs()
    path = profile_path(profile)
    tmp = path.with_suffix('.json.tmp')
    try:
        tmp.write_text(json.dumps(data, indent=2, sort_keys=True))
        os.replace(tmp, path)
        return True
    except OSError:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass
        return False


def parse_grid(grid: List[str]):
    walls = set()
    goals = set()
    blocks = set()
    player = None
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == '#':
                walls.add((r, c))
            elif ch == 'G':
                goals.add((r, c))
            elif ch == 'B':
                blocks.add((r, c))
            elif ch == 'P':
                player = (r, c)
    return walls, goals, blocks, player


def render(grid: List[str], player, blocks, goals):
    out = []
    for r, row in enumerate(grid):
        chars = []
        for c, ch in enumerate(row):
            pos = (r, c)
            if pos == player:
                chars.append('@')
            elif pos in blocks:
                chars.append('O')
            elif pos in goals:
                chars.append('*')
            elif ch == '#':
                chars.append('#')
            else:
                chars.append('.')
        out.append(''.join(chars))
    return '\n'.join(out)


def is_completed(blocks, goals):
    return goals.issubset(blocks) and len(blocks) == len(goals)


def score_for(moves: int, time_seconds: int) -> int:
    return max(0, 1000 - moves * 10 - time_seconds)


def play_level(level: dict) -> AttemptResult:
    grid = level['grid']
    walls, goals, blocks, player = parse_grid(grid)
    moves = 0
    time_seconds = 0
    strict = level.get('strict_sequence')
    strict_used = False
    strict_idx = 0
    print(level['name'])
    print(level['description'])
    if strict:
        print('This level requires a strict move sequence.')
    while True:
        print(render(grid, player, blocks, goals))
        if is_completed(blocks, goals):
            print('Puzzle completed!')
            return AttemptResult(level['name'], True, moves, time_seconds, score_for(moves, time_seconds), strict_sequence_used=strict_used)
        cmd = input('Move (WASD, r=restart, q=quit): ').strip().lower()
        time_seconds += 1
        if cmd == 'q':
            return AttemptResult(level['name'], False, moves, time_seconds, 0)
        if cmd == 'r':
            return AttemptResult(level['name'], False, moves, time_seconds, 0)
        if cmd not in MOVE_DELTAS:
            print('Invalid input.')
            continue
        if strict:
            expected = strict[strict_idx] if strict_idx < len(strict) else None
            if expected is not None and cmd != expected:
                print('That move would break the required sequence.')
                continue
            strict_idx += 1
            strict_used = True
        dr, dc = MOVE_DELTAS[cmd]
        nr, nc = player[0] + dr, player[1] + dc
        dest = (nr, nc)
        if dest in walls:
            print('Illegal move.')
            continue
        if dest in blocks:
            beyond = (nr + dr, nc + dc)
            if beyond in walls or beyond in blocks:
                print('Illegal move.')
                continue
            blocks.remove(dest)
            blocks.add(beyond)
            player = dest
            moves += 1
            continue
        player = dest
        moves += 1


def cmd_list(args):
    for i, lvl in enumerate(LEVELS, 1):
        print(f'{i}. {lvl["name"]} - {lvl["description"]}')


def cmd_play(args):
    profile = load_profile(args.profile)
    level = LEVELS[args.level - 1]
    result = play_level(level)
    if result.completed:
        profile.setdefault('results', []).append(asdict(result))
        ok = save_profile(args.profile, profile)
        if ok:
            print('Result saved locally.')
        else:
            print('Save unavailable; result not stored.')
    else:
        print('Attempt ended without completion.')


def cmd_results(args):
    profile = load_profile(args.profile)
    results = profile.get('results', [])
    if not results:
        print('No completed results yet.')
        return
    for r in results:
        extra = []
        if r.get('undo_used'):
            extra.append('undo used')
        if r.get('strict_sequence_used'):
            extra.append('strict sequence')
        suffix = f" ({', '.join(extra)})" if extra else ''
        print(f"{r['level_name']}: moves={r['moves']} time={r['time_seconds']} score={r['score']}{suffix}")


def main():
    parser = argparse.ArgumentParser(prog='qheadache', description='Qheadache puzzle game')
    parser.add_argument('--profile', default='default', help='Profile name')
    sub = parser.add_subparsers(dest='cmd', required=True)
    sub.add_parser('list')
    p = sub.add_parser('play')
    p.add_argument('level', type=int, nargs='?', default=1)
    sub.add_parser('results')
    args = parser.parse_args()
    if args.cmd == 'list':
        cmd_list(args)
    elif args.cmd == 'play':
        cmd_play(args)
    elif args.cmd == 'results':
        cmd_results(args)

if __name__ == '__main__':
    main()
