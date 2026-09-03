import argparse
from datetime import datetime
import json
from pathlib import Path
import sys
import uuid

# Add root and src to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "src"))

from src.config import InterviewConfig
from src.interviewer import LLMREIInterviewer
from src.models import RequirementCase
from src.project_store import ProjectStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a new LLMREI-long requirements interview project.")
    parser.add_argument("--input", "-i", required=True, help="Path to input JSON file containing project_name and initial_requirements.")
    parser.add_argument("--config", "-c", default="config/default.yaml", help="Path to configuration YAML file.")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with input_path.open("r", encoding="utf-8") as f:
        input_data = json.load(f)

    project_name = input_data.get("project_name", "Untitled Project")
    initial_requirements = input_data.get("initial_requirements", "")
    project_id = input_data.get("case_id") or f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

    # Resolve config path
    config_path = Path(args.config)
    if not config_path.is_absolute():
        resolved_config = root_dir / args.config
        if resolved_config.is_file():
            config_path = resolved_config
        else:
            example_config = root_dir / "config" / "default.example.yaml"
            if example_config.is_file():
                config_path = example_config

    if not config_path.is_file():
        print(f"Error: Configuration file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    config = InterviewConfig.from_yaml(config_path)

    # Resolve relative paths in config against root_dir
    if not Path(config.runs_dir).is_absolute():
        config.runs_dir = str(root_dir / config.runs_dir)
    if not Path(config.prompt_path).is_absolute():
        config.prompt_path = str(root_dir / config.prompt_path)

    store = ProjectStore(base_runs_dir=config.runs_dir)
    store.init_project_dir(project_id, input_data)

    print(f"=== Initializing Project: {project_name} ===")

    case = RequirementCase(
        case_id=project_id,
        project_name=project_name,
        initial_requirements=initial_requirements,
    )

    interviewer = LLMREIInterviewer(config=config)
    interviewer.initialize(case)
    first_question = interviewer.get_first_question()

    transcript = interviewer.export_transcript()
    store.save_initial_state(transcript)
    store.save_transcript(transcript)

    print("\n--- Project Initialized Successfully ---")
    print(f"Project ID    : {project_id}")
    print(f"Runs Dir      : {store.get_project_dir(project_id)}")
    if interviewer.is_finished:
        print("Status        : FINISHED")
    else:
        print("\n[Interviewer First Question]:")
        print(first_question)
    print("----------------------------------------\n")


if __name__ == "__main__":
    main()
