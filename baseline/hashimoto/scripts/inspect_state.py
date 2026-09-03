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
    parser = argparse.ArgumentParser(description="Inspect current Hashimoto project state, slots, and abduction history.")
    parser.add_argument("--project-id", "-p", required=True, help="Project ID.")
    parser.add_argument("--config", "-c", default="config/default.yaml", help="Path to configuration YAML file.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all slots and full abduction history.")
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

    checkpoint = store.load_state(args.project_id)
    total_slots = len(checkpoint.slots)
    filled_slots = sum(1 for s in checkpoint.slots if s.is_filled)
    fill_rate = (filled_slots / total_slots) if total_slots > 0 else 0.0

    print("\n=======================================================")
    print(f" Project : {checkpoint.project_name} ({checkpoint.case_id})")
    print(f" Status  : {'Completed' if checkpoint.is_finished else 'Ongoing'} | Completed Turns: {len(checkpoint.turns)}")
    print(f" Coverage: {filled_slots}/{total_slots} slots ({fill_rate:.1%})")
    print(f" Abductions: {len(checkpoint.abduction_history)} reasoning records")
    print("=======================================================")

    print("\n--- Requirement Slots ---")
    grouped: dict[str, list] = {}
    for s in checkpoint.slots:
        grouped.setdefault(s.category, []).append(s)

    for cat, slots in sorted(grouped.items()):
        print(f"\n[{cat}]")
        for s in sorted(slots, key=lambda x: x.name):
            status = "[FILLED]" if s.is_filled else "[EMPTY] "
            val = f'"{s.value}"' if s.value else "<empty>"
            if args.verbose or s.is_filled:
                print(f"  * {status} {s.name}: {val}")
            else:
                print(f"  * {status} {s.name}")

    if checkpoint.abduction_history:
        print("\n--- Abductive Reasoning History ---")
        for idx, rec in enumerate(checkpoint.abduction_history, 1):
            print(f"  {idx}. Fact: {rec.surprising_fact}")
            print(f"     Reason: {rec.suspected_reason}")
            print(f"     New Slot: {rec.new_slot}")

    if checkpoint.pending_question and not checkpoint.is_finished:
        print(f"\n--- Pending Interviewer Question ---")
        if checkpoint.pending_target_slots:
            print(f"Target Slots: {', '.join(checkpoint.pending_target_slots)}")
        print(f"{checkpoint.pending_question}")

    print("\n--- Recent Dialogue Turns (Last 3) ---")
    for t in checkpoint.turns[-3:]:
        print(f"\n[Turn {t.turn_id}]")
        print(f"  Q: {t.interviewer_utterance}")
        print(f"  A: {t.interviewee_utterance}")
    print("=======================================================\n")


if __name__ == "__main__":
    main()
