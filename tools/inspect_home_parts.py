# tools/inspect_home_parts.py
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

left_start = text.find('<div class="ref-left-col">')
right_start = text.find('<div class="ref-right-col">')
right_end = text.find('</div>\n        </div>\n      </div>\n\n      <!-- ════════════════════════════════════════════════════════════════')

print("left_start:", left_start)
print("right_start:", right_start)
print("right_end:", right_end)

if left_start != -1 and right_start != -1:
    left_content = text[left_start + len('<div class="ref-left-col">'):right_start].strip()
    # Remove trailing </div> that closed ref-left-col
    if left_content.endswith('</div>'):
        left_content = left_content[:-6].strip()
    print("Left content length:", len(left_content))

    right_content = text[right_start:right_end].strip()
    print("Right content length:", len(right_content))
