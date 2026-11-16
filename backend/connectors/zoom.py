"""Zoom meeting URL utilities."""
from __future__ import annotations

import re

# ── Patterns ──────────────────────────────────────────────────────────────────

# Matches zoom.us and zoomgov.com (both standard and vanity-subdomain URLs)
_ZOOM_HOST_RE = re.compile(
    r"^https?://(?:[a-z0-9\-]+\.)?(?:zoom\.us|zoomgov\.com)/",
    re.IGNORECASE,
)

# Extracts the numeric meeting ID from the URL path  (/j/12345678901)
_ZOOM_MEETING_ID_RE = re.compile(
    r"/j/(\d{9,11})",
    re.IGNORECASE,
)

# Passcode may be embedded in the URL as ?pwd=<base64>
_ZOOM_PWD_RE = re.compile(r"[?&]pwd=([^&]+)", re.IGNORECASE)


# ── Public API ────────────────────────────────────────────────────────────────

def is_zoom_url(url: str) -> bool:
    """
    Return ``True`` if *url* looks like a Zoom or ZoomGov meeting URL.

    Examples of accepted URLs::

        https://zoom.us/j/12345678901
        https://us02web.zoom.us/j/98765432109?pwd=ABC123
        https://example.zoomgov.com/j/11111111111
    """
    return bool(_ZOOM_HOST_RE.match(url))


def parse_zoom_url(url: str) -> dict:
    """
    Parse a Zoom meeting URL and return a dict of extracted fields.

    Returns::

        {
            "meeting_id": str,        # numeric meeting ID (empty string if not found)
            "passcode":   str | None, # URL-embedded pwd parameter, or None
            "platform":   "zoom",
        }

    Args:
        url: A Zoom meeting URL (zoom.us or zoomgov.com).
    """
    meeting_id_match = _ZOOM_MEETING_ID_RE.search(url)
    meeting_id = meeting_id_match.group(1) if meeting_id_match else ""

    pwd_match = _ZOOM_PWD_RE.search(url)
    passcode: str | None = pwd_match.group(1) if pwd_match else None

    return {
        "meeting_id": meeting_id,
        "passcode": passcode,
        "platform": "zoom",
    }
