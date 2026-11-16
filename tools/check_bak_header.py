# tools/check_bak_header.py
import sys

with open('frontend/index.html.bak_ref_vibe', 'r', encoding='utf-8') as f:
    text = f.read()

sub_bar_start = text.find('<div class="ref-sub-header-bar">')
sub_bar_end = text.find('<div class="wp-tab-view" id="view-home">')

sys.stdout.buffer.write(text[sub_bar_start:sub_bar_end].encode('utf-8', errors='replace'))
