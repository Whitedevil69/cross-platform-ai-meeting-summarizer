# tools/restore_header.py
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

clean_sub_bar = """      <!-- Horizontal Capsule Tabs Bar (Exact Previous Match) -->
      <div class="ref-sub-header-bar">
        <div class="ref-header-left-tools">
          <button type="button" class="ref-tab-pill active" id="navTab-home" onclick="switchMainTab('home')">
            <span style="font-size:13px;">🏢</span> Organization
          </button>
          <button type="button" class="ref-tab-pill" id="navTab-workspaces" onclick="switchMainTab('workspaces')" title="Switch Workspace">
            <span>Workspaces</span> <span style="font-size:10px;opacity:0.7;">▾</span>
          </button>
        </div>

        <!-- Integrated Search Bar alongside Organization -->
        <div class="ref-search-container">
          <svg class="ref-search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input type="text" id="wpGlobalSearch" class="ref-search-input" placeholder="Search meetings, decisions, or attendees..." autocomplete="off">
          <span class="ref-search-badge">Search</span>
        </div>

        <div class="ref-header-right-tools">
          <button type="button" class="ref-tab-pill" id="navTab-apps" onclick="switchMainTab('apps')" title="Installed Workplace Apps">
            <span>🧩 Apps Hub</span>
          </button>
          <button type="button" class="ref-tab-pill" id="navTab-docs" onclick="switchMainTab('docs')" title="View All Meeting Records">
            <span>📑 All Records</span>
          </button>
        </div>
      </div>"""

sb_start = text.find('<!-- Horizontal Capsule Tabs Bar')
sb_end = text.find('<!-- ══════════════════════════════════════════════════════════════════════ -->\n      <!-- UNIFIED DASHBOARD GRID')

if sb_start != -1 and sb_end != -1:
    text = text[:sb_start] + clean_sub_bar + "\n\n      " + text[sb_end:]
    print("[OK] Restored clean previous header sub-bar")
else:
    print("[WARN] Could not find exact sub_bar slice")

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("[COMPLETE] Successfully restored previous header")
