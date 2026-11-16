# tools/inspect_room_html.py
import sys

with open('frontend/room.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find topbar, main area, bottom bar
print("Topbar:", bool(re.search(r'<header|<div class="topbar"', text)))
print("Bottombar:", bool(re.search(r'<footer|<div class="bottombar"|<div class="controls', text)))

# Let's inspect where <body> starts
body_idx = text.find('<body')
print("Body pos:", body_idx)
sys.stdout.buffer.write(text[body_idx:body_idx+1500].encode('utf-8', errors='replace'))
