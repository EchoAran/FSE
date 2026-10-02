import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
APP = ROOT / 'qheadache.py'
DATA = ROOT / 'data'
STATE = DATA / 'state.json'
ARCHIVE = DATA / 'archive.json'


def run_input(inp, *args):
    return subprocess.run([sys.executable, str(APP), *args], input=inp, text=True, capture_output=True, cwd=ROOT)


def setup_module(module):
    if DATA.exists():
        for p in DATA.iterdir():
            p.unlink()
    else:
        DATA.mkdir()


def test_game_can_solve_and_persist():
    p = run_input('1\nstarter\nmove A right\nmove A down\nmove B down\nmove B left\n3\n')
    assert p.returncode == 0, p.stderr
    state = json.loads(STATE.read_text())
    assert len(state['player_records']) == 1
    assert state['player_records'][0]['puzzle_id'] == 'starter'


def test_admin_can_archive_results():
    p = run_input('7\n8\n', '--admin')
    assert p.returncode == 0, p.stderr
    assert STATE.exists()
    assert ARCHIVE.exists()
