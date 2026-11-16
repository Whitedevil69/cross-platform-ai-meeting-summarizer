#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meeting Intelligence Evaluator — eval/benchmark.py
====================================================
End-to-end benchmark script that runs the full backend pipeline and computes
the five whitepaper metrics:

  1. Word Error Rate (WER)
  2. Extraction F1  (precision / recall / F1)
  3. Evidence Precision
  4. Read-back Correction Rate (simulated)
  5. Pipeline Latency

Usage
-----
Single file:
  python eval/benchmark.py --audio sample.wav --ground-truth eval/samples/english_sample.json

Batch (all *.json in a directory):
  python eval/benchmark.py --batch eval/samples/

Save results:
  python eval/benchmark.py --audio sample.wav --ground-truth eval/samples/english_sample.json --save

Module style (from project root):
  python -m eval.benchmark --help
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── ensure project root is on sys.path when run as a script ──────────────────
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

logging.basicConfig(level=logging.WARNING)   # suppress backend chatter by default

# ─────────────────────────────────────────────────────────────────────────────
# WER  (edit-distance based)
# ─────────────────────────────────────────────────────────────────────────────

def _normalize_text(text: str) -> str:
    """NFKC + lowercase — handles both Devanagari and Roman Hindi."""
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _edit_distance_ops(ref: list[str], hyp: list[str]) -> tuple[int, int, int]:
    """Return (substitutions, deletions, insertions) via DP."""
    n, m = len(ref), len(hyp)
    # dp[i][j] = (S, D, I) minimal edit to align ref[:i] → hyp[:j]
    INF = float("inf")

    # Use flat arrays for speed
    prev = [(0, i, 0) for i in range(m + 1)]   # (S, D, I)

    for i in range(1, n + 1):
        curr = [(0, 0, i)] + [None] * m         # type: ignore[list-item]
        for j in range(1, m + 1):
            s_prev, d_prev, ins_prev = prev[j - 1]
            if ref[i - 1] == hyp[j - 1]:
                curr[j] = (s_prev, d_prev, ins_prev)   # match
            else:
                # substitution
                sub = (s_prev + 1, d_prev, ins_prev)
                # deletion  (ref word not in hyp)
                ps, pd, pi = prev[j]
                dlt = (ps, pd + 1, pi)
                # insertion (hyp word not in ref)
                cs, cd, ci = curr[j - 1]
                ins = (cs, cd, ci + 1)
                # pick minimum total edits
                opts = [sub, dlt, ins]
                curr[j] = min(opts, key=lambda t: sum(t))
        prev = curr

    return prev[m]   # type: ignore[return-value]


def compute_wer(reference: str, hypothesis: str) -> dict[str, Any]:
    """Compute WER between reference and hypothesis strings."""
    ref_words = _normalize_text(reference).split()
    hyp_words = _normalize_text(hypothesis).split()

    if not ref_words:
        return {"wer": 0.0, "S": 0, "D": 0, "I": 0, "N": 0}

    S, D, I = _edit_distance_ops(ref_words, hyp_words)
    N = len(ref_words)
    wer = (S + D + I) / N
    return {"wer": round(wer, 4), "S": S, "D": D, "I": I, "N": N}


# ─────────────────────────────────────────────────────────────────────────────
# Extraction F1
# ─────────────────────────────────────────────────────────────────────────────

def _word_overlap_ratio(a: str, b: str) -> float:
    a_words = set(_normalize_text(a).split())
    b_words = set(_normalize_text(b).split())
    if not a_words or not b_words:
        return 0.0
    return len(a_words & b_words) / max(len(a_words), len(b_words))


