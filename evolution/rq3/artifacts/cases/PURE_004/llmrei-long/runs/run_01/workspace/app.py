#!/usr/bin/env python3
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / 'qheadache_state.json'
PORT = 8000

START_BOARD = [
    ['A', 'A', '.', '.', 'B'],
    ['.', '.', '.', '.', 'B'],
    ['C', 'C', 'D', 'D', '.'],
    ['.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.'],
]
TARGET = {
    'A': {'x': 3, 'y': 0, 'w': 2, 'h': 1},
    'B': {'x': 3, 'y': 2, 'w': 1, 'h': 2},
    'C': {'x': 0, 'y': 2, 'w': 2, 'h': 1},
    'D': {'x': 2, 'y': 2, 'w': 2, 'h': 1},
}
BLOCK_COLORS = {'A': '#4f83ff', 'B': '#ff8a4f', 'C': '#4fb36f', 'D': '#b04fff'}


def board_to_state(board):
    return [''.join(row) for row in board]


def state_to_board(state):
    return [list(row) for row in state]


def default_state():
    return {
        'board': board_to_state(START_BOARD),
        'initial_board': board_to_state(START_BOARD),
        'moves': 0,
        'started_at': None,
        'elapsed_before': 0,
        'finished': False,
        'results': [],
        'message': 'Move blocks by dragging them one step at a time.',
        'flash': '',
    }


def load_state():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text())
            base = default_state()
            base.update(data)
            return base
        except Exception:
            return default_state()
    return default_state()


def save_state(state):
    DATA_FILE.write_text(json.dumps(state, indent=2))


def find_blocks(board):
    seen = set()
    blocks = {}
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == '.' or cell in seen:
                continue
            coords = [(yy, xx) for yy, r in enumerate(board) for xx, c in enumerate(r) if c == cell]
            seen.add(cell)
            blocks[cell] = coords
    return blocks


def block_bounds(coords):
    ys = [y for y, _ in coords]
    xs = [x for _, x in coords]
    return min(xs), min(ys), max(xs), max(ys)


def can_move(board, block, dx, dy):
    coords = find_blocks(board)[block]
    for y, x in coords:
        ny, nx = y + dy, x + dx
        if ny < 0 or nx < 0 or ny >= len(board) or nx >= len(board[0]):
            return False
        if board[ny][nx] not in ('.', block):
            return False
    return True


def move_block(board, block, dx, dy):
    if not can_move(board, block, dx, dy):
        return None
    new_board = [row[:] for row in board]
    coords = find_blocks(board)[block]
    for y, x in coords:
        new_board[y][x] = '.'
    for y, x in coords:
        new_board[y + dy][x + dx] = block
    return new_board


def solved(board):
    blocks = find_blocks(board)
    for name, target in TARGET.items():
        coords = blocks.get(name, [])
        x0, y0, x1, y1 = block_bounds(coords)
        if (x0, y0, x1 - x0 + 1, y1 - y0 + 1) != (target['x'], target['y'], target['w'], target['h']):
            return False
    return True


def elapsed_seconds(state):
    started = state.get('started_at')
    if not started:
        return int(state.get('elapsed_before', 0))
    import time
    return int(state.get('elapsed_before', 0) + (time.time() - started))


def html_page(state):
    board = state['board']
    cells = []
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == '.':
                cells.append(f'<button class="cell empty" data-x="{x}" data-y="{y}"></button>')
            else:
                cells.append(f'<button class="cell block" data-x="{x}" data-y="{y}" data-block="{cell}" style="background:{BLOCK_COLORS[cell]}">{cell}</button>')
    grid = ''.join(cells)
    result_items = ''.join(f'<li>{r}</li>' for r in state.get('results', [])[:10]) or '<li>No completions yet.</li>'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qheadache</title>
