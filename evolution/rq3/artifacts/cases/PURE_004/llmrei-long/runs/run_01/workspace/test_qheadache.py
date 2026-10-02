#!/usr/bin/env python3
from app import START_BOARD, state_to_board, move_block, solved, default_state, save_state, load_state, DATA_FILE


def assert_true(x, msg):
    if not x:
        raise AssertionError(msg)

board = state_to_board([''.join(r) for r in START_BOARD])
new_board = move_block(board, 'C', 0, 1)
assert_true(new_board is not None, 'Expected C to move down')
assert_true(new_board[3][0] == 'C' and new_board[3][1] == 'C', 'C should have moved down')
assert_true(move_block(board, 'A', -1, 0) is None, 'Expected A to be blocked moving left')
assert_true(not solved(board), 'Start board should not be solved')
state = default_state()
state['results'] = ['x']
save_state(state)
loaded = load_state()
assert_true(loaded['results'] == ['x'], 'State should round-trip')
DATA_FILE.unlink(missing_ok=True)
print('ok')