def compute_extraction_f1(
    extracted: list[dict],
    expected: list[dict],
    overlap_threshold: float = 0.70,
) -> dict[str, Any]:
    """
    Match extracted items to expected items by text similarity.
    TP = extracted item matched to at least one expected item (>=70% word overlap).
    """
    matched_expected: set[int] = set()
    tp = 0

    for ext in extracted:
        ext_text = ext.get("text", "")
        for idx, exp in enumerate(expected):
            if idx in matched_expected:
                continue
            if _word_overlap_ratio(ext_text, exp.get("text", "")) >= overlap_threshold:
                tp += 1
                matched_expected.add(idx)
                break

    fp = len(extracted) - tp
    fn = len(expected) - len(matched_expected)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "tp": tp, "fp": fp, "fn": fn,
        "precision": round(precision, 4),
        "recall":    round(recall, 4),
        "f1":        round(f1, 4),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Evidence Precision
# ─────────────────────────────────────────────────────────────────────────────

def compute_evidence_precision(items: list) -> dict[str, Any]:
    """
    Percentage of items whose status is NOT 'unsupported'
    (i.e., they passed the verify_items evidence check in evidence.py).
    """
    if not items:
        return {"evidence_precision": 1.0, "verified": 0, "total": 0}

    verified = sum(1 for i in items if getattr(i, "status", "proposed") != "unsupported")
    total    = len(items)
    return {
        "evidence_precision": round(verified / total, 4),
        "verified": verified,
        "total":    total,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Read-back Correction Rate (simulated)
# ─────────────────────────────────────────────────────────────────────────────

def compute_correction_rate(items: list, expected: list[dict]) -> dict[str, Any]:
    """
    Simulate correction rate: items that did NOT match expected ground truth
    would require correction during the read-back phase.
    correction_rate = FP / total_extracted  (items that are wrong / all items)
    """
    if not items:
        return {"correction_rate": 0.0, "corrections_needed": 0, "total": 0}

    extracted_dicts = [{"text": getattr(i, "text", "")} for i in items]
    f1_data = compute_extraction_f1(extracted_dicts, expected)

    fp = f1_data["fp"]
    total = len(items)
    correction_rate = fp / total if total else 0.0
    return {
        "correction_rate": round(correction_rate, 4),
        "corrections_needed": fp,
        "total": total,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Pipeline runner
# ─────────────────────────────────────────────────────────────────────────────

def run_pipeline(audio_path: str, ground_truth: dict, verbose: bool = True) -> dict[str, Any]:
    """
    Run the full backend pipeline and collect all metrics.
    Returns a result dict ready for JSON serialisation.
    """
    # ── Check Ollama availability early ──────────────────────────────────────
    try:
        import ollama as _ollama
        _ollama.list()          # lightweight connectivity check
    except Exception as e:
        raise RuntimeError(
            f"Ollama is not reachable: {e}\n"
            "Make sure Ollama is running (`ollama serve`) and the model is pulled\n"
            f"  ollama pull {os.getenv('OLLAMA_MODEL', 'llama3.1:8b')}"
        ) from e

    # ── Lazy imports (after path setup) ──────────────────────────────────────
    from backend.asr         import transcribe
    from backend.translation import translate_segments_to_english, is_translation_available
    from backend.extraction  import extract_items
    from backend.evidence    import verify_items

    meeting_id = str(uuid.uuid4())

    t_start = time.perf_counter()

    # ── Step 1: ASR ──────────────────────────────────────────────────────────
    _print_step(1, 5, "ASR Transcription...", verbose)
    segments = transcribe(audio_path, meeting_id)
    _print_done(f"{len(segments)} segments", verbose)

    # ── Step 2: Translation ───────────────────────────────────────────────────
    _print_step(2, 5, "Translation...", verbose)
    hindi_segs = [s for s in segments if s.language not in ("en",)]
    if hindi_segs and is_translation_available():
        translate_segments_to_english(segments)
        _print_done(f"{len(hindi_segs)} Hindi segments translated", verbose)
    else:
        _print_done("skipped (all English or transformers unavailable)", verbose)

    # ── Step 3: Extraction ────────────────────────────────────────────────────
    _print_step(3, 5, "Extraction...", verbose)
    items = extract_items(segments, meeting_id)
    _print_done(f"{len(items)} items extracted", verbose)

    # ── Step 4: Evidence Verification ─────────────────────────────────────────
    _print_step(4, 5, "Evidence Verification...", verbose)
    items = verify_items(items, segments)
    verified_count = sum(1 for i in items if i.status != "unsupported")
    _print_done(f"{verified_count}/{len(items)} items verified", verbose)

    # ── Step 5: Compute Metrics ───────────────────────────────────────────────
    _print_step(5, 5, "Computing Metrics...", verbose)

    t_end  = time.perf_counter()
    latency = round(t_end - t_start, 2)

    # --- WER ---
    gt_transcript = ground_truth.get("transcript", [])
    ref_text = " ".join(seg["text"] for seg in gt_transcript)
    hyp_text = " ".join(seg.text   for seg in segments)
    wer_result = compute_wer(ref_text, hyp_text)

    # --- Extraction F1 ---
    expected_items = ground_truth.get("expected_items", [])
    extracted_dicts = [{"text": i.text} for i in items]
    f1_result = compute_extraction_f1(extracted_dicts, expected_items)

    # --- Evidence Precision ---
    ev_result = compute_evidence_precision(items)

    # --- Correction Rate ---
    cr_result = compute_correction_rate(items, expected_items)

    _print_done("", verbose)

    return {
        "audio_path":       audio_path,
        "meeting_id":       meeting_id,
        "timestamp":        datetime.now(timezone.utc).isoformat(),
        "segments":         len(segments),
        "items_extracted":  len(items),
        "wer":              wer_result,
        "extraction_f1":    f1_result,
        "evidence":         ev_result,
        "correction_rate":  cr_result,
        "latency_seconds":  latency,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Ground-truth-only mode (no audio — metrics from GT transcript only)
# ─────────────────────────────────────────────────────────────────────────────

def run_pipeline_gt_only(ground_truth: dict, verbose: bool = True) -> dict[str, Any]:
    """
    Dry-run using the ground truth transcript as the ASR output.
    Useful for smoke-testing extraction + evidence metrics without real audio.
    """
    # ── Check Ollama availability early ──────────────────────────────────────
    try:
        import ollama as _ollama
        _ollama.list()
    except Exception as e:
        raise RuntimeError(
            f"Ollama is not reachable: {e}\n"
            "Make sure Ollama is running (`ollama serve`) and the model is pulled\n"
            f"  ollama pull {os.getenv('OLLAMA_MODEL', 'llama3.1:8b')}"
        ) from e

    from backend.meeting_record import Segment
    from backend.extraction     import extract_items
    from backend.evidence       import verify_items

    meeting_id = str(uuid.uuid4())
    t_start = time.perf_counter()

    _print_step(1, 5, "Building segments from ground truth...", verbose)
    gt_segs_raw = ground_truth.get("transcript", [])
    segments = [
        Segment(
            id=s["id"],
            start=s["start"],
            end=s["end"],
            text=s["text"],
            language=s.get("language", "en"),
        )
        for s in gt_segs_raw
    ]
    _print_done(f"{len(segments)} segments (from GT)", verbose)

    _print_step(2, 5, "Translation...", verbose)
    _print_done("skipped in GT-only mode", verbose)

    _print_step(3, 5, "Extraction...", verbose)
    items = extract_items(segments, meeting_id)
    _print_done(f"{len(items)} items extracted", verbose)

    _print_step(4, 5, "Evidence Verification...", verbose)
    items = verify_items(items, segments)
    verified_count = sum(1 for i in items if i.status != "unsupported")
    _print_done(f"{verified_count}/{len(items)} items verified", verbose)

    _print_step(5, 5, "Computing Metrics...", verbose)
    t_end   = time.perf_counter()
    latency = round(t_end - t_start, 2)

    # WER is 0 by definition (GT text == GT text)
    wer_result = {"wer": 0.0, "S": 0, "D": 0, "I": 0, "N": sum(len(s["text"].split()) for s in gt_segs_raw)}

    expected_items = ground_truth.get("expected_items", [])
    extracted_dicts = [{"text": i.text} for i in items]
    f1_result  = compute_extraction_f1(extracted_dicts, expected_items)
    ev_result  = compute_evidence_precision(items)
    cr_result  = compute_correction_rate(items, expected_items)

    _print_done("", verbose)

    return {
        "audio_path":       "(ground-truth only — no audio)",
        "meeting_id":       meeting_id,
        "timestamp":        datetime.now(timezone.utc).isoformat(),
        "segments":         len(segments),
        "items_extracted":  len(items),
        "wer":              wer_result,
        "extraction_f1":    f1_result,
        "evidence":         ev_result,
        "correction_rate":  cr_result,
        "latency_seconds":  latency,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Pretty printing helpers
# ─────────────────────────────────────────────────────────────────────────────

def _print_step(n: int, total: int, label: str, verbose: bool) -> None:
    if verbose:
        print(f"[{n}/{total}] {label:<35}", end="", flush=True)


def _print_done(detail: str, verbose: bool) -> None:
    if verbose:
        tick = "\u2713"
        print(f" {tick} {detail}")


def print_header(audio: str, gt_path: str) -> None:
    width = 50
    print("=" * width)
    print(" Meeting Intelligence Evaluator".center(width))
    print("=" * width)
    print(f"Audio:        {audio}")
    print(f"Ground Truth: {gt_path}")
    print(f"Started:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


def print_results(result: dict) -> None:
    wer       = result["wer"]
    f1        = result["extraction_f1"]
    ev        = result["evidence"]
    cr        = result["correction_rate"]
    latency   = result["latency_seconds"]

    sep = "\u2501" * 50
    print(f"\n{sep}")
    print(" RESULTS".center(50))
    print(sep)
    print(f"{'Word Error Rate (WER)':<32}: {wer['wer']*100:.1f}%  (S={wer['S']} D={wer['D']} I={wer['I']} N={wer['N']})")
    print(f"{'Extraction Precision':<32}: {f1['precision']*100:.1f}%")
    print(f"{'Extraction Recall':<32}: {f1['recall']*100:.1f}%")
    print(f"{'Extraction F1':<32}: {f1['f1']*100:.1f}%  (TP={f1['tp']} FP={f1['fp']} FN={f1['fn']})")
    print(f"{'Evidence Precision':<32}: {ev['evidence_precision']*100:.1f}%  ({ev['verified']}/{ev['total']} verified)")
    print(f"{'Simulation Correction Rate':<32}: {cr['correction_rate']*100:.1f}%  ({cr['corrections_needed']} of {cr['total']} need fix)")
    print(f"{'Pipeline Latency':<32}: {latency:.1f}s")
    print(sep)
    print()


def save_results(result: dict, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"results_{ts}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Results saved → {out_path}")
    return out_path


# ─────────────────────────────────────────────────────────────────────────────
# Batch runner
# ─────────────────────────────────────────────────────────────────────────────

def run_batch(
    samples_dir: Path,
    save: bool,
    gt_only: bool,
    verbose: bool,
) -> None:
    """Run evaluation for every *.json file in samples_dir."""
    json_files = sorted(samples_dir.glob("*.json"))
    if not json_files:
        print(f"No *.json ground-truth files found in {samples_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"\nBatch mode: {len(json_files)} sample(s) found in {samples_dir}\n")
    all_results = []

    for gt_path in json_files:
        print(f"\n{'─'*50}")
        print(f" Sample: {gt_path.name}")
        print(f"{'─'*50}")

        with open(gt_path, encoding="utf-8") as f:
            ground_truth = json.load(f)

        try:
            if gt_only:
                result = run_pipeline_gt_only(ground_truth, verbose=verbose)
            else:
                # In batch mode without explicit audio, fall back to gt_only
                print("  \u26a0  No --audio provided. Running GT-only (extraction+evidence) mode.")
                result = run_pipeline_gt_only(ground_truth, verbose=verbose)

            result["ground_truth_file"] = str(gt_path)
            print_results(result)
            all_results.append(result)

            if save:
                save_results(result, _ROOT / "eval" / "results")

        except RuntimeError as e:
            print(f"\n  ✗ ERROR: {e}\n", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"\n  ✗ Unexpected error on {gt_path.name}: {e}\n", file=sys.stderr)
            import traceback
            traceback.print_exc()

    # Aggregate summary
    if len(all_results) > 1:
        print("\n" + "=" * 50)
        print(" BATCH AGGREGATE SUMMARY")
        print("=" * 50)
        avg_wer       = sum(r["wer"]["wer"] for r in all_results) / len(all_results)
        avg_f1        = sum(r["extraction_f1"]["f1"] for r in all_results) / len(all_results)
        avg_ev        = sum(r["evidence"]["evidence_precision"] for r in all_results) / len(all_results)
        avg_cr        = sum(r["correction_rate"]["correction_rate"] for r in all_results) / len(all_results)
        avg_lat       = sum(r["latency_seconds"] for r in all_results) / len(all_results)
        print(f"  Samples evaluated   : {len(all_results)}")
        print(f"  Avg WER             : {avg_wer*100:.1f}%")
        print(f"  Avg Extraction F1   : {avg_f1*100:.1f}%")
        print(f"  Avg Evidence Prec.  : {avg_ev*100:.1f}%")
        print(f"  Avg Correction Rate : {avg_cr*100:.1f}%")
        print(f"  Avg Latency         : {avg_lat:.1f}s")
        print("=" * 50)


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="benchmark",
        description="Meeting Intelligence End-to-End Evaluator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--audio",
        metavar="AUDIO",
        help="Path to input audio file (.wav / .mp3 / etc.)",
    )
    mode.add_argument(
        "--batch",
        metavar="SAMPLES_DIR",
        help="Directory containing ground-truth *.json files. Runs GT-only mode for each.",
    )

    p.add_argument(
        "--ground-truth",
        metavar="GT_JSON",
        help="Path to ground-truth JSON file (required with --audio).",
    )
    p.add_argument(
        "--gt-only",
        action="store_true",
        help="Use ground-truth transcript as ASR output (no real audio needed). "
             "Skips WER; tests extraction/evidence/latency only.",
    )
    p.add_argument(
        "--save",
        action="store_true",
        help="Save results to eval/results/results_<timestamp>.json",
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress step-by-step progress output.",
    )
    p.add_argument(
        "--verbose-log",
        action="store_true",
        help="Enable DEBUG logging from the backend modules.",
    )
    return p


def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    if args.verbose_log:
        logging.getLogger().setLevel(logging.DEBUG)

    verbose = not args.quiet

    # ── Single file mode ──────────────────────────────────────────────────────
    if args.audio:
        if not args.ground_truth:
            parser.error("--ground-truth is required when using --audio")

        audio_path = Path(args.audio)
        gt_path    = Path(args.ground_truth)

        if not audio_path.exists():
            print(f"ERROR: audio file not found: {audio_path}", file=sys.stderr)
            sys.exit(1)
        if not gt_path.exists():
            print(f"ERROR: ground-truth file not found: {gt_path}", file=sys.stderr)
            sys.exit(1)

        with open(gt_path, encoding="utf-8") as f:
            ground_truth = json.load(f)

        print_header(str(audio_path), str(gt_path))

        try:
            if args.gt_only:
                result = run_pipeline_gt_only(ground_truth, verbose=verbose)
            else:
                result = run_pipeline(str(audio_path), ground_truth, verbose=verbose)
        except RuntimeError as e:
            print(f"\n✗ ERROR: {e}\n", file=sys.stderr)
            sys.exit(1)

        print_results(result)

        if args.save:
            save_results(result, _ROOT / "eval" / "results")

    # ── Batch mode ────────────────────────────────────────────────────────────
    elif args.batch:
        samples_dir = Path(args.batch)
        if not samples_dir.is_dir():
            print(f"ERROR: batch directory not found: {samples_dir}", file=sys.stderr)
            sys.exit(1)
        run_batch(samples_dir, save=args.save, gt_only=args.gt_only, verbose=verbose)


if __name__ == "__main__":
    main()
