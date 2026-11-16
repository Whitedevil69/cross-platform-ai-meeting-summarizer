# tools/check_remaining_apps.py
import sys

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

count = 0
for i in range(5500, min(6500, len(lines))):
    line = lines[i]
    if any(k in line for k in ['color:#38bdf8', 'color:#c4b5fd', 'color:#e2e8f0', 'color:#cbd5e1', 'background:rgba(124,58,237']):
        count += 1
        sys.stdout.buffer.write(f"Line {i+1}: {line.strip()[:100]}\n".encode('utf-8', errors='replace'))

print(f"Total occurrences found in remaining apps: {count}")
