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
    parser = argparse.ArgumentParser(description="Advance LLMREI-long interview by providing stakeholder response.")
    parser.add_argument("--project-id", "-p", required=True, help="Project ID.")
    parser.add_argument("--answer", "-a", required=True, help="Stakeholder's response text.")
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

    # Resolve relative paths
    if not Path(config.runs_dir).is_absolute():
        config.runs_dir = str(root_dir / config.runs_dir)
    if not Path(config.prompt_path).is_absolute():
        config.prompt_path = str(root_dir / config.prompt_path)

    store = ProjectStore(base_runs_dir=config.runs_dir)
    if not store.project_exists(args.project_id):
        print(f"Error: Project state not found for ID: {args.project_id}", file=sys.stderr)
        sys.exit(1)

    transcript = store.load_state(args.project_id)
    if transcript.is_finished:
        print(f"Notice: Interview for project '{args.project_id}' is already finished.")
        sys.exit(0)
    if not transcript.pending_question:
        print(f"Error: Project '{args.project_id}' has no pending interviewer question.", file=sys.stderr)
        sys.exit(1)

    interviewer = LLMREIInterviewer(config=config)
    interviewer.resume_from_transcript(transcript)

    print(f"\n[Interviewee Answer]: {args.answer}\n")
    print("Processing step...")

    next_question = interviewer.step(args.answer)
    updated_transcript = interviewer.export_transcript()

    store.save_state(updated_transcript)
    store.save_transcript(updated_transcript)

    print("\n--- Step Completed ---")
    print(f"Turn Index        : {interviewer.turn_count}")

    if interviewer.is_finished:
        print(f"Status            : FINISHED")
        print(f"Finish Message    : Interview completed.")
    else:
        print(f"Status            : ONGOING")
        print("\n[Interviewer Next Question]:")
        print(next_question)
    print("----------------------\n")


if __name__ == "__main__":
    main()
