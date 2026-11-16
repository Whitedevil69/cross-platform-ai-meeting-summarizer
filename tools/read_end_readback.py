import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open("frontend/readback.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines[560:]:
    print(line, end='')
