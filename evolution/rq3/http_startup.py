"""Observe an HTTP response from a delivered service before stopping it."""

import json
import os
import signal
import subprocess
import sys
import time

import requests


def observe(command: str, url: str, timeout: float) -> None:
    process = subprocess.Popen(["bash", "-lc", command], start_new_session=True)
    try:
        time.sleep(2)
        if process.poll() is not None:
            raise RuntimeError(f"The service exited before observation with code {process.returncode}.")
        response = requests.get(url, timeout=timeout, allow_redirects=False)
        print(json.dumps({"observation": "http_response", "url": url,
                          "status": response.status_code, "body": response.text[:4096]}), flush=True)
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
        process.wait()


if __name__ == "__main__":
    observe(sys.argv[1], sys.argv[2], float(sys.argv[3]))
