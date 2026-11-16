# tools/inspect_home_end.py
import sys

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(3515, 3530):
    sys.stdout.buffer.write(f"{i+1}: {repr(lines[i])}\n".encode('utf-8', errors='replace'))
