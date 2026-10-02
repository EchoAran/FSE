"""Worker entry that runs mini-swe-agent against one coding task container.

The module is executed by the interpreter of the dedicated mini-swe-agent
environment, so the agent, its model client and the container adapter share a
single process while the container itself stays under the runner's control.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any

import yaml
from minisweagent import package_dir
from minisweagent.agents.default import DefaultAgent
from minisweagent.exceptions import Submitted
from minisweagent.models.litellm_model import LitellmModel

from evolution.rq3.container import WORKSPACE_MOUNT, execute_in_container
from evolution.rq3.coding import MODEL_API_BASE_ENV, MODEL_API_KEY_ENV, sanitize_run_data

SUBMIT_MARKER = "COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"


class RunAgent(DefaultAgent):
    """Serialize trajectories without model connection details or absolute host paths."""

    def serialize(self, *extra_dicts) -> dict:
        return sanitize_run_data(
            super().serialize(*extra_dicts), os.environ[MODEL_API_BASE_ENV], os.environ[MODEL_API_KEY_ENV]
        )


class ContainerEnvironment:
    """mini-swe-agent environment that forwards agent actions to a task container."""

    def __init__(self, container_id: str, command_timeout_seconds: float) -> None:
        self.container_id = container_id
        self.command_timeout_seconds = command_timeout_seconds
        self.config = {"container_id": container_id, "cwd": WORKSPACE_MOUNT}
        self._system_vars = self._read_system_vars()

    def execute(self, action: dict, cwd: str = "") -> dict[str, Any]:
        """Run one agent action inside the container and return its observation."""
        result = execute_in_container(self.container_id, action["command"], self.command_timeout_seconds)
        observation: dict[str, Any] = {
            "output": result.output,
            "returncode": result.returncode,
            "exception_info": "",
        }
        if result.timed_out:
            observation["exception_info"] = (
                f"Command exceeded the {self.command_timeout_seconds} second timeout and was killed."
            )
        self._check_finished(observation)
        return observation

    def get_template_vars(self, **kwargs) -> dict[str, Any]:
        return {**self._system_vars, **kwargs}

    def serialize(self) -> dict:
        return {
            "info": {
                "environment": {
                    "environment_type": f"{self.__class__.__module__}.{self.__class__.__name__}",
                    "container_id": self.container_id,
                },
            },
        }

    def _read_system_vars(self) -> dict[str, str]:
        """Read the uname fields that the agent templates render."""
        result = execute_in_container(
            self.container_id, "uname -s; uname -r; uname -v; uname -m", self.command_timeout_seconds
        )
        system, release, version, machine = result.output.strip().splitlines()
        return {"system": system, "release": release, "version": version, "machine": machine}

    def _check_finished(self, observation: dict[str, Any]) -> None:
        """Raise Submitted when an observation reports task completion."""
        lines = observation["output"].lstrip().splitlines(keepends=True)
        if lines and lines[0].strip() == SUBMIT_MARKER and observation["returncode"] == 0:
            submission = "".join(lines[1:])
            raise Submitted(
                {
                    "role": "exit",
                    "content": submission,
                    "extra": {"exit_status": "Submitted", "submission": submission},
                }
            )


def load_agent_settings() -> tuple[dict[str, Any], dict[str, Any]]:
    """Read the packaged mini-swe-agent defaults for agent and model behaviour."""
    config = yaml.safe_load((package_dir / "config" / "mini.yaml").read_text(encoding="utf-8"))
    agent_settings = dict(config["agent"])
    agent_settings.pop("mode", None)
    return agent_settings, dict(config.get("model", {}))


def run_agent(spec: dict[str, Any]) -> None:
    """Run the agent on one task and save its trajectory."""
    agent_settings, model_settings = load_agent_settings()
    agent_settings["step_limit"] = spec["step_limit"]
    agent_settings["cost_limit"] = spec["cost_limit"]
    trajectory_path = Path(spec["trajectory_path"])
    agent_settings["output_path"] = trajectory_path

    # LiteLLM reads the configured API base and key from the worker environment,
    # keeping connection details out of the serialized model configuration.
    model = LitellmModel(model_name=spec["model_name"], **model_settings)

    environment = ContainerEnvironment(spec["container_id"], spec["command_timeout_seconds"])
    agent = RunAgent(model, environment, **agent_settings)
    try:
        agent.run(task=spec["task_statement"])
    finally:
        agent.save(trajectory_path)


def main() -> None:
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    run_agent(spec)


if __name__ == "__main__":
    main()