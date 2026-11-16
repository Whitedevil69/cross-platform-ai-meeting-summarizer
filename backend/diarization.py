"""
Diarization — Phase B speaker attribution for single-channel audio files.

Two backends (selected automatically):
  1. pyannote.audio (best quality) — requires HF_TOKEN env var and:
       pip install pyannote.audio
  2. Lightweight energy-based fallback (zero extra deps) — rough speaker turns
     based on silence gaps. Less accurate but always available.

Env vars:
  DIARIZATION_ENABLED=true/false  (default: false — opt-in)
  HF_TOKEN=hf_...                 (for pyannote.audio; get from hf.co/settings/tokens)
  DIARIZATION_BACKEND=auto        (auto | pyannote | energy)
  DIARIZATION_NUM_SPEAKERS=0      (0 = auto-detect; or set expected number)
"""
from __future__ import annotations

import logging
import os
from pathlib import Path

from .meeting_record import Segment

logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────

_SILENCE_THRESHOLD_S  = 1.0   # seconds of silence → speaker change boundary
_WINDOW_S             = 0.5   # RMS window size in seconds
_SPEAKER_LABELS       = [
    "Speaker A", "Speaker B", "Speaker C", "Speaker D",
    "Speaker E", "Speaker F", "Speaker G", "Speaker H",
]


# ── Public API ────────────────────────────────────────────────────────────────

def assign_speakers(
    segments: list[Segment],
    audio_path: str | Path,
) -> list[Segment]:
    """
    Assign speaker labels to each Segment in-place, then return the list.

    When DIARIZATION_ENABLED is not 'true' (the default), this is a no-op and
    segments are returned unchanged with their original speaker values.

    Selection logic (DIARIZATION_BACKEND env var):
      auto     → try pyannote first; fall back to energy on failure
      pyannote → pyannote only (raises if unavailable)
      energy   → energy-based heuristic only
    """
    enabled = os.getenv("DIARIZATION_ENABLED", "false").lower() == "true"
    if not enabled:
        logger.debug("Diarization disabled — skipping (set DIARIZATION_ENABLED=true to enable)")
        return segments

    if not segments:
        return segments

    audio_path = Path(audio_path)
    backend    = os.getenv("DIARIZATION_BACKEND", "auto").lower()
    hf_token   = os.getenv("HF_TOKEN", "").strip()

    logger.info(
        "Diarization starting: backend=%s, audio=%s, segments=%d",
        backend, audio_path.name, len(segments),
    )

    if backend == "pyannote":
        _apply_pyannote(segments, audio_path, hf_token)
    elif backend == "energy":
        _apply_energy(segments, audio_path)
    else:  # auto
        if hf_token:
            try:
                _apply_pyannote(segments, audio_path, hf_token)
            except Exception as exc:
                logger.warning(
                    "pyannote backend failed (%s); falling back to energy-based diarization", exc
                )
                _apply_energy(segments, audio_path)
        else:
            logger.info("No HF_TOKEN set — using energy-based diarization fallback")
            _apply_energy(segments, audio_path)

    speaker_count = len({s.speaker for s in segments if s.speaker != "Unknown"})
    logger.info("Diarization complete — %d distinct speaker(s) assigned", speaker_count)
    return segments


# ── pyannote backend ──────────────────────────────────────────────────────────

def _apply_pyannote(
    segments: list[Segment],
    audio_path: Path,
    hf_token: str,
) -> None:
    """
    Run pyannote.audio speaker diarization and assign speaker labels.
    Lazy-imports pyannote so it is only required when this backend is actually used.
    """
    if not hf_token:
        raise ValueError(
            "HF_TOKEN env var is required for pyannote backend. "
            "Get a token at https://hf.co/settings/tokens and grant access at "
            "https://hf.co/pyannote/speaker-diarization-3.1"
        )

    # Lazy import — do not import at module level
    try:
        from pyannote.audio import Pipeline  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "pyannote.audio is not installed. "
            "Run: pip install pyannote.audio"
        ) from exc

    num_speakers = int(os.getenv("DIARIZATION_NUM_SPEAKERS", "0")) or None

    logger.info("Loading pyannote pipeline (pyannote/speaker-diarization-3.1)…")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token,
    )

    diarize_kwargs: dict = {}
    if num_speakers:
        diarize_kwargs["num_speakers"] = num_speakers

    logger.info("Running pyannote diarization on %s…", audio_path.name)
    diarization = pipeline(str(audio_path), **diarize_kwargs)

    # Build a list of (start, end, speaker_label) turns for fast overlap search
    turns: list[tuple[float, float, str]] = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        turns.append((turn.start, turn.end, speaker))

    if not turns:
        logger.warning("pyannote returned no speaker turns — speakers will remain 'Unknown'")
        return

    # Map each Segment to the speaker turn with maximum overlap
    for seg in segments:
        best_label = "Unknown"
        best_overlap = 0.0
        for t_start, t_end, label in turns:
            overlap = _overlap(seg.start, seg.end, t_start, t_end)
            if overlap > best_overlap:
                best_overlap = overlap
                best_label = label
        seg.speaker = best_label

    logger.debug("pyannote: assigned speakers to %d segments", len(segments))


