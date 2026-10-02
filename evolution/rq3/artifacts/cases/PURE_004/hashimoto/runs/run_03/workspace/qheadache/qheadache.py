#!/usr/bin/env python3
import json
import sys
import time
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / 'data'
STATE_FILE = DATA_DIR / 'state.json'
ARCHIVE_FILE = DATA_DIR / 'archive.json'
DEFAULT_STATE = {'settings': {'difficulty': 'normal', 'beginner_puzzles': ['starter'], 'advanced_puzzles': ['starter'], 'small_setting_changes_apply_immediately': True}, 'puzzles': {'starter': {'name': 'Starter', 'board_size': [2, 2], 'blocks': {'A': [0, 0]}, 'target': {'A': [0, 0]}}}, 'player_records': []}


def ensure_data_dir(): DATA_DIR.mkdir(parents=True, exist_ok=True)
def load_json(path, default): return json.loads(path.read_text()) if path.exists() else default

def save_json(path, obj): path.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')

def load_state():
    ensure_data_dir(); state = load_json(STATE_FILE, DEFAULT_STATE)
    for k, v in DEFAULT_STATE.items(): state.setdefault(k, v)
    state.setdefault('settings', {}).setdefault('difficulty', 'normal')
    state['settings'].setdefault('beginner_puzzles', ['starter'])
    state['settings'].setdefault('advanced_puzzles', ['starter'])
    state['settings'].setdefault('small_setting_changes_apply_immediately', True)
    state.setdefault('puzzles', DEFAULT_STATE['puzzles']); state.setdefault('player_records', [])
    return state

def save_state(state): save_json(STATE_FILE, state)
def archive_records(records): ensure_data_dir(); archive = load_json(ARCHIVE_FILE, []); archive.extend(records); save_json(ARCHIVE_FILE, archive)
def puzzle_positions(puzzle): return {k: tuple(v) for k, v in puzzle['blocks'].items()}
def render_board(size, blocks):
    w, h = size; grid = [['.' for _ in range(w)] for _ in range(h)]
    for name, (x, y) in blocks.items(): grid[y][x] = name
    return '\n'.join(' '.join(row) for row in grid)
def is_solved(blocks, target): return blocks == target

def play_puzzle(state, puzzle_id):
    puzzle = state['puzzles'][puzzle_id]; size = puzzle['board_size']; blocks = puzzle_positions(puzzle); target = {k: tuple(v) for k, v in puzzle['target'].items()}
    start = time.time(); actions = 0
    print(f"Playing puzzle: {puzzle['name']} ({puzzle_id})"); print('Move blocks with commands like: move A up / down / left / right')
    while True:
        print('\nBoard:'); print(render_board(size, blocks))
        if is_solved(blocks, target):
            elapsed = int(time.time() - start); score = max(1000 - elapsed * 10 - actions * 5, 0)
            state['player_records'].append({'puzzle_id': puzzle_id, 'puzzle_name': puzzle['name'], 'time_seconds': elapsed, 'actions': actions, 'score': score, 'timestamp': int(time.time())})
            save_state(state); print(f'Solved! time={elapsed}s actions={actions} score={score}'); return
        try: cmd = input('> ').strip().lower()
        except EOFError: print('Leaving puzzle.'); return
        if cmd in {'quit', 'exit'}: print('Leaving puzzle.'); return
        parts = cmd.split()
        if len(parts) != 3 or parts[0] != 'move' or parts[1].upper() not in blocks: print('Invalid command.'); continue
        block, direction = parts[1].upper(), parts[2]
        x, y = blocks[block]; dx, dy = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}.get(direction, (None, None))
        if dx is None: print('Unknown direction.'); continue
        nx, ny = x + dx, y + dy
        if not (0 <= nx < size[0] and 0 <= ny < size[1]): print('Move blocked by board edge.'); continue
        if any((nx, ny) == pos for name, pos in blocks.items() if name != block): print('Move blocked by another block.'); continue
        blocks[block] = (nx, ny); actions += 1

def show_results(state):
    if not state['player_records']: print('No player results yet.'); return
    for r in state['player_records']: print(f"{r['puzzle_name']} | time={r['time_seconds']}s | actions={r['actions']} | score={r['score']}")

def admin_menu(state):
    while True:
        print('\nAdmin menu:'); print('1) list puzzles'); print('2) add puzzle'); print('3) set difficulty'); print('4) configure visible puzzles'); print('5) view results'); print('6) clear results'); print('7) archive results'); print('8) save and exit')
        try: choice = input('Select: ').strip()
        except EOFError: save_state(state); return
        if choice == '1':
            for pid, p in state['puzzles'].items(): print(pid, p['name'], p['board_size'])
        elif choice == '2':
            try:
                pid = input('Puzzle id: ').strip(); name = input('Name: ').strip(); w = int(input('Board width: ')); h = int(input('Board height: '))
            except EOFError: return
            state['puzzles'][pid] = {'name': name, 'board_size': [w, h], 'blocks': {'A': [0, 0]}, 'target': {'A': [w - 1, h - 1]}}
        elif choice == '3': state['settings']['difficulty'] = input('Difficulty (beginner/normal/advanced): ').strip()
        elif choice == '4': state['settings']['beginner_puzzles'] = input('Beginner puzzle ids comma-separated: ').split(','); state['settings']['advanced_puzzles'] = input('Advanced puzzle ids comma-separated: ').split(','); state['settings']['small_setting_changes_apply_immediately'] = False
        elif choice == '5': show_results(state)
        elif choice == '6': state['player_records'] = []; print('Results cleared.')
        elif choice == '7': archive_records(state['player_records']); state['player_records'] = []; print('Results archived.')
        elif choice == '8': save_state(state); print('Saved.'); return
        else: print('Unknown choice.')

def main():
    state = load_state(); args = sys.argv[1:]
    if args and args[0] == '--admin': admin_menu(state); return
    while True:
        print('\nQheadache'); print('1) play'); print('2) results'); print('3) quit')
        try: choice = input('Select: ').strip()
        except EOFError: save_state(state); return
        if choice == '1':
            available = state['settings'].get('beginner_puzzles', list(state['puzzles'].keys())) or list(state['puzzles'].keys())
            print('Available puzzles:', ', '.join(available)); pid = input('Puzzle id: ').strip()
            if pid not in state['puzzles']: print('Unknown puzzle.'); continue
            play_puzzle(state, pid)
        elif choice == '2': show_results(state)
        elif choice == '3': save_state(state); return
        else: print('Unknown choice.')

if __name__ == '__main__': main()
