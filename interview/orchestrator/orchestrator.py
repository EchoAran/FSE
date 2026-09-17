"""Core orchestrator executing requirements elicitation interviews."""

from pathlib import Path
import sys
from typing import Optional, Union

from interview.adapters.registry import get_method_descriptor
from interview.adapters.worker_client import ProcessWorkerClient
from interview.cases.loader import CaseLoader
from interview.cases.models import CaseRecord
from interview.config.interviewee_config import IntervieweeConfig
from interview.orchestrator.recovery import RecoveryManager
from interview.interviewee.agent import IntervieweeAgent
from interview.storage.conversation import ConversationLogger
from interview.storage.manifest import ManifestManager
from interview.storage.models import InterviewManifest, InterviewStatus, PendingAnswer
from interview.storage.pending_store import PendingAnswerStore


class InterviewOrchestrator:
    """Orchestrates multi-turn dialogue between method interviewers and interviewee agents."""

    def __init__(
        self,
        method_id: str,
        case_id: str,
        method_config_path: Optional[Union[str, Path]] = None,
        interviewee_config_path: Optional[Union[str, Path]] = None,
        cases_path: Optional[Union[str, Path]] = None,
        project_root: Optional[Union[str, Path]] = None,
        results_root: Optional[Union[str, Path]] = None,
    ) -> None:
        self.project_root = Path(project_root or Path.cwd()).resolve()
        self.descriptor = get_method_descriptor(method_id)
        self.method_id = self.descriptor.method_id

        # Load case record
        self.cases_path = Path(cases_path) if cases_path else self.project_root / "dataset" / "cases.jsonl"
        self.case: CaseRecord = CaseLoader.get_case(case_id, self.cases_path)

        # Resolve method configuration
        if method_config_path:
            self.method_config_path = Path(method_config_path).resolve()
        else:
            self.method_config_path = self.descriptor.resolve_default_config(self.project_root)

        if not self.method_config_path.is_file():
            # For proposed_method, check if default.example.yaml exists if default.yaml does not
            if self.method_id == "proposed_method":
                fallback = self.method_config_path.parent / "default.example.yaml"
                if fallback.is_file():
                    self.method_config_path = fallback
            if not self.method_config_path.is_file():
                raise FileNotFoundError(f"Method configuration file not found: {self.method_config_path}")

        # Resolve interviewee configuration
        self.interviewee_config_path: Optional[Path] = None
        self.interviewee_config: Optional[IntervieweeConfig] = None
        if interviewee_config_path:
            self.interviewee_config_path = Path(interviewee_config_path).resolve()
            self.interviewee_config = IntervieweeConfig.load_from_yaml(self.interviewee_config_path)

        # Establish standardized results paths
        self.results_root = Path(results_root).resolve() if results_root else (self.project_root / "results")
        self.results_dir = (self.results_root / self.method_id / self.case.case_id).resolve()
        self.native_dir = self.results_dir / "native"

    def run(self, interactive: bool = False) -> InterviewManifest:
        """Execute or resume interview session until completion or interruption."""
        # Check existing results directory
        if ManifestManager.exists(self.results_dir):
            existing_manifest = ManifestManager.load(self.results_dir)
            if existing_manifest.status == InterviewStatus.METHOD_FINISHED:
                print(
                    f"\n[Notice] Interview for '{self.method_id} x {self.case.case_id}' is already completed.\n"
                    f"Results directory: {self.results_dir} (read-only, overwrite rejected)."
                )
                return existing_manifest

            # Inspect current method configuration for consistency verification
            method_model, method_max_turns = self.descriptor.config_inspector(self.method_config_path)
            RecoveryManager.verify_config_consistency(
                existing_manifest=existing_manifest,
                method_model=method_model,
                method_max_turns=method_max_turns,
                interviewee_config=self.interviewee_config,
            )

            manifest = existing_manifest
            is_resuming = True
        else:
            # Initial run: extract config metadata and create manifest
            method_model, method_max_turns = self.descriptor.config_inspector(self.method_config_path)
            manifest = InterviewManifest(
                case_id=self.case.case_id,
                method_id=self.method_id,
                project_name=self.case.project_name,
                native_project_id=self.case.case_id,
                method_model=method_model,
                method_max_turns=method_max_turns,
                interviewee_model=self.interviewee_config.model.model_name if self.interviewee_config else None,
                status=InterviewStatus.INITIALIZED,
                completed_turns=0,
                native_path="native",
            )
            ManifestManager.save(self.results_dir, manifest)
            is_resuming = False

        # Prepare interviewee agent if automated mode
        interviewee_agent: Optional[IntervieweeAgent] = None
        if not interactive:
            if not self.interviewee_config:
                raise ValueError(
                    "Automated interview execution requires a valid interviewee configuration. "
                    "Provide --interviewee-config or specify --interactive."
                )
            interviewee_agent = IntervieweeAgent(self.interviewee_config)

        # Launch method in isolated worker subprocess
        adapter = ProcessWorkerClient(
            method_id=self.method_id,
            method_config_path=self.method_config_path,
            native_dir=self.native_dir,
            project_root=self.project_root,
        )

        try:
            if is_resuming:
                current_q, is_finished, completed_turns = RecoveryManager.reconcile_pending_answer(
                    results_dir=self.results_dir,
                    method_id=self.method_id,
                    adapter=adapter,
                    case=self.case,
                )
                manifest = ManifestManager.load(self.results_dir)
            else:
                start_result = adapter.start(self.case)
                current_q = start_result.question
                is_finished = start_result.finished
                completed_turns = start_result.turn_count

                # If method signals completion during initialization
                if is_finished:
                    manifest.status = InterviewStatus.METHOD_FINISHED
                    manifest.completed_turns = completed_turns
                    manifest.finish_message = (
                        start_result.finish_message
                        or "Interview method signaled completion during initialization."
                    )
                    if current_q and current_q.strip():
                        ConversationLogger.append_message(
                            results_dir=self.results_dir,
                            turn_index=0,
                            role="interviewer",
                            content=current_q,
                        )
                    ManifestManager.save(self.results_dir, manifest)
                    print(f"\n=======================================================")
                    print(f" Interview Completed Immediately: {self.method_id} x {self.case.case_id}")
                    print(f" Project          : {self.case.project_name}")
                    print(f" Results Dir      : {self.results_dir}")
                    print(f" Status           : {manifest.status.value}")
                    print(f" Finish Message   : {manifest.finish_message}")
                    print(f"=======================================================\n")
                    return manifest

                # Record first question into conversation.jsonl at turn_index=0
                ConversationLogger.append_message(
                    results_dir=self.results_dir,
                    turn_index=0,
                    role="interviewer",
                    content=current_q,
                )
                manifest.status = InterviewStatus.INITIALIZED
                manifest.completed_turns = completed_turns
                ManifestManager.save(self.results_dir, manifest)

            print(f"\n=======================================================")
            print(f" Interview Started: {self.method_id} x {self.case.case_id}")
            print(f" Project          : {self.case.project_name}")
            print(f" Results Dir      : {self.results_dir}")
            print(f" Status           : {manifest.status.value}")
            print(f"=======================================================\n")
            print(f"[Interviewer Initial Question]:\n{current_q}\n")

            # Main question-answer loop
            while not is_finished:
                next_turn_idx = completed_turns + 1

                # Generate stakeholder answer
                if interactive:
                    print(f"--- Turn {next_turn_idx} ---")
                    print(f"Interviewer asks: {current_q}")
                    answer = input("Stakeholder Response (or type 'exit' to pause) > ").strip()
                    if answer.lower() in ("exit", "quit"):
                        print("[Interrupted by user]")
                        manifest.status = InterviewStatus.INTERRUPTED
                        ManifestManager.save(self.results_dir, manifest)
                        break
                else:
                    assert interviewee_agent is not None
                    recent_pairs = ConversationLogger.get_recent_dialogue_pairs(
                        results_dir=self.results_dir,
                        window_size=self.interviewee_config.history_window_pairs,
                    )
                    print(f"[Generating Interviewee Answer for Turn {next_turn_idx}...]")
                    answer = interviewee_agent.respond(
                        case=self.case,
                        current_question=current_q,
                        recent_dialogue=recent_pairs,
                    )
                    print(f"[Interviewee Answer ({next_turn_idx})]:\n{answer}\n")

                # Record as pending answer before submitting to method
                PendingAnswerStore.save(
                    results_dir=self.results_dir,
                    pending=PendingAnswer(
                        turn_index=next_turn_idx,
                        question=current_q,
                        answer=answer,
                    ),
                )

                # Submit to method adapter
                step_res = adapter.submit_answer(answer)

                # Commit public dialogue records
                ConversationLogger.append_message(
                    results_dir=self.results_dir,
                    turn_index=next_turn_idx,
                    role="interviewee",
                    content=answer,
                )

                if not step_res.finished:
                    ConversationLogger.append_message(
                        results_dir=self.results_dir,
                        turn_index=next_turn_idx,
                        role="interviewer",
                        content=step_res.question,
                    )
                    current_q = step_res.question
                    is_finished = False
                    completed_turns = step_res.turn_count
                    manifest.status = InterviewStatus.RUNNING
                    manifest.completed_turns = completed_turns
                    print(f"[Interviewer Next Question ({completed_turns})]:\n{current_q}\n")
                else:
                    is_finished = True
                    completed_turns = step_res.turn_count
                    manifest.status = InterviewStatus.METHOD_FINISHED
                    manifest.completed_turns = completed_turns
                    manifest.finish_message = step_res.finish_message or "Interview method signaled completion."
                    print(f"\n[Interview Completed]: {manifest.finish_message}")

                # Clear pending answer and update manifest
                PendingAnswerStore.delete(self.results_dir)
                ManifestManager.save(self.results_dir, manifest)

            return manifest

        except KeyboardInterrupt:
            print("\n[Interview interrupted by KeyboardInterrupt]")
            manifest.status = InterviewStatus.INTERRUPTED
            ManifestManager.save(self.results_dir, manifest)
            return manifest
        except Exception as exc:
            from interview.storage.sanitizer import sanitize_error_message
            if ManifestManager.exists(self.results_dir):
                disk_manifest = ManifestManager.load(self.results_dir)
                if disk_manifest.status == InterviewStatus.INTERRUPTED:
                    manifest.status = InterviewStatus.INTERRUPTED
            if manifest.status != InterviewStatus.INTERRUPTED:
                manifest.status = InterviewStatus.FAILED
            manifest.error_message = sanitize_error_message(exc, self.project_root)
            ManifestManager.save(self.results_dir, manifest)
            raise
        finally:
            adapter.close()
