"""Client managing child worker subprocess and implementing BaseMethodAdapter."""

from multiprocessing.connection import Listener
from pathlib import Path
import subprocess
import sys
import time
from typing import Any, Dict, Optional
import uuid

from interview.adapters.base import AdapterResult, BaseMethodAdapter
from interview.adapters.registry import get_method_descriptor
from interview.adapters.worker_protocol import WorkerCommand, WorkerResponse
from interview.cases.models import CaseRecord


class ProcessWorkerClient(BaseMethodAdapter):
    """Manages method lifecycle in an isolated process via bidirectional IPC."""

    def __init__(
        self,
        method_id: str,
        method_config_path: Path,
        native_dir: Path,
        project_root: Optional[Path] = None,
        timeout_seconds: float = 120.0,
    ) -> None:
        self.method_id = method_id
        self.method_config_path = Path(method_config_path).resolve()
        self.native_dir = Path(native_dir).resolve()
        self.project_root = Path(project_root or Path.cwd()).resolve()
        self.timeout_seconds = timeout_seconds

        self.native_dir.mkdir(parents=True, exist_ok=True)
        self.worker_log_path = self.native_dir / "worker.log"

        descriptor = get_method_descriptor(self.method_id)
        self.method_root = descriptor.resolve_root(self.project_root)

        # Generate ephemeral authkey and start local listener
        self.authkey_str = uuid.uuid4().hex
        self.listener = Listener(("127.0.0.1", 0), authkey=self.authkey_str.encode("utf-8"))
        port = self.listener.address[1]

        # Spawn child worker process
        cmd_args = [
            sys.executable,
            "-m",
            "interview.workers.runner",
            "--method",
            self.method_id,
            "--port",
            str(port),
            "--authkey",
            self.authkey_str,
            "--native-dir",
            str(self.native_dir),
            "--config-path",
            str(self.method_config_path),
            "--method-root",
            str(self.method_root),
        ]

        self.log_file = self.worker_log_path.open("a", encoding="utf-8")
        self.process = subprocess.Popen(
            cmd_args,
            cwd=str(self.project_root),
            stdout=self.log_file,
            stderr=subprocess.STDOUT,
        )

        # Accept incoming connection from spawned worker
        try:
            self.conn = self.listener.accept()
            ready_msg = self.conn.recv()
            if not ready_msg.get("success"):
                err = ready_msg.get("error", "Unknown worker initialization failure")
                tb = ready_msg.get("traceback", "")
                raise RuntimeError(f"Worker startup failed: {err}\n{tb}")
        except Exception as exc:
            self.close()
            log_content = self._read_recent_log()
            raise RuntimeError(
                f"Failed to establish IPC handshake with method worker '{method_id}': {exc}\n"
                f"Recent worker log output:\n{log_content}"
            ) from exc

    def _read_recent_log(self, max_chars: int = 2000) -> str:
        """Read recent output lines from worker log for error reporting."""
        if not self.worker_log_path.is_file():
            return "<no log output>"
        try:
            content = self.worker_log_path.read_text(encoding="utf-8", errors="replace")
            return content[-max_chars:] if len(content) > max_chars else content
        except Exception:
            return "<error reading log>"

    def _send_command(self, command: WorkerCommand) -> WorkerResponse:
        """Send command over IPC, handle worker failure, and receive response."""
        if self.process.poll() is not None:
            raise RuntimeError(
                f"Method worker process terminated unexpectedly (exit code {self.process.returncode}).\n"
                f"Log snippet:\n{self._read_recent_log()}"
            )

        try:
            self.conn.send(command.to_dict())
            raw_response = self.conn.recv()
            return WorkerResponse.from_dict(raw_response)
        except Exception as exc:
            raise RuntimeError(
                f"IPC communication failure with worker '{self.method_id}': {exc}\n"
                f"Log snippet:\n{self._read_recent_log()}"
            ) from exc

    def start(self, case: CaseRecord) -> AdapterResult:
        """Start method interview and return first question."""
        cmd = WorkerCommand(cmd="start", case=case.to_dict())
        resp = self._send_command(cmd)
        if not resp.success:
            raise RuntimeError(f"Worker failed on 'start': {resp.error}\n{resp.traceback or ''}")
        return AdapterResult.from_dict(resp.data or {})

    def submit_answer(self, answer: str) -> AdapterResult:
        """Submit stakeholder answer and advance to next turn."""
        cmd = WorkerCommand(cmd="submit_answer", answer=answer)
        resp = self._send_command(cmd)
        if not resp.success:
            raise RuntimeError(f"Worker failed on 'submit_answer': {resp.error}\n{resp.traceback or ''}")
        return AdapterResult.from_dict(resp.data or {})

    def inspect(self) -> AdapterResult:
        """Inspect current status without stepping."""
        cmd = WorkerCommand(cmd="inspect")
        resp = self._send_command(cmd)
        if not resp.success:
            raise RuntimeError(f"Worker failed on 'inspect': {resp.error}\n{resp.traceback or ''}")
        return AdapterResult.from_dict(resp.data or {})

    def resume(self, case: CaseRecord) -> AdapterResult:
        """Resume session from checkpoint/transcript."""
        cmd = WorkerCommand(cmd="resume", case=case.to_dict())
        resp = self._send_command(cmd)
        if not resp.success:
            raise RuntimeError(f"Worker failed on 'resume': {resp.error}\n{resp.traceback or ''}")
        return AdapterResult.from_dict(resp.data or {})

    def close(self) -> None:
        """Terminate worker process cleanly."""
        try:
            if hasattr(self, "conn") and self.conn:
                try:
                    self.conn.send({"cmd": "close"})
                    self.conn.recv()
                except Exception:
                    pass
                self.conn.close()
        finally:
            if hasattr(self, "listener") and self.listener:
                try:
                    self.listener.close()
                except Exception:
                    pass

            if hasattr(self, "process") and self.process:
                if self.process.poll() is None:
                    try:
                        self.process.terminate()
                        self.process.wait(timeout=3.0)
                    except Exception:
                        self.process.kill()

            if hasattr(self, "log_file") and self.log_file and not self.log_file.closed:
                try:
                    self.log_file.close()
                except Exception:
                    pass

            # Scrub any machine paths from worker.log
            if hasattr(self, "worker_log_path") and self.worker_log_path.is_file():
                try:
                    from interview.storage.sanitizer import sanitize_text
                    raw_log = self.worker_log_path.read_text(encoding="utf-8", errors="replace")
                    sanitized_log = sanitize_text(raw_log, project_root=self.project_root)
                    self.worker_log_path.write_text(sanitized_log, encoding="utf-8")
                except Exception:
                    pass
