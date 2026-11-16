# tools/find_exact_unbalance.py
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

d = 0
for i in range(3000, 4220):
    op = lines[i].count('<div')
    cl = lines[i].count('</div')
    d += (op - cl)
    # print when d decreases or changes
    if 'id="view-' in lines[i]:
        print(f"Line {i+1} [{lines[i].strip()[:35]}]: depth={d}")
    if op != cl:
        # check
        pass

print(f"End at 4220: depth={d}")
