# tools/test_all_17_views.py
import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

all_views = [
    'home', 'chat', 'phone', 'docs', 'whiteboards', 'clips',
    'mail', 'calendar', 'scheduler', 'surveys', 'apps', 'workspaces',
    'contacts', 'events', 'revenue', 'contactcenter', 'workvivo'
]

print(f"Testing all {len(all_views)} views for the Dribbble homepage template components:")
for v in all_views:
    m = re.search(rf'<div class="wp-tab-view" id="view-{v}".*?</div>\s*(?=<div class="wp-tab-view"|</div\s*>\s*<!-- RIGHT COLUMN)', text, re.DOTALL)
    if not m:
        print(f"  [ERROR] view-{v} not found or boundary issue")
        continue
    vt = m.group(0)
    has_three_cards = 'ref-three-cards-row' in vt
    has_metric = 'ref-card-metric' in vt
    has_highlight = 'ref-card-highlight' in vt
    has_hero = 'ref-card-dark-hero' in vt
    has_capsules = 'ref-capsules-row' in vt
    all_ok = has_three_cards and has_metric and has_highlight and has_hero and has_capsules
    print(f"  view-{v}: {'[OK] Matches Homepage Template' if all_ok else '[WARN] Missing components'} (length: {len(vt)})")
