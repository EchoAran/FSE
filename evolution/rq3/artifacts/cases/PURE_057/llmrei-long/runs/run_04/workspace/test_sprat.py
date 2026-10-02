import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

PY = ['python3', '/workspace/sprat.py']

class SpratTests(unittest.TestCase):
    def run_cmd(self, args, db):
        env = os.environ.copy()
        env['SPRAT_DB'] = str(db)
        return subprocess.run(PY + args, env=env, text=True, capture_output=True, check=True)

    def test_create_link_show_and_compare(self):
        with tempfile.TemporaryDirectory() as d:
            db = Path(d) / 'db.json'
            self.run_cmd(['set-user', 'alice', 'admin'], db)
            self.run_cmd(['create', 'policy', 'Policy A', '--user', 'alice'], db)
            self.run_cmd(['create', 'requirement', 'Req 1', '--user', 'alice', '--sources', '1', '--primary-source', '1'], db)
            self.run_cmd(['link', '2', '1', '--relation', 'derived-from', '--user', 'alice'], db)
            shown = self.run_cmd(['show', '2', '--user', 'guest'], db)
            data = json.loads(shown.stdout)
            self.assertEqual(data['id'], 2)
            self.assertEqual(data['source_artifacts'], ['Policy A'])
            cmp_out = self.run_cmd(['compare', '1', '2', '--user', 'guest'], db)
            cmp_data = json.loads(cmp_out.stdout)
            self.assertEqual(cmp_data['first']['title'], 'Policy A')
            self.assertEqual(cmp_data['second']['title'], 'Req 1')

    def test_permissions_and_undo(self):
        with tempfile.TemporaryDirectory() as d:
            db = Path(d) / 'db.json'
            self.run_cmd(['set-user', 'alice', 'analyst'], db)
            self.run_cmd(['create', 'goal', 'G1', '--user', 'alice'], db)
            self.run_cmd(['undo', '--user', 'alice'], db)
            out = subprocess.run(PY + ['show', '1', '--user', 'guest'], env={**os.environ, 'SPRAT_DB': str(db)}, text=True, capture_output=True)
            self.assertNotEqual(out.returncode, 0)

if __name__ == '__main__':
    unittest.main()
