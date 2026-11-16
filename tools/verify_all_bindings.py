# tools/verify_all_bindings.py
import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all getElementById calls
elem_calls = set(re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", content))
print(f"Total unique document.getElementById references: {len(elem_calls)}")

missing_in_dom = []
for el_id in elem_calls:
    if f'id="{el_id}"' not in content and f"id='{el_id}'" not in content:
        # Note: Some elements like mailSubject, mailRecipients, schedDuration etc. are dynamically injected by render*App()
        # Let's check if they exist either in static DOM or inside JS strings
        if f'id=\\"{el_id}\\"' not in content and f'id=\'{el_id}\'' not in content and f'id="{el_id}"' not in content:
            missing_in_dom.append(el_id)

print(f"Missing from DOM or dynamic templates: {len(missing_in_dom)}")
if missing_in_dom:
    print("Missing IDs:", missing_in_dom)
else:
    print("[OK] Every referenced element ID exists statically or dynamically!")

# Check all window.* assignments
window_funcs = set(re.findall(r"window\.([a-zA-Z0-9_]+)\s*=", content))
print(f"Total window functions exposed: {len(window_funcs)}")
for wf in sorted(window_funcs):
    print(f"  window.{wf}")
