"""Enumeration and execution of RQ3 coding tasks.

Each task renders a reviewed SRS into a task statement, runs mini-swe-agent in a
dedicated container that mounts only the task workspace, and records the exit
state, the delivered source tree, the agent trajectory and the model usage.
"""

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Iterable, Sequence

from evolution.rq3.config import CodingConfig
from evolution.rq3.container import cleanup_container, create_container
from evolution.rq3.models import CodingResult, CodingTask, SRSRecord
from evolution.rq3.srs import render_srs
from evolution.rq3.storage import atomic_write_json, atomic_write_text, read_json

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKER_MODULE = "evolution.rq3.agent_runtime"
# Environment variable that carries the configured model key into the worker process.
MODEL_API_KEY_ENV = "OPENAI_API_KEY"
MODEL_API_BASE_ENV = "OPENAI_BASE_URL"
SKIPPED_STATUSES = ("completed", "limits_exceeded")
TASK_STATEMENT_NAME = "task.md"
SUPERSEDED_DIR_NAME = "superseded"

DELIVERY_REQUIREMENTS = """\
## Delivery requirements

Implement the software described by the requirements above in `/workspace`.
`/workspace` is the only directory available to this task and starts empty.

1. Create a runnable program that implements the requirements.
2. Decide a build command, a test command and a run command for the program.
3. Run the build and test commands that apply and fix the problems you find.
4. Write `/workspace/delivery.json` describing how to build, test and run the program.

`delivery.json` is a JSON object with exactly these fields:

- `build_command`: shell command that prepares the program, or an empty string when no build step is needed
- `test_command`: shell command that runs the delivered tests, or an empty string when no tests are delivered
- `run_command`: shell command that starts the program
- `interface_type`: one of `http`, `cli`, `gui`, `file`
- `local_url`: URL that reaches the program when `interface_type` is `http`, otherwise an empty string
- `known_limitations`: list of strings describing what the delivered software does not do

An empty `test_command` records that no test entry point was delivered. It does
not mean that the software passes tests. Implement only what the requirements
state and do not assume behaviour that the requirements leave open.
"""


def create_tasks(
    srs_inputs: Iterable[Path | str],
    runs_per_srs: int,
    artifacts_root: Path | str,
) -> list[CodingTask]:
    """Enumerate one task per reviewed SRS and implementation run."""
    root = Path(artifacts_root).resolve()
    tasks: list[CodingTask] = []
    for srs_input in srs_inputs:
        srs_path = Path(srs_input).resolve()
        srs = SRSRecord.model_validate(read_json(srs_path))
        for run_index in range(1, runs_per_srs + 1):
            run_dir = root / "cases" / srs.case_id / srs.method_id / "runs" / f"run_{run_index:02d}"
            tasks.append(
                CodingTask(
                    task_id=f"{srs.case_id}__{srs.method_id}__run_{run_index:02d}",
                    case_id=srs.case_id,
                    method_id=srs.method_id,
                    run_index=run_index,
                    srs_file=str(srs_path),
                    artifacts_root=str(root),
                    run_dir=str(run_dir),
                    workspace_dir=str(run_dir / "workspace"),
                )
            )
    return tasks


def select_tasks(
    tasks: Sequence[CodingTask],
    case_id: str | None = None,
    method_id: str | None = None,
    run_indices: Sequence[int] | None = None,
) -> list[CodingTask]:
    """Select tasks by case, method and run index."""
    selected: list[CodingTask] = []
    for task in tasks:
        if case_id is not None and task.case_id != case_id:
            continue
        if method_id is not None and task.method_id != method_id:
            continue
        if run_indices is not None and task.run_index not in run_indices:
            continue
        selected.append(task)
    return selected


def render_task_statement(srs: SRSRecord) -> str:
    """Render the agent-facing task statement from a reviewed SRS."""
    header = (
        f"# Implementation task: {srs.project_name}\n\n"
        "The requirements below were elicited in an interview and reviewed before delivery.\n\n"
        "## Reviewed requirements\n\n"
    )
    return header + render_srs(srs, include_evidence=False) + "\n" + DELIVERY_REQUIREMENTS


