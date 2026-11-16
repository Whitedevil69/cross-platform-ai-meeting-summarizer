# tools/clean_switch_js.py
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find where window.switchMainTab starts and where window.loadDocsView starts
start = text.find('window.switchMainTab = function')
end = text.find('// ── View Loader: Docs ──')

print(f"Slice from {start} to {end}")
print(text[start:end])
