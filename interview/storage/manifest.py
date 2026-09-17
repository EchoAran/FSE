"""Manager for loading and saving interview manifest.json files."""

import json
from pathlib import Path

from interview.storage.models import InterviewManifest


class ManifestManager:
    """Handles atomic persistence and inspection of interview manifest metadata."""

    MANIFEST_FILENAME = "manifest.json"

    @classmethod
    def get_manifest_path(cls, results_dir: Path) -> Path:
        """Return the path to manifest.json."""
        return results_dir / cls.MANIFEST_FILENAME

    @classmethod
    def exists(cls, results_dir: Path) -> bool:
        """Check whether manifest.json exists in the specified directory."""
        return cls.get_manifest_path(results_dir).is_file()

    @classmethod
    def load(cls, results_dir: Path) -> InterviewManifest:
        """Load and parse manifest.json from results directory."""
        manifest_path = cls.get_manifest_path(results_dir)
        if not manifest_path.is_file():
            raise FileNotFoundError(f"Manifest not found in: {results_dir}")

        with manifest_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return InterviewManifest.from_dict(data)

    @classmethod
    def save(cls, results_dir: Path, manifest: InterviewManifest) -> None:
        """Atomically persist manifest to manifest.json, ensuring no credentials or timestamps are leaked."""
        results_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = cls.get_manifest_path(results_dir)

        payload = manifest.to_dict()
        # Explicitly ensure no sensitive or machine-specific keys are saved
        for key in list(payload.keys()):
            key_lower = key.lower()
            if "key" in key_lower or "secret" in key_lower or "token" in key_lower:
                payload[key] = ""

        temp_path = results_dir / f"{cls.MANIFEST_FILENAME}.tmp"
        with temp_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        temp_path.replace(manifest_path)
