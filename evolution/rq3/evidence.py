"""Evidence collection from the software that one coding run delivered.

Collection mounts a disposable copy of the delivered source tree in a fresh
container, so build, run, interface and file observations are recorded as files
next to the coding artifacts while the agent's own output stays untouched.
"""

import re
import shlex
import shutil
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Sequence

from evolution.rq3.container import (
    WORKSPACE_MOUNT,
    cleanup_container,
    create_container,
    execute_in_container,
)
from evolution.rq3.models import (
    CodingResult,
    CommandLog,
    CommandResult,
    DeliverySpec,
    EvidenceRecord,
    InvocationSpec,
    ScenarioRecord,
    SourceLocation,
    StrictBaseModel,
    UiStep,
    VerificationResult,
)
from evolution.rq3.storage import atomic_write_json, read_json

EVIDENCE_DIR_NAME = "evidence"
EVIDENCE_RECORDS_NAME = "evidence.json"
VERIFICATION_RECORD_NAME = "verification.json"
SOURCE_INDEX_NAME = "source_index.json"
BUILD_RUN_SCENARIO = "build_run"
DELIVERY_FILE_NAME = "delivery.json"

# Directory inside the mounted workspace that receives raw collection output.
COLLECTION_DIR_NAME = ".rq3-evidence"

SOURCE_EXTENSIONS = {
    ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".java", ".cs", ".go", ".rs",
    ".rb", ".php", ".c", ".h", ".cpp", ".hpp", ".sh", ".bash", ".sql", ".html", ".css",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".md", ".txt", ".xml", ".csv",
}
SKIPPED_DIRECTORIES = {
    ".git", "__pycache__", "node_modules", ".venv", "venv", ".mypy_cache", COLLECTION_DIR_NAME,
}
SOURCE_MAX_BYTES = 1_000_000

COMMAND_RECORD_SUFFIX = "command.json"
STEP_EXIT_PATTERN = re.compile(r"^step (\d+) exit=(\d+)$")

UI_SCREEN_GEOMETRY = "1280x1280x24"
UI_WINDOW_SIZE = "1280,1280"


class VerificationConfig(StrictBaseModel):
    """Container settings used to observe one delivered implementation."""

    artifacts_root: Path
    image: str = "rq3-coding"
    network: str = "none"
    command_timeout_seconds: float = 60.0


@dataclass(frozen=True)
class VerificationSession:
    """Disposable workspace and container that host one collection attempt."""

    container_id: str
    workspace: Path
    run_dir: Path
    case_id: str
    method_id: str
    run_index: int
    artifacts_root: Path

    def collection_dir(self, scenario_id: str) -> str:
        """Container path that receives the raw output of one scenario collection."""
        return f"{WORKSPACE_MOUNT}/{COLLECTION_DIR_NAME}/{scenario_id}"

    def host_collection_dir(self, scenario_id: str) -> Path:
        """Host path of the same raw collection output."""
        return self.workspace / COLLECTION_DIR_NAME / scenario_id

    def evidence_dir(self, scenario_id: str) -> Path:
        """Directory that permanently holds the artifacts of one scenario."""
        return evidence_directory(self.artifacts_root, self.case_id, self.method_id, self.run_index) / scenario_id


def run_directory(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
    run_index: int,
) -> Path:
    """Locate the directory that holds one coding run's artifacts."""
    return Path(artifacts_root).resolve() / "cases" / case_id / method_id / "runs" / f"run_{run_index:02d}"


def evidence_directory(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
    run_index: int,
) -> Path:
    """Locate the directory that holds one coding run's collected evidence."""
    return run_directory(artifacts_root, case_id, method_id, run_index) / EVIDENCE_DIR_NAME


def load_invocations(path: Path | str) -> list[InvocationSpec]:
    """Read the invocation descriptions that drive evidence collection."""
    resolved_path = Path(path).resolve()
    if not resolved_path.exists():
        raise FileNotFoundError(f"Invocation file not found: {resolved_path}")

    data: Any = read_json(resolved_path)
    if not isinstance(data, list):
        raise ValueError(f"Invocation file {resolved_path} must contain a JSON array of descriptions.")
    return [InvocationSpec.model_validate(entry) for entry in data]


