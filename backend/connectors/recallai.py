"""
Recall.ai Platform Connector — Phase E.
Sends a bot into Zoom, Google Meet, or Microsoft Teams meetings.
Env vars: RECALL_API_KEY, RECALL_REGION (default us-west-2), RECALL_WEBHOOK_SECRET
"""
from __future__ import annotations

import hashlib
import hmac
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass  # httpx lazily imported at call time

# ── Configuration ─────────────────────────────────────────────────────────────

def _get_api_key() -> str:
    key = os.getenv("RECALL_API_KEY", "")
    if not key:
        raise RuntimeError(
            "RECALL_API_KEY environment variable is not set. "
            "Sign up at https://app.recall.ai to get your API key."
        )
    return key


def _get_region() -> str:
    return os.getenv("RECALL_REGION", "us-west-2")


def _base_url() -> str:
    return f"https://{_get_region()}.recall.ai/api/v1"


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Token {_get_api_key()}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


# ── Bot lifecycle ─────────────────────────────────────────────────────────────

async def create_bot(meeting_url: str, meeting_title: str, meeting_id: str) -> dict:
    """
    Send a Recall.ai recording bot into a Zoom, Google Meet, or Teams meeting.

    Args:
        meeting_url:   Full meeting URL (zoom.us, meet.google.com, or teams.microsoft.com)
        meeting_title: Human-readable title stored in bot metadata
        meeting_id:    Internal meeting_id to correlate webhook callbacks

    Returns:
        Recall.ai bot object dict including ``id`` (the bot_id).
    """
    key = os.getenv("RECALL_API_KEY", "")
    if not key or key == "demo":
        # Graceful simulation fallback for local development / testing
        sim_id = f"bot_sim_{meeting_id[:8]}"
        return {
            "id": sim_id,
            "bot_id": sim_id,
            "meeting_url": meeting_url,
            "status": "in_call_recording",
            "bot_name": "Meeting Intelligence Bot (Simulated)",
            "is_simulation": True,
        }

    import httpx  # lazy import — only required when using Recall.ai

    payload = {
        "meeting_url": meeting_url,
        "bot_name": "Meeting Intelligence Bot",
        "metadata": {
            "meeting_id": meeting_id,
            "meeting_title": meeting_title,
        },
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{_base_url()}/bot/",
            headers=_headers(),
            json=payload,
        )
        response.raise_for_status()
        data: dict = response.json()

    # Normalise: Recall returns the bot id as "id"
    if "id" in data and "bot_id" not in data:
        data["bot_id"] = data["id"]

    return data


async def get_bot_status(bot_id: str) -> dict:
    """
    Fetch the current status of a Recall.ai bot.

    Args:
        bot_id: The bot id returned by :func:`create_bot`.

    Returns:
        Recall.ai bot object dict with ``status_changes`` and current state.
    """
    if bot_id.startswith("bot_sim_"):
        return {
            "id": bot_id,
            "status": "in_call_recording",
            "status_changes": [{"code": "in_call_recording", "created_at": "2026-11-14T00:00:00Z"}],
            "is_simulation": True,
        }

    import httpx

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(
            f"{_base_url()}/bot/{bot_id}/",
            headers=_headers(),
        )
        response.raise_for_status()
        return response.json()


async def delete_bot(bot_id: str) -> bool:
    """
    Remove / stop a Recall.ai bot from a meeting.

    Args:
        bot_id: The bot id to stop and delete.

    Returns:
        ``True`` if the bot was successfully deleted (HTTP 204 or 200).
    """
    if bot_id.startswith("bot_sim_"):
        return True

    import httpx

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.delete(
            f"{_base_url()}/bot/{bot_id}/",
            headers=_headers(),
        )
        # 204 No Content is the success response for DELETE
        return response.status_code in (200, 204)


# ── Webhook helpers ───────────────────────────────────────────────────────────

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """
    Verify the HMAC-SHA256 signature on an incoming Recall.ai webhook.

    Recall.ai signs the raw request body with the webhook secret and sends the
    hex digest in the ``X-Recall-Signature`` header.

    Args:
        payload:   Raw request body bytes.
        signature: Value of the ``X-Recall-Signature`` header.
        secret:    Webhook secret from the Recall.ai dashboard.

    Returns:
        ``True`` if the signature is valid; ``False`` otherwise.
    """
    expected = hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def parse_transcript_webhook(payload: dict, meeting_id: str) -> list:
    """
    Convert a Recall.ai ``transcript.data`` webhook payload into a list of
    :class:`~backend.meeting_record.Segment` objects grouped by speaker turn.

    Recall.ai transcript format::

        {
            "data": {
                "transcript": [
                    {
                        "speaker": "Alice",
                        "words": [
                            {"text": "Hello", "start_time": 0.0, "end_time": 0.5},
                            ...
                        ]
                    },
                    ...
                ]
            }
        }

    Consecutive entries from the same speaker are merged into a single Segment.

    Args:
        payload:    Parsed JSON body of the Recall.ai webhook.
        meeting_id: Internal meeting_id used to populate :attr:`Segment.meeting_id`.

    Returns:
        List of :class:`~backend.meeting_record.Segment` objects.
    """
    from ..meeting_record import Segment  # lazy relative import

    raw_transcript: list[dict] = (
        payload.get("data", {}).get("transcript", [])
    )

    segments: list[Segment] = []
    seg_id = 0

    # Group consecutive turns by speaker into single Segment objects
    current_speaker: str | None = None
    current_words: list[dict] = []
    current_start: float = 0.0
    current_end: float = 0.0

    def _flush(speaker: str, words: list[dict], start: float, end: float) -> Segment:
        nonlocal seg_id
        text = " ".join(w.get("text", "") for w in words).strip()
        seg = Segment(
            id=seg_id,
            start=round(start, 3),
            end=round(end, 3),
            text=text,
            speaker=speaker,
            language="en",  # Recall.ai transcripts are typically English
        )
        seg_id += 1
        return seg

    for turn in raw_transcript:
        speaker: str = turn.get("speaker") or "Unknown"
        words: list[dict] = turn.get("words", [])
        if not words:
            continue

        turn_start: float = words[0].get("start_time", 0.0)
        turn_end: float = words[-1].get("end_time", turn_start)

        if speaker == current_speaker:
            # Merge with current turn
            current_words.extend(words)
            current_end = turn_end
        else:
            # Flush previous turn
            if current_speaker is not None and current_words:
                segments.append(_flush(current_speaker, current_words, current_start, current_end))
            # Start new turn
            current_speaker = speaker
            current_words = list(words)
            current_start = turn_start
            current_end = turn_end

    # Flush the last accumulated turn
    if current_speaker is not None and current_words:
        segments.append(_flush(current_speaker, current_words, current_start, current_end))

    return segments
