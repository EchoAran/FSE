#!/usr/bin/env python3
import subprocess, sys, time, urllib.request, urllib.error

p = subprocess.Popen([sys.executable, 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
try:
    time.sleep(1.5)
    with urllib.request.urlopen('http://127.0.0.1:8000/') as r:
        body = r.read().decode()
        assert 'Nenios Child Care Management' in body
    with urllib.request.urlopen('http://127.0.0.1:8000/families') as r:
        body = r.read().decode()
        assert 'Families' in body
    print('smoke test ok')
finally:
    p.terminate()
    try:
        p.wait(timeout=5)
    except Exception:
        p.kill()