def collect_build_run(result: CodingResult, container_config: VerificationConfig) -> VerificationResult:
    """Execute the delivered build and run entries and record their commands.

    A missing delivery file is reported as a missing entry rather than a failed
    build, because the agent never declared how the software is started.
    """
    with _verification_session(result, container_config) as session:
        delivery_path = session.workspace / DELIVERY_FILE_NAME
        if not delivery_path.exists():
            return VerificationResult(
                case_id=result.case_id,
                method_id=result.method_id,
                run_index=result.run_index,
                status="entry_missing",
                error=f"{DELIVERY_FILE_NAME} is missing from the workspace delivered by {result.task_id}.",
            )

        delivery = DeliverySpec.model_validate(read_json(delivery_path))
        timeout = container_config.command_timeout_seconds
        evidence = [_store_source_index(session)]
        logs: dict[str, CommandLog] = {}

        for label, command in (("build", delivery.build_command), ("run", delivery.run_command)):
            if not command:
                continue
            context = f"{label.capitalize()} command"
            if label == "run" and delivery.interface_type == "http":
                worker = Path(__file__).with_name("http_startup.py").read_text(encoding="utf-8")
                command = (f"python3 -c {shlex.quote(worker)} {shlex.quote(command)} "
                           f"{shlex.quote(delivery.local_url)} {timeout:g}")
                context = f"HTTP startup probe at {delivery.local_url}"
            logs[label] = _capture_command(session, BUILD_RUN_SCENARIO, label, command, timeout)
            if label == "run":
                logs[label].command = delivery.run_command
            evidence.extend(
                _command_evidence(
                    session,
                    BUILD_RUN_SCENARIO,
                    label,
                    context,
                    logs[label],
                    start=len(evidence) + 1,
                )
            )

        return VerificationResult(
            case_id=result.case_id,
            method_id=result.method_id,
            run_index=result.run_index,
            status="collected",
            build=logs.get("build"),
            run=logs.get("run"),
            evidence=evidence,
        )


def collect_scenario(
    result: CodingResult,
    scenario: ScenarioRecord,
    invocation: InvocationSpec,
    container_config: VerificationConfig,
) -> list[EvidenceRecord]:
    """Observe one scenario of a delivered implementation and record its evidence."""
    _require_matching_invocation(result, scenario, invocation)
    if invocation.interface_type == "unavailable":
        root = Path(container_config.artifacts_root).resolve()
        target = evidence_directory(root, result.case_id, result.method_id, result.run_index) / scenario.scenario_id / "limitation.txt"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(invocation.unavailable.reason, encoding="utf-8")
        return [EvidenceRecord(
            evidence_id=f"EV-{result.run_index:02d}-{scenario.scenario_id}-01",
            case_id=result.case_id, method_id=result.method_id, run_index=result.run_index,
            scenario_id=scenario.scenario_id, evidence_type="observation_limit",
            relative_path=_relative(target, root), summary=invocation.unavailable.reason,
        )]
    with _verification_session(result, container_config) as session:
        return _COLLECTORS[invocation.interface_type](session, invocation)


def index_source(workspace: Path | str) -> list[SourceLocation]:
    """Index the delivered source tree into path and line references."""
    root = Path(workspace).resolve()
    locations: list[SourceLocation] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in SKIPPED_DIRECTORIES for part in relative.parts):
            continue
        if path.suffix.lower() not in SOURCE_EXTENSIONS or path.stat().st_size > SOURCE_MAX_BYTES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            locations.append(SourceLocation(path=relative.as_posix(), line=number, snippet=line))
    return locations


def save_evidence(records: Sequence[EvidenceRecord], output_dir: Path | str) -> None:
    """Write the evidence records of one run to a JSON index."""
    atomic_write_json(
        Path(output_dir).resolve() / EVIDENCE_RECORDS_NAME,
        [record.model_dump(mode="json") for record in records],
    )


def save_verification_result(result: VerificationResult, output_dir: Path | str) -> None:
    """Write the build and run verification of one run to a JSON record."""
    atomic_write_json(Path(output_dir).resolve() / VERIFICATION_RECORD_NAME, result)


def load_evidence(output_dir: Path | str) -> list[EvidenceRecord]:
    """Read the evidence records of one run from their JSON index."""
    data: Any = read_json(Path(output_dir).resolve() / EVIDENCE_RECORDS_NAME)
    return [EvidenceRecord.model_validate(entry) for entry in data]


