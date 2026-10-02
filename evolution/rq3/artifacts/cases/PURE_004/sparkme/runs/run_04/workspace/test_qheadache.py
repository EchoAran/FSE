import json
import tempfile
from pathlib import Path

import qheadache


def run_cmd(args):
    return qheadache.main(args)


def test_start_and_move_and_stats():
    with tempfile.TemporaryDirectory() as td:
        save = Path(td) / 'save.json'
        export = Path(td) / 'export.json'
        assert run_cmd(['--save-file', str(save), '--export-file', str(export), 'start']) == 0
        assert save.exists()
        assert run_cmd(['--save-file', str(save), 'move', 'left']) == 0
        assert run_cmd(['--save-file', str(save), 'undo']) == 0
        assert run_cmd(['--save-file', str(save), 'stats']) == 0
        assert run_cmd(['--save-file', str(save), '--export-file', str(export), 'export']) == 0
        data = json.loads(export.read_text())
        assert 'basic_stats' in data


def test_corrupt_save_recovers():
    with tempfile.TemporaryDirectory() as td:
        save = Path(td) / 'save.json'
        save.write_text('{bad json', encoding='utf-8')
        assert run_cmd(['--save-file', str(save), 'recover']) == 0
        assert save.with_suffix('.json.corrupt').exists()


if __name__ == '__main__':
    test_start_and_move_and_stats()
    test_corrupt_save_recovers()
    print('ok')
