"""
LLM Extraction — multi-provider structured JSON output.
Extracts decisions, actions, open questions from transcript segments.
Every item MUST cite segment_id + exact quote (enforced by schema + evidence checker).

Supported providers (set via LLM_PROVIDER env var):
  ollama    — fully local, default (requires: ollama package + running Ollama server)
  openai    — OpenAI API (requires: pip install openai + OPENAI_API_KEY)
  gemini    — Google Gemini API (requires: pip install google-generativeai + GEMINI_API_KEY)
  anthropic — Anthropic API (requires: pip install anthropic + ANTHROPIC_API_KEY)
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any

from pydantic import BaseModel, Field, ValidationError

from .meeting_record import Evidence, Item, ItemType

logger = logging.getLogger(__name__)

# ── Provider / model configuration ──────────────────────────────────────────

LLM_PROVIDER   = os.getenv("LLM_PROVIDER", "ollama").lower()

# Ollama
MODEL          = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# OpenAI
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL    = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Google Gemini
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL    = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL   = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-20241022")


# ── Pydantic schema for LLM output ──────────────────────────────────────────

class EvidenceOut(BaseModel):
    segment_id: int      = Field(description="The segment id from the transcript")
    quote:      str      = Field(description="Exact words from that segment supporting this item")

class ItemOut(BaseModel):
    type:     str                = Field(description="One of: decision, action, question")
    text:     str                = Field(description="Clear, concise statement of the item")
    owner:    str | None         = Field(None, description="Person responsible; null if unclear")
    deadline: str | None         = Field(None, description="Due date/time; null if not mentioned")
    evidence: list[EvidenceOut]  = Field(description="1-3 evidence citations from the transcript")

class ExtractionResult(BaseModel):
    items: list[ItemOut] = Field(description="List of all extracted items")


# ── System prompt ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a meeting analyst. Extract decisions, action items, and open questions from the transcript.

Rules (STRICT):
1. Every item MUST have at least one evidence citation with segment_id and exact quote from that segment.
2. If you cannot cite an exact quote, do NOT include the item.
3. owner and deadline MUST be null if not explicitly stated — never guess.
4. type must be exactly one of: "decision", "action", "question".
5. Extract ONLY what is clearly stated. Do not infer or hallucinate.
6. For Hindi or Hinglish text, cite the original segment text as the quote.

Return valid JSON matching the schema exactly."""


# ── Extraction function ──────────────────────────────────────────────────────

def extract_items(segments: list, meeting_id: str = "") -> list[Item]:
    """
    Extract decisions, actions, and open questions from transcript segments.

    Routes to the appropriate LLM provider based on the LLM_PROVIDER env var:
      - "ollama"    (default) → local Ollama
      - "openai"              → OpenAI API
      - "gemini"              → Google Gemini API
      - "anthropic"           → Anthropic API

    Returns a list of Item objects with status="proposed".
    """
    if not segments:
        return []

    # Build transcript text with segment IDs
    transcript_lines = []
    for seg in segments:
        lang_label = f"[{seg.language.upper()}]" if seg.language else ""
        line = f"[{seg.id}] ({seg.start:.1f}s) {lang_label} {seg.text}"
        if seg.translated_text:
            line += f"  // EN: {seg.translated_text}"
        transcript_lines.append(line)

    transcript = "\n".join(transcript_lines)

    user_prompt = f"""Transcript (format: [segment_id] (timestamp) [LANG] text):

{transcript}

Extract all decisions, action items, and open questions. Follow the schema exactly."""

    # Route to the selected provider
    if LLM_PROVIDER == "openai":
        raw = _call_openai(user_prompt)
    elif LLM_PROVIDER == "gemini":
        raw = _call_gemini(user_prompt)
    elif LLM_PROVIDER == "anthropic":
        raw = _call_anthropic(user_prompt)
    else:
        # Default: ollama
        raw = _call_ollama(user_prompt)

    if raw is None:
        return []

    try:
        result = ExtractionResult.model_validate_json(raw)
        return _convert_items(result.items, segments)
    except ValidationError as e:
        logger.error("[%s] LLM output failed schema validation: %s", LLM_PROVIDER, e)
        return _fallback_extraction(segments)


# ── Provider implementations (lazily imported) ───────────────────────────────

def _call_ollama(user_prompt: str) -> str | None:
    """Call the local Ollama server and return raw JSON string."""
    try:
        import ollama  # noqa: PLC0415 — lazy import
    except ImportError:
        logger.error("ollama package is not installed. Run: pip install ollama")
        return None

    try:
        logger.info("Calling Ollama model '%s' for extraction…", MODEL)
        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
            format=ExtractionResult.model_json_schema(),
            options={"temperature": 0, "num_predict": 2048},
        )
        raw = response.message.content
        logger.debug("Raw Ollama response: %s", raw[:500])
        return raw
    except Exception as e:
        logger.error("Ollama extraction error: %s", e)
        return None