def load_verification_result(output_dir: Path | str) -> VerificationResult:
    """Read the build and run verification of one run from its JSON record."""
    return VerificationResult.model_validate(
        read_json(Path(output_dir).resolve() / VERIFICATION_RECORD_NAME)
    )


def load_run_evidence(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
    run_index: int,
) -> list[EvidenceRecord]:
    """Read the evidence records of one coding run."""
    return load_evidence(evidence_directory(artifacts_root, case_id, method_id, run_index))


def load_run_verification(
    artifacts_root: Path | str,
    case_id: str,
    method_id: str,
    run_index: int,
) -> VerificationResult:
    """Read the build and run verification of one coding run."""
    return load_verification_result(evidence_directory(artifacts_root, case_id, method_id, run_index))


@contextmanager
def _verification_session(
    result: CodingResult,
    container_config: VerificationConfig,
) -> Iterator[VerificationSession]:
    """Mount a disposable copy of the delivered source tree in a fresh container."""
    run_dir = run_directory(
        container_config.artifacts_root, result.case_id, result.method_id, result.run_index
    )
    source_workspace = run_dir / "workspace"
    if not source_workspace.is_dir():
        raise FileNotFoundError(f"No delivered workspace is available for {result.task_id}: {source_workspace}")

    mount_root = Path(tempfile.mkdtemp(prefix="rq3-verify-"))
    container_id: str | None = None
    try:
        workspace = mount_root / "workspace"
        shutil.copytree(source_workspace, workspace)
        container_id = create_container(container_config, workspace)
        yield VerificationSession(
            container_id=container_id,
            workspace=workspace,
            run_dir=run_dir,
            case_id=result.case_id,
            method_id=result.method_id,
            run_index=result.run_index,
            artifacts_root=Path(container_config.artifacts_root).resolve(),
        )
    finally:
        try:
            if container_id is not None:
                _remove_container(container_id)
        finally:
            shutil.rmtree(mount_root)


def _remove_container(container_id: str) -> None:
    """Remove the verification container and report a removal that did not succeed."""
    cleaned = cleanup_container(container_id)
    if cleaned.returncode != 0:
        raise RuntimeError(f"Failed to remove verification container {container_id}: {cleaned.output}")


def _collect_cli(session: VerificationSession, invocation: InvocationSpec) -> list[EvidenceRecord]:
    """Run the delivered command line entry with the recorded input."""
    log = _capture_command(
        session,
        invocation.scenario_id,
        "cli",
        invocation.cli.command,
        invocation.timeout_seconds,
        invocation.cli.stdin,
        invocation.working_directory,
    )
    return _command_evidence(session, invocation.scenario_id, "cli", "Command line entry", log)


def _collect_http(session: VerificationSession, invocation: InvocationSpec) -> list[EvidenceRecord]:
    """Replay preparation and the target action against the same service and session."""
    spec = invocation.http
    container_dir = session.collection_dir(invocation.scenario_id)
    lines = _script_header(session, invocation)
    lines.append(f'nohup bash -lc {shlex.quote(spec.start_command)} > "{container_dir}/service.log" 2>&1 &')
    lines.append("service_pid=$!")
    lines.append(f"sleep {spec.wait_seconds:g}")
    worker = Path(__file__).with_name("http_probe.py").read_text(encoding="utf-8")
    lines.append("# HTTP scenario probe")
    lines.append(
        f'python3 -c {shlex.quote(worker)} {shlex.quote(spec.model_dump_json())} '
        f'"{container_dir}" {invocation.timeout_seconds:g} '
        f'> "{container_dir}/probe.stdout.txt" 2> "{container_dir}/probe.stderr.txt"'
    )
    lines.append(f'echo -n "$?" > "{container_dir}/probe.rc"')
    lines.append('kill "$service_pid" 2>/dev/null')
    result = _run_script(session, lines, invocation.timeout_seconds)

    target_step = len(spec.setup) + 1
    target_response = session.host_collection_dir(invocation.scenario_id) / f"step_{target_step:02d}.response.txt"
    response = target_response.read_text(encoding="utf-8") if target_response.exists() else _collection_text(session, invocation, "response.txt")
    status = _collection_text(session, invocation, "status.txt").strip()
    probe_code = _collection_text(session, invocation, "probe.rc").strip()
    observed = (session.host_collection_dir(invocation.scenario_id) / "action.observed").exists()
    if result.timed_out:
        outcome = f"exceeded its {invocation.timeout_seconds:g} second collection timeout"
    elif observed:
        outcome = f"returned HTTP status {status}"
    else:
        outcome = f"did not execute the target action; the probe exited with code {probe_code}"
    records = [
        _record(
            session, invocation.scenario_id, 1, "http_response" if observed else "observation_limit",
            _store_artifact(session, invocation.scenario_id, "response.txt", response),
            f"{spec.method} {spec.url} {outcome}.",
        ),
        _record(
            session, invocation.scenario_id, 2, "command_log" if observed else "observation_limit",
            _store_artifact(
                session, invocation.scenario_id, "service.log",
                _collection_text(session, invocation, "service.log"),
            ),
            f"Service log of the command that started the entry for {spec.url}.",
        ),
        _record(
            session, invocation.scenario_id, 3, "command_log" if observed else "observation_limit",
            _store_artifact(
                session, invocation.scenario_id, "probe.stderr.txt",
                _collection_text(session, invocation, "probe.stderr.txt"),
            ),
            f"Request diagnostics of the probe for {spec.url}.",
        ),
    ]
    for index in range(1, len(spec.setup) + len(spec.actions) + 2):
        name = f"step_{index:02d}.response.txt"
        path = session.host_collection_dir(invocation.scenario_id) / name
        if index == target_step or not path.exists():
            continue
        phase = "Preparation request" if index < target_step else "Follow-up action"
        records.append(_record(
            session, invocation.scenario_id, len(records) + 1,
            "http_response",
            _store_artifact(session, invocation.scenario_id, name, path.read_text(encoding="utf-8")),
            f"{phase} {index:02d} for {spec.method} {spec.url}.",
        ))
    return records


