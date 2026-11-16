# tools/refactor_views.py
import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print('Length of frontend/index.html:', len(content))
print('Check ids:')
for tag_id in ['view-home', 'view-chat', 'view-phone', 'view-docs', 'view-whiteboards', 'view-clips', 'wpMoreAppsPopover', 'wpAppSuiteModalOverlay']:
    print(f'  {tag_id}: {content.count(tag_id)}')
