"""Consistency verification and crash recovery manager for interview environment."""

from pathlib import Path
from typing import Optional, Tuple

from interview.cases.models import CaseRecord
from interview.config.interviewee_config import IntervieweeConfig
from interview.storage.conversation import ConversationLogger
from interview.storage.manifest import ManifestManager
from interview.storage.models import InterviewManifest, InterviewStatus
from interview.storage.pending_store import PendingAnswerStore


class RecoveryManager:
    """Handles consistency validation, crash detection, and safe session restoration."""

    @classmethod
    def verify_config_consistency(
        cls,
        existing_manifest: InterviewManifest,
        method_model: Optional[str],
        method_max_turns: Optional[int],
        interviewee_config: Optional[IntervieweeConfig] = None,
    ) -> None:
        """Ensure critical parameters have not changed between runs on an existing directory."""
        mismatches = []
        if method_model and existing_manifest.method_model and existing_manifest.method_model != method_model:
            mismatches.append(
                f"method_model mismatch: manifest has '{existing_manifest.method_model}', invocation has '{method_model}'"
            )

        if method_max_turns is not None and existing_manifest.method_max_turns is not None:
            if existing_manifest.method_max_turns != method_max_turns:
                mismatches.append(
                    f"method_max_turns mismatch: manifest has '{existing_manifest.method_max_turns}', invocation has '{method_max_turns}'"
                )

        if interviewee_config:
            curr_model = interviewee_config.model.model_name
            existing_model = existing_manifest.interviewee_model
            if existing_model and existing_model != curr_model:
                mismatches.append(
                    f"interviewee_model mismatch: manifest has '{existing_model}', invocation has '{curr_model}'"
                )

        if mismatches:
            raise ValueError(
                "Cannot resume interview due to conflicting configuration parameters:\n"
                + "\n".join(f" - {m}" for m in mismatches)
                + "\nPlease use the original configurations or remove/archive the existing results directory."
            )

    @classmethod
    def reconcile_pending_answer(
        cls,
        results_dir: Path,
        method_id: str,
        adapter,
        case: CaseRecord,
    ) -> Tuple[str, bool, int]:
        manifest = ManifestManager.load(results_dir)

        # For SparkMe, cross-process resumption with in-memory state is not supported
        if method_id == "sparkme":
            manifest.status = InterviewStatus.INTERRUPTED
            manifest.error_message = (
                "SparkMe session is maintained in-memory and cannot be losslessly resumed "
                "after worker process termination. Mark run as interrupted."
            )
            ManifestManager.save(results_dir, manifest)
            raise RuntimeError(manifest.error_message)

        pending = PendingAnswerStore.load(results_dir)

        if not pending:
            # No pending answer to reconcile: resume adapter and sync manifest
            res = adapter.resume(case)
            manifest.completed_turns = res.turn_count
            if res.finished:
                manifest.status = InterviewStatus.METHOD_FINISHED
                manifest.finish_message = res.finish_message or "Interview method signaled completion."
            elif res.turn_count > 0:
                manifest.status = InterviewStatus.RUNNING
            ManifestManager.save(results_dir, manifest)
            return res.question, res.finished, res.turn_count

        # Resume adapter to check current state
        res = adapter.resume(case)

        # If turn count in method has already advanced past pending answer
        if res.turn_count >= pending.turn_index:
            # Pending answer was committed natively before crash; catch up conversation log
            messages = ConversationLogger.load_messages(results_dir)
            has_answer = any(m.role == "interviewee" and m.turn_index == pending.turn_index for m in messages)
            if not has_answer:
                ConversationLogger.append_message(
                    results_dir=results_dir,
                    turn_index=pending.turn_index,
                    role="interviewee",
                    content=pending.answer,
                )
                if not res.finished and res.question:
                    ConversationLogger.append_message(
                        results_dir=results_dir,
                        turn_index=pending.turn_index,
                        role="interviewer",
                        content=res.question,
                    )

            PendingAnswerStore.delete(results_dir)
            manifest.completed_turns = res.turn_count
            manifest.status = InterviewStatus.METHOD_FINISHED if res.finished else InterviewStatus.RUNNING
            manifest.finish_message = res.finish_message
            ManifestManager.save(results_dir, manifest)
            return res.question, res.finished, res.turn_count

        # Pending answer was not yet processed natively: submit it now
        step_res = adapter.submit_answer(pending.answer)
        ConversationLogger.append_message(
            results_dir=results_dir,
            turn_index=pending.turn_index,
            role="interviewee",
            content=pending.answer,
        )
        if not step_res.finished and step_res.question:
            ConversationLogger.append_message(
                results_dir=results_dir,
                turn_index=pending.turn_index,
                role="interviewer",
                content=step_res.question,
            )

        PendingAnswerStore.delete(results_dir)
        manifest.completed_turns = step_res.turn_count
        manifest.status = InterviewStatus.METHOD_FINISHED if step_res.finished else InterviewStatus.RUNNING
        manifest.finish_message = step_res.finish_message
        ManifestManager.save(results_dir, manifest)
        return step_res.question, step_res.finished, step_res.turn_count