def _collect_ui(session: VerificationSession, invocation: InvocationSpec) -> list[EvidenceRecord]:
    """Launch the interface under Xvfb, apply the recorded steps and capture the screen."""
    spec = invocation.ui
    container_dir = session.collection_dir(invocation.scenario_id)
    launch = (
        f'chromium --no-sandbox --disable-dev-shm-usage --no-first-run --no-default-browser-check --window-size={UI_WINDOW_SIZE} {shlex.quote(spec.url)}'
        if spec.target == "browser"
        else spec.start_command
    )
    lines = _script_header(session, invocation)
    if spec.target == "browser" and spec.start_command:
        lines.append(f'nohup bash -lc {shlex.quote(spec.start_command)} > "{container_dir}/service.log" 2>&1 &')
        lines.append(f"sleep {spec.wait_seconds:g}")
    lines.append('export DISPLAY=:99')
    lines.append(f'Xvfb :99 -screen 0 {UI_SCREEN_GEOMETRY} > "{container_dir}/xvfb.log" 2>&1 &')
    lines.append("xvfb_pid=$!")
    lines.append("sleep 2")
    lines.append(f'{launch} > "{container_dir}/application.log" 2>&1 &')
    lines.append("application_pid=$!")
    lines.append(f"sleep {spec.wait_seconds:g}")
    for index, step in enumerate(spec.steps, start=1):
        label = f"step {index:02d}"
        lines.append(f'echo {shlex.quote(f"{label}: {step.action} {step.value}".strip())} >> "{container_dir}/steps.log"')
        lines.append(f'{_step_command(step)} >> "{container_dir}/steps.log" 2>&1')
        lines.append(f'echo {shlex.quote(f"{label} exit=")}$? >> "{container_dir}/steps.log"')
    lines.append(f'import -window root "{container_dir}/{spec.screenshot_name}"')
    lines.append('kill "$application_pid" 2>/dev/null')
    lines.append('kill "$xvfb_pid" 2>/dev/null')
    _run_script(session, lines, invocation.timeout_seconds)

    capture = session.host_collection_dir(invocation.scenario_id) / spec.screenshot_name
    if not capture.exists():
        raise RuntimeError(
            f"The interface capture {spec.screenshot_name} was not produced for scenario "
            f"{invocation.scenario_id}; the application log holds the launch output."
        )

    target = f"the browser at {spec.url}" if spec.target == "browser" else spec.start_command
    actions = "; ".join(step.action for step in spec.steps) or "none"
    failed_steps = _failed_steps(_collection_text(session, invocation, "steps.log"))
    step_summary = f"Recorded interface steps: {actions}."
    if failed_steps:
        step_summary += f" {len(failed_steps)} step(s) exited with a non-zero code: {', '.join(failed_steps)}."
    return [
        _record(
            session, invocation.scenario_id, 1, "ui_capture",
            _store_artifact(
                session, invocation.scenario_id, spec.screenshot_name,
                _collection_bytes(session, invocation, spec.screenshot_name),
            ),
            f"Screen capture of {target} after {len(spec.steps)} recorded steps.",
        ),
        _record(
            session, invocation.scenario_id, 2, "command_log",
            _store_artifact(
                session, invocation.scenario_id, "application.log",
                _collection_text(session, invocation, "application.log"),
            ),
            f"Application log of {target}.",
        ),
        _record(
            session, invocation.scenario_id, 3, "command_log",
            _store_artifact(
                session, invocation.scenario_id, "steps.log",
                _collection_text(session, invocation, "steps.log"),
            ),
            step_summary,
        ),
    ]


