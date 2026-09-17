import argparse
from pathlib import Path
import sys

# Add root and src to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "src"))

from src.config import InterviewConfig
from src.project_store import ProjectStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect current LLMREI-long project state and dialogue turns.")
    parser.add_argument("--project-id", "-p", required=True, help="Project ID.")
    parser.add_argument("--config", "-c", default="config/default.yaml", help="Path to configuration YAML file.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all dialogue turns.")
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

    print("\n=======================================================")
    print(f" Project : {transcript.project_name} ({transcript.case_id})")
    print(f" Status  : {'Completed' if transcript.is_finished else 'Ongoing'} | Completed Turns: {len(transcript.turns)}")
    print("=======================================================")

    print("\n--- Initial Requirements ---")
    print(transcript.initial_requirements.strip() or "<none>")

    if transcript.pending_question and not transcript.is_finished:
        print(f"\n--- Pending Interviewer Question ---")
        print(f"{transcript.pending_question}")

    turns_to_show = transcript.turns if args.verbose else transcript.turns[-3:]
    header = "--- All Dialogue Turns ---" if args.verbose else "--- Recent Dialogue Turns (Last 3) ---"
    print(f"\n{header}")
    for t in turns_to_show:
        print(f"\n[Turn {t.turn_id}]")
        print(f"  Q: {t.interviewer_utterance}")
        print(f"  A: {t.interviewee_utterance}")
    print("=======================================================\n")


if __name__ == "__main__":
    main()
