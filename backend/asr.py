"""
ASR — faster-whisper wrapper.
Produces Segment objects with per-segment language detection.
Extracts audio clips for each segment (used in evidence display).
"""
from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Generator

from faster_whisper import WhisperModel

from .meeting_record import Segment
from .audio_store import extract_clip

logger = logging.getLogger(__name__)

_MODEL: WhisperModel | None = None


def _get_model() -> WhisperModel:
    global _MODEL
    if _MODEL is None:
        model_size = os.getenv("WHISPER_MODEL", "small")
        device     = os.getenv("WHISPER_DEVICE", "cpu")
        compute    = os.getenv("WHISPER_COMPUTE", "int8")
        logger.info("Loading Whisper model '%s' on %s (%s)…", model_size, device, compute)
        _MODEL = WhisperModel(model_size, device=device, compute_type=compute)
    return _MODEL


def transcribe(
    audio_path: str | Path,
    meeting_id: str,
    initial_prompt: str | None = None,
) -> list[Segment]:
    """
    Transcribe audio file → list of Segment objects.
    Each segment has start/end, text, language, and a saved audio clip.
    """
    model = _get_model()
    audio_path = str(audio_path)

    segments_raw, info = model.transcribe(
        audio_path,
        beam_size=5,
        language=None,          # auto-detect per segment
        task="transcribe",
        initial_prompt=initial_prompt or
            "This meeting may contain Hindi, English, or Hinglish (code-switched).",
        word_timestamps=False,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    logger.info("Detected language: %s (%.0f%%)", info.language, info.language_probability * 100)

    segments: list[Segment] = []
    for raw in segments_raw:
        seg = Segment(
            id=raw.id,
            start=round(raw.start, 3),
            end=round(raw.end, 3),
            text=raw.text.strip(),
            language=raw.language or info.language,
        )
        # Extract clip for evidence playback
        try:
            extract_clip(audio_path, seg.id, seg.start, seg.end, meeting_id)
        except Exception as e:
            logger.warning("Clip extraction failed for segment %d: %s", seg.id, e)

        segments.append(seg)

    logger.info("Transcribed %d segments", len(segments))
    return segments


def transcribe_stream(
    audio_path: str | Path,
    meeting_id: str,
) -> Generator[Segment, None, None]:
    """
    Streaming variant — yields Segment objects one by one as Whisper processes them.
    Used for real-time display during file upload.
    """
    model = _get_model()
    segments_raw, _ = model.transcribe(
        str(audio_path),
        beam_size=3,
        language=None,
        task="transcribe",
        vad_filter=True,
    )
    for raw in segments_raw:
        seg = Segment(
            id=raw.id,
            start=round(raw.start, 3),
            end=round(raw.end, 3),
            text=raw.text.strip(),
            language=raw.language or "en",
        )
        try:
            extract_clip(str(audio_path), seg.id, seg.start, seg.end, meeting_id)
        except Exception:
            pass
        yield seg
