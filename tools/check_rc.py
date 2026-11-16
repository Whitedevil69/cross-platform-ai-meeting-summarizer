# tools/check_rc.py
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

right_start = text.find('<div class="ref-right-col">')
chat_start = text.find('<div class="wp-tab-view" id="view-chat"')

print("rc slice:")
import sys
sys.stdout.buffer.write(text[right_start + 4200:chat_start].encode('utf-8', errors='replace'))
