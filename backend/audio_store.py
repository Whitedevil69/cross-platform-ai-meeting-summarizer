"""
Audio Store — save original audio, extract per-segment clips.
Clips are saved as .wav and served via /audio/{meeting_id}/{segment_id}.wav
"""
from __future__ import annotations

import json
import os
import wave
from pathlib import Path

import soundfile as sf
import numpy as np


MEETINGS_DIR = Path(os.getenv("MEETINGS_DIR", "meetings"))


def meeting_dir(meeting_id: str) -> Path:
    d = MEETINGS_DIR / meeting_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def clips_dir(meeting_id: str) -> Path:
    d = meeting_dir(meeting_id) / "clips"
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_audio(meeting_id: str, audio_bytes: bytes, ext: str = ".wav") -> Path:
    """Save the original uploaded/recorded audio and return its path."""
    dest = meeting_dir(meeting_id) / f"audio{ext}"
    dest.write_bytes(audio_bytes)
    return dest


def extract_clip(
    audio_path: str | Path,
    segment_id: int,
    start: float,
    end: float,
    meeting_id: str,
) -> str:
    """
    Cut [start, end] from audio_path, save as clips/<segment_id>.wav.
    Returns relative path string for storage in Evidence.
    """
    audio_path = Path(audio_path)
    out_path = clips_dir(meeting_id) / f"{segment_id}.wav"

    try:
        data, samplerate = sf.read(str(audio_path))
        start_frame = int(start * samplerate)
        end_frame   = int(end   * samplerate)
        clip = data[start_frame:end_frame]
        if clip.ndim == 1:
            clip = clip[:, np.newaxis]
        sf.write(str(out_path), clip, samplerate)
    except Exception as e:
        # If soundfile fails (e.g. mp4), write a silent placeholder
        _write_silent_wav(out_path)

    return str(out_path.relative_to(MEETINGS_DIR))


def save_meeting_record(meeting_id: str, record_json: str, owner_id: str = "dev-user", workspace_id: str = "ws-engineering") -> None:
    """Save meeting record to SQLite DB + keep .json backup."""
    from .database import get_db
    get_db().save_meeting(meeting_id, record_json, owner_id, workspace_id)
    # backup json file
    backup = meeting_dir(meeting_id) / "record.json"
    backup.write_text(record_json, encoding="utf-8")


def load_meeting_record(meeting_id: str) -> str | None:
    """Load from SQLite; fall back to JSON file for auto-migration."""
    from .database import get_db
    db = get_db()
    result = db.load_meeting(meeting_id)
    if result is None:
        json_path = meeting_dir(meeting_id) / "record.json"
        if json_path.exists():
            data = json_path.read_text(encoding="utf-8")
            db.save_meeting(meeting_id, data)
            return data
    return result


def clip_path_absolute(meeting_id: str, segment_id: int) -> Path:
    return clips_dir(meeting_id) / f"{segment_id}.wav"


# ── helpers ──────────────────────────────────────────────────────────────────

def _write_silent_wav(path: Path, duration: float = 1.0, samplerate: int = 16000):
    samples = int(duration * samplerate)
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(b"\x00\x00" * samples)
