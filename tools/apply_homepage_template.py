# tools/apply_homepage_template.py
import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ══════════════════════════════════════════════════════════════════════
# 1. NEW POPOVER CSS (Replaces lines ~873 to 970)
# ══════════════════════════════════════════════════════════════════════
new_popover_css = """    /* ══════════════════════════════════════════════════════════════════════ */
    /* ⚡ SYNCRA MORE APPS POPOVER TRAY (Dribbble Light-Mode Floating Card)   */
    /* ══════════════════════════════════════════════════════════════════════ */
    .wp-more-popover {
      position: fixed;
      width: 320px;
      background: #ffffff;
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 18px 16px 14px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.14), 0 4px 14px rgba(0, 0, 0, 0.04);
      z-index: 99999;
      display: none;
      animation: popoverFadeIn 0.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      pointer-events: auto;
      user-select: none;
    }

    .wp-more-popover.active {
      display: block !important;
    }

    @keyframes popoverFadeIn {
      from { opacity: 0; transform: scale(0.95) translateY(6px); }
      to { opacity: 1; transform: scale(1) translateY(0); }
    }

    .wp-more-popover-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
      padding-bottom: 10px;
      border-bottom: 1px solid #edf0ed;
    }

    .wp-more-popover-title {
      font-size: 0.84rem;
      font-weight: 700;
      color: var(--text-dark);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .wp-more-popover-count {
      font-size: 0.68rem;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: 9999px;
      background: var(--highlight-lime);
      color: var(--text-dark);
      border: 1px solid #d4ee68;
    }

    .wp-apps-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      row-gap: 12px;
      column-gap: 8px;
    }

    .wp-app-tile {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 7px;
      padding: 10px 4px 8px;
      border-radius: 16px;
      background: #fbfcfb;
      border: 1px solid #edf0ed;
      cursor: pointer;
      user-select: none;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      color: var(--text-dark);
    }

    .wp-app-tile:hover {
      background: #ffffff;
      border-color: var(--dock-dark);
      transform: translateY(-3px);
      box-shadow: 0 6px 18px rgba(24, 25, 27, 0.08);
    }

    .wp-app-tile-icon {
      width: 40px;
      height: 40px;
      border-radius: 12px;
      background: #f4f7f4;
      display: grid;
      place-items: center;
      transition: all 0.2s ease;
    }

    .wp-app-tile:hover .wp-app-tile-icon {
      background: var(--highlight-lime);
      transform: scale(1.05);
    }

    .wp-app-tile svg {
      width: 20px;
      height: 20px;
      color: var(--text-dark);
      stroke-width: 1.85;
      transition: transform 0.15s ease;
    }

    .wp-app-tile span {
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--text-dark);
      line-height: 1.18;
      letter-spacing: -0.01em;
    }

    .wp-more-popover-footer {
      margin-top: 12px;
      padding-top: 10px;
      border-top: 1px solid #edf0ed;
      text-align: center;
      font-size: 0.74rem;
      font-weight: 600;
      color: #64748b;
      cursor: pointer;
      transition: color 0.15s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
    }

    .wp-more-popover-footer:hover {
      color: var(--text-dark);
    }"""

# Replace popover CSS
css_popover_pattern = re.compile(r'/\* ══════════════════════════════════════════════════════════════════════ \*/\s*/\* ⚡ SYNCRA MORE APPS POPOVER TRAY.*?(?=\s*/\* ══════════════════════════════════════════════════════════════════════ \*/\s*/\* 1\. DOCK NAVIGATION)', re.DOTALL)
if css_popover_pattern.search(html):
    html = css_popover_pattern.sub(new_popover_css + "\n\n    ", html, count=1)
    print("[OK] Replaced Popover CSS")
else:
    # Try alternate match around .wp-more-popover
    alt_pattern = re.compile(r'\.wp-more-popover\s*\{.*?\.dark \.wp-app-tile:hover span\s*\{.*?\}', re.DOTALL)
    if alt_pattern.search(html):
        html = alt_pattern.sub(new_popover_css, html, count=1)
        print("[OK] Replaced Popover CSS (alternate)")
    else:
        print("[WARN] Could not match Popover CSS")

