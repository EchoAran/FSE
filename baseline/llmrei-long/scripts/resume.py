import argparse
from pathlib import Path
import sys

# Add root and src to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "src"))

from src.config import InterviewConfig
from src.interviewer import LLMREIInterviewer
from src.project_store import ProjectStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and resume an interrupted LLMREI-long interview session.")
    parser.add_argument("--project-id", "-p", required=True, help="Project ID to resume.")
    parser.add_argument("--config", "-c", default="config/default.yaml", help="Path to configuration YAML file.")
    args = parser.parse_args()

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
    if not Path(config.runs_dir).is_absolute():
        config.runs_dir = str(root_dir / config.runs_dir)

    store = ProjectStore(base_runs_dir=config.runs_dir)
    if not store.project_exists(args.project_id):
        print(f"Error: Project state not found for ID: {args.project_id}", file=sys.stderr)
        sys.exit(1)

    transcript = store.load_state(args.project_id)
    if transcript.is_finished:
        print(f"Error: Interview for project '{args.project_id}' is completed and cannot be resumed.", file=sys.stderr)
        sys.exit(1)
    if not transcript.pending_question:
        print(f"Error: Project '{args.project_id}' has no pending interviewer question.", file=sys.stderr)
        sys.exit(1)

    interviewer = LLMREIInterviewer(config=config)
    interviewer.resume_from_transcript(transcript)

    print(f"=== Validating & Resuming Project: {args.project_id} ===")
    print("\n--- Project Resumed Successfully ---")
    print(f"Project Name   : {transcript.project_name}")
    print("Project Status : In Progress")
    print(f"Current Turns  : {interviewer.turn_count}")

    if transcript.pending_question:
        print("\n[Active Question Awaiting Response]:")
        print(transcript.pending_question)
        print("\nTo advance the interview, run:")
        print(f"python scripts/step.py --project-id {args.project_id} --answer \"<your answer>\"")
    print("------------------------------------\n")


if __name__ == "__main__":
    main()
