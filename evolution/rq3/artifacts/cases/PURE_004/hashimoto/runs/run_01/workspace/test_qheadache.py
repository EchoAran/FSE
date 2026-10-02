import tempfile
import unittest
from pathlib import Path

import qheadache.app as qa

class QHeadacheTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        qa.DATA_DIR = Path(self.tmp.name)
        qa.DB_PATH = qa.DATA_DIR / 'qheadache.sqlite3'
        qa.init_db()
        qa.app.testing = True
        self.client = qa.app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def test_index_and_admin(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/admin').status_code, 200)

    def test_progress_save(self):
        p = qa.get_puzzle(1)
        goal = __import__('json').loads(p['goal_json'])
        resp = self.client.post('/play/1', data={
            'player': 'Ada',
            'moves': '4',
            'elapsed': '12',
            'board': __import__('json').dumps(goal),
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Ada', self.client.get('/results').data)

if __name__ == '__main__':
    unittest.main()
