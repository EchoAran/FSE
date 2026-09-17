"""Worker subprocess entry point providing isolated execution for interview methods."""

import argparse
from multiprocessing.connection import Client
import os
from pathlib import Path
import sys
import traceback


def main() -> None:
    parser = argparse.ArgumentParser(description="Isolated method worker runner.")
    parser.add_argument("--method", required=True, help="Method identifier.")
    parser.add_argument("--port", type=int, required=True, help="IPC listener port.")
    parser.add_argument("--authkey", required=True, help="IPC authentication key.")
    parser.add_argument("--native-dir", required=True, help="Native results directory path.")
    parser.add_argument("--config-path", required=True, help="Path to method native configuration.")
    parser.add_argument("--method-root", required=True, help="Root directory of the method.")
    args = parser.parse_args()

    method_id = args.method.strip().lower()
    native_dir = Path(args.native_dir).resolve()
    config_path = Path(args.config_path).resolve()
    method_root = Path(args.method_root).resolve()

    # Crucial: isolate environment variables before importing any method module
    if method_id == "sparkme":
        logs_dir = native_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        os.environ["LOGS_DIR"] = str(logs_dir)

    # Prepend method paths to sys.path
    sys.path.insert(0, str(method_root))
    src_dir = method_root / "src"
    if src_dir.is_dir():
        sys.path.insert(0, str(src_dir))

    # Connect to parent IPC listener
    conn = Client(("127.0.0.1", args.port), authkey=args.authkey.encode("utf-8"))

    # Instantiate handler for specified method
    handler = None
    try:
        if method_id == "hashimoto":
            from interview.workers.handlers.hashimoto_handler import HashimotoHandler
            handler = HashimotoHandler(config_path, native_dir, method_root)
        elif method_id == "llmrei-long":
            from interview.workers.handlers.llmrei_handler import LLMREIHandler
            handler = LLMREIHandler(config_path, native_dir, method_root)
        elif method_id == "sparkme":
            from interview.workers.handlers.sparkme_handler import SparkMeHandler
            handler = SparkMeHandler(config_path, native_dir, method_root)
        elif method_id == "proposed_method":
            from interview.workers.handlers.proposed_handler import ProposedMethodHandler
            handler = ProposedMethodHandler(config_path, native_dir, method_root)
        else:
            raise ValueError(f"Unsupported method ID: {method_id}")

        conn.send({"success": True, "data": {"status": "ready"}})
    except Exception as exc:
        from interview.storage.sanitizer import sanitize_error_message, sanitize_text
        proj_root = Path.cwd()
        conn.send({
            "success": False,
            "error": sanitize_error_message(exc, proj_root),
            "traceback": sanitize_text(traceback.format_exc(), proj_root),
        })
        conn.close()
        sys.exit(1)

    # Command loop
    while True:
        try:
            msg = conn.recv()
        except EOFError:
            break

        cmd = msg.get("cmd")
        if cmd == "close":
            try:
                handler.close()
            except Exception:
                pass
            conn.send({"success": True, "data": None})
            break
        elif cmd == "start":
            try:
                res = handler.start(msg["case"])
                conn.send({"success": True, "data": res})
            except Exception as exc:
                from interview.storage.sanitizer import sanitize_error_message, sanitize_text
                proj_root = Path.cwd()
                conn.send({
                    "success": False,
                    "error": sanitize_error_message(exc, proj_root),
                    "traceback": sanitize_text(traceback.format_exc(), proj_root),
                })
        elif cmd == "submit_answer":
            try:
                res = handler.submit_answer(msg["answer"])
                conn.send({"success": True, "data": res})
            except Exception as exc:
                from interview.storage.sanitizer import sanitize_error_message, sanitize_text
                proj_root = Path.cwd()
                conn.send({
                    "success": False,
                    "error": sanitize_error_message(exc, proj_root),
                    "traceback": sanitize_text(traceback.format_exc(), proj_root),
                })
        elif cmd == "inspect":
            try:
                res = handler.inspect()
                conn.send({"success": True, "data": res})
            except Exception as exc:
                from interview.storage.sanitizer import sanitize_error_message, sanitize_text
                proj_root = Path.cwd()
                conn.send({
                    "success": False,
                    "error": sanitize_error_message(exc, proj_root),
                    "traceback": sanitize_text(traceback.format_exc(), proj_root),
                })
        elif cmd == "resume":
            try:
                res = handler.resume(msg["case"])
                conn.send({"success": True, "data": res})
            except Exception as exc:
                from interview.storage.sanitizer import sanitize_error_message, sanitize_text
                proj_root = Path.cwd()
                conn.send({
                    "success": False,
                    "error": sanitize_error_message(exc, proj_root),
                    "traceback": sanitize_text(traceback.format_exc(), proj_root),
                })
        else:
            conn.send({"success": False, "error": f"Unknown command: {cmd}", "traceback": None})

    conn.close()
    sys.exit(0)


if __name__ == "__main__":
    main()
