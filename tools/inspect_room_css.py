# tools/inspect_room_css.py
with open('frontend/room.html', 'r', encoding='utf-8') as f:
    text = f.read()

style_start = text.find('<style>')
style_end = text.find('</style>')

print(f"Style length: {style_end - style_start}")

import re
classes = re.findall(r'\.([a-zA-Z0-9_\-]+)\s*\{', text[style_start:style_end])
print(f"Found {len(set(classes))} unique CSS classes in room.html")
print("Sample classes:", list(set(classes))[:40])
