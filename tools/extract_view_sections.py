# tools/extract_view_sections.py
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find view-home
vh_match = re.search(r'(<div class="wp-tab-view" id="view-home">.*?</div>\s*</div>\s*</div>\s*</div>)', text, re.DOTALL)
print("View home matched:", bool(vh_match))
if vh_match:
    print("Length:", len(vh_match.group(1)))

# Let's inspect where view-home starts and where view-clips ends
start_idx = text.find('<div class="wp-tab-view" id="view-home">')
end_idx = text.find('</main>')

print(f"Indices: {start_idx} to {end_idx}")
slice_text = text[start_idx:end_idx]
print(f"Total slice length: {len(slice_text)}")

# Let's count views in slice
for v in ['view-home', 'view-chat', 'view-phone', 'view-docs', 'view-whiteboards', 'view-clips']:
    print(f"  {v}: {slice_text.count(v)}")
