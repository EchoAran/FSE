"""Loader and validator for requirement interview cases."""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union

from interview.cases.models import CaseRecord


class CaseLoader:
    """Loads and validates case records from cases.jsonl."""

    DEFAULT_CASES_PATH = Path("dataset/cases.jsonl")

    @classmethod
    def load_all(cls, cases_path: Optional[Union[str, Path]] = None) -> Dict[str, CaseRecord]:
        """Load all cases from a JSONL file, validating required fields and unique case_id."""
        resolved_path = Path(cases_path) if cases_path else cls.DEFAULT_CASES_PATH
        if not resolved_path.is_file():
            raise FileNotFoundError(f"Cases dataset file not found: {resolved_path}")

        cases: Dict[str, CaseRecord] = {}
        with resolved_path.open("r", encoding="utf-8") as f:
            for line_no, raw_line in enumerate(f, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSON at line {line_no} in {resolved_path}: {exc}") from exc

                case_id = payload.get("case_id")
                project_name = payload.get("project_name")
                initial_requirements = payload.get("initial_requirements")

                if not case_id or not isinstance(case_id, str) or not case_id.strip():
                    raise ValueError(f"Missing or empty 'case_id' at line {line_no} in {resolved_path}")
                if not project_name or not isinstance(project_name, str) or not project_name.strip():
                    raise ValueError(f"Missing or empty 'project_name' for case '{case_id}' at line {line_no}")
                if (
                    not initial_requirements
                    or not isinstance(initial_requirements, str)
                    or not initial_requirements.strip()
                ):
                    raise ValueError(f"Missing or empty 'initial_requirements' for case '{case_id}' at line {line_no}")

                case_id = case_id.strip()
                if case_id in cases:
                    raise ValueError(f"Duplicate 'case_id' detected: '{case_id}' at line {line_no}")

                cases[case_id] = CaseRecord(
                    case_id=case_id,
                    project_name=project_name.strip(),
                    initial_requirements=initial_requirements.strip(),
                )

        return cases

    @classmethod
    def get_case(cls, case_id: str, cases_path: Optional[Union[str, Path]] = None) -> CaseRecord:
        """Retrieve a specific case by its case_id."""
        cases = cls.load_all(cases_path)
        normalized_id = case_id.strip()
        if normalized_id not in cases:
            available_ids = ", ".join(list(cases.keys())[:10])
            raise KeyError(f"Case ID '{normalized_id}' not found. Available samples: {available_ids}...")
        return cases[normalized_id]

    @classmethod
    def list_case_ids(cls, cases_path: Optional[Union[str, Path]] = None) -> List[str]:
        """List all available case IDs in order."""
        cases = cls.load_all(cases_path)
        return list(cases.keys())
