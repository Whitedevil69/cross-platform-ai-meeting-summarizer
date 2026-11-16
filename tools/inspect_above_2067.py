# tools/inspect_above_2067.py
import sys
with open('temp_script_1.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(max(0, 1990), min(len(lines), 2060)):
    sys.stdout.buffer.write(f"{i+1}: {repr(lines[i])}\n".encode('utf-8', errors='replace'))
