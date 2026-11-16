# tools/find_div_mismatch.py
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

depth = 0
for line_no, line in enumerate(lines):
    opens = line.count('<div')
    closes = line.count('</div')
    depth += (opens - closes)
    if depth < 0:
        print(f"Negative depth at line {line_no+1}: depth={depth}, line: {repr(line.strip()[:60])}")
        break

print(f"Final depth at end of file: {depth}")
