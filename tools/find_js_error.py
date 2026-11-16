# tools/find_js_error.py
import sys
with open('temp_script_1.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(max(0, 2055), min(len(lines), 2080)):
    sys.stdout.buffer.write(f"{i+1}: {repr(lines[i])}\n".encode('utf-8', errors='replace'))
