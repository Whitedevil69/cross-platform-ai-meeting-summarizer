"""Google Meet URL utilities."""
from __future__ import annotations

import re

# ── Patterns ──────────────────────────────────────────────────────────────────

# Google Meet URLs follow the pattern: meet.google.com/<code>
# Meeting codes are three groups of letters separated by hyphens, e.g. abc-defg-hij
_MEET_HOST_RE = re.compile(
    r"^https?://meet\.google\.com/",
    re.IGNORECASE,
)

# Extract the meeting code from the path: /abc-defg-hij
_MEET_CODE_RE = re.compile(
    r"/([a-z]{3,4}-[a-z]{4}-[a-z]{3,4})(?:[/?#]|$)",
    re.IGNORECASE,
)


# ── Public API ────────────────────────────────────────────────────────────────

def is_meet_url(url: str) -> bool:
    """
    Return ``True`` if *url* is a Google Meet meeting link.

    Accepted formats::

        https://meet.google.com/abc-defg-hij
        https://meet.google.com/abc-defg-hij?authuser=0
    """
    return bool(_MEET_HOST_RE.match(url))


def parse_meet_url(url: str) -> dict:
    """
    Parse a Google Meet URL and extract the meeting code.

    Returns::

        {
            "meeting_code": str,        # e.g. "abc-defg-hij" (empty if not parsed)
            "platform":     "google_meet",
        }

    Args:
        url: A Google Meet URL (meet.google.com/…).
    """
    code_match = _MEET_CODE_RE.search(url)
    meeting_code = code_match.group(1).lower() if code_match else ""

    return {
        "meeting_code": meeting_code,
        "platform": "google_meet",
    }
