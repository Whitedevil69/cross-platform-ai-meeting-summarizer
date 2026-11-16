"""Auto-detect platform from URL and return parsed meeting info."""
from __future__ import annotations

from .zoom import is_zoom_url, parse_zoom_url
from .meet import is_meet_url, parse_meet_url
from .teams import is_teams_url, parse_teams_url


def detect_platform(url: str) -> str:
    """
    Detect which video-conferencing platform a meeting URL belongs to.

    Args:
        url: Any meeting URL string.

    Returns:
        One of ``"zoom"``, ``"google_meet"``, ``"teams"``, or ``"unknown"``.
    """
    if is_zoom_url(url):
        return "zoom"
    if is_meet_url(url):
        return "google_meet"
    if is_teams_url(url):
        return "teams"
    return "unknown"


def parse_meeting_url(url: str) -> dict:
    """
    Auto-detect the platform and parse the meeting URL into a structured dict.

    The returned dict always contains at minimum::

        {
            "platform": "zoom" | "google_meet" | "teams" | "unknown",
            "url":      <original url>,
        }

    Platform-specific keys are merged in on top of these base fields:

    * **zoom**:        ``meeting_id``, ``passcode``
    * **google_meet**: ``meeting_code``
    * **teams**:       (no additional structured fields; URL is opaque)
    * **unknown**:     (no additional fields)

    Args:
        url: Any meeting URL string (Zoom, Google Meet, Teams, or other).

    Returns:
        Dict with platform and parsed fields.
    """
    platform = detect_platform(url)
    base = {"platform": platform, "url": url}

    if platform == "zoom":
        base.update(parse_zoom_url(url))
    elif platform == "google_meet":
        base.update(parse_meet_url(url))
    elif platform == "teams":
        base.update(parse_teams_url(url))

    return base
