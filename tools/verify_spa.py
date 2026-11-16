# tools/verify_spa.py
import re
import sys
import subprocess

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("File size:", len(content))

# 1. Check required view IDs
required_ids = [
    'view-home', 'view-chat', 'view-phone', 'view-docs', 'view-whiteboards', 'view-clips',
    'wpMoreAppsPopover', 'wpAppSuiteModalOverlay', 'wpAppSuiteModalDialog', 'wpAppModalNavBar', 'wpAppModalBody',
    'dialScreen', 'chatMessagesScroll', 'chatInputText', 'docViewerTitle', 'docViewerMeta', 'docItemsTableBody',
    'whiteboardSvg', 'clipsFeedList', 'wpGlobalSearch', 'btnToggleMoreApps'
]

missing_ids = []
for req_id in required_ids:
    c = content.count(f'id="{req_id}"')
    if c != 1:
        missing_ids.append((req_id, c))

if missing_ids:
    print("[ERROR] Issues with required IDs:", missing_ids)
else:
    print("[OK] All required element IDs exist exactly once!")

# 2. Check unclosed div count
open_divs = content.count('<div')
close_divs = content.count('</div>')
print(f"Open divs: {open_divs}, Close divs: {close_divs}")
if open_divs == close_divs:
    print("[OK] <div> tags are perfectly balanced!")
else:
    print(f"[WARN] Div mismatch: {open_divs - close_divs}")

# 3. Check JavaScript syntax via Node.js
scripts = re.findall(r'<script(?:\s+[^>]*)?>(.*?)</script>', content, re.DOTALL)
print(f"Found {len(scripts)} script tags")

for idx, s in enumerate(scripts):
    if not s.strip():
        continue
    # write to temp js
    with open(f'temp_script_{idx}.js', 'w', encoding='utf-8') as tf:
        tf.write(s)
    try:
        res = subprocess.run(['node', '-c', f'temp_script_{idx}.js'], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[OK] Script tag #{idx+1} passed Node.js syntax check")
        else:
            print(f"[ERROR] Script tag #{idx+1} syntax error:\n{res.stderr}")
    except Exception as e:
        print(f"Node test failed to run: {e}")
