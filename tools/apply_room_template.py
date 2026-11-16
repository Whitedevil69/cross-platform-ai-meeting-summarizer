# tools/apply_room_template.py
import re
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from build_room_css import NEW_CSS

with open("frontend/room.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Head: Fonts
new_head_fonts = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">"""

content = re.sub(
    r'<link rel="preconnect" href="https://fonts\.googleapis\.com">[\s\S]*?<link href="https://fonts\.googleapis\.com/css2\?family=Outfit[^"]*" rel="stylesheet">',
    new_head_fonts,
    content,
    count=1
)

# 2. Update CSS inside <style> ... </style>
style_start = content.find("<style>")
style_end = content.find("</style>")

if style_start == -1 or style_end == -1:
    print("[ERROR] Could not find <style> tags")
    sys.exit(1)

content = content[:style_start + 7] + "\n" + NEW_CSS + "\n  " + content[style_end:]

# 3. Clean up the top right navigation links in header.top-bar
old_nav_pattern = r'<a href="/app/index\.html" style="[^"]*">.*?</a>\s*<a href="/app/report\.html" style="[^"]*">.*?</a>\s*<a href="/app/login\.html" style="[^"]*">.*?</a>'
new_nav_links = """<a href="/app/index.html" class="top-nav-link" title="Dashboard">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"></rect><rect width="7" height="5" x="14" y="3" rx="1"></rect><rect width="7" height="9" x="14" y="12" rx="1"></rect><rect width="7" height="5" x="3" y="16" rx="1"></rect></svg>
          <span>Dashboard</span>
        </a>
        <a href="/app/report.html" class="top-nav-link" title="Reports">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
          <span>Reports</span>
        </a>
        <a href="/app/login.html" class="top-nav-link" title="Account">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
          <span>Account</span>
        </a>"""

content = re.sub(old_nav_pattern, new_nav_links, content, count=1)

# 4. Clean up the language filter pills in transcript-subbar
content = re.sub(
    r'<span class="lang-filter-pill" data-lang="hi">.*?Hindi</span>',
    '<span class="lang-filter-pill" data-lang="hi">🇮🇳 Hindi</span>',
    content,
    count=1
)
content = re.sub(
    r'<span class="lang-filter-pill" data-lang="en">.*?English</span>',
    '<span class="lang-filter-pill" data-lang="en">🇬🇧 English</span>',
    content,
    count=1
)

# 5. Update avatar gradients in getAvatarColor to sleek dark & refined gradients
old_grad = r"""        const gradients = \[
          'linear-gradient\(135deg, #7c3aed 0%, #4f46e5 100%\)',
          'linear-gradient\(135deg, #06b6d4 0%, #0284c7 100%\)',
          'linear-gradient\(135deg, #10b981 0%, #059669 100%\)',
          'linear-gradient\(135deg, #f59e0b 0%, #d97706 100%\)',
          'linear-gradient\(135deg, #ec4899 0%, #db2777 100%\)',
          'linear-gradient\(135deg, #8b5cf6 0%, #6366f1 100%\)'
        \];"""

new_grad = """        const gradients = [
          'linear-gradient(135deg, #18191b 0%, #2f3336 100%)',
          'linear-gradient(135deg, #0f766e 0%, #115e59 100%)',
          'linear-gradient(135deg, #1e3a8a 0%, #172554 100%)',
          'linear-gradient(135deg, #374151 0%, #1f2937 100%)',
          'linear-gradient(135deg, #047857 0%, #064e3b 100%)',
          'linear-gradient(135deg, #312e81 0%, #1e1b4b 100%)'
        ];"""

content = re.sub(old_grad, new_grad, content, count=1)

# Write updated content
with open("frontend/room.html", "w", encoding="utf-8") as f:
    f.write(content)

print("[OK] Successfully updated frontend/room.html with Dribbble theme!")
