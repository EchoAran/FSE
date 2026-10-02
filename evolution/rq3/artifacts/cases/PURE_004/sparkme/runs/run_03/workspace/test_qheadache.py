import json
import os
import tempfile
from pathlib import Path

import qheadache as q


def run():
    with tempfile.TemporaryDirectory() as td:
        q.SAVE_DIR = Path(td)
        q.SAVE_FILE = q.SAVE_DIR / 'save.json'
        q.EXPORT_FILE = q.SAVE_DIR / 'stats_export.json'
        stats = q.default_stats()
        session = q.Session(size=3, board=q.solved_board(3), initial_board=q.solved_board(3), started_at=q.now())
        ok, _ = q.save_state(session, stats)
        assert ok
        loaded_session, loaded_stats = q.load_state()
        assert loaded_session.board == session.board
        assert loaded_stats['puzzles_completed'] == 0
        p = q.export_stats(stats)
        assert p.exists()
        q.SAVE_FILE.write_text('{broken')
        loaded_session, warning = q.load_state()
        assert loaded_session is None
        assert warning['warning']
    print('ok')


if __name__ == '__main__':
    run()
