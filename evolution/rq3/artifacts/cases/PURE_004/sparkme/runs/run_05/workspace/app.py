from __future__ import annotations

import json
import os
import random
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

DATA_DIR = Path(os.environ.get('QHEADACHE_DATA_DIR', Path(__file__).with_name('data')))
STATE_FILE = DATA_DIR / 'state.json'
EXPORT_DIR = DATA_DIR / 'exports'


def now_ms() -> int:
    return int(time.time() * 1000)


def safe_mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def default_session() -> dict[str, Any]:
    return {
        'active': False,
        'session_id': None,
        'started_at': None,
        'updated_at': None,
        'puzzle': [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
        'solved': True,
        'move_count': 0,
        'hint_count': 0,
        'message': 'Welcome to Qheadache. Start a new puzzle to begin.',
        'last_completion_time_ms': None,
        'best_completion_time_ms': None,
        'best_move_count': None,
        'completed_puzzles': 0,
        'history': [],
        'undo_stack': [],
        'stats': {
            'total_sessions': 0,
            'total_moves': 0,
            'total_completions': 0,
            'best_completion_time_ms': None,
            'best_move_count': None,
        },
        'update_prompt': None,
        'save_warning': None,
        'export_info': None,
    }


def load_state() -> dict[str, Any]:
    safe_mkdir(DATA_DIR)
    if not STATE_FILE.exists():
        return default_session()
    try:
        data = json.loads(STATE_FILE.read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            raise ValueError('state is not an object')
        base = default_session()
        base.update(data)
        base.setdefault('undo_stack', [])
        return base
    except Exception:
        quarantine = STATE_FILE.with_suffix('.corrupt.json')
        try:
            if STATE_FILE.exists():
                STATE_FILE.replace(quarantine)
        except Exception:
            pass
        s = default_session()
        s['message'] = 'A corrupted save was detected and skipped. You can start a new session.'
        s['save_warning'] = 'Corrupted save recovered by starting fresh.'
        return s


def save_state(state: dict[str, Any]) -> tuple[bool, str | None]:
    safe_mkdir(DATA_DIR)
    try:
        tmp = STATE_FILE.with_suffix('.tmp')
        tmp.write_text(json.dumps(state, indent=2), encoding='utf-8')
        tmp.replace(STATE_FILE)
        return True, None
    except Exception as e:
        return False, str(e)


def board_to_text(board: list[list[int]]) -> str:
    return '\n'.join(' '.join('_' if n == 0 else str(n) for n in row) for row in board)


def find_zero(board: list[list[int]]) -> tuple[int, int]:
    for r, row in enumerate(board):
        for c, n in enumerate(row):
            if n == 0:
                return r, c
    raise ValueError('no zero tile')


def move_tile(board: list[list[int]], tile: int) -> tuple[bool, str]:
    zr, zc = find_zero(board)
    tr = tc = -1
    for r, row in enumerate(board):
        for c, n in enumerate(row):
            if n == tile:
                tr, tc = r, c
    if tr < 0:
        return False, 'Invalid move: tile not found.'
    if abs(tr - zr) + abs(tc - zc) != 1:
        return False, 'Invalid move: tile must be adjacent to the empty space.'
    board[zr][zc], board[tr][tc] = board[tr][tc], board[zr][zc]
    return True, 'Move accepted.'


def solved(board: list[list[int]]) -> bool:
    return [n for row in board for n in row] == [1, 2, 3, 4, 5, 6, 7, 8, 0]


def shuffle_board() -> list[list[int]]:
    while True:
        tiles = list(range(9))
        random.shuffle(tiles)
        board = [tiles[i:i + 3] for i in range(0, 9, 3)]
        inv = sum(1 for i in range(8) for j in range(i + 1, 9) if tiles[i] and tiles[j] and tiles[i] > tiles[j])
        if inv % 2 == 0 and not solved(board):
            return board


def render_page(state: dict[str, Any]) -> str:
    board = board_to_text(state['puzzle'])
    stats = state['stats']
    history = state['history'][-10:]
    history_lines = ''.join(f'<li>{h}</li>' for h in reversed(history)) or '<li>No completed puzzles yet.</li>'
    return f'''<!doctype html>
<html><head><meta charset="utf-8"><title>Qheadache</title>
<style>
body {{ font-family: sans-serif; max-width: 1000px; margin: 2rem auto; padding: 0 1rem; }}
pre {{ background: #f6f6f6; padding: 1rem; font-size: 1.2rem; }}
.notice {{ background: #eef; padding: .75rem; border-left: 4px solid #88f; margin: 1rem 0; }}
.warn {{ background: #ffe; border-left-color: #cc0; }}
.small {{ color: #555; font-size: .92rem; }}
</style></head><body>
<h1>Qheadache</h1>
<p>Offline puzzle game with local saves, stats, undo, restart, and export.</p>
<div class="notice">{state['message']}</div>
{f'<div class="notice warn">{state["save_warning"]}</div>' if state.get('save_warning') else ''}
{f'<div class="notice">{state["update_prompt"]}</div>' if state.get('update_prompt') else ''}
{f'<div class="notice">{state["export_info"]}</div>' if state.get('export_info') else ''}
<h2>Board</h2>
<pre>{board}</pre>
<form method="post" action="/move">
<label>Move tile: <input name="tile" type="number" min="1" max="8"></label>
<button type="submit">Move</button>
</form>
<form method="post" action="/new" style="display:inline"><button type="submit">New Puzzle</button></form>
<form method="post" action="/undo" style="display:inline"><button type="submit">Undo</button></form>
<form method="post" action="/restart" style="display:inline"><button type="submit">Restart</button></form>
<form method="post" action="/hint" style="display:inline"><button type="submit">Hint</button></form>
<form method="post" action="/export" style="display:inline"><button type="submit">Export Stats</button></form>
<form method="post" action="/clear-warning" style="display:inline"><button type="submit">Dismiss Notices</button></form>
<h2>Progress</h2>
<ul>
<li>Puzzles completed: {state['completed_puzzles']}</li>
<li>Current moves: {state['move_count']}</li>
<li>Current session age: {((now_ms() - state['started_at']) // 1000) if state['started_at'] else 0} seconds</li>
<li>Total sessions: {stats['total_sessions']}</li>
<li>Total moves: {stats['total_moves']}</li>
<li>Best completion time: {stats['best_completion_time_ms'] or 'n/a'}</li>
<li>Best move count: {stats['best_move_count'] or 'n/a'}</li>
</ul>
<h2>Recent history</h2>
<ul>{history_lines}</ul>
<p class="small">Hint: tiles can move only when adjacent to the empty space. Save data is local only.</p>
</body></html>'''


def complete_if_needed(state: dict[str, Any]) -> None:
    if solved(state['puzzle']) and state['active']:
        state['active'] = False
        duration = now_ms() - state['started_at'] if state['started_at'] else 0
        state['last_completion_time_ms'] = duration
        state['completed_puzzles'] += 1
        state['stats']['total_completions'] += 1
        best = state['stats']['best_completion_time_ms']
        state['stats']['best_completion_time_ms'] = duration if best is None else min(best, duration)
        if state['stats']['best_move_count'] is None or state['move_count'] < state['stats']['best_move_count']:
            state['stats']['best_move_count'] = state['move_count']
        state['history'].append({'session_id': state['session_id'], 'completed_at': now_ms(), 'moves': state['move_count'], 'time_ms': duration})
        state['message'] = f'Puzzle solved in {state["move_count"]} moves.'


class Handler(BaseHTTPRequestHandler):
    state = load_state()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/':
            self.respond(200, render_page(self.state), 'text/html; charset=utf-8')
        elif parsed.path == '/state':
            self.respond(200, json.dumps(self.state, indent=2), 'application/json')
        else:
            self.respond(404, 'Not found')

    def do_POST(self):
        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length).decode('utf-8')
        data = parse_qs(body)
        path = urlparse(self.path).path
        self.state['update_prompt'] = None
        self.state['save_warning'] = None
        self.state['export_info'] = None
        if path == '/new':
            self.state = default_session()
            self.state['puzzle'] = shuffle_board()
            self.state['active'] = True
            self.state['solved'] = False
            self.state['session_id'] = f'session-{now_ms()}'
            self.state['started_at'] = now_ms()
            self.state['stats']['total_sessions'] += 1
            self.state['message'] = 'New puzzle started.'
        elif path == '/move':
            if self.state.get('solved'):
                self.state['message'] = 'Start a new puzzle first.'
            else:
                tile = int(data.get('tile', ['0'])[0] or '0')
                board_copy = json.loads(json.dumps(self.state['puzzle']))
                self.state['undo_stack'].append(self.state['puzzle'])
                ok, msg = move_tile(board_copy, tile)
                if ok:
                    self.state['puzzle'] = board_copy
                    self.state['move_count'] += 1
                    self.state['stats']['total_moves'] += 1
                    self.state['message'] = msg
                    if solved(self.state['puzzle']):
                        self.state['solved'] = True
                        complete_if_needed(self.state)
                else:
                    self.state['undo_stack'].pop()
                    self.state['message'] = msg
        elif path == '/undo':
            if self.state['undo_stack']:
                self.state['puzzle'] = self.state['undo_stack'].pop()
                self.state['move_count'] = max(0, self.state['move_count'] - 1)
                self.state['message'] = 'Undid the last move.'
            else:
                self.state['message'] = 'Nothing to undo.'
        elif path == '/restart':
            self.state['puzzle'] = shuffle_board()
            self.state['move_count'] = 0
            self.state['solved'] = False
            self.state['active'] = True
            self.state['started_at'] = now_ms()
            self.state['undo_stack'] = []
            self.state['message'] = 'Puzzle restarted.'
        elif path == '/hint':
            self.state['hint_count'] += 1
            self.state['message'] = 'Hint: move tiles next to the empty space. Solve the board to win.'
        elif path == '/export':
            safe_mkdir(EXPORT_DIR)
            fname = EXPORT_DIR / f'qheadache-stats-{now_ms()}.json'
            payload = {'summary': self.state['stats'], 'completed_puzzles': self.state['completed_puzzles'], 'recent_history': self.state['history'][-20:]}
            try:
                fname.write_text(json.dumps(payload, indent=2), encoding='utf-8')
                self.state['export_info'] = f'Stats exported successfully to {fname.name}.'
            except Exception:
                self.state['export_info'] = 'Stats export failed, but the game continues normally.'
        elif path == '/clear-warning':
            self.state['save_warning'] = None
            self.state['update_prompt'] = None
            self.state['message'] = 'Notices dismissed.'
        ok, err = save_state(self.state)
        if not ok:
            self.state['save_warning'] = f'Save warning: {err}. The game will continue with current state.'
        self.respond(303, '', headers={'Location': '/'})

    def respond(self, status: int, body: str, content_type: str = 'text/plain; charset=utf-8', headers: dict[str, str] | None = None):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        if headers:
            for k, v in headers.items():
                self.send_header(k, v)
        self.end_headers()
        if body:
            self.wfile.write(body.encode('utf-8'))

    def log_message(self, format: str, *args):
        return


def main():
    host = os.environ.get('QHEADACHE_HOST', '127.0.0.1')
    port = int(os.environ.get('QHEADACHE_PORT', '8000'))
    safe_mkdir(DATA_DIR)
    server = ThreadingHTTPServer((host, port), Handler)
    print(f'Qheadache running at http://{host}:{port}')
    server.serve_forever()


if __name__ == '__main__':
    main()
