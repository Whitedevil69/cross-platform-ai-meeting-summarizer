# tools/inspect_room_root.py
import sys

with open('frontend/room.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(15, 80):
    sys.stdout.buffer.write(f"{i+1}: {lines[i]}".encode('utf-8', errors='replace'))