def collect_token_usage(trajectory: dict[str, Any]) -> dict[str, int]:
    """Sum the token counters that the model reported over all agent steps."""
    totals = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    for message in trajectory.get("messages", []):
        usage = (message.get("extra", {}).get("response") or {}).get("usage") or {}
        for key in totals:
            totals[key] += usage.get(key) or 0
    return totals


def run_task(task: CodingTask, coding_config: CodingConfig) -> CodingResult:
    """Run one coding task end to end and persist its result.

    A finished result is reused only while the run recorded the same task input. An
    earlier attempt that was produced from a different reviewed SRS is moved aside, so
    the current input starts from an empty output directory while its deliverables stay.
    """
    run_dir = Path(task.run_dir)
    result_path = run_dir / "result.json"

    srs = SRSRecord.model_validate(read_json(Path(task.srs_file)))
    statement = render_task_statement(srs)
    recorded_input = _recorded_input(run_dir)

    existing = _read_previous_result(run_dir, recorded_input, statement)
    if existing is not None:
        return existing

    agent_python = _resolve_agent_python(coding_config)

    workspace_dir = Path(task.workspace_dir)
    if recorded_input is not None and recorded_input != statement:
        _supersede_attempt(run_dir)
    else:
        existing_output = _existing_output_reason(run_dir, workspace_dir)
        if existing_output is not None:
            return _build_result(task, "infrastructure_failed", existing_output)

    run_dir.mkdir(parents=True, exist_ok=True)
    workspace_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_text(run_dir / TASK_STATEMENT_NAME, statement)

    process_log_path = run_dir / "process.log"
    spec_path = run_dir / "run_spec.json"
    trajectory_path = run_dir / "trajectory.json"

    try:
        container_id = create_container(coding_config, workspace_dir)
    except subprocess.CalledProcessError as exc:
        log = _merged_output(exc.stdout, exc.stderr)
        log = sanitize_run_text(log, coding_config.api_url, coding_config.api_key)
        atomic_write_text(process_log_path, log)
        return _persist(
            result_path,
            _build_result(task, "infrastructure_failed", f"Container start failed: {log.strip()}"),
        )

    spec = {
        "task_id": task.task_id,
        "task_statement": statement,
        "container_id": container_id,
        "model_name": coding_config.model_name,
        "step_limit": int(coding_config.step_limit),
        "cost_limit": float(coding_config.cost_limit),
        "command_timeout_seconds": coding_config.command_timeout_seconds,
        "trajectory_path": trajectory_path.name,
    }
    atomic_write_json(spec_path, spec)

    try:
        try:
            log, exit_code = _run_worker(coding_config, agent_python, spec_path, process_log_path)
        except subprocess.TimeoutExpired:
            result = _build_result(
                task,
                "limits_exceeded",
                f"Task process exceeded wall_time_seconds={coding_config.wall_time_seconds}.",
            )
        except OSError as exc:
            result = _build_result(task, "infrastructure_failed", f"Agent worker could not be started: {exc}")
        except KeyboardInterrupt:
            _persist(
                result_path,
                _build_result(task, "interrupted", "Task execution was interrupted externally."),
            )
            raise
        else:
            result = _build_result_from_trajectory(task, trajectory_path, log, exit_code)
    finally:
        cleanup = cleanup_container(container_id)

    if cleanup.returncode != 0:
        cleanup_note = f"Container cleanup failed: {cleanup.output}"
        result.reason = f"{result.reason} {cleanup_note}" if result.reason else cleanup_note

    result.reason = sanitize_run_text(result.reason, coding_config.api_url, coding_config.api_key)
    return _persist(result_path, result)


def run_tasks(tasks: Sequence[CodingTask], coding_config: CodingConfig) -> list[CodingResult]:
    """Run tasks with bounded concurrency while preserving the input order."""
    with ThreadPoolExecutor(max_workers=coding_config.concurrency) as executor:
        return list(executor.map(lambda task: run_task(task, coding_config), tasks))


