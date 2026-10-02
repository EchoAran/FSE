import json
import os
import tempfile
import unittest
from pathlib import Path

import qheadache

class TestQheadache(unittest.TestCase):
    def test_completion_detection(self):
        level = qheadache.LEVELS[0]
        _, goals, blocks, _ = qheadache.parse_grid(level['grid'])
        self.assertFalse(qheadache.is_completed(blocks, goals))
        self.assertEqual(qheadache.score_for(10, 5), 895)

    def test_profile_save_load(self):
        with tempfile.TemporaryDirectory() as td:
            old_home = os.environ.get('HOME')
            os.environ['HOME'] = td
            try:
                data = {'profile': 'alice', 'results': [{'level_name': 'x', 'completed': True}]}
                self.assertTrue(qheadache.save_profile('alice', data))
                loaded = qheadache.load_profile('alice')
                self.assertEqual(loaded['profile'], 'alice')
                self.assertEqual(loaded['results'][0]['level_name'], 'x')
            finally:
                if old_home is None:
                    del os.environ['HOME']
                else:
                    os.environ['HOME'] = old_home

    def test_profile_separation(self):
        with tempfile.TemporaryDirectory() as td:
            old_home = os.environ.get('HOME')
            os.environ['HOME'] = td
            try:
                qheadache.save_profile('a', {'profile': 'a', 'results': [1]})
                qheadache.save_profile('b', {'profile': 'b', 'results': [2]})
                self.assertEqual(qheadache.load_profile('a')['results'], [1])
                self.assertEqual(qheadache.load_profile('b')['results'], [2])
            finally:
                if old_home is None:
                    del os.environ['HOME']
                else:
                    os.environ['HOME'] = old_home

if __name__ == '__main__':
    unittest.main()
