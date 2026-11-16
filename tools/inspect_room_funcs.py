import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open("frontend/room.html", "r", encoding="utf-8") as f:
    text = f.read()

body_start = text.find("<body>")
script_start = text.find("<script>")
html_content = text[body_start:script_start]

for m in re.finditer(r'style=["\']([^"\']+)["\']', html_content):
    start = max(0, m.start() - 30)
    end = min(len(html_content), m.end() + 30)
    print(html_content[start:end])
    print("-" * 30)
