import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / 'qheadache_data'


def run(inp, *args):
    return subprocess.run([sys.executable, str(ROOT / 'qheadache.py'), *args], input=inp.encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout.decode()


def main():
    if DATA.exists():
        for p in DATA.iterdir():
            p.unlink()
        DATA.rmdir()
    out = run('Alice\nquit\n')
    assert 'Welcome, Alice' in out
    assert DATA.exists()
    cfg = json.loads((DATA / 'config.json').read_text())
    assert cfg['selected_puzzle'] == 'starter'
    out = run('admin\n7\n', '--admin')
    assert 'Admin menu' in out
    print('OK')


if __name__ == '__main__':
    main()