def _call_openai(user_prompt: str) -> str | None:
    """Call the OpenAI API with JSON mode and return raw JSON string."""
    try:
        import openai  # noqa: PLC0415 — lazy import
    except ImportError:
        logger.error(
            "openai package is not installed. Run: pip install openai"
        )
        return None

    try:
        logger.info("Calling OpenAI model '%s' for extraction…", OPENAI_MODEL)
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0,
            max_tokens=2048,
        )
        raw = response.choices[0].message.content
        logger.debug("Raw OpenAI response: %s", raw[:500])
        # Wrap in {"items": [...]} if the model returned a bare list
        raw = _ensure_items_wrapper(raw)
        return raw
    except Exception as e:
        logger.error("OpenAI extraction error: %s", e)
        return None


def _call_gemini(user_prompt: str) -> str | None:
    """Call the Google Gemini API with JSON mode and return raw JSON string."""
    try:
        import google.generativeai as genai  # noqa: PLC0415 — lazy import
    except ImportError:
        logger.error(
            "google-generativeai package is not installed. "
            "Run: pip install google-generativeai"
        )
        return None

    try:
        logger.info("Calling Gemini model '%s' for extraction…", GEMINI_MODEL)
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0,
                max_output_tokens=2048,
            ),
        )
        response = model.generate_content(user_prompt)
        raw = response.text
        logger.debug("Raw Gemini response: %s", raw[:500])
        raw = _ensure_items_wrapper(raw)
        return raw
    except Exception as e:
        logger.error("Gemini extraction error: %s", e)
        return None


def _call_anthropic(user_prompt: str) -> str | None:
    """Call the Anthropic API and return raw JSON string."""
    try:
        import anthropic  # noqa: PLC0415 — lazy import
    except ImportError:
        logger.error(
            "anthropic package is not installed. Run: pip install anthropic"
        )
        return None

    try:
        logger.info("Calling Anthropic model '%s' for extraction…", ANTHROPIC_MODEL)
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        # Prepend JSON instruction to system prompt for Anthropic
        anthropic_system = (
            SYSTEM_PROMPT
            + "\n\nIMPORTANT: Your entire response must be valid JSON only — "
            "no prose, no markdown fences."
        )

        message = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=2048,
            system=anthropic_system,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )
        raw = message.content[0].text
        logger.debug("Raw Anthropic response: %s", raw[:500])
        raw = _ensure_items_wrapper(raw)
        return raw
    except Exception as e:
        logger.error("Anthropic extraction error: %s", e)
        return None


# ── Helpers ──────────────────────────────────────────────────────────────────

def _ensure_items_wrapper(raw: str) -> str:
    """
    Some cloud models return a bare JSON array instead of {"items": [...]}.
    Wrap it so ExtractionResult.model_validate_json() always sees the expected shape.
    """
    stripped = raw.strip()
    if stripped.startswith("["):
        return json.dumps({"items": json.loads(stripped)})
    return raw


def _convert_items(raw_items: list[ItemOut], segments: list) -> list[Item]:
    """Convert ItemOut → Item with Evidence objects and segment timestamps."""
    seg_map = {s.id: s for s in segments}
    items: list[Item] = []

    for raw in raw_items:
        # Validate item type
        item_type: ItemType = raw.type if raw.type in ("decision", "action", "question") else "decision"

        evidences: list[Evidence] = []
        for ev in raw.evidence:
            seg = seg_map.get(ev.segment_id)
            if seg is None:
                continue  # segment doesn't exist — skip
            evidences.append(Evidence(
                segment_id=ev.segment_id,
                quote=ev.quote,
                timestamp=seg.start,
                clip_path=None,  # filled in by audio_store if available
            ))

        if not evidences:
            logger.warning("Item '%s…' has no valid evidence — skipping", raw.text[:40])
            continue

        items.append(Item(
            type=item_type,
            text=raw.text,
            owner=raw.owner,
            deadline=raw.deadline,
            evidence=evidences,
            status="proposed",
        ))

    logger.info("Extracted %d items via provider '%s'", len(items), LLM_PROVIDER)
    return items


def _fallback_extraction(segments: list) -> list[Item]:
    """
    Last-resort fallback: return empty list with a warning.
    The UI will show 'No items extracted' and ask user to add manually.
    """
    logger.warning("Falling back to empty extraction — check your LLM provider config and prompt.")
    return []
