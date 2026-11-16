# tools/inspect_line_4216.py
import sys

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(4195, min(4235, len(lines))):
    sys.stdout.buffer.write(f"{i+1}: {repr(lines[i])}\n".encode('utf-8', errors='replace'))
