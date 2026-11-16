# tools/inspect_room_body2.py
import sys

with open('frontend/room.html', 'r', encoding='utf-8') as f:
    text = f.read()

body_idx = text.find('<body')
sys.stdout.buffer.write(text[body_idx+1500:body_idx+4500].encode('utf-8', errors='replace'))