# ══════════════════════════════════════════════════════════════════════
# 2. NEW VIEWS CSS (Chat, Phone, Docs, Whiteboards, Clips)
# ══════════════════════════════════════════════════════════════════════
new_views_css = """    /* ══════════════════════════════════════════════════════════════════════ */
    /* ⚡ SIDEBAR SPA VIEWS: CHAT, PHONE, DOCS, WHITEBOARDS, CLIPS           */
    /* (Unified Dribbble Light-Mode Aesthetic Matching Homepage)             */
    /* ══════════════════════════════════════════════════════════════════════ */

    /* ── 1. View: Chat ── */
    .chat-layout {
      width: 100%;
      display: grid;
      grid-template-columns: 240px 1fr;
      min-height: 540px;
      background: #ffffff;
      border: 1px solid var(--card-border);
      border-radius: 24px;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    }
    .chat-sidebar {
      background: #fbfcfb;
      border-right: 1px solid #edf0ed;
      padding: 16px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      overflow-y: auto;
    }
    .chat-channel-item {
      padding: 10px 14px;
      border-radius: 14px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 0.82rem;
      color: var(--text-secondary);
      background: #ffffff;
      border: 1px solid #edf0ed;
      transition: all 0.15s ease;
    }
    .chat-channel-item:hover {
      background: #f4f7f4;
      color: var(--text-dark);
      border-color: #cbd5e1;
    }
    .chat-channel-item.active {
      background: var(--dock-dark);
      color: #ffffff;
      border-color: var(--dock-dark);
      box-shadow: 0 3px 10px rgba(24, 25, 27, 0.15);
    }
    .chat-channel-item.active div div {
      color: #ffffff !important;
    }
    .chat-main-area {
      display: flex;
      flex-direction: column;
      height: 100%;
      background: #ffffff;
    }
    .chat-header-bar {
      padding: 16px 20px;
      border-bottom: 1px solid #edf0ed;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 700;
      font-size: 0.95rem;
      background: #fbfcfb;
      color: var(--text-dark);
    }
    .chat-messages-scroll {
      flex: 1;
      padding: 20px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 14px;
      background: #fafbfa;
    }
    .chat-msg {
      display: flex;
      gap: 10px;
      max-width: 82%;
    }
    .chat-msg.user {
      align-self: flex-end;
      flex-direction: row-reverse;
    }
    .chat-msg-avatar {
      width: 34px;
      height: 34px;
      border-radius: 50%;
      background: var(--dock-dark);
      display: grid;
      place-items: center;
      font-size: 0.8rem;
      font-weight: 700;
      color: #ffffff;
      flex-shrink: 0;
    }
    .chat-msg-bubble {
      background: #ffffff;
      border: 1px solid #edf0ed;
      border-radius: 18px;
      padding: 12px 16px;
      font-size: 0.85rem;
      color: var(--text-dark);
      line-height: 1.5;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
    }
    .chat-msg.user .chat-msg-bubble {
      background: var(--dock-dark);
      border-color: var(--dock-dark);
      color: #ffffff;
      border-bottom-right-radius: 4px;
    }
    .chat-input-bar {
      padding: 14px 20px;
      border-top: 1px solid #edf0ed;
      display: flex;
      gap: 10px;
      background: #ffffff;
    }

    /* ── 2. View: Phone ── */
    .phone-container {
      width: 100%;
      display: grid;
      grid-template-columns: 320px 1fr;
      gap: 20px;
    }
    .dialpad-card {
      background: #ffffff;
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    }
    .dialpad-screen {
      width: 100%;
      background: #fbfcfb;
      border: 1.5px solid #e2e8e2;
      border-radius: 16px;
      padding: 12px 16px;
      text-align: right;
      font-family: var(--font-mono);
      font-size: 1.35rem;
      font-weight: 700;
      color: var(--text-dark);
      min-height: 52px;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      margin-bottom: 18px;
      overflow-x: auto;
      box-sizing: border-box;
    }
    .dialpad-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      width: 100%;
      margin-bottom: 18px;
    }
    .dial-btn {
      height: 56px;
      border-radius: 16px;
      background: #fbfcfb;
      border: 1px solid #edf0ed;
      color: var(--text-dark);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      user-select: none;
      transition: all 0.15s ease;
    }
    .dial-btn:hover {
      background: var(--highlight-lime);
      border-color: #d4ee68;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }
    .dial-btn:active {
      transform: scale(0.96);
    }
    .dial-num { font-size: 1.25rem; font-weight: 700; line-height: 1; }
    .dial-sub { font-size: 0.6rem; color: #8b95a5; letter-spacing: 0.1em; font-weight: 600; }
    .dial-actions-row {
      display: flex;
      width: 100%;
      gap: 10px;
    }
    .dial-call-btn {
      flex: 1;
      height: 48px;
      border-radius: 9999px;
      background: var(--dock-dark);
      border: none;
      color: #ffffff;
      font-size: 0.95rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s ease;
      box-shadow: 0 4px 14px rgba(24, 25, 27, 0.18);
    }
    .dial-call-btn:hover {
      background: #059669;
      transform: translateY(-1px);
    }
    .dial-del-btn {
      width: 48px;
      height: 48px;
      border-radius: 14px;
      background: #f4f7f4;
      border: 1px solid #e2e8e2;
      color: #475569;
      cursor: pointer;
      display: grid;
      place-items: center;
      transition: all 0.15s ease;
    }
    .dial-del-btn:hover {
      background: #e9eee9;
      border-color: var(--dock-dark);
      color: var(--text-dark);
    }

    /* ── 3. View: Docs ── */
    .docs-container {
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .doc-card {
      background: #ffffff;
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 26px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    }
    .doc-header-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 18px;
      border-bottom: 1px solid #edf0ed;
      padding-bottom: 16px;
    }
    .doc-title { font-size: 1.3rem; font-weight: 800; color: var(--text-dark); margin-bottom: 4px; letter-spacing: -0.02em; }
    .doc-meta { font-size: 0.78rem; color: #64748b; font-family: var(--font-mono); }
    .doc-section-title { font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin: 18px 0 8px; }
    .doc-summary-text { font-size: 0.9rem; line-height: 1.65; color: #334155; }
    .doc-items-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; margin-top: 10px; }
    .doc-items-table th { text-align: left; padding: 10px 12px; border-bottom: 1px solid #edf0ed; color: #64748b; font-size: 0.75rem; text-transform: uppercase; font-weight: 700; }
    .doc-items-table td { padding: 12px; border-bottom: 1px solid #f4f6f4; color: var(--text-dark); }
    .doc-items-table tr:hover td { background: #fafbfa; }

    /* ── 4. View: Whiteboards ── */
    .whiteboard-container {
      width: 100%;
      height: 560px;
      background: #ffffff;
      border: 1px solid var(--card-border);
      border-radius: 24px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    }
    .whiteboard-toolbar {
      padding: 12px 20px;
      background: #fbfcfb;
      border-bottom: 1px solid #edf0ed;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    #whiteboardSvg {
      flex: 1;
      width: 100%;
      height: 100%;
      background: radial-gradient(circle at center, #cbd5e1 1px, transparent 1px);
      background-size: 24px 24px;
      background-color: #fafbfa;
    }

    /* ── 5. View: Clips ── */
    .clips-container {
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .clip-card {
      background: #fbfcfb;
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 18px 22px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      transition: all 0.2s ease;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }
    .clip-card:hover {
      background: #ffffff;
      border-color: var(--dock-dark);
      transform: translateY(-2px);
      box-shadow: 0 6px 18px rgba(24, 25, 27, 0.06);
    }
    .clip-play-btn {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: var(--dock-dark);
      border: none;
      color: #ffffff;
      display: grid;
      place-items: center;
      font-size: 1.1rem;
      cursor: pointer;
      flex-shrink: 0;
      transition: all 0.15s ease;
      box-shadow: 0 4px 12px rgba(24, 25, 27, 0.15);
    }
    .clip-play-btn:hover {
      transform: scale(1.08);
      background: var(--highlight-lime);
      color: var(--text-dark);
    }
    .clip-info { flex: 1; }
    .clip-quote { font-size: 0.88rem; color: var(--text-dark); font-style: italic; font-weight: 500; margin-bottom: 4px; line-height: 1.45; }
    .clip-meta { font-size: 0.74rem; color: #64748b; font-family: var(--font-mono); }
    .clip-verified-badge {
      padding: 4px 12px;
      border-radius: 9999px;
      background: #eafaf1;
      border: 1px solid #c2eed5;
      color: #107e4a;
      font-size: 0.72rem;
      font-weight: 700;
      white-space: nowrap;
    }"""

