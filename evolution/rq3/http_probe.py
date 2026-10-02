"""Replay setup and target requests in one HTTP session inside the collector."""

import json
import re
import sys
from pathlib import Path

import requests


def probe(spec: dict, directory: Path, timeout: float) -> None:
    values: dict[str, object] = {}
    def substitute(text: str) -> str:
        return re.sub(r"\$\{([A-Za-z_]\w*)\}", lambda match: str(values[match[1]]), text)

    with requests.Session() as session:
        for index, step in enumerate([*spec["setup"], spec, *spec["actions"]], start=1):
            phase = "setup" if index <= len(spec["setup"]) else "action"
            url = substitute(step["url"])
            body = re.sub(r'"\$\{([A-Za-z_]\w*)\}"|\$\{([A-Za-z_]\w*)\}',
                          lambda match: json.dumps(values[match[1]]) if match[1] else str(values[match[2]]),
                          step["request_body"])
            headers = {key: substitute(value) for key, value in step["headers"].items()}
            response = session.request(
                step["method"], url, data=body.encode("utf-8") if body else None,
                headers=headers, timeout=timeout, allow_redirects=True,
            )
            record = (
                f"Step {index:02d} ({phase}): {step['method']} {url}\n"
                f"Request headers: {json.dumps(headers)}\nRequest body: {body}\n"
                f"HTTP status: {response.status_code}\n"
                f"Response headers: {json.dumps(dict(response.headers))}\n"
            )
            for hop in [*response.history, response]:
                record += (
                    f"HTTP exchange: {hop.request.method} {hop.request.url}\n"
                    f"Effective request headers: {json.dumps(dict(hop.request.headers))}\n"
                    f"Response status: {hop.status_code}\n"
                    f"Response headers: {json.dumps(dict(hop.headers))}\n"
                )
            for hop in response.history:
                record += f"Response body: {hop.text}\n"
            record += f"Response body: {response.text}\n"
            (directory / f"step_{index:02d}.response.txt").write_text(record, encoding="utf-8")
            (directory / "response.txt").write_text(record, encoding="utf-8")
            if index <= len(spec["setup"]) + 1:
                (directory / "status.txt").write_text(str(response.status_code), encoding="utf-8")
            if phase == "action":
                (directory / "action.observed").write_text("true", encoding="utf-8")
            if phase == "setup":
                response.raise_for_status()
            for name, path in step["capture"].items():
                value = response.json()
                for component in path.split("."):
                    value = value[int(component)] if isinstance(value, list) else value[component]
                values[name] = value


if __name__ == "__main__":
    probe(json.loads(sys.argv[1]), Path(sys.argv[2]), float(sys.argv[3]))
