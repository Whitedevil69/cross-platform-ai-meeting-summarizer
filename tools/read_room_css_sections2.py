# tools/read_room_css_sections2.py
import sys

with open('frontend/room.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_lines(start, end):
    for i in range(start, min(end, len(lines))):
        sys.stdout.buffer.write(f"{i+1}: {lines[i]}".encode('utf-8', errors='replace'))

print("=== Section 2: top-bar, panels, tiles ===")
print_lines(90, 220)
