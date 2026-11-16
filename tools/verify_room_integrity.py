# tools/verify_room_integrity.py
import re
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open("frontend/room.html.bak_ref_vibe", "r", encoding="utf-8") as f:
    bak_text = f.read()

with open("frontend/room.html", "r", encoding="utf-8") as f:
    new_text = f.read()

# 1. Compare IDs
bak_ids = set(re.findall(r'id=["\']([^"\']+)["\']', bak_text))
new_ids = set(re.findall(r'id=["\']([^"\']+)["\']', new_text))

missing_ids = bak_ids - new_ids
if missing_ids:
    print(f"[FAIL] Missing IDs: {missing_ids}")
else:
    print(f"[OK] All {len(bak_ids)} original DOM IDs are preserved!")

# 2. Extract JS and test with node
script_m = re.search(r'<script>([\s\S]*?)</script>', new_text)
if script_m:
    js_code = script_m.group(1)
    with open("tools/temp_room_script.js", "w", encoding="utf-8") as f:
        f.write(js_code)
    
    res = subprocess.run(["node", "-c", "tools/temp_room_script.js"], capture_output=True, text=True)
    if res.returncode == 0:
        print("[OK] JavaScript syntax check PASSED (node -c returned 0)")
    else:
        print("[FAIL] JavaScript syntax error:")
        print(res.stderr)
else:
    print("[FAIL] Could not find <script> in new_text")
