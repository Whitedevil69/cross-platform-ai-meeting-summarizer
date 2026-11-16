# tools/inspect_sub_bar.py
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

sub_bar_start = text.find('<div class="ref-sub-header-bar">')
sub_bar_end = text.find('<div class="ref-dashboard-grid">')

print(f"sub_bar slice ({sub_bar_start} to {sub_bar_end}):")
import sys
sys.stdout.buffer.write(text[sub_bar_start:sub_bar_end].encode('utf-8', errors='replace'))
