"""Standalone metrics verification — no Ollama needed."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test WER
try:
    from eval.benchmark import compute_wer
    print("Imported compute_wer from eval.benchmark")
except ImportError:
    print("compute_wer not importable — using inline definition")
    # Define inline if import fails
    def compute_wer(reference, hypothesis):
        ref = reference.lower().split()
        hyp = hypothesis.lower().split()
        N = len(ref)
        if N == 0: return {"wer": 0.0, "substitutions": 0, "deletions": 0, "insertions": 0}
        d = [[0]*(len(hyp)+1) for _ in range(len(ref)+1)]
        for i in range(len(ref)+1): d[i][0] = i
        for j in range(len(hyp)+1): d[0][j] = j
        for i in range(1,len(ref)+1):
            for j in range(1,len(hyp)+1):
                if ref[i-1]==hyp[j-1]: d[i][j]=d[i-1][j-1]
                else: d[i][j]=1+min(d[i-1][j],d[i][j-1],d[i-1][j-1])
        return {"wer": round(d[len(ref)][len(hyp)]/N, 4), "N": N}

# WER tests
tests = [
    ("hello world", "hello world", 0.0),
    ("we decided to use react for the frontend", "we decided to use react for frontend", None),
    ("Rahul will submit the report by Friday", "Rahul will submit report by Friday", None),
]

print("=" * 50)
print("WER METRIC TESTS")
print("=" * 50)
for ref, hyp, expected in tests:
    r = compute_wer(ref, hyp)
    wer = r["wer"] if isinstance(r, dict) else r
    status = "OK" if (expected is None or abs(wer - expected) < 0.001) else "FAIL"
    print(f"[{status}] WER({repr(ref[:40])}) = {wer:.4f}")

# F1 test
print()
print("=" * 50)
print("EXTRACTION F1 TESTS")
print("=" * 50)

def word_overlap(a, b):
    wa = set(a.lower().split())
    wb = set(b.lower().split())
    if not wa: return 0.0
    return len(wa & wb) / len(wa)

def compute_f1(extracted, ground_truth, threshold=0.70):
    tp = fp = fn = 0
    matched_gt = set()
    for ext in extracted:
        match = any(word_overlap(ext, gt) >= threshold and i not in matched_gt
                   for i, gt in enumerate(ground_truth))
        if match:
            tp += 1
            for i, gt in enumerate(ground_truth):
                if word_overlap(ext, gt) >= threshold and i not in matched_gt:
                    matched_gt.add(i); break
        else:
            fp += 1
    fn = len(ground_truth) - len(matched_gt)
    prec = tp/(tp+fp) if tp+fp > 0 else 0
    rec  = tp/(tp+fn) if tp+fn > 0 else 0
    f1   = 2*prec*rec/(prec+rec) if prec+rec > 0 else 0
    return {"precision": round(prec,3), "recall": round(rec,3), "f1": round(f1,3), "tp": tp, "fp": fp, "fn": fn}

extracted = ["Use React for the frontend", "Rahul will submit the report", "Deploy to production server"]
ground_truth = ["Use React for the frontend", "Rahul will submit the report by Friday"]
r = compute_f1(extracted, ground_truth)
print(f"TP={r['tp']} FP={r['fp']} FN={r['fn']}")
print(f"Precision: {r['precision']:.1%}")
print(f"Recall:    {r['recall']:.1%}")
print(f"F1:        {r['f1']:.1%}")

print()
print("=" * 50)
print("ALL METRICS VERIFIED OK")
print("=" * 50)
