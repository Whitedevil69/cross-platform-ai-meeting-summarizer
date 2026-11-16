# tools/build_all_views_spa.py
import re
import sys

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# ══════════════════════════════════════════════════════════════════════
# 1. NEW SUB-BAR WITH SCROLLABLE CAPSULE TABS FOR ALL OPTIONS
# ══════════════════════════════════════════════════════════════════════
new_sub_bar = """      <!-- Horizontal Capsule Tabs Bar (Matching Dribbble Reference) -->
      <div class="ref-sub-header-bar">
        <div class="ref-header-left-tools" style="overflow-x:auto;max-width:calc(100% - 320px);white-space:nowrap;padding-bottom:4px;">
          <button type="button" class="ref-tab-pill active" id="navTab-home" onclick="switchMainTab('home')">
            <span>🏢</span> Organization
          </button>
          <button type="button" class="ref-tab-pill" id="navTab-mail" onclick="switchMainTab('mail')">
            <span>📬</span> Mail
          </button>
          <button type="button" class="ref-tab-pill" id="navTab-calendar" onclick="switchMainTab('calendar')">
            <span>📅</span> Calendar
          </button>
          <button type="button" class="ref-tab-pill" id="navTab-scheduler" onclick="switchMainTab('scheduler')">
            <span>⚡</span> Scheduler
          </button>
          <button type="button" class="ref-tab-pill" id="navTab-surveys" onclick="switchMainTab('surveys')">
            <span>📊</span> Surveys
          </button>
          <button type="button" class="ref-tab-pill" id="navTab-apps" onclick="switchMainTab('apps')">
            <span>🧩</span> Apps
          </button>
          <button type="button" class="ref-tab-pill" id="navTab-workspaces" onclick="switchMainTab('workspaces')">
            <span>🗂️</span> Workspaces
          </button>
          <button type="button" class="ref-tab-pill" id="navTab-contacts" onclick="switchMainTab('contacts')">
            <span>👥</span> Contacts
          </button>
          <button type="button" class="ref-tab-pill" id="navTab-events" onclick="switchMainTab('events')">
            <span>🎟️</span> Events
          </button>
          <button type="button" class="ref-tab-pill" id="navTab-revenue" onclick="switchMainTab('revenue')">
            <span>📈</span> Revenue
          </button>
          <button type="button" class="ref-tab-pill" id="navTab-contactcenter" onclick="switchMainTab('contactcenter')">
            <span>🎧</span> Contact Center
          </button>
          <button type="button" class="ref-tab-pill" id="navTab-workvivo" onclick="switchMainTab('workvivo')">
            <span>✨</span> Workvivo
          </button>
        </div>

        <!-- Integrated Search Bar alongside Tabs -->
        <div class="ref-search-container" style="max-width:280px;min-width:200px;">
          <svg class="ref-search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input type="text" id="wpGlobalSearch" class="ref-search-input" placeholder="Search meetings..." autocomplete="off">
          <span class="ref-search-badge">Search</span>
        </div>
      </div>"""

# Replace sub-bar
sub_bar_pattern = re.compile(r'<div class="ref-sub-header-bar">.*?</div>\s*</div>(?=\s*<!-- ══════════════════════════════════════════════════════════════════════ -->\s*<!-- UNIFIED DASHBOARD GRID)', re.DOTALL)
if sub_bar_pattern.search(text):
    text = sub_bar_pattern.sub(new_sub_bar + "\n\n", text, count=1)
    print("[OK] Replaced Sub-Bar with horizontal capsule tabs")
else:
    print("[WARN] Could not match Sub-Bar via regex, trying string find")
    sb_start = text.find('<div class="ref-sub-header-bar">')
    sb_end = text.find('<!-- UNIFIED DASHBOARD GRID')
    if sb_start != -1 and sb_end != -1:
        text = text[:sb_start] + new_sub_bar + "\n\n      " + text[sb_end:]
        print("[OK] Replaced Sub-Bar via string find")

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("[OK] Sub-bar update complete")
