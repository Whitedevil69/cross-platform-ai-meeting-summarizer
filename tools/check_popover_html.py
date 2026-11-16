# tools/check_popover_html.py
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'(<div class="wp-more-popover" id="wpMoreAppsPopover".*?</div>\s*</div>)', text, re.DOTALL)
if m:
    print("Found Popover HTML, length:", len(m.group(1)))
    print(m.group(1)[:300])
    print("...")
    print(m.group(1)[-200:])
else:
    print("Not found")
