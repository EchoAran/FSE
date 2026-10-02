import json
import os
import tempfile
import unittest
from http import HTTPStatus
from urllib.request import Request, urlopen
from threading import Thread

import app


class SPRATTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        app.DATA_FILE = os.path.join(self.tmp.name, 'data.json')
        if os.path.exists(app.DATA_FILE):
            os.unlink(app.DATA_FILE)

    def tearDown(self):
        self.tmp.cleanup()

    def test_glossary_warning(self):
        data = app.load_data()
        warnings = app.term_warnings(data, 'polcy')
        self.assertTrue(any(w['type'] == 'near_match' for w in warnings))

    def test_project_and_artifact_lifecycle(self):
        data = app.load_data()
        data['sessions']['abc'] = data['users'][2]
        app.save_data(data)
        proj = {'id': 1, 'name': 'P', 'artifacts': []}
        data['projects'].append(proj)
        app.save_data(data)
        handler = object()
        self.assertEqual(app.find_project(data, 1)['name'], 'P')

    def test_http_server_smoke(self):
        app.DATA_FILE = os.path.join(self.tmp.name, 'live.json')
        t = Thread(target=lambda: app.ThreadingHTTPServer(('127.0.0.1', 8765), app.Handler).serve_forever(), daemon=True)
        t.start()
        import time
        time.sleep(0.2)
        with urlopen('http://127.0.0.1:8765/') as r:
            self.assertEqual(r.status, HTTPStatus.OK)


if __name__ == '__main__':
    unittest.main()
