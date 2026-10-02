#!/usr/bin/env python3
import json
import os
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path

DATA_DIR = Path(__file__).with_name('qheadache_data')
CONFIG_FILE = DATA_DIR / 'config.json'
STATE_FILE = DATA_DIR / 'state.json'
ARCHIVE_FILE = DATA_DIR / 'archive.json'

DEFAULT_CONFIG = {
    'board_width': 5,
    'board_height': 5,
    'difficulty': 'normal',
    'beginner_puzzles': ['starter'],
    'advanced_puzzles': ['cross'],
    'selected_puzzle': 'starter',
    'admin_password': 'admin',
}

DEFAULT_STATE = {
    'players': {},
    'results': [],
    'archived_results': [],
}

PUZZLES = {
    'starter': {'start': 'A..\n...\n..B', 'goal': 'A..\n...\n..B'},
    'cross': {'start': 'AB.\n...\n...', 'goal': 'A.B\n...\n...'},
}


def ensure_data():
    DATA_DIR.mkdir(exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, indent=2))
    if not STATE_FILE.exists():
        STATE_FILE.write_text(json.dumps(DEFAULT_STATE, indent=2))
    if not ARCHIVE_FILE.exists():
        ARCHIVE_FILE.write_text(json.dumps([], indent=2))


def load_json(path, default):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def save_json(path, obj):
    path.write_text(json.dumps(obj, indent=2))


def render_board(board):
    print('\n'.join(' '.join(row) for row in board))


def parse_board(text):
    return [list(line) for line in text.splitlines()]


def board_to_text(board):
    return '\n'.join(''.join(row) for row in board)


def play(player, config, state):
    puzzle = PUZZLES[config['selected_puzzle']]
    board = parse_board(puzzle['start'])
    goal = puzzle['goal']
    start = time.time()
    actions = 0
    print(f"Welcome, {player}. Solve the puzzle by swapping adjacent blocks.")
    while True:
        print('\nCurrent board:')
        render_board(board)
        print("Enter move as 'r1 c1 r2 c2' (1-based), 'goal', or 'quit'.")
        cmd = input('> ').strip().lower()
        if cmd == 'quit':
            print('Game exited.')
            return
        if cmd == 'goal':
            print('Goal board:')
            render_board(parse_board(goal))
            continue
        parts = cmd.split()
        if len(parts) != 4 or not all(p.isdigit() for p in parts):
            print('Invalid move.')
            continue
        r1, c1, r2, c2 = (int(p) - 1 for p in parts)
        if not (0 <= r1 < len(board) and 0 <= r2 < len(board) and 0 <= c1 < len(board[0]) and 0 <= c2 < len(board[0])):
            print('Move out of bounds.')
            continue
        if abs(r1 - r2) + abs(c1 - c2) != 1:
            print('Blocks must be adjacent.')
            continue
        board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
        actions += 1
        if board_to_text(board) == goal:
            elapsed = round(time.time() - start, 2)
            score = max(0, 1000 - int(elapsed * 10) - actions * 5)
            result = {'player': player, 'time_seconds': elapsed, 'actions': actions, 'score': score, 'puzzle': config['selected_puzzle']}
            state['results'].append(result)
            state['players'][player] = {'last_score': score, 'last_time_seconds': elapsed}
            save_json(STATE_FILE, state)
            print('Puzzle solved!')
            print(json.dumps(result, indent=2))
            return


def admin(config, state):
    if input('Admin password: ').strip() != config['admin_password']:
        print('Access denied.')
        return
    while True:
        print('\nAdmin menu:')
        print('1. Select puzzle')
        print('2. Configure board')
        print('3. Set difficulty')
        print('4. Show results')
        print('5. Clear results')
        print('6. Archive results')
        print('7. Exit')
        choice = input('> ').strip()
        if choice == '1':
            print('Available puzzles:', ', '.join(PUZZLES))
            p = input('Puzzle name: ').strip()
            if p in PUZZLES:
                config['selected_puzzle'] = p
                save_json(CONFIG_FILE, config)
                print('Puzzle updated. Takes effect next game start unless very small setting.')
        elif choice == '2':
            config['board_width'] = int(input('Width: '))
            config['board_height'] = int(input('Height: '))
            save_json(CONFIG_FILE, config)
            print('Board configuration saved for next game start.')
        elif choice == '3':
            config['difficulty'] = input('Difficulty (beginner/normal/advanced): ').strip()
            save_json(CONFIG_FILE, config)
            print('Difficulty updated.')
        elif choice == '4':
            print(json.dumps(state['results'], indent=2))
        elif choice == '5':
            state['results'] = []
            save_json(STATE_FILE, state)
            print('Results cleared.')
        elif choice == '6':
            archived = load_json(ARCHIVE_FILE, [])
            archived.extend(state['results'])
            save_json(ARCHIVE_FILE, archived)
            state['archived_results'] = archived
            state['results'] = []
            save_json(STATE_FILE, state)
            print('Results archived.')
        elif choice == '7':
            return


def main():
    ensure_data()
    config = load_json(CONFIG_FILE, DEFAULT_CONFIG.copy())
    state = load_json(STATE_FILE, DEFAULT_STATE.copy())
    args = sys.argv[1:]
    if args and args[0] == '--admin':
        admin(config, state)
    else:
        player = input('Player name: ').strip() or 'Player1'
        play(player, config, state)


if __name__ == '__main__':
    main()
