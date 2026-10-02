import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable

def run(*args):
    return subprocess.run([PY, str(ROOT / 'sprat.py'), *args], capture_output=True, text=True, check=True)

subprocess.run([PY, str(ROOT / 'sprat.py'), 'init'], check=True, capture_output=True, text=True)
run('add-user', 'alice', 'analyst')
run('add-user', 'pm', 'project_manager')
run('add-user', 'admin', 'administrator')
run('add-user', 'guest', 'guest')
run('add-project', 'demo')
item = run('create', '--user', 'alice', '--project', 'demo', '--type', 'requirement', '--title', 'T', '--content', 'C', '--classification', 'security').stdout.strip()
assert item.startswith('I')
out = run('show', '--user', 'guest', item).stdout
assert '<hidden>' in out
run('submit', '--user', 'alice', item, '--reviewers', 'pm')
run('review', '--user', 'pm', item, '--approve', '--finalize')
out = run('show', '--user', 'guest', item).stdout
assert 'final' in out
path = ROOT / 't.json'
run('export', str(path))
assert json.loads(path.read_text())['items'][item]['state'] == 'final'
print('ok')