def _collect_file(session: VerificationSession, invocation: InvocationSpec) -> list[EvidenceRecord]:
    """Run the delivered command that writes files and inspect the produced outputs."""
    spec = invocation.file
    log = _capture_command(
        session,
        invocation.scenario_id,
        "output",
        spec.command,
        invocation.timeout_seconds,
        working_directory=invocation.working_directory,
    )
    _copy_output_files(session, invocation)

    records = _command_evidence(
        session,
        invocation.scenario_id,
        "output",
        f"Command that was expected to produce {len(spec.output_files)} file(s)",
        log,
    )
    for position, output in enumerate(spec.output_files, start=1):
        name = Path(output).name
        if (session.host_collection_dir(invocation.scenario_id) / "files" / name).exists():
            relative_path = _store_artifact(
                session, invocation.scenario_id, f"files/{name}",
                _collection_bytes(session, invocation, f"files/{name}"),
            )
            summary = f"{output} was produced: {_describe_file(session, invocation, name, spec.inspect_pdf)}"
        else:
            label = f"missing_{position:02d}"
            check = _capture_command(
                session,
                invocation.scenario_id,
                label,
                f"test -f {shlex.quote(output)}",
                invocation.timeout_seconds,
                working_directory=invocation.working_directory,
            )
            relative_path = _store_command_log(session, invocation.scenario_id, label, check)
            summary = (
                f"{output} was not produced by the command; "
                f"the file check exited with code {check.returncode}."
            )
        records.append(
            _record(session, invocation.scenario_id, len(records) + 1, "file_output", relative_path, summary)
        )
    return records


def _copy_output_files(session: VerificationSession, invocation: InvocationSpec) -> None:
    """Copy the files that the delivered command was expected to write into the evidence area."""
    spec = invocation.file
    container_dir = session.collection_dir(invocation.scenario_id)
    lines = _script_header(session, invocation)
    lines.append(f'mkdir -p "{container_dir}/files"')
    for output in spec.output_files:
        quoted = shlex.quote(output)
        name = Path(output).name
        lines.append(f'if [ -f {quoted} ]; then cp {quoted} "{container_dir}/files/{name}"; fi')
        if spec.inspect_pdf and Path(output).suffix.lower() == ".pdf":
            lines.append(f'if [ -f {quoted} ]; then pdfinfo {quoted} > "{container_dir}/files/{name}.pdfinfo.txt" 2>&1; fi')
            inspection = (
                "import json,sys; from pypdf import PdfReader; "
                "r=PdfReader(sys.argv[1]); "
                "print(json.dumps([{'page':i+1,'rotation':p.rotation,"
                "'size':[float(p.mediabox.width),float(p.mediabox.height)],"
                "'text':p.extract_text()} for i,p in enumerate(r.pages)],ensure_ascii=False))"
            )
            lines.append(
                f'if [ -f {quoted} ]; then python3 -c {shlex.quote(inspection)} {quoted} '
                f'> "{container_dir}/files/{name}.pages.json" 2>&1; fi'
            )
    _run_script(session, lines, invocation.timeout_seconds)


_COLLECTORS = {
    "cli": _collect_cli,
    "http": _collect_http,
    "ui": _collect_ui,
    "file": _collect_file,
}


