"""
LiveKit Manager — generate join tokens for meeting rooms.
Uses livekit-api Python SDK.
"""
from __future__ import annotations

import os
import time
from datetime import timedelta
from livekit import api


LIVEKIT_URL        = os.getenv("LIVEKIT_URL",        "ws://localhost:7880")
LIVEKIT_API_KEY    = os.getenv("LIVEKIT_API_KEY",    "devkey")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "devsecret_at_least_32_chars_long!")


def generate_token(room_name: str, participant_name: str, ttl_seconds: int = 7200) -> str:
    """
    Generate a LiveKit JWT access token for a participant to join a room.
    ttl_seconds: token validity duration (default 2 hours).
    """
    token = (
        api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(participant_name)
        .with_name(participant_name)
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
            )
        )
        .with_ttl(timedelta(seconds=ttl_seconds))
        .to_jwt()
    )
    return token


def get_livekit_url() -> str:
    return LIVEKIT_URL


def room_name_for_meeting(meeting_id: str) -> str:
    """Deterministic room name from meeting ID."""
    return f"meeting-{meeting_id}"
