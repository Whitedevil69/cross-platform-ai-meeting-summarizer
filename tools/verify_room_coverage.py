import re
import sys
from build_room_css import NEW_CSS

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open("frontend/room.html", "r", encoding="utf-8") as f:
    text = f.read()

html_part = text[text.find("<body>"):text.find("<script>")]
script_content = text[text.find("<script>"):]

classes_in_html = set(re.findall(r'class=["\']([^"\']+)["\']', html_part))
flat_html_classes = set()
for c in classes_in_html:
    for item in c.split():
        flat_html_classes.add(item)

classes_in_script = set(re.findall(r'class(?:Name)?\s*=\s*["\']([^"\']+)["\']', script_content))
flat_script_classes = set()
for c in classes_in_script:
    for item in c.split():
        # filter out template variables like ${...}
        clean = re.sub(r'\$\{[^}]+\}', '', item)
        if clean:
            flat_script_classes.add(clean)

class_lists = set(re.findall(r'classList\.(?:add|remove|toggle)\(["\']([^"\']+)["\']\)', script_content))

all_needed_classes = flat_html_classes.union(flat_script_classes).union(class_lists)

css_classes = set(re.findall(r'\.([a-zA-Z0-9_-]+)', NEW_CSS))

missing_classes = sorted(all_needed_classes - css_classes)
print(f"Total needed classes: {len(all_needed_classes)}")
print(f"Missing in new CSS: {len(missing_classes)}")
for mc in missing_classes:
    print(" - Missing:", mc)
