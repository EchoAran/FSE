"""Sanitization utility to remove absolute machine paths from logs, manifests, and error reports."""

from pathlib import Path
import re
from typing import Any, Optional


def sanitize_text(text: str, project_root: Optional[Path] = None) -> str:
    """Scrub local filesystem paths and usernames from text, replacing them with generic placeholders."""
    if not text:
        return ""

    sanitized = text

    # 1. Replace project_root path (Windows backslash and POSIX forward slash)
    if project_root:
        root_str_win = str(project_root)
        root_str_posix = project_root.as_posix()
        sanitized = re.sub(re.escape(root_str_win), "<project_root>", sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(re.escape(root_str_posix), "<project_root>", sanitized, flags=re.IGNORECASE)

    # 2. Replace user directory path (e.g. C:\Users\<user> or /Users/<user> or /home/<user>)
    try:
        user_home = str(Path.home())
        user_home_posix = Path.home().as_posix()
        sanitized = re.sub(re.escape(user_home), "<user_home>", sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(re.escape(user_home_posix), "<user_home>", sanitized, flags=re.IGNORECASE)
    except Exception:
        pass

    # 3. Replace any remaining Windows absolute drive paths (e.g. E:\... or C:\...)
    sanitized = re.sub(r"[A-Za-z]:\\[^:\n\r\t\"\'<>|]+", "<sanitized_path>", sanitized)
    sanitized = re.sub(r"[A-Za-z]:/[^:\n\r\t\"\'<>|]+", "<sanitized_path>", sanitized)

    return sanitized


def sanitize_error_message(error: Any, project_root: Optional[Path] = None) -> str:
    """Produce a clean, sanitized error description with local machine paths scrubbed."""
    if error is None:
        return ""

    err_str = str(error).strip()
    return sanitize_text(err_str, project_root=project_root)