def _require_matching_invocation(
    result: CodingResult,
    scenario: ScenarioRecord,
    invocation: InvocationSpec,
) -> None:
    """Reject an invocation that does not describe the task and scenario it is used for."""
    expected = (result.case_id, result.method_id, result.run_index, scenario.scenario_id)
    described = (invocation.case_id, invocation.method_id, invocation.run_index, invocation.scenario_id)
    if described != expected:
        raise ValueError(
            f"Invocation describes {described}, which does not match the requested "
            f"case, method, run and scenario {expected}."
        )


def _script_header(session: VerificationSession, invocation: InvocationSpec) -> list[str]:
    """Compose the opening lines of a collection script: output directory and working directory."""
    lines = [f'mkdir -p "{session.collection_dir(invocation.scenario_id)}"']
    if invocation.working_directory:
        lines.append(f'cd "{WORKSPACE_MOUNT}/{invocation.working_directory}"')
    return lines


def _step_command(step: UiStep) -> str:
    """Translate one recorded interface step into the command that performs it."""
    if step.action == "wait":
        return f"sleep {step.seconds:g}"
    if step.action == "key":
        return f"xdotool key -- {shlex.quote(step.value)}"
    if step.action == "type":
        return f"xdotool type --delay 50 -- {shlex.quote(step.value)}"
    horizontal, separator, vertical = step.value.partition(",")
    if not separator or not horizontal.strip() or not vertical.strip():
        raise ValueError(f"A click step needs 'x,y' coordinates, got '{step.value}'.")
    return f"xdotool mousemove {horizontal.strip()} {vertical.strip()} click 1"


def _failed_steps(steps_log: str) -> list[str]:
    """Collect the recorded interface steps whose command exited with a non-zero code."""
    failed: list[str] = []
    for line in steps_log.splitlines():
        match = STEP_EXIT_PATTERN.match(line.strip())
        if match and match.group(2) != "0":
            failed.append(f"step {match.group(1)}")
    return failed


def _run_script(session: VerificationSession, lines: Sequence[str], timeout: float) -> CommandResult:
    """Execute a generated collection script inside the verification container."""
    return execute_in_container(session.container_id, "\n".join(lines), timeout)


def _capture_command(
    session: VerificationSession,
    scenario_id: str,
    label: str,
    command: str,
    timeout: float,
    stdin_text: str = "",
    working_directory: str = "",
) -> CommandLog:
    """Run one command inside the container and keep its separate output streams.

    A command killed by the deadline leaves no exit code of its own, so the code
    reported by the container-side timeout utility is recorded instead.
    """
    container_dir = session.collection_dir(scenario_id)
    host_dir = session.host_collection_dir(scenario_id)
    host_dir.mkdir(parents=True, exist_ok=True)

    lines = [f'mkdir -p "{container_dir}"']
    if working_directory:
        lines.append(f'cd "{WORKSPACE_MOUNT}/{working_directory}"')
    stdin_redirect = " < /dev/null"
    if stdin_text:
        lines.append(f'cat > "{container_dir}/{label}.stdin.txt" <<\'RQ3_STDIN\'\n{stdin_text}\nRQ3_STDIN')
        stdin_redirect = f' < "{container_dir}/{label}.stdin.txt"'
    lines.append(
        f'({command}){stdin_redirect} > "{container_dir}/{label}.stdout.txt" '
        f'2> "{container_dir}/{label}.stderr.txt"'
    )
    lines.append(f'echo -n "$?" > "{container_dir}/{label}.rc"')
    result = _run_script(session, lines, timeout)

    code_path = host_dir / f"{label}.rc"
    returncode = int(code_path.read_text(encoding="utf-8").strip()) if code_path.exists() else result.returncode
    return CommandLog(
        command=command,
        working_directory=working_directory,
        returncode=returncode,
        timed_out=result.timed_out,
        stdout_path=_store_artifact(
            session, scenario_id, f"{label}.stdout.txt",
            (host_dir / f"{label}.stdout.txt").read_text(encoding="utf-8", errors="replace"),
        ),
        stderr_path=_store_artifact(
            session, scenario_id, f"{label}.stderr.txt",
            (host_dir / f"{label}.stderr.txt").read_text(encoding="utf-8", errors="replace"),
        ),
    )


