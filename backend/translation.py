"""
Translation — NLLB-200 via HuggingFace transformers.
Lazy-loaded: only imported when a Hindi segment is detected.
Uses distilled-600M by default; upgrade to 1.3B via env var.
"""
from __future__ import annotations

import os
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

# Language code mapping (Whisper lang → NLLB BCP-47 style)
WHISPER_TO_NLLB = {
    "hi":  "hin_Deva",
    "en":  "eng_Latn",
    # Hinglish has no single code — treat as Hindi for translation
}
NLLB_HINDI   = "hin_Deva"
NLLB_ENGLISH = "eng_Latn"


@lru_cache(maxsize=1)
def _load_pipeline():
    """Lazy-load the NLLB pipeline (downloads model on first call)."""
    from transformers import pipeline as hf_pipeline
    model_name = os.getenv("NLLB_MODEL", "facebook/nllb-200-distilled-600M")
    logger.info("Loading NLLB translation model: %s …", model_name)
    pipe = hf_pipeline(
        "translation",
        model=model_name,
        device=-1,  # CPU; set to 0 for GPU
        max_length=512,
    )
    logger.info("NLLB model loaded.")
    return pipe


def translate(text: str, src_lang: str = "hi", tgt_lang: str = "en") -> str:
    """
    Translate text between Hindi and English.
    src_lang / tgt_lang use Whisper codes ("hi" / "en").
    Returns translated string, or original text if translation not applicable.
    """
    if not text.strip():
        return text

    src_nllb = WHISPER_TO_NLLB.get(src_lang, NLLB_HINDI)
    tgt_nllb = WHISPER_TO_NLLB.get(tgt_lang, NLLB_ENGLISH)

    if src_nllb == tgt_nllb:
        return text  # same language, no-op

    try:
        pipe = _load_pipeline()
        result = pipe(
            text,
            src_lang=src_nllb,
            tgt_lang=tgt_nllb,
        )
        return result[0]["translation_text"]
    except Exception as e:
        logger.error("Translation failed: %s", e)
        return text  # fall back to original


def translate_segments_to_english(segments) -> list:
    """
    Translate any non-English segments to English and store in translated_text.
    Returns segments with translated_text populated where applicable.
    """
    for seg in segments:
        if seg.language not in ("en", "eng_Latn"):
            try:
                seg.translated_text = translate(seg.text, src_lang=seg.language, tgt_lang="en")
                logger.debug("Translated seg %d: %s → %s", seg.id, seg.text[:40], seg.translated_text[:40])
            except Exception as e:
                logger.warning("Could not translate segment %d: %s", seg.id, e)
    return segments


def is_translation_available() -> bool:
    """Check if transformers is installed (translation is optional)."""
    try:
        import transformers  # noqa: F401
        return True
    except ImportError:
        return False
