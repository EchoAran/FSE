import json
import os
import tempfile
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location('app', '/workspace/app.py')
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

with tempfile.TemporaryDirectory() as d:
    os.environ['QHEADACHE_DATA_DIR'] = d
    app.DATA_DIR = Path(d)
    app.STATE_FILE = app.DATA_DIR / 'state.json'
    app.EXPORT_DIR = app.DATA_DIR / 'exports'

    state = app.load_state()
    assert state['completed_puzzles'] == 0
    assert state['message']

    state['puzzle'] = [[1,2,3],[4,5,6],[0,7,8]]
    ok, msg = app.move_tile(state['puzzle'], 1)
    assert not ok and 'adjacent' in msg.lower()

    ok, msg = app.move_tile(state['puzzle'], 7)
    assert ok
    assert state['puzzle'] == [[1,2,3],[4,5,6],[7,0,8]]

    bad = Path(d) / 'state.json'
    bad.write_text('{not json', encoding='utf-8')
    recovered = app.load_state()
    assert 'corrupted save' in recovered['message'].lower()

    app.save_state(recovered)
    assert bad.exists()

print('ok')
