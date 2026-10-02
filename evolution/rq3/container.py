"""Docker adapter that builds the shared coding image and manages task containers."""

import subprocess
import uuid
from pathlib import Path
from typing import Protocol

from evolution.rq3.config import CodingConfig
from evolution.rq3.models import CommandResult, ImageBuildResult

DOCKERFILE_PATH = Path(__file__).resolve().parent / "container" / "Dockerfile"


class ContainerSettings(Protocol):
    """Image and network selection shared by coding and verification containers."""

    image: str
    network: str


WORKSPACE_MOUNT = "/workspace"
# Written to stderr by the timeout utility whenever the deadline makes it send a signal.
TIMEOUT_SIGNAL_MARKER = "timeout: sending signal"
_DOCKER_ENCODING = {"text": True, "encoding": "utf-8", "errors": "replace"}


def build_image(coding_config: CodingConfig) -> ImageBuildResult:
    """Build the shared coding image from the bundled Dockerfile."""
    context_dir = DOCKERFILE_PATH.parent
    completed = subprocess.run(
        ["docker", "build", "-t", coding_config.image, "-f", str(DOCKERFILE_PATH), str(context_dir)],
        capture_output=True,
        **_DOCKER_ENCODING,
    )
    log = completed.stdout + completed.stderr
    if completed.returncode != 0:
        return ImageBuildResult(
            status="failed",
            image=coding_config.image,
            log=log,
            error=f"docker build exited with code {completed.returncode}.",
        )
    return ImageBuildResult(status="success", image=coding_config.image, log=log)


def create_container(container_settings: ContainerSettings, workspace_dir: Path | str) -> str:
    """Start a detached container that mounts only the given task workspace."""
    container_name = f"rq3-{uuid.uuid4().hex[:12]}"
    mount = f"{Path(workspace_dir).resolve().as_posix()}:{WORKSPACE_MOUNT}"
    subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "--name",
            container_name,
            "-w",
            WORKSPACE_MOUNT,
            "-v",
            mount,
            "--network",
            container_settings.network,
            container_settings.image,
            "sleep",
            "infinity",
        ],
        check=True,
        capture_output=True,
        **_DOCKER_ENCODING,
    )
    return container_name


def execute_in_container(container_id: str, command: str, timeout: float) -> CommandResult:
    """Run one shell command inside a running task container.

    The command is bounded by the container-side timeout utility, so that the
    deadline terminates the command and its child processes inside the container
    instead of only releasing the caller on the host. The command writes both of
    its streams to the captured stdout, which keeps the timeout utility's own
    diagnostics on stderr, where they alone decide whether a timeout happened.
    """
    completed = subprocess.run(
        [
            "docker",
            "exec",
            "-w",
            WORKSPACE_MOUNT,
            container_id,
            "timeout",
            "--verbose",
            "--kill-after=1",
            f"{timeout:g}",
            "bash",
            "-lc",
            f"exec 2>&1; {command}",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        **_DOCKER_ENCODING,
    )
    return CommandResult(
        command=command,
        output=completed.stdout,
        returncode=completed.returncode,
        timed_out=TIMEOUT_SIGNAL_MARKER in completed.stderr,
    )


def cleanup_container(container_id: str) -> CommandResult:
    """Stop and remove a task container and report the outcome of the removal."""
    completed = subprocess.run(
        ["docker", "rm", "-f", container_id],
        capture_output=True,
        **_DOCKER_ENCODING,
    )
    return CommandResult(
        command=f"docker rm -f {container_id}",
        output=(completed.stdout + completed.stderr).strip(),
        returncode=completed.returncode,
    )