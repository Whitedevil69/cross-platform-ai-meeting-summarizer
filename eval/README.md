# Evaluation Test Harness

End-to-end benchmark suite for the Meeting Intelligence System.  
Computes the **five whitepaper metrics** against ground-truth JSON samples.

---

## Directory Structure

```
eval/
├── benchmark.py          # CLI benchmark script
├── __init__.py
├── README.md             # this file
├── samples/
│   ├── english_sample.json   # 5-segment pure-English meeting
│   └── hinglish_sample.json  # 6-segment Hindi-English code-switched meeting
└── results/              # auto-created by --save; one JSON per run
```

---

## Prerequisites

1. **Ollama running** with the target model pulled:
   ```bash
   ollama serve                        # in one terminal
   ollama pull llama3.1:8b             # or your OLLAMA_MODEL env var
   ```

2. **Python dependencies** installed:
   ```bash
   pip install -r requirements.txt
   ```

3. Run commands from the **project root** directory.

---

## Usage

### Single file (real audio)

```bash
python eval/benchmark.py \
  --audio path/to/meeting.wav \
  --ground-truth eval/samples/english_sample.json
```

### Single file — GT-only mode (no audio needed)

Uses the ground-truth transcript directly as ASR output.  
Skips WER (trivially 0); tests extraction, evidence verification, and latency.

```bash
python eval/benchmark.py \
  --ground-truth eval/samples/english_sample.json \
  --audio eval/samples/english_sample.json \
  --gt-only
```

### Batch mode (all samples in a directory)

```bash
python eval/benchmark.py --batch eval/samples/
```

### Save results to JSON

Add `--save` to any command; results are written to `eval/results/results_<timestamp>.json`.

```bash
python eval/benchmark.py --batch eval/samples/ --save
```

### Module invocation (from project root)

```bash
python -m eval.benchmark --batch eval/samples/
```

### All flags

| Flag | Description |
|------|-------------|
| `--audio FILE` | Input audio file |
| `--ground-truth FILE` | Ground-truth JSON (required with `--audio`) |
| `--batch DIR` | Batch mode — run all `*.json` in directory |
| `--gt-only` | Skip real ASR; use GT transcript as hypothesis |
| `--save` | Save results to `eval/results/` |
| `--quiet` | Suppress step-by-step progress |
| `--verbose-log` | Enable DEBUG logging from backend |

---

## Metrics

| Metric | Formula | Notes |
|--------|---------|-------|
| **WER** | `(S + D + I) / N` | NFKC + lowercase normalisation before comparison |
| **Extraction Precision** | `TP / (TP + FP)` | ≥70 % word overlap = True Positive |
| **Extraction Recall** | `TP / (TP + FN)` | Matched against `expected_items` in GT |
| **Extraction F1** | harmonic mean of P & R | |
| **Evidence Precision** | `verified / total` | Items whose quote passes `verify_items` |
| **Correction Rate** | `FP / total_extracted` | Simulated: items needing fix in read-back |
| **Pipeline Latency** | wall-clock seconds | Includes ASR + translation + extraction + evidence |

---

## Ground-Truth JSON Format

```json
{
  "transcript": [
    {"id": 0, "start": 0.0, "end": 3.5, "text": "We decided to use React.", "language": "en"},
    {"id": 1, "start": 3.5, "end": 7.0, "text": "Rahul will submit the report by Friday.", "language": "en"}
  ],
  "expected_items": [
    {"type": "decision", "text": "Use React for the frontend"},
    {"type": "action",   "text": "Rahul will submit the report", "owner": "Rahul", "deadline": "Friday"}
  ],
  "meta": {
    "description": "Optional description",
    "language": "en"
  }
}
```

> [!NOTE]
> The `transcript` field is used both as the WER reference and (in `--gt-only` mode) as the direct ASR input to the extraction pipeline.

---

## Example Output

```
==================================================
        Meeting Intelligence Evaluator
==================================================
Audio:        meeting.wav
Ground Truth: eval/samples/english_sample.json
Started:      2026-11-02 23:45:00

[1/5] ASR Transcription...           ✓ 5 segments
[2/5] Translation...                 ✓ skipped (all English or transformers unavailable)
[3/5] Extraction...                  ✓ 4 items extracted
[4/5] Evidence Verification...       ✓ 4/4 items verified
[5/5] Computing Metrics...           ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Word Error Rate (WER)           : 12.3%  (S=3 D=1 I=2 N=48)
Extraction Precision            : 80.0%
Extraction Recall               : 64.0%
Extraction F1                   : 71.1%  (TP=4 FP=1 FN=1)
Evidence Precision              : 100.0%  (4/4 verified)
Simulation Correction Rate      : 20.0%  (1 of 5 need fix)
Pipeline Latency                : 18.4s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Adding New Samples

1. Create a new JSON file in `eval/samples/` following the ground-truth format above.
2. Run `python eval/benchmark.py --batch eval/samples/` — it will be picked up automatically.
3. For real-audio tests, pair each JSON with a matching `.wav` file and call `--audio` explicitly.
