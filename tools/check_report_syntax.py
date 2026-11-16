import re, subprocess

with open("frontend/report.html", "r", encoding="utf-8") as f:
    text = f.read()

script_m = re.search(r'<script>([\s\S]*?)</script>', text)
if script_m:
    with open("tools/temp_report_script.js", "w", encoding="utf-8") as f:
        f.write(script_m.group(1))
    res = subprocess.run(["node", "-c", "tools/temp_report_script.js"], capture_output=True, text=True)
    if res.returncode == 0:
        print("[OK] Report JavaScript syntax is valid!")
    else:
        print("[FAIL] Report JavaScript error:", res.stderr)