views_css_pattern = re.compile(r'/\* ── View: Chat ── \*/.*?(?=/\* ══════════════════════════════════════════════════════════════════════ \*/\s*/\* ⚡ SYNCRA MORE APPS SUITE)', re.DOTALL)
if views_css_pattern.search(html):
    html = views_css_pattern.sub(new_views_css + "\n\n    ", html, count=1)
    print("[OK] Replaced Views CSS")
else:
    print("[WARN] Could not match Views CSS")

# ══════════════════════════════════════════════════════════════════════
# 3. NEW APP MODAL CSS (Replaces lines ~2183 to 2543)
# ══════════════════════════════════════════════════════════════════════
new_app_modal_css = """    /* ══════════════════════════════════════════════════════════════════════ */
    /* ⚡ SYNCRA MORE APPS SUITE (11 Apps Modal Dialog - Light Mode Dribbble) */
    /* ══════════════════════════════════════════════════════════════════════ */
    .wp-app-modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(24, 25, 27, 0.45);
      backdrop-filter: blur(14px);
      z-index: 100005;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .wp-app-modal-overlay.active {
      display: flex !important;
    }
    .wp-app-modal-dialog {
      width: 100%;
      max-width: 960px;
      height: 86vh;
      max-height: 820px;
      background: #ffffff;
      border: 1px solid var(--card-border);
      border-radius: 28px;
      box-shadow: 0 25px 70px rgba(0, 0, 0, 0.18), 0 4px 16px rgba(0, 0, 0, 0.06);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      color: var(--text-dark);
      animation: modalSlideUp 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .wp-app-modal-header {
      padding: 18px 26px;
      background: #fbfcfb;
      border-bottom: 1px solid #edf0ed;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }
    .wp-app-modal-title-group {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .wp-app-modal-icon {
      font-size: 1.5rem;
      width: 44px;
      height: 44px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f4f7f4;
      border: 1px solid #edf0ed;
      border-radius: 14px;
      flex-shrink: 0;
    }
    .wp-app-modal-title {
      font-size: 1.22rem;
      font-weight: 800;
      color: var(--text-dark);
      margin: 0;
      line-height: 1.2;
      letter-spacing: -0.02em;
    }
    .wp-app-modal-subtitle {
      font-size: 0.8rem;
      color: #64748b;
      margin: 3px 0 0;
    }
    .wp-app-modal-close-btn {
      width: 34px;
      height: 34px;
      border-radius: 50%;
      background: #f4f6f4;
      border: 1px solid #e2e8e2;
      color: #475569;
      font-size: 1.1rem;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .wp-app-modal-close-btn:hover {
      background: var(--dock-dark);
      color: #ffffff;
      border-color: var(--dock-dark);
    }
    .wp-app-modal-nav-bar {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px 26px;
      background: #f4f7f4;
      border-bottom: 1px solid #edf0ed;
      overflow-x: auto;
      white-space: nowrap;
    }
    .wp-app-modal-nav-bar::-webkit-scrollbar {
      height: 4px;
    }
    .wp-app-modal-nav-bar::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 4px;
    }
    .wp-app-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 15px;
      border-radius: 9999px;
      background: #ffffff;
      border: 1px solid #e2e8e2;
      color: #475569;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
      flex-shrink: 0;
    }
    .wp-app-pill:hover {
      background: #ffffff;
      color: var(--text-dark);
      border-color: var(--dock-dark);
    }
    .wp-app-pill.active {
      background: var(--dock-dark);
      border-color: var(--dock-dark);
      color: #ffffff;
      box-shadow: 0 4px 12px rgba(24, 25, 27, 0.15);
    }
    .wp-app-modal-body {
      flex: 1;
      overflow-y: auto;
      padding: 24px 26px;
      background: #ffffff;
      color: var(--text-dark);
    }
    .wp-app-modal-body::-webkit-scrollbar {
      width: 6px;
    }
    .wp-app-modal-body::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 6px;
    }
    .app-input {
      width: 100%;
      background: #ffffff;
      border: 1.5px solid #e2e8e2;
      border-radius: 12px;
      padding: 10px 14px;
      color: var(--text-dark);
      font-size: 0.88rem;
      font-family: inherit;
      outline: none;
      transition: all 0.15s ease;
      box-sizing: border-box;
    }
    .app-input:focus {
      border-color: var(--dock-dark);
      box-shadow: 0 0 0 3px rgba(24, 25, 27, 0.08);
    }
    .app-textarea {
      width: 100%;
      background: #ffffff;
      border: 1.5px solid #e2e8e2;
      border-radius: 14px;
      padding: 12px 14px;
      color: var(--text-dark);
      font-size: 0.85rem;
      font-family: var(--font-mono);
      line-height: 1.55;
      outline: none;
      resize: vertical;
      min-height: 120px;
      box-sizing: border-box;
      transition: all 0.15s ease;
    }
    .app-textarea:focus {
      border-color: var(--dock-dark);
      box-shadow: 0 0 0 3px rgba(24, 25, 27, 0.08);
    }
    .app-btn-primary {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 10px 22px;
      border-radius: 9999px;
      background: var(--dock-dark);
      border: none;
      color: #ffffff !important;
      font-size: 0.84rem;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(24, 25, 27, 0.15);
      transition: all 0.15s ease;
    }
    .app-btn-primary:hover {
      background: var(--dock-active);
      transform: translateY(-1px);
      box-shadow: 0 6px 18px rgba(24, 25, 27, 0.22);
    }
    .app-btn-secondary {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 9px 18px;
      border-radius: 9999px;
      background: #f4f6f4;
      border: 1px solid #e2e8e2;
      color: #334155;
      font-size: 0.84rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .app-btn-secondary:hover {
      background: #e9eee9;
      border-color: #cbd5e1;
    }
    .app-card {
      background: #fbfcfb;
      border: 1px solid #edf0ed;
      border-radius: 20px;
      padding: 20px;
      margin-bottom: 16px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }
    .app-badge-status {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 0.72rem;
      font-weight: 700;
    }
    .app-badge-green {
      background: #eafaf1;
      border: 1px solid #c2eed5;
      color: #107e4a;
    }
    .app-badge-purple {
      background: #f5f0ff;
      border: 1px solid #e9d5ff;
      color: #6b21a8;
    }
    .app-badge-blue {
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      color: #1d4ed8;
    }
    .app-badge-amber {
      background: #fffbeb;
      border: 1px solid #fde68a;
      color: #b45309;
    }
    /* Calendar App Grid (Light Mode) */
    .cal-grid {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 6px;
      margin-top: 10px;
    }
    .cal-day-header {
      font-size: 0.75rem;
      font-weight: 700;
      color: #8b95a5;
      text-align: center;
      padding: 6px 0;
    }
    .cal-cell {
      background: #ffffff;
      border: 1px solid #edf0ed;
      border-radius: 12px;
      min-height: 50px;
      padding: 6px 8px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.15s ease;
    }
    .cal-cell:hover {
      background: #f4f7f4;
      border-color: var(--dock-dark);
      transform: translateY(-1px);
    }
    .cal-cell.active {
      background: #fbfcfb;
      border-color: var(--dock-dark);
      box-shadow: 0 0 0 2px rgba(24, 25, 27, 0.1);
    }
    .cal-cell.today {
      border-color: var(--dock-dark);
      background: #fdfefe;
    }
    .cal-date-num {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-dark);
    }
    .cal-event-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--dock-dark);
      align-self: flex-end;
    }
    /* Polls */
    .poll-bar-bg {
      height: 10px;
      border-radius: 9999px;
      background: #f4f7f4;
      border: 1px solid #e2e8e2;
      overflow: hidden;
      margin-top: 6px;
    }
    .poll-bar-fill {
      height: 100%;
      border-radius: 9999px;
      background: var(--dock-dark);
      transition: width 0.4s ease;
    }
    /* Workvivo Post Cards */
    .wv-feed-card {
      background: #fbfcfb;
      border: 1px solid #edf0ed;
      border-radius: 20px;
      padding: 20px;
      margin-bottom: 16px;
    }
    .wv-reaction-btn {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 6px 12px;
      border-radius: 9999px;
      background: #ffffff;
      border: 1px solid #e2e8e2;
      color: #475569;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .wv-reaction-btn:hover {
      background: #f4f7f4;
      color: var(--text-dark);
      border-color: var(--dock-dark);
    }
    .wv-reaction-btn.active {
      background: var(--dock-dark);
      border-color: var(--dock-dark);
      color: #ffffff;
    }
    .wv-comment-row {
      display: flex;
      gap: 8px;
      padding: 8px 12px;
      background: #f4f7f4;
      border-radius: 12px;
      margin-top: 6px;
      font-size: 0.82rem;
      color: var(--text-dark);
    }"""

app_modal_pattern = re.compile(r'/\* ══════════════════════════════════════════════════════════════════════ \*/\s*/\* ⚡ SYNCRA MORE APPS SUITE \(Mail, Calendar, Scheduler, Surveys, etc\.\) \*/.*?(?=\s*/\* ── POINT 1: REFINED HEADER SUB-BAR)', re.DOTALL)
if app_modal_pattern.search(html):
    html = app_modal_pattern.sub(new_app_modal_css + "\n\n    ", html, count=1)
    print("[OK] Replaced App Modal CSS")
else:
    print("[WARN] Could not match App Modal CSS")

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Stage 1 (CSS updates) finished.")