def _store_source_index(session: VerificationSession) -> EvidenceRecord:
    """Index the delivered source tree and persist the index as source evidence."""
    locations = index_source(session.workspace)
    target = evidence_directory(
        session.artifacts_root, session.case_id, session.method_id, session.run_index
    ) / SOURCE_INDEX_NAME
    atomic_write_json(target, [location.model_dump(mode="json") for location in locations])
    files = len({location.path for location in locations})
    return _record(
        session, BUILD_RUN_SCENARIO, 1, "source_code",
        _relative(target, session.artifacts_root),
        f"Source index of the delivered workspace: {files} file(s), {len(locations)} line(s).",
    )


def _store_artifact(
    session: VerificationSession,
    scenario_id: str,
    name: str,
    content: str | bytes,
) -> str:
    """Persist one collected artifact next to the coding artifacts and return its relative path."""
    target = session.evidence_dir(scenario_id) / name
    target.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        target.write_bytes(content)
    else:
        target.write_text(content, encoding="utf-8")
    return _relative(target, session.artifacts_root)


def _command_evidence(
    session: VerificationSession,
    scenario_id: str,
    label: str,
    context: str,
    log: CommandLog,
    start: int = 1,
) -> list[EvidenceRecord]:
    """Record one command's metadata, standard output and standard error as artifacts."""
    return [
        _record(
            session, scenario_id, start, "command_log",
            _store_command_log(session, scenario_id, label, log),
            _command_summary(context, log),
        ),
        _record(
            session, scenario_id, start + 1, "command_log",
            log.stdout_path,
            f"Standard output of the {context.lower()}.",
        ),
        _record(
            session, scenario_id, start + 2, "command_log",
            log.stderr_path,
            f"Standard error of the {context.lower()}.",
        ),
    ]


def _store_command_log(
    session: VerificationSession,
    scenario_id: str,
    label: str,
    log: CommandLog,
) -> str:
    """Persist the command, directory, exit code and timeout of one recorded command."""
    target = session.evidence_dir(scenario_id) / f"{label}.{COMMAND_RECORD_SUFFIX}"
    atomic_write_json(target, log)
    return _relative(target, session.artifacts_root)


def _describe_file(
    session: VerificationSession,
    invocation: InvocationSpec,
    name: str,
    inspect_pdf: bool,
) -> str:
    """Report the size of a produced file and, for PDFs, its page count."""
    artifact = session.host_collection_dir(invocation.scenario_id) / "files" / name
    description = f"{artifact.stat().st_size} byte(s)"
    if not inspect_pdf:
        return description
    pdfinfo = _collection_text(session, invocation, f"files/{name}.pdfinfo.txt")
    pages = [line for line in pdfinfo.splitlines() if line.startswith("Pages:")]
    if pages:
        observations = _collection_text(session, invocation, f"files/{name}.pages.json")
        return f"{description}, {pages[0].strip().lower()}; page observations: {observations}"
    return description


def _collection_text(session: VerificationSession, invocation: InvocationSpec, name: str) -> str:
    """Read one raw collection output as text, or report that it was not written."""
    path = session.host_collection_dir(invocation.scenario_id) / name
    if not path.exists():
        return f"{name} was not written."
    return path.read_text(encoding="utf-8", errors="replace")


def _collection_bytes(session: VerificationSession, invocation: InvocationSpec, name: str) -> bytes:
    """Read one raw collection output as bytes."""
    return (session.host_collection_dir(invocation.scenario_id) / name).read_bytes()


def _command_summary(label: str, log: CommandLog) -> str:
    """Describe the directory and the outcome of one recorded command."""
    directory = log.working_directory or WORKSPACE_MOUNT
    if log.timed_out:
        return (
            f"{label} command in {directory} exceeded its timeout and was killed; "
            "its output was still recorded."
        )
    return f"{label} command in {directory} exited with code {log.returncode}."


def _record(
    session: VerificationSession,
    scenario_id: str,
    sequence: int,
    evidence_type: str,
    relative_path: str,
    summary: str,
) -> EvidenceRecord:
    """Compose one evidence record with its stable identifier."""
    return EvidenceRecord(
        evidence_id=f"EV-{session.run_index:02d}-{scenario_id}-{sequence:02d}",
        case_id=session.case_id,
        method_id=session.method_id,
        run_index=session.run_index,
        scenario_id=scenario_id,
        evidence_type=evidence_type,  # type: ignore[arg-type]
        relative_path=relative_path,
        summary=summary,
    )


def _relative(path: Path, artifacts_root: Path) -> str:
    return path.resolve().relative_to(artifacts_root).as_posix()
