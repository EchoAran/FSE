"""Prompt template loader reading verbatim prompt files with robust path resolution."""

from pathlib import Path


class PromptLoader:
    """Loads prompt templates from disk with package-aware path resolution."""

    def __init__(self, base_path: str | Path | None = None) -> None:
        """Initialize loader with explicit base path or default to package root."""
        if base_path:
            self._base_path = Path(base_path).resolve()
        else:
            # Resolve to the root directory of the llmrei-long package
            self._base_path = Path(__file__).resolve().parent.parent.parent

    def load(self, prompt_path: str | Path) -> str:
        """Read and return the raw text content of a prompt template file."""
        target = Path(prompt_path)

        if target.is_absolute():
            resolved = target
        else:
            cwd_candidate = (Path.cwd() / target).resolve()
            package_candidate = (self._base_path / target).resolve()

            if cwd_candidate.is_file():
                resolved = cwd_candidate
            elif package_candidate.is_file():
                resolved = package_candidate
            else:
                resolved = cwd_candidate

        if not resolved.is_file():
            raise FileNotFoundError(f"Prompt template file not found at: {resolved}")

        return resolved.read_text(encoding="utf-8")
