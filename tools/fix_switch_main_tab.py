# tools/fix_switch_main_tab.py
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('window.switchMainTab = function')
end = text.find('// ── View Loader: Docs ──')

clean_code = """window.switchMainTab = function(tabKey) {
      if (!tabKey) tabKey = 'home';
      tabKey = tabKey.toLowerCase().replace(/\\s+/g, '');
      if (tabKey === 'revenueaccelerator') tabKey = 'revenue';
      if (tabKey === 'contactcenter') tabKey = 'contactcenter';

      // 1. Update left dock buttons
      document.querySelectorAll('.ref-dock-btn').forEach(btn => btn.classList.remove('active'));
      const activeDock = document.getElementById('dockNav-' + tabKey);
      if (activeDock) activeDock.classList.add('active');

      // 2. Update top horizontal capsule tabs
      document.querySelectorAll('.ref-tab-pill').forEach(btn => btn.classList.remove('active'));
      const activeTab = document.getElementById('navTab-' + tabKey);
      if (activeTab) activeTab.classList.add('active');

      // 3. Update main header title dynamically to match active option
      const viewTitles = {
        home: { pre: 'Managing', badge: '⚙', t1: 'Your Meetings', sub: 'and', spark: '⚡', t2: 'Workflows' },
        chat: { pre: 'Managing', badge: '💬', t1: 'Team Conversations', sub: 'and', spark: '✨', t2: 'Live Streams' },
        phone: { pre: 'Managing', badge: '📞', t1: 'Voice Telephony', sub: 'and', spark: '🎙️', t2: 'Call Streams' },
        docs: { pre: 'Managing', badge: '📑', t1: 'Executive Briefings', sub: 'and', spark: '📄', t2: 'Meeting Records' },
        whiteboards: { pre: 'Managing', badge: '🕸️', t1: 'Decision Graph', sub: 'and', spark: '🎨', t2: 'Whiteboards' },
        clips: { pre: 'Managing', badge: '🎙️', t1: 'Audio Evidence', sub: 'and', spark: '⚡', t2: 'Verbatim Quotes' },
        mail: { pre: 'Managing', badge: '📬', t1: 'Executive Briefings', sub: 'and', spark: '⚡', t2: 'Email Digests' },
        calendar: { pre: 'Managing', badge: '📅', t1: 'Workplace Schedule', sub: 'and', spark: '⚡', t2: 'Calendar Sync' },
        scheduler: { pre: 'Managing', badge: '⚡', t1: '1-Click Meeting Booker', sub: 'and', spark: '🤖', t2: 'AI Notetakers' },
        surveys: { pre: 'Managing', badge: '📊', t1: 'Consensus Polling', sub: 'and', spark: '⚡', t2: 'Live Team Feedback' },
        apps: { pre: 'Managing', badge: '🧩', t1: 'Ecosystem Connectors', sub: 'and', spark: '⚡', t2: 'Integration Webhooks' },
        workspaces: { pre: 'Managing', badge: '🗂️', t1: 'Department Workspaces', sub: 'and', spark: '⚡', t2: 'Multi-Tenant Isolation' },
        contacts: { pre: 'Managing', badge: '👥', t1: 'Team Directory', sub: 'and', spark: '⚡', t2: 'Action Owners' },
        events: { pre: 'Managing', badge: '🎟️', t1: 'Live Webinars', sub: 'and', spark: '⚡', t2: 'Townhall Studios' },
        revenue: { pre: 'Managing', badge: '📈', t1: 'Deal Intelligence', sub: 'and', spark: '⚡', t2: 'Revenue Telemetry' },
        contactcenter: { pre: 'Managing', badge: '🎧', t1: 'Supervisor Desk', sub: 'and', spark: '⚡', t2: 'AI Whisper Coaching' },
        workvivo: { pre: 'Managing', badge: '✨', t1: 'Employee Engagement', sub: 'and', spark: '⚡', t2: 'Social Recognition' }
      };
      const mainTitleEl = document.querySelector('.ref-main-title');
      if (mainTitleEl && viewTitles[tabKey]) {
        const vt = viewTitles[tabKey];
        mainTitleEl.innerHTML = `${vt.pre} <span class="ref-title-badge gear">${vt.badge}</span> ${vt.t1}<br>${vt.sub} <span class="ref-title-badge spark">${vt.spark}</span> ${vt.t2}`;
      }

      // 4. Close popover and modal if open
      const popover = document.getElementById('wpMoreAppsPopover');
      if (popover) { popover.style.display = 'none'; popover.classList.remove('active'); }
      const modal = document.getElementById('wpAppSuiteModalOverlay');
      if (modal) { modal.style.display = 'none'; modal.classList.remove('active'); }

      // 5. Switch visible view
      const allViews = [
        'home', 'chat', 'phone', 'docs', 'whiteboards', 'clips',
        'mail', 'calendar', 'scheduler', 'surveys', 'apps', 'workspaces',
        'contacts', 'events', 'revenue', 'contactcenter', 'workvivo'
      ];
      allViews.forEach(v => {
        const viewEl = document.getElementById('view-' + v);
        if (viewEl) {
          viewEl.style.display = (v === tabKey) ? 'flex' : 'none';
        }
      });

      // 6. Trigger view-specific dynamic loaders
      if (tabKey === 'docs') loadDocsView();
      if (tabKey === 'chat') loadChatView();
      if (tabKey === 'whiteboards') loadWhiteboardsView();
      if (tabKey === 'clips') loadClipsView();
    };

    // Forward openMoreApp and openAppSuiteModal directly to switchMainTab!
    window.openMoreApp = function(appName) {
      window.switchMainTab(appName);
    };
    window.openAppSuiteModal = function(appName) {
      window.switchMainTab(appName);
    };

    """

text = text[:start] + clean_code + text[end:]

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("[OK] Successfully cleanly replaced switchMainTab")
