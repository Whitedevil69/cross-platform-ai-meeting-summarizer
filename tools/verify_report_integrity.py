# tools/verify_report_integrity.py
import re
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open("frontend/report.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Extract script and test with node
script_m = re.search(r'<script>([\s\S]*?)</script>', text)
if script_m:
    js_code = script_m.group(1)
    with open("tools/temp_report_script.js", "w", encoding="utf-8") as f:
        f.write(js_code)
    res = subprocess.run(["node", "-c", "tools/temp_report_script.js"], capture_output=True, text=True)
    if res.returncode == 0:
        print("[OK] JavaScript syntax check PASSED")
    else:
        print("[FAIL] JavaScript syntax error:", res.stderr)
else:
    print("[FAIL] No <script> found")

# 2. Check essential IDs
essential_ids = ["loading-state", "content", "report-title", "report-meta", "stats-grid", "items-panel", "graph-svg", "header-readback-link", "toast"]
for eid in essential_ids:
    if f'id="{eid}"' in text:
        print(f" [OK] id='{eid}' present")
    else:
        print(f" [FAIL] id='{eid}' missing!")

# 3. Check JSON removal
if "exportJSON" in text:
    print(" [NOTE] exportJSON function still in text (unused if button removed)")
if "JSON" in text:
    lines_with_json = [line.strip() for line in text.splitlines() if "JSON" in line]
    print(f" Lines containing 'JSON': {lines_with_json}")
