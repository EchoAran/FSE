"""Registry for supported elicitation interview methods."""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple
import yaml


@dataclass(frozen=True)
class MethodDescriptor:
    """Metadata and paths descriptor for a registered interview method."""

    method_id: str
    relative_root: Path
    default_config: Path
    config_inspector: Callable[[Path], Tuple[Optional[str], Optional[int]]]

    def resolve_root(self, project_root: Path) -> Path:
        """Resolve method root directory, checking both methods/baseline/ and baseline/ layouts."""
        target = project_root / self.relative_root
        if target.is_dir():
            return target.resolve()
        # Fallback: if relative_root starts with methods/, check without methods/
        parts = self.relative_root.parts
        if len(parts) > 1 and parts[0] == "methods":
            alt = project_root / Path(*parts[1:])
            if alt.is_dir():
                return alt.resolve()
        return target.resolve()

    def resolve_default_config(self, project_root: Path) -> Path:
        """Resolve default config path, checking both layouts."""
        target = project_root / self.default_config
        if target.is_file():
            return target.resolve()
        parts = self.default_config.parts
        if len(parts) > 1 and parts[0] == "methods":
            alt = project_root / Path(*parts[1:])
            if alt.is_file():
                return alt.resolve()
        return target.resolve()


def _inspect_hashimoto_config(config_path: Path) -> Tuple[Optional[str], Optional[int]]:
    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("model"), data.get("max_turns")


def _inspect_llmrei_config(config_path: Path) -> Tuple[Optional[str], Optional[int]]:
    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("model"), data.get("max_turns")


def _inspect_sparkme_config(config_path: Path) -> Tuple[Optional[str], Optional[int]]:
    model_name = None
    max_turns = None
    with config_path.open("r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "=" in stripped:
                k, v = stripped.split("=", 1)
                k = k.strip()
                v = v.strip().strip("\"'")
                if k == "MODEL_NAME":
                    model_name = v
                elif k == "MAX_TURNS":
                    try:
                        max_turns = int(v)
                    except ValueError:
                        pass
    return model_name, max_turns


def _inspect_proposed_config(config_path: Path) -> Tuple[Optional[str], Optional[int]]:
    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    model_name = data.get("model", {}).get("model_name")
    max_turns = data.get("runtime", {}).get("max_turns")
    return model_name, max_turns


METHOD_REGISTRY: Dict[str, MethodDescriptor] = {
    "hashimoto": MethodDescriptor(
        method_id="hashimoto",
        relative_root=Path("methods/baseline/hashimoto"),
        default_config=Path("methods/baseline/hashimoto/config/default.yaml"),
        config_inspector=_inspect_hashimoto_config,
    ),
    "llmrei-long": MethodDescriptor(
        method_id="llmrei-long",
        relative_root=Path("methods/baseline/llmrei-long"),
        default_config=Path("methods/baseline/llmrei-long/config/default.yaml"),
        config_inspector=_inspect_llmrei_config,
    ),
    "sparkme": MethodDescriptor(
        method_id="sparkme",
        relative_root=Path("methods/baseline/sparkme"),
        default_config=Path("methods/baseline/sparkme/.env"),
        config_inspector=_inspect_sparkme_config,
    ),
    "proposed_method": MethodDescriptor(
        method_id="proposed_method",
        relative_root=Path("methods/proposed_method"),
        default_config=Path("methods/proposed_method/configs/default.yaml"),
        config_inspector=_inspect_proposed_config,
    ),
}


def get_method_descriptor(method_id: str) -> MethodDescriptor:
    """Retrieve method descriptor by its registered identifier."""
    normalized_id = method_id.strip().lower()
    if normalized_id not in METHOD_REGISTRY:
        supported = ", ".join(sorted(METHOD_REGISTRY.keys()))
        raise KeyError(f"Unsupported method '{method_id}'. Supported methods are: {supported}")
    return METHOD_REGISTRY[normalized_id]
