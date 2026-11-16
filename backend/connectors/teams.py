"""Microsoft Teams URL utilities."""
from __future__ import annotations

import re

# ── Patterns ──────────────────────────────────────────────────────────────────

# Standard Teams meeting URLs (web client, desktop deep-link, and Teams Live)
_TEAMS_HOST_RE = re.compile(
    r"^https?://(?:"
    r"teams\.microsoft\.com"       # enterprise Teams
    r"|teams\.live\.com"           # Teams (personal / consumer)
    r"|[a-z0-9\-]+\.teams\.microsoft\.com"  # regional / vanity subdomains
    r")/",
    re.IGNORECASE,
)


# ── Public API ────────────────────────────────────────────────────────────────

def is_teams_url(url: str) -> bool:
    """
    Return ``True`` if *url* is a Microsoft Teams meeting link.

    Accepted hosts::

        teams.microsoft.com   — enterprise / work accounts
        teams.live.com        — personal / consumer accounts
        <subdomain>.teams.microsoft.com — regional deployments
    """
    return bool(_TEAMS_HOST_RE.match(url))


def parse_teams_url(url: str) -> dict:
    """
    Parse a Microsoft Teams meeting URL.

    Teams meeting URLs are long, opaque links that encode the tenant, channel,
    and meeting parameters inside query-string segments — there is no simple
    human-readable meeting ID.  We return the full original URL for use with
    the Recall.ai bot API which accepts the raw link directly.

    Returns::

        {
            "platform": "teams",
            "url":      <original_url>,
        }

    Args:
        url: A Microsoft Teams meeting URL.
    """
    return {
        "platform": "teams",
        "url": url,
    }
