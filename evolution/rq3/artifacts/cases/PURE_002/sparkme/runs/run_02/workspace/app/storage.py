import json, os, tempfile
from copy import deepcopy

DEFAULT_DATA = {
    'store_info': {'name': '', 'currency': 'USD'},
    'products': [],
    'customers': [],
    'orders': [],
    'cart': [],
    'audit_log': [],
    'notifications': [],
    'issues': [],
    'setup_completed': False,
    'import_history': []
}

class Storage:
    def __init__(self, path):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            self._write(DEFAULT_DATA)

    def load(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        merged = deepcopy(DEFAULT_DATA)
        merged.update(data)
        return merged

    def save(self, data):
        self._write(data)

    def _write(self, data):
        d = os.path.dirname(self.path) or '.'
        fd, tmp = tempfile.mkstemp(dir=d, prefix='.store-', suffix='.json')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            os.replace(tmp, self.path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
