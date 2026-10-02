from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json, os, uuid

LEVELS = [
    {'id': 1, 'name': 'Easy Start', 'size': 3, 'goal': [1,2,3,4,5,6,7,8,0], 'start': [1,2,3,4,5,6,0,7,8], 'hint': 'Move the blank right, then down to finish.'},
    {'id': 2, 'name': 'Second Step', 'size': 3, 'goal': [1,2,3,4,5,6,7,8,0], 'start': [1,2,3,4,5,6,7,0,8], 'hint': 'The blank needs to reach the bottom-right corner.'},
    {'id': 3, 'name': 'Challenge', 'size': 3, 'goal': [1,2,3,4,5,6,7,8,0], 'start': [1,2,3,5,0,6,4,7,8], 'hint': 'Solve the middle row first.'},
]

SAVE_FILE = os.path.join('data', 'save.json')
EXPORT_DIR = os.path.join('data', 'exports')


def now_iso():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def make_session(level_id=1):
    lvl = next(l for l in LEVELS if l['id'] == level_id)
    return {
        'session_id': str(uuid.uuid4()),
        'level_id': lvl['id'],
        'level_name': lvl['name'],
        'size': lvl['size'],
        'board': list(lvl['start']),
        'goal': list(lvl['goal']),
        'moves': 0,
        'started_at': now_iso(),
        'completed_at': None,
        'history': [],
        'status': 'active',
        'message': 'Welcome! Use the buttons to move tiles into the blank space.',
        'hint': lvl['hint'],
        'score': 0,
    }


def serialize_state(state):
    return json.dumps(state, indent=2)


def save_state(state):
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    os.makedirs(EXPORT_DIR, exist_ok=True)
    tmp = SAVE_FILE + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(serialize_state(state))
    os.replace(tmp, SAVE_FILE)


def load_state():
    if not os.path.exists(SAVE_FILE):
        return make_session(), None
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict) or 'board' not in data:
            raise ValueError('invalid save')
        return data, None
    except Exception as e:
        return make_session(), f'Save data was unreadable and a fresh session was started: {e}'


def valid_moves(board, size):
    idx = board.index(0)
    r, c = divmod(idx, size)
    moves = {}
    if r > 0: moves['up'] = idx - size
    if r < size - 1: moves['down'] = idx + size
    if c > 0: moves['left'] = idx - 1
    if c < size - 1: moves['right'] = idx + 1
    return moves


def apply_move(state, direction):
    if state.get('processing'):
        return state, 'Action already in progress; extra input ignored.'
    state['processing'] = True
    try:
        moves = valid_moves(state['board'], state['size'])
        if direction not in moves:
            return state, 'That move is not allowed because the blank cannot move that way.'
        blank = state['board'].index(0)
        other = moves[direction]
        state['history'].append(list(state['board']))
        state['board'][blank], state['board'][other] = state['board'][other], state['board'][blank]
        state['moves'] += 1
        state['score'] = max(0, 1000 - state['moves'] * 10)
        if state['board'] == state['goal']:
            state['status'] = 'completed'
            state['completed_at'] = now_iso()
            state['message'] = 'Puzzle solved! Progress was saved.'
            state['history'].append(list(state['board']))
        else:
            state['message'] = 'Move accepted.'
        return state, None
    finally:
        state['processing'] = False


def undo(state):
    if not state['history']:
        return state, 'Nothing to undo.'
    state['board'] = state['history'].pop()
    state['moves'] = max(0, state['moves'] - 1)
    state['status'] = 'active'
    state['message'] = 'Undid the last move.'
    return state, None


def restart(state):
    new = make_session(state['level_id'])
    new['message'] = 'Puzzle restarted.'
    return new


def export_stats(state, detailed=False):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    name = f"stats_{state['session_id']}.json"
    path = os.path.join(EXPORT_DIR, name)
    payload = {
        'session_id': state['session_id'],
        'level_name': state['level_name'],
        'moves': state['moves'],
        'score': state['score'],
        'status': state['status'],
        'completed_at': state.get('completed_at'),
    }
    if detailed:
        payload['history'] = state['history'][-20:]
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
    return path
