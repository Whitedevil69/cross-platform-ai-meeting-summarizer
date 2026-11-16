"""
Evidence Checker — verify that LLM's cited quotes actually exist in cited segments.
This is the core trustworthiness mechanism of the system.
Items that fail the check are marked "unsupported".
"""
from __future__ import annotations

import logging
import re
import unicodedata

from .meeting_record import Item, Segment

logger = logging.getLogger(__name__)


def _normalize(text: str) -> str:
    """Lowercase, strip punctuation, normalize unicode for fuzzy matching."""
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)   # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _quote_in_segment(quote: str, segment_text: str) -> bool:
    """
    Check if the cited quote appears in the segment text.
    Uses normalized comparison to handle case/punctuation differences.
    Also tries a word-overlap heuristic for partial matches (≥70% overlap).
    """
    norm_quote   = _normalize(quote)
    norm_segment = _normalize(segment_text)

    # 1. Exact substring match (normalized)
    if norm_quote and norm_quote in norm_segment:
        return True

    # 2. Word overlap — at least 70% of quote words must appear in segment
    quote_words   = set(norm_quote.split())
    segment_words = set(norm_segment.split())
    if not quote_words:
        return False
    overlap = quote_words & segment_words
    ratio = len(overlap) / len(quote_words)
    if ratio >= 0.70:
        return True

    return False


def verify_items(items: list[Item], segments: list[Segment]) -> list[Item]:
    """
    For every item, verify each evidence citation.
    - If ANY evidence citation passes → item status stays "proposed"
    - If ALL evidence citations fail → item status → "unsupported"
    Returns the same list with statuses updated in place.
    """
    seg_map = {s.id: s for s in segments}

    for item in items:
        if not item.evidence:
            item.status = "unsupported"
            logger.warning("Item '%s…' has no evidence — marking unsupported", item.text[:40])
            continue

        passed = []
        for ev in item.evidence:
            seg = seg_map.get(ev.segment_id)
            if seg is None:
                logger.warning(
                    "Evidence for '%s…' references non-existent segment %d",
                    item.text[:30], ev.segment_id
                )
                passed.append(False)
                continue

            ok = _quote_in_segment(ev.quote, seg.text)
            if not ok:
                logger.warning(
                    "Evidence check FAILED for item '%s…': quote '%s' not in seg %d: '%s'",
                    item.text[:30], ev.quote[:30], ev.segment_id, seg.text[:40]
                )
            passed.append(ok)

        if any(passed):
            # At least one valid citation — keep as proposed
            logger.debug("Item '%s…' passed evidence check", item.text[:40])
        else:
            item.status = "unsupported"
            logger.warning("Item '%s…' FAILED all evidence checks → unsupported", item.text[:40])

    n_ok = sum(1 for i in items if i.status == "proposed")
    n_fail = sum(1 for i in items if i.status == "unsupported")
    logger.info("Evidence check: %d passed, %d unsupported", n_ok, n_fail)
    return items


def evidence_summary(items: list[Item]) -> dict:
    """Return a summary dict for the API / reporting."""
    total = len(items)
    supported   = sum(1 for i in items if i.status != "unsupported")
    unsupported = sum(1 for i in items if i.status == "unsupported")
    return {
        "total": total,
        "supported": supported,
        "unsupported": unsupported,
        "evidence_accuracy": round(supported / total, 3) if total else 1.0,
    }