# ── Energy-based fallback backend ─────────────────────────────────────────────

def _apply_energy(
    segments: list[Segment],
    audio_path: Path,
) -> None:
    """
    Lightweight energy-based speaker turn detection.

    Algorithm:
      1. Load audio with soundfile (int16 or float32).
      2. Compute RMS energy over non-overlapping 0.5 s windows.
      3. Detect silence gaps > 1.0 s (consecutive low-energy windows).
      4. Assign alternating labels (Speaker A, Speaker B, …) at each boundary.
      5. Map each Segment to its label by timestamp overlap.
    """
    try:
        import soundfile as sf  # type: ignore[import]
        import numpy as np      # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "soundfile and numpy are required for the energy-based diarization fallback. "
            "Run: pip install soundfile numpy"
        ) from exc

    logger.info("Loading audio for energy-based diarization: %s", audio_path.name)
    audio, sr = sf.read(str(audio_path), dtype="float32", always_2d=True)

    # Convert to mono
    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    window_samples  = int(sr * _WINDOW_S)
    silence_windows = int(_SILENCE_THRESHOLD_S / _WINDOW_S)

    # Compute RMS per window
    num_windows = len(audio) // window_samples
    if num_windows == 0:
        logger.warning("Audio too short for energy diarization — using single speaker label")
        for seg in segments:
            seg.speaker = _SPEAKER_LABELS[0]
        return

    rms_values = np.array([
        np.sqrt(np.mean(audio[i * window_samples:(i + 1) * window_samples] ** 2))
        for i in range(num_windows)
    ])

    # Dynamic silence threshold: 10% of the mean RMS
    silence_thresh = rms_values.mean() * 0.10

    # Detect speaker change boundaries (silence gap of >= silence_windows consecutive silent frames)
    is_silent = rms_values < silence_thresh
    boundaries: list[float] = [0.0]  # first speaker starts at t=0

    silent_run = 0
    for i, silent in enumerate(is_silent):
        if silent:
            silent_run += 1
            if silent_run == silence_windows:
                # Mark a boundary at the START of this silence run
                boundary_t = (i - silence_windows + 1) * _WINDOW_S
                if boundary_t > boundaries[-1]:
                    boundaries.append(boundary_t)
        else:
            silent_run = 0

    # Total audio duration
    duration = len(audio) / sr
    boundaries.append(duration)

    # Build turn list: (start, end, label)
    turns: list[tuple[float, float, str]] = []
    speaker_idx = 0
    for i in range(len(boundaries) - 1):
        t_start = boundaries[i]
        t_end   = boundaries[i + 1]
        if t_end - t_start < 0.1:
            # Skip tiny gaps (< 100ms)
            continue
        label = _SPEAKER_LABELS[speaker_idx % len(_SPEAKER_LABELS)]
        turns.append((t_start, t_end, label))
        speaker_idx += 1

    if not turns:
        logger.warning("Energy diarization produced no turns — assigning single speaker")
        for seg in segments:
            seg.speaker = _SPEAKER_LABELS[0]
        return

    logger.info(
        "Energy diarization: %d speaker turn(s) detected (silence threshold=%.4f)",
        len(turns), silence_thresh,
    )

    # Assign speaker to each segment by maximum overlap
    for seg in segments:
        best_label   = "Unknown"
        best_overlap = 0.0
        for t_start, t_end, label in turns:
            overlap = _overlap(seg.start, seg.end, t_start, t_end)
            if overlap > best_overlap:
                best_overlap = overlap
                best_label   = label
        # If no overlap found (e.g. segment outside audio bounds), use first label
        if best_label == "Unknown" and turns:
            best_label = turns[0][2]
        seg.speaker = best_label

    logger.debug("Energy diarization: assigned speakers to %d segments", len(segments))


# ── Utility ───────────────────────────────────────────────────────────────────

def _overlap(a_start: float, a_end: float, b_start: float, b_end: float) -> float:
    """Return the length of the intersection of intervals [a_start, a_end] and [b_start, b_end]."""
    return max(0.0, min(a_end, b_end) - max(a_start, b_start))