<style>
body {{ font-family: system-ui, sans-serif; background:#f6f7fb; color:#222; margin:0; padding:20px; }}
main {{ max-width: 760px; margin: 0 auto; }}
.board {{ display:grid; grid-template-columns: repeat(5, 72px); gap:8px; margin:20px 0; touch-action: manipulation; }}
.cell {{ width:72px; height:72px; border:1px solid #cbd5e1; border-radius:12px; font-size:20px; font-weight:700; }}
.empty {{ background:#fff; }}
.block {{ color:#fff; border:none; box-shadow:0 2px 6px rgba(0,0,0,.12); }}
.flash-invalid {{ outline: 4px solid #ffb4b4; animation: pulse .25s ease-in-out 0s 2; }}
.flash-success {{ outline: 4px solid #9de6a0; }}
.controls button {{ margin-right:8px; padding:10px 14px; border-radius:10px; border:1px solid #94a3b8; background:#fff; }}
.status {{ min-height: 1.5em; font-weight:600; }}
small {{ color:#475569; }}
</style>
</head>
<body>
<main>
<h1>Qheadache</h1>
<p>Drag a block to move it one step. Invalid moves show a gentle cue. Progress saves locally.</p>
<div class="status" id="status">{state.get('message','')}</div>
<div>Moves: <span id="moves">{state.get('moves',0)}</span> | Time: <span id="time">{elapsed_seconds(state)}</span>s</div>
<div class="board" id="board">{grid}</div>
<div class="controls">
<button onclick="postAction('reset')">Reset / Replay</button>
<button onclick="postAction('resume')">Resume Saved Puzzle</button>
</div>
<h2>Completion History</h2>
<ul>{result_items}</ul>
</main>
<script>
const board = document.getElementById('board');
let dragged = null;
function refresh(data) {{
  document.getElementById('status').textContent = data.message || '';
  document.getElementById('moves').textContent = data.moves;
  document.getElementById('time').textContent = data.elapsed;
  if (data.flash === 'invalid') board.classList.add('flash-invalid'); else board.classList.remove('flash-invalid');
  if (data.flash === 'success') board.classList.add('flash-success'); else if (data.flash !== 'success') board.classList.remove('flash-success');
  if (data.html) document.body.innerHTML = data.html;
}}
async function postAction(action, payload={{}}) {{
  const form = new URLSearchParams();
  form.set('action', action);
  for (const [k,v] of Object.entries(payload)) form.set(k, v);
  const r = await fetch('/action', {{ method:'POST', headers: {{'Content-Type':'application/x-www-form-urlencoded'}}, body: form }});
  const data = await r.json();
  location.reload();
}}
board.addEventListener('pointerdown', e => {{
  const b = e.target.closest('[data-block]');
  if (b) dragged = b.dataset.block;
}});
board.addEventListener('pointerup', async e => {{
  if (!dragged) return;
  const cell = e.target.closest('.cell');
  if (!cell) return;
  const from = e.target.closest('[data-block]');
  const dx = Number(cell.dataset.x) - Number((from || e.target).dataset.x || 0);
  const dy = Number(cell.dataset.y) - Number((from || e.target).dataset.y || 0);
  let dir = null;
  if (Math.abs(dx) + Math.abs(dy) === 1) {{
    if (dx === 1) dir = 'right'; if (dx === -1) dir = 'left'; if (dy === 1) dir = 'down'; if (dy === -1) dir = 'up';
  }}
  if (dir) await postAction('move', {{block: dragged, dir}});
  dragged = null;
}});
</script>
</body>
</html>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path != '/':
            self.send_error(404)
            return
        state = load_state()
        body = html_page(state).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if urlparse(self.path).path != '/action':
            self.send_error(404)
            return
        length = int(self.headers.get('Content-Length', '0'))
        data = parse_qs(self.rfile.read(length).decode())
        action = data.get('action', [''])[0]
        state = load_state()
        import time
        if action == 'resume':
            state['message'] = 'Resumed saved puzzle.'
        elif action == 'reset':
            state = default_state()
            state['message'] = 'Puzzle reset to the original start.'
        elif action == 'move':
            block = data.get('block', [''])[0]
            dir_ = data.get('dir', [''])[0]
            dxdy = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}.get(dir_)
            if block and dxdy:
                if not state.get('started_at'):
                    state['started_at'] = time.time()
                new_board = move_block(state_to_board(state['board']), block, *dxdy)
                if new_board is None:
                    state['flash'] = 'invalid'
                    state['message'] = 'That move is not allowed. Try another direction.'
                else:
                    state['board'] = board_to_state(new_board)
                    state['moves'] = state.get('moves', 0) + 1
                    state['flash'] = ''
                    state['message'] = 'Move accepted.'
                    if solved(new_board) and not state.get('finished'):
                        state['finished'] = True
                        elapsed = elapsed_seconds(state)
                        score = max(0, 1000 - state['moves'] * 10 - elapsed)
                        result = f'Completed in {elapsed}s, {state["moves"]} moves, score {score}.'
                        state.setdefault('results', []).insert(0, result)
                        state['message'] = 'Puzzle completed! Great job.'
                        state['flash'] = 'success'
                        state['elapsed_before'] = elapsed
                        state['started_at'] = None
            else:
                state['flash'] = 'invalid'
                state['message'] = 'Invalid move input.'
        save_state(state)
        out = json.dumps({'message': state['message'], 'moves': state['moves'], 'elapsed': elapsed_seconds(state), 'flash': state.get('flash','')}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(out)))
        self.end_headers()
        self.wfile.write(out)


def main():
    save_state(load_state())
    print(f'Qheadache running at http://127.0.0.1:{PORT}/')
    ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()


if __name__ == '__main__':
    main()
