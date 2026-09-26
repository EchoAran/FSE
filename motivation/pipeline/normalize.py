"""Shared URL canonicalization and stable conversation identifiers."""

from __future__ import annotations

import hashlib
from urllib.parse import urlparse

CANONICAL_HOST = "chatgpt.com"


def canonicalize_shared_url(raw: str) -> str:
    """Reduce a ChatGPT shared URL to its canonical host and share identifier."""
    parsed = urlparse(raw.strip())
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(f"invalid shared URL: {raw}")
    segments = [segment for segment in parsed.path.split("/") if segment]
    if len(segments) != 2 or segments[0] != "share":
        raise ValueError(f"shared URL has no /share/<id> path: {raw}")
    return f"https://{CANONICAL_HOST}/share/{segments[1]}"


def conversation_id(canonical_url: str) -> str:
    """Derive a machine independent conversation identifier from a canonical URL."""
    return hashlib.sha256(canonical_url.encode("utf-8")).hexdigest()[:20]