def _run_worker(
    coding_config: CodingConfig,
    agent_python: str,
    spec_path: Path,
    process_log_path: Path,
) -> tuple[str, int]:
    """Run the agent worker process and record its output.

    The configured model key and API base reach the worker through the environment of the child
    process, so it stays out of the run specification that the worker reads.
    """
    environment = {
        **os.environ,
        MODEL_API_KEY_ENV: coding_config.api_key,
        MODEL_API_BASE_ENV: coding_config.api_url,
        "MSWEA_SILENT_STARTUP": "1",
        "PYTHONPATH": os.pathsep.join([str(REPO_ROOT), os.environ.get("PYTHONPATH", "")]),
    }
    process = subprocess.Popen(
        [agent_python, "-m", WORKER_MODULE, str(spec_path)],
        cwd=spec_path.parent,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    try:
        log, _ = process.communicate(timeout=coding_config.wall_time_seconds)
    except subprocess.TimeoutExpired:
        process.kill()
        log, _ = process.communicate()
        log = sanitize_run_text(log, coding_config.api_url, coding_config.api_key)
        atomic_write_text(process_log_path, log)
        raise
    except KeyboardInterrupt:
        process.kill()
        log, _ = process.communicate()
        log = sanitize_run_text(log, coding_config.api_url, coding_config.api_key)
        atomic_write_text(process_log_path, log)
        raise
    log = sanitize_run_text(log, coding_config.api_url, coding_config.api_key)
    atomic_write_text(process_log_path, log)
    return log, process.returncode


def _build_result_from_trajectory(
    task: CodingTask,
    trajectory_path: Path,
    process_log: str,
    exit_code: int,
) -> CodingResult:
    """Read the outcome from the worker exit code and the trajectory it produced."""
    if not trajectory_path.exists():
        tail = process_log[-500:]
        return _build_result(
            task,
            "infrastructure_failed",
            f"Agent worker produced no trajectory (exit code {exit_code}). Log tail: {tail}",
        )

    trajectory = json.loads(trajectory_path.read_text(encoding="utf-8"))
    info = trajectory.get("info", {})
    model_stats = info.get("model_stats", {})
    status, reason = _interpret_exit_status(info, trajectory)
    if exit_code != 0:
        status = "infrastructure_failed"
        reason = (
            f"Agent worker exited with exit code {exit_code} while the trajectory recorded "
            f"{info.get('exit_status', '')!r}."
        )
    result = _build_result(task, status, reason)
    result.exit_status = info.get("exit_status", "")
    result.model_calls = model_stats.get("api_calls", 0)
    result.cost = model_stats.get("instance_cost", 0.0)
    result.usage = collect_token_usage(trajectory)
    return result


def _interpret_exit_status(info: dict[str, Any], trajectory: dict[str, Any]) -> tuple[str, str | None]:
    exit_status = info.get("exit_status", "")
    if exit_status == "Submitted":
        return "completed", None
    if exit_status in ("LimitsExceeded", "TimeExceeded"):
        return "limits_exceeded", f"Agent stopped after reaching the {exit_status} budget limit."
    if exit_status == "UserInterruption":
        return "interrupted", "Agent stopped after an external interruption."
    if exit_status == "RepeatedFormatError":
        return "infrastructure_failed", "Agent stopped after repeated model response format errors."
    return "infrastructure_failed", _agent_failure_message(exit_status, trajectory)


def _agent_failure_message(exit_status: str, trajectory: dict[str, Any]) -> str:
    messages = trajectory.get("messages", [])
    exception = messages[-1].get("extra", {}).get("exception_str", "") if messages else ""
    if exception:
        return f"Agent exited with status {exit_status!r}: {exception}"
    return f"Agent exited with unexpected status {exit_status!r}."


def _build_result(task: CodingTask, status: str, reason: str | None) -> CodingResult:
    artifacts_root = Path(task.artifacts_root)
    run_dir = Path(task.run_dir)
    return CodingResult(
        task_id=task.task_id,
        case_id=task.case_id,
        method_id=task.method_id,
        run_index=task.run_index,
        status=status,
        reason=reason,
        workspace_dir=_relative(Path(task.workspace_dir), artifacts_root),
        trajectory_path=_relative(run_dir / "trajectory.json", artifacts_root),
        process_log=_relative(run_dir / "process.log", artifacts_root),
    )


def _existing_output_reason(run_dir: Path, workspace_dir: Path) -> str | None:
    """Report why an earlier attempt's output stops a new run from starting.

    Every run owns an empty workspace and writes its own trajectory, so a
    directory that already holds output is refused instead of being cleared.
    """
    trajectory_path = run_dir / "trajectory.json"
    if trajectory_path.exists():
        return f"A trajectory from an earlier attempt exists at {trajectory_path}. Provide an empty run directory."
    if workspace_dir.exists() and any(workspace_dir.iterdir()):
        return f"Workspace {workspace_dir} already holds output. Provide an empty run directory."
    return None


def _persist(result_path: Path, result: CodingResult) -> CodingResult:
    atomic_write_json(result_path, result)
    return result


def _read_previous_result(
    run_dir: Path,
    recorded_input: str | None,
    statement: str,
) -> CodingResult | None:
    """Report the recorded result that may be reused for the current task input.

    Only a finished result that the run produced from the same task statement is reused.
    A result from another input belongs to a task that the current input replaced, and a
    run without a recorded input cannot be attributed to the current task at all.
    """
    result_path = run_dir / "result.json"
    if not result_path.exists():
        return None
    result = CodingResult.model_validate(read_json(result_path))
    if result.status not in SKIPPED_STATUSES or recorded_input != statement:
        return None
    return result


def _recorded_input(run_dir: Path) -> str | None:
    """Read the task statement that a run directory recorded when it started."""
    statement_path = run_dir / TASK_STATEMENT_NAME
    if not statement_path.exists():
        return None
    return statement_path.read_text(encoding="utf-8")


def _supersede_attempt(run_dir: Path) -> None:
    """Move an earlier attempt aside so the current input starts from an empty run directory.

    The attempt was produced from a reviewed SRS that the current input replaced, so it no
    longer answers this task. Its deliverables are kept under the superseded area of the
    method instead of being cleared.
    """
    attempts_dir = run_dir.parent.parent / SUPERSEDED_DIR_NAME / run_dir.name
    attempt = 1
    while (attempts_dir / f"attempt_{attempt:02d}").exists():
        attempt += 1
    target = attempts_dir / f"attempt_{attempt:02d}"
    target.parent.mkdir(parents=True, exist_ok=True)
    run_dir.rename(target)


def _resolve_agent_python(coding_config: CodingConfig) -> str:
    """Resolve the interpreter of the dedicated mini-swe-agent environment."""
    python_path = Path(coding_config.agent_python)
    if not python_path.is_absolute():
        python_path = REPO_ROOT / python_path
    return str(python_path)


def _merged_output(*streams: Any) -> str:
    parts = []
    for stream in streams:
        if stream is None:
            continue
        parts.append(stream.decode("utf-8", errors="replace") if isinstance(stream, bytes) else stream)
    return "".join(parts)


def _relative(path: Path, artifacts_root: Path) -> str:
    return path.resolve().relative_to(artifacts_root).as_posix()


def sanitize_run_text(text: str | None, api_url: str, api_key: str) -> str | None:
    """Remove model connection details and render host paths relative to the repository."""
    if text is None:
        return None
    text = text.replace(api_url.rstrip("/"), "[API URL removed]").replace(api_key, "[API key removed]")
    roots = {REPO_ROOT: "", Path(sys.prefix): "agent-python/", Path(sys.base_prefix): "python/", Path.home(): ""}
    for root, prefix in sorted(roots.items(), key=lambda item: len(str(item[0])), reverse=True):
        text = text.replace(str(root) + os.sep, prefix).replace(root.as_posix() + "/", prefix)
    return text


def sanitize_run_data(value: Any, api_url: str, api_key: str) -> Any:
    """Apply the run artifact privacy contract to serialized agent state."""
    if isinstance(value, dict):
        return {
            key: sanitize_run_data(item, api_url, api_key)
            for key, item in value.items()
            if key not in {"api_url", "api_base", "base_url"}
        }
    if isinstance(value, list):
        return [sanitize_run_data(item, api_url, api_key) for item in value]
    if isinstance(value, str):
        return sanitize_run_text(value, api_url, api_key)
    return value