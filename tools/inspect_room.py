# inspect_room.py
import re

with open("frontend/room.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's see what classes are referenced in the <script> tag
script_start = text.find("<script>")
script_content = text[script_start:]

classes_in_script = set(re.findall(r'class(?:Name)?\s*=\s*["\']([^"\']+)["\']', script_content))
class_lists = set(re.findall(r'classList\.(?:add|remove|toggle)\(["\']([^"\']+)["\']\)', script_content))

print(f"Classes dynamically used in JS: {len(classes_in_script)}")
for c in sorted(classes_in_script)[:20]:
    print(" -", c)

print(f"\nClassList tokens used in JS: {len(class_lists)}")
for c in sorted(class_lists)[:20]:
    print(" -", c)
