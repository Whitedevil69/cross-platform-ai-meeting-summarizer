# -*- coding: utf-8 -*-
"""
apply_forest_green_light_theme.py
Transforms Syncra Workplace to a Light Mode aesthetic inspired by the Dribbble reference layout:
- Canvas: Soft sage mist background (#edf3ee / #eef2ee) with a floating rounded white container (#ffffff)
- Forest Green Gradient: Replaces the yellow highlight card & accents with a luxury Forest Green gradient
  (linear-gradient(135deg, #064e3b 0%, #059669 100%)) and soft emerald highlight washes (#e8f5e9 -> #d1fae5)
- Typography: High-contrast dark charcoal/forest text (#0c1c15, #1e293b, #475569) using Plus Jakarta Sans & Inter
- Active pills: Rounded dark pine capsule pills (#064e3b) with crisp white text, matching the reference screenshot
- Default: 100% Light Mode (no dark mode default)
- Preserves ALL options, buttons, and functionalities with zero breaks.
"""

def transform_index():
    path = "frontend/index.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Force Light Mode Default at head script
    old_head_script = """  <script>
    if (localStorage.getItem('theme') === 'dark' ||
        (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
    }
  </script>"""

    new_head_script = """  <script>
    // Default to Light Mode as requested by user
    if (localStorage.getItem('theme') === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  </script>"""

    if old_head_script in html:
        html = html.replace(old_head_script, new_head_script)
        print("Updated head theme initialization to default to light mode.")

    # 2. Update :root CSS Variables with Forest Green Light Mode
    old_root = """:root {
      /* ══════════════════════════════════════════════════════════════════════ */
      /* 60% — DOMINANT CANVAS (Deep Space Obsidian & Architectural Ground)     */
      /* ══════════════════════════════════════════════════════════════════════ */
      --bg-base: #07090e;
      --bg-subtle: #0b0e17;
      --bg-surface: #0f131f;
      --bg-card: rgba(15, 19, 31, 0.85);
      --bg-hover: #151b2a;

      /* ══════════════════════════════════════════════════════════════════════ */
      /* 30% — STRUCTURAL SURFACES, BORDERS & TYPOGRAPHY                        */
      /* ══════════════════════════════════════════════════════════════════════ */
      --border-hairline: rgba(255, 255, 255, 0.08);
      --border-subtle: rgba(255, 255, 255, 0.04);
      --border-hover: rgba(255, 255, 255, 0.16);

      --text-headings: #ffffff;
      --text-primary: #f1f5f9;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --text-subtle: #475569;

      /* ══════════════════════════════════════════════════════════════════════ */
      /* 10% — FUNCTIONAL PRECISION ACCENT (Electric Cobalt & Titanium Blue)   */
      /* ══════════════════════════════════════════════════════════════════════ */
      --primary: #2563eb;
      --primary-light: #3b82f6;
      --primary-hover: #1d4ed8;
      --primary-glow: rgba(37, 99, 235, 0.35);
      --accent-wash: rgba(37, 99, 235, 0.12);

      --secondary: #0ea5e9;
      --secondary-light: #38bdf8;
      --secondary-glow: rgba(14, 165, 233, 0.25);

      --accent-pink: #38bdf8;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;

      --glass-bg: rgba(255, 255, 255, 0.03);
      --glass-bg-hover: rgba(255, 255, 255, 0.06);
      --glass-border: 1px solid rgba(255, 255, 255, 0.08);
      --glass-border-hover: 1px solid rgba(255, 255, 255, 0.16);
      --glass-blur: blur(20px);
      --glass-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.06);

      --font-main: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;

      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --radius-xl: 24px;
      --radius-full: 9999px;
    }"""

    new_root = """:root {
      /* ══════════════════════════════════════════════════════════════════════ */
      /* 60% — DOMINANT CANVAS (Soft Sage Mist & Floating Pristine Porcelain)   */
      /* ══════════════════════════════════════════════════════════════════════ */
      --bg-base: #edf3ee;             /* Soft airy sage background (matching Dribbble backdrop) */
      --bg-subtle: #f5f9f6;           /* Subtle surface container */
      --bg-surface: #ffffff;          /* Pure crisp white card surface */
      --bg-card: #ffffff;             /* Crisp card background */
      --bg-hover: #f0f6f1;            /* Soft hover state */

      /* ══════════════════════════════════════════════════════════════════════ */
      /* 30% — STRUCTURAL SURFACES, BORDERS & HIGH-CONTRAST TYPOGRAPHY          */
      /* ══════════════════════════════════════════════════════════════════════ */
      --border-hairline: #e2ece3;     /* Structural crisp borders */
      --border-subtle: #edf4ee;       /* Dividers */
      --border-hover: #cbdcd0;        /* Hover borders */

      --text-headings: #0c1c15;       /* Deep forest slate for display headings */
      --text-primary: #1e293b;        /* Crisp dark slate for body text */
      --text-secondary: #475569;      /* Descriptions & labels */
      --text-muted: #64748b;          /* Subtitles & metadata */
      --text-subtle: #94a3b8;         /* Subtle text & placeholders */

      /* ══════════════════════════════════════════════════════════════════════ */
      /* 10% — FOREST GREEN GRADIENT ACCENTS (Replaces Yellow Highlight Card)  */
      /* ══════════════════════════════════════════════════════════════════════ */
      --primary: #065f46;             /* Forest Green */
      --primary-dark: #064e3b;        /* Deep Pine */
      --primary-light: #047857;       /* Rich Emerald */
      --primary-hover: #064e3b;       /* Hover */
      --primary-glow: rgba(6, 95, 70, 0.22);
      
      --accent-wash: #e6f4ea;         /* Soft forest sage wash for active pills */
      --accent-highlight: #d1fae5;    /* Mint highlight */
      --forest-grad: linear-gradient(135deg, #064e3b 0%, #059669 100%);
      --forest-grad-card: linear-gradient(135deg, #e8f5e9 0%, #d1fae5 100%);
      --forest-grad-subtle: linear-gradient(135deg, #f0fdf4 0%, #e6f4ea 100%);

      --secondary: #059669;           /* Secondary Emerald */
      --secondary-light: #10b981;     /* Mint */
      --secondary-glow: rgba(5, 150, 105, 0.18);

      --success: #059669;
      --warning: #d97706;
      --danger: #dc2626;

      --glass-bg: rgba(255, 255, 255, 0.9);
      --glass-bg-hover: rgba(255, 255, 255, 1);
      --glass-border: 1px solid #e2ece3;
      --glass-border-hover: 1px solid #cbdcd0;
      --glass-blur: blur(20px);
      --glass-shadow: 0 4px 20px -2px rgba(6, 78, 59, 0.05), 0 2px 6px -1px rgba(0, 0, 0, 0.03);

      --font-main: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;

      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 18px;
      --radius-xl: 26px;
      --radius-full: 9999px;
    }"""

    if old_root in html:
        html = html.replace(old_root, new_root)
        print("Updated :root variables to Forest Green Light Mode.")

    # 3. Body Background & Floating App Frame
    old_body = """body {
      background-color: var(--bg-base);
      background-image: 
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(37, 99, 235, 0.08) 0%, transparent 60%),
        radial-gradient(rgba(255, 255, 255, 0.035) 1px, transparent 1px);
      background-size: 100% 100%, 28px 28px;
      background-attachment: fixed;
      color: var(--text-primary);
      font-family: var(--font-main);
      min-height: 100vh;
      overflow-x: hidden;
      line-height: 1.6;
      letter-spacing: -0.012em;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }"""

    new_body = """body {
      background-color: var(--bg-base);
      background-image: 
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(6, 95, 70, 0.06) 0%, transparent 60%),
        radial-gradient(rgba(6, 78, 59, 0.04) 1px, transparent 1px);
      background-size: 100% 100%, 24px 24px;
      background-attachment: fixed;
      color: var(--text-primary);
      font-family: var(--font-main);
      min-height: 100vh;
      overflow-x: hidden;
      line-height: 1.6;
      letter-spacing: -0.012em;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      padding: 14px 18px;
    }

    /* Floating Rounded App Shell matching Dribbble reference */
    .app-window-frame {
      display: flex;
      flex-direction: column;
      min-height: calc(100vh - 28px);
      max-width: 1540px;
      margin: 0 auto;
      background: #ffffff;
      border: 1px solid rgba(6, 78, 59, 0.1);
      border-radius: 28px;
      box-shadow: 0 16px 50px -10px rgba(6, 78, 59, 0.1), 0 2px 10px rgba(0, 0, 0, 0.03);
      position: relative;
      overflow: hidden;
      z-index: 1;
    }"""

    if old_body in html:
        html = html.replace(old_body, new_body)
        print("Updated body and .app-window-frame to floating rounded design.")

    # 4. Top Header Styling in Light Mode
    html = html.replace(
        "background: rgba(8, 11, 18, 0.88);",
        "background: rgba(255, 255, 255, 0.95); border-bottom: 1px solid #e5ede6;"
    )

    # Header nav buttons: pill shapes with active dark forest pill (like Organization in Dribbble reference)
    old_nav_btn = """    .wp-header-nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 8px;
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      font-size: 0.82rem;
      font-weight: 500;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.18s ease;
      white-space: nowrap;
      font-family: inherit;
    }

    .wp-header-nav-btn svg {
      width: 16px;
      height: 16px;
      stroke-width: 1.85;
      color: inherit;
    }

    .wp-header-nav-btn:hover {
      background: rgba(255, 255, 255, 0.08);
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.12);
    }

    .wp-header-nav-btn.active {
      background: var(--accent-wash);
      color: #60a5fa;
      border-color: rgba(59, 130, 246, 0.35);
      font-weight: 600;
      box-shadow: 0 0 12px rgba(37, 99, 235, 0.2);
    }"""

    new_nav_btn = """    .wp-header-nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 9999px;
      background: #f4f8f4;
      border: 1px solid #dce8dd;
      color: #475569;
      font-size: 0.82rem;
      font-weight: 500;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.18s ease;
      white-space: nowrap;
      font-family: inherit;
    }

    .wp-header-nav-btn svg {
      width: 15px;
      height: 15px;
      stroke-width: 2;
      color: inherit;
    }

    .wp-header-nav-btn:hover {
      background: #eaf3ec;
      color: #064e3b;
      border-color: #cbdcd0;
    }

    .wp-header-nav-btn.active {
      background: #064e3b;
      color: #ffffff;
      border-color: #064e3b;
      font-weight: 600;
      box-shadow: 0 2px 8px rgba(6, 78, 59, 0.25);
    }
    .wp-header-nav-btn.active svg {
      color: #ffffff;
    }"""

    if old_nav_btn in html:
        html = html.replace(old_nav_btn, new_nav_btn)
        print("Updated header navigation buttons to pill style with active dark forest pill.")

    # 5. Search Bar in Header
    html = html.replace(
        "background: rgba(0, 0, 0, 0.35);\n      border: 1px solid rgba(255, 255, 255, 0.12);",
        "background: #f4f8f4;\n      border: 1px solid #dce8dd;"
    )

    # 6. Global Search Input Text
    html = html.replace(
        ".wp-global-search input {\n      flex: 1;\n      border: none;\n      outline: none;\n      background: transparent;\n      color: #ffffff;",
        ".wp-global-search input {\n      flex: 1;\n      border: none;\n      outline: none;\n      background: transparent;\n      color: #1e293b;"
    )

    # 7. AI Sparkle Pill in Header
    html = html.replace(
        "background: var(--accent-wash);\n      border: 1px solid rgba(59, 130, 246, 0.3);\n      color: #93c5fd;",
        "background: #e6f4ea;\n      border: 1px solid #c6e6cb;\n      color: #065f46;"
    )

    # 8. Window Control Buttons
    html = html.replace(
        "background: rgba(255, 255, 255, 0.06);\n      border: 1px solid rgba(255, 255, 255, 0.08);\n      color: var(--text-muted);",
        "background: #f4f8f4;\n      border: 1px solid #dce8dd;\n      color: #475569;"
    )

    # 9. Center Greeting & Account Banner
    html = html.replace(
        "color: #ffffff;\n      font-size: 2.5rem;\n      font-weight: 800;",
        "color: #064e3b;\n      font-size: 2.5rem;\n      font-weight: 800;"
    )
    html = html.replace(
        "background: rgba(20, 20, 36, 0.7);\n      border: 1px solid rgba(255, 255, 255, 0.14);",
        "background: #ffffff;\n      border: 1px solid #dce8dd;\n      box-shadow: 0 4px 16px rgba(6, 78, 59, 0.06);"
    )
    html = html.replace(
        "color: #ffffff;\n      font-weight: 600;\n      letter-spacing: -0.01em;\n      overflow: hidden;",
        "color: #0c1c15;\n      font-weight: 600;\n      letter-spacing: -0.01em;\n      overflow: hidden;"
    )

    # 10. The 4 Hero Quick Action Cards
    # Hero Card 1 (Start Video Meeting) -> highlighted Forest Green Gradient card (replacing yellow card)
    old_card_css = """    .wp-quick-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-hairline);
      border-radius: var(--radius-lg);
      padding: 22px 18px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
      overflow: hidden;
      box-shadow: 0 10px 25px -10px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    .wp-quick-card:hover {
      transform: translateY(-2px);
      border-color: rgba(59, 130, 246, 0.35);
      box-shadow: 0 16px 36px -10px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.08);
      background: #141a29;
    }"""

    new_card_css = """    .wp-quick-card {
      background: #ffffff;
      border: 1px solid #e2ece3;
      border-radius: 20px;
      padding: 24px 20px 22px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
      overflow: hidden;
      box-shadow: 0 4px 20px -2px rgba(6, 78, 59, 0.05), 0 1px 3px rgba(0, 0, 0, 0.03);
    }

    .wp-quick-card:hover {
      transform: translateY(-3px);
      border-color: #a7f3d0;
      box-shadow: 0 12px 30px -4px rgba(6, 78, 59, 0.12), 0 2px 6px rgba(0, 0, 0, 0.04);
      background: #fafdfb;
    }

    /* Highlight Card: Forest Green Gradient Accent (Replaces Dribbble Yellow Card) */
    .wp-quick-card.wp-hero-highlight {
      background: linear-gradient(135deg, #e8f5e9 0%, #d1fae5 60%, #ecfdf5 100%);
      border: 1px solid #86efac;
      box-shadow: 0 8px 24px rgba(5, 150, 105, 0.14);
    }
    .wp-quick-card.wp-hero-highlight:hover {
      background: linear-gradient(135deg, #def0e0 0%, #c4f3dc 60%, #e2fbf0 100%);
      border-color: #4ade80;
    }
    .wp-quick-card.wp-hero-highlight .wp-card-title {
      color: #064e3b !important;
    }
    .wp-quick-card.wp-hero-highlight .wp-card-desc {
      color: #047857 !important;
    }"""

    if old_card_css in html:
        html = html.replace(old_card_css, new_card_css)
        print("Updated quick action cards to light mode with Forest Green gradient hero highlight.")

    # Apply .wp-hero-highlight to Card 1
    html = html.replace(
        '<div class="wp-quick-card" id="btnActionStartMeeting">',
        '<div class="wp-quick-card wp-hero-highlight" id="btnActionStartMeeting">'
    )

    # 11. Quick Card Titles and Descriptions
    html = html.replace(
        ".wp-card-title {\n      font-size: 0.95rem;\n      font-weight: 700;\n      color: #ffffff;",
        ".wp-card-title {\n      font-size: 0.95rem;\n      font-weight: 700;\n      color: #0c1c15;"
    )
    html = html.replace(
        ".wp-card-desc {\n      font-size: 0.78rem;\n      color: var(--text-muted);",
        ".wp-card-desc {\n      font-size: 0.78rem;\n      color: #64748b;"
    )

    # 12. Quick Card Icons
    old_icons = """.icon-video { background: linear-gradient(135deg, #1d4ed8, #0ea5e9); box-shadow: 0 4px 14px rgba(14, 165, 233, 0.3); }
    .icon-bot { background: linear-gradient(135deg, #3730a3, #4f46e5); box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3); }
    .icon-upload { background: linear-gradient(135deg, #065f46, #10b981); box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3); }
    .icon-graph { background: linear-gradient(135deg, #92400e, #f59e0b); box-shadow: 0 4px 14px rgba(245, 158, 11, 0.3); }"""

    new_icons = """.icon-video { background: linear-gradient(135deg, #064e3b, #059669); box-shadow: 0 4px 14px rgba(6, 78, 59, 0.28); color: #ffffff; }
    .icon-bot { background: linear-gradient(135deg, #0f172a, #134e4a); box-shadow: 0 4px 14px rgba(15, 23, 42, 0.2); color: #ffffff; }
    .icon-upload { background: linear-gradient(135deg, #047857, #10b981); box-shadow: 0 4px 14px rgba(4, 120, 87, 0.25); color: #ffffff; }
    .icon-graph { background: linear-gradient(135deg, #065f46, #34d399); box-shadow: 0 4px 14px rgba(6, 95, 70, 0.25); color: #ffffff; }"""

    if old_icons in html:
        html = html.replace(old_icons, new_icons)
        print("Updated quick card icon gradients to forest green family.")

    # 13. Cross-Platform Section Card
    old_cp_style = """    .wp-cross-platform-card {
      width: 100%;
      max-width: 860px;
      background: var(--bg-surface);
      border: 1px solid var(--border-hairline);
      border-radius: 18px;
      padding: 24px 28px;
      margin-bottom: 28px;
      backdrop-filter: blur(20px);
      position: relative;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    .wp-cross-platform-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: linear-gradient(90deg, #2563eb, #0ea5e9);
    }"""

    new_cp_style = """    .wp-cross-platform-card {
      width: 100%;
      max-width: 860px;
      background: #ffffff;
      border: 1px solid #e2ece3;
      border-radius: 20px;
      padding: 26px 28px;
      margin-bottom: 28px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 4px 20px -2px rgba(6, 78, 59, 0.06), 0 1px 3px rgba(0, 0, 0, 0.03);
    }

    .wp-cross-platform-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, #064e3b, #059669, #10b981);
    }"""

    if old_cp_style in html:
        html = html.replace(old_cp_style, new_cp_style)
        print("Updated cross-platform card style.")

    # 14. Cross-Platform Card Titles and Text
    html = html.replace(
        ".wp-cp-title {\n      font-size: 1.15rem;\n      font-weight: 700;\n      color: #ffffff;",
        ".wp-cp-title {\n      font-size: 1.15rem;\n      font-weight: 700;\n      color: #0c1c15;"
    )
    html = html.replace(
        ".wp-cp-desc {\n      font-size: 0.86rem;\n      color: var(--text-muted);",
        ".wp-cp-desc {\n      font-size: 0.86rem;\n      color: #475569;"
    )

    # 15. Platform Pills in Cross-Platform Card
    old_pills = """    .wp-cp-pill {
      padding: 6px 14px;
      border-radius: var(--radius-full);
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--text-muted);
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .wp-cp-pill:hover {
      background: rgba(255, 255, 255, 0.12);
      color: #ffffff;
    }

    .wp-cp-pill.active {
      background: var(--accent-wash);
      color: #60a5fa;
      border-color: rgba(59, 130, 246, 0.35);
    }"""

    new_pills = """    .wp-cp-pill {
      padding: 6px 14px;
      border-radius: var(--radius-full);
      background: #f4f8f4;
      border: 1px solid #dce8dd;
      color: #475569;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .wp-cp-pill:hover {
      background: #eaf3ec;
      color: #064e3b;
    }

    .wp-cp-pill.active {
      background: #064e3b;
      color: #ffffff;
      border-color: #064e3b;
      box-shadow: 0 2px 8px rgba(6, 78, 59, 0.25);
    }"""

    if old_pills in html:
        html = html.replace(old_pills, new_pills)
        print("Updated platform pills to Forest Green active style.")

    # 16. Inputs & Buttons in Cross-Platform Card
    html = html.replace(
        "background: rgba(0, 0, 0, 0.4);\n      border: 1px solid rgba(255, 255, 255, 0.14);\n      color: #ffffff;",
        "background: #f8faf8;\n      border: 1px solid #cbd5e1;\n      color: #1e293b;"
    )

    # 17. Primary Buttons throughout index.html (Forest Green Gradient)
    html = html.replace(
        "linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%)",
        "linear-gradient(180deg, #065f46 0%, #047857 100%)"
    )
    html = html.replace(
        "linear-gradient(135deg, #2563eb, #0ea5e9)",
        "linear-gradient(135deg, #064e3b, #059669)"
    )
    html = html.replace(
        "linear-gradient(90deg, #2563eb, #0ea5e9)",
        "linear-gradient(90deg, #064e3b, #059669)"
    )

    # 18. AI Companion Rail (Right)
    html = html.replace(
        "background: rgba(14, 14, 26, 0.95);\n      border-left: 1px solid rgba(255, 255, 255, 0.08);",
        "background: #fbfdfb;\n      border-left: 1px solid #e5ede6;"
    )

    old_comp_card = """    .wp-companion-card {
      display: flex;
      flex-direction: column;
      flex: 1;
      border-radius: 18px;
      padding: 20px;
      background: var(--bg-surface);
      border: 1px solid var(--border-hairline);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.06);
      overflow: hidden;
    }"""

    new_comp_card = """    .wp-companion-card {
      display: flex;
      flex-direction: column;
      flex: 1;
      border-radius: 20px;
      padding: 20px;
      background: #ffffff;
      border: 1px solid #e2ece3;
      box-shadow: 0 4px 20px rgba(6, 78, 59, 0.06);
      overflow: hidden;
    }"""

    if old_comp_card in html:
        html = html.replace(old_comp_card, new_comp_card)
        print("Updated companion card to light mode.")

    # Companion Text & Chat Bubble
    html = html.replace(
        ".wp-companion-title {\n      font-size: 1.05rem;\n      font-weight: 700;\n      color: #ffffff;",
        ".wp-companion-title {\n      font-size: 1.05rem;\n      font-weight: 700;\n      color: #0c1c15;"
    )
    html = html.replace(
        ".wp-companion-title span.highlight {\n      color: #38bdf8;",
        ".wp-companion-title span.highlight {\n      color: #059669;"
    )
    html = html.replace(
        "background: rgba(56, 189, 248, 0.12);\n      border: 1px solid rgba(56, 189, 248, 0.25);\n      border-radius: 16px 16px 4px 16px;\n      padding: 10px 14px;\n      font-size: 0.82rem;\n      color: #e0f2fe;",
        "background: #eaf6ec;\n      border: 1px solid #cce7d0;\n      border-radius: 16px 16px 4px 16px;\n      padding: 10px 14px;\n      font-size: 0.82rem;\n      color: #064e3b;\n      font-weight: 500;"
    )
    html = html.replace(
        ".wp-cap-heading {\n      font-size: 0.85rem;\n      font-weight: 600;\n      color: #ffffff;",
        ".wp-cap-heading {\n      font-size: 0.85rem;\n      font-weight: 600;\n      color: #0c1c15;"
    )
    html = html.replace(
        ".wp-prompt-chip {\n      padding: 4px 10px;\n      border-radius: var(--radius-full);\n      background: rgba(255, 255, 255, 0.06);\n      border: 1px solid rgba(255, 255, 255, 0.1);\n      color: var(--text-muted);",
        ".wp-prompt-chip {\n      padding: 5px 12px;\n      border-radius: var(--radius-full);\n      background: #f4f8f4;\n      border: 1px solid #dce8dd;\n      color: #064e3b;\n      font-weight: 500;"
    )
    html = html.replace(
        ".wp-prompt-chip:hover {\n      background: rgba(255, 255, 255, 0.12);\n      color: #ffffff;",
        ".wp-prompt-chip:hover {\n      background: #e6f4ea;\n      color: #064e3b;\n      border-color: #86efac;"
    )
    html = html.replace(
        ".wp-companion-input-box {\n      margin-top: auto;\n      display: flex;\n      align-items: center;\n      gap: 8px;\n      background: rgba(0, 0, 0, 0.35);\n      border: 1px solid rgba(255, 255, 255, 0.12);",
        ".wp-companion-input-box {\n      margin-top: auto;\n      display: flex;\n      align-items: center;\n      gap: 8px;\n      background: #f4f8f4;\n      border: 1px solid #dce8dd;"
    )
    html = html.replace(
        ".wp-companion-input {\n      flex: 1;\n      border: none;\n      outline: none;\n      background: transparent;\n      color: #ffffff;",
        ".wp-companion-input {\n      flex: 1;\n      border: none;\n      outline: none;\n      background: transparent;\n      color: #1e293b;"
    )

    # 19. More Popover in Light Mode
    html = html.replace(
        ".wp-more-popover {\n      position: fixed;\n      width: 275px;\n      background: #ffffff;\n      border: 1px solid #e2e8f0;",
        ".wp-more-popover {\n      position: fixed;\n      width: 275px;\n      background: #ffffff;\n      border: 1px solid #e2ece3;\n      box-shadow: 0 16px 45px rgba(6, 78, 59, 0.12), 0 2px 10px rgba(0, 0, 0, 0.04);"
    )

    # 20. App Suite Modal Dialog in Light Mode
    old_modal_dialog = """    .wp-app-modal-dialog {
      width: 100%;
      max-width: 940px;
      height: 88vh;
      max-height: 820px;
      background: #0f1322;
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 20px;
      box-shadow: 0 30px 80px rgba(0, 0, 0, 0.85);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      animation: modalSlideUp 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }"""

    new_modal_dialog = """    .wp-app-modal-dialog {
      width: 100%;
      max-width: 940px;
      height: 88vh;
      max-height: 820px;
      background: #ffffff;
      border: 1px solid #e2ece3;
      border-radius: 24px;
      box-shadow: 0 25px 60px rgba(6, 78, 59, 0.18), 0 4px 16px rgba(0, 0, 0, 0.05);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      animation: modalSlideUp 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }"""

    if old_modal_dialog in html:
        html = html.replace(old_modal_dialog, new_modal_dialog)
        print("Updated app modal dialog to light mode.")

    # Modal Header & Nav
    html = html.replace(
        "background: rgba(255, 255, 255, 0.03);\n      border-bottom: 1px solid rgba(255, 255, 255, 0.08);",
        "background: #f8faf8;\n      border-bottom: 1px solid #e5ede6;"
    )
    html = html.replace(
        ".wp-app-modal-title {\n      font-size: 1.15rem;\n      font-weight: 700;\n      color: #ffffff;",
        ".wp-app-modal-title {\n      font-size: 1.15rem;\n      font-weight: 700;\n      color: #0c1c15;"
    )
    html = html.replace(
        "background: rgba(0, 0, 0, 0.25);\n      border-bottom: 1px solid rgba(255, 255, 255, 0.06);",
        "background: #f4f8f4;\n      border-bottom: 1px solid #e5ede6;"
    )

    # Active Pill in Modal Nav Bar (Forest Green Capsule)
    old_modal_pill = """    .wp-app-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: var(--text-muted);
      font-size: 0.78rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.15s ease;
      flex-shrink: 0;
    }
    .wp-app-pill:hover {
      background: rgba(255, 255, 255, 0.1);
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.18);
    }
    .wp-app-pill.active {
      background: var(--accent-wash);
      border-color: rgba(59, 130, 246, 0.45);
      color: #60a5fa;
      font-weight: 600;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
    }"""

    new_modal_pill = """    .wp-app-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 9999px;
      background: #ffffff;
      border: 1px solid #dce8dd;
      color: #475569;
      font-size: 0.78rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.15s ease;
      flex-shrink: 0;
    }
    .wp-app-pill:hover {
      background: #eef6f0;
      color: #064e3b;
      border-color: #cbdcd0;
    }
    .wp-app-pill.active {
      background: #064e3b;
      border-color: #064e3b;
      color: #ffffff;
      font-weight: 600;
      box-shadow: 0 2px 8px rgba(6, 78, 59, 0.25);
    }"""

    if old_modal_pill in html:
        html = html.replace(old_modal_pill, new_modal_pill)
        print("Updated modal pills to Forest Green capsule pills.")

    # Modal Body Background & Text
    html = html.replace(
        ".wp-app-modal-body {\n      flex: 1;\n      overflow-y: auto;\n      padding: 22px;\n      color: #ffffff;\n    }",
        ".wp-app-modal-body {\n      flex: 1;\n      overflow-y: auto;\n      padding: 24px;\n      color: #1e293b;\n      background: #ffffff;\n    }"
    )

    # 21. Modal App Components (.app-card, .app-input, .app-textarea, .app-btn-secondary)
    old_app_comps = """    .app-input {
      width: 100%;
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      padding: 9px 12px;
      color: #ffffff;
      font-size: 0.88rem;
      outline: none;
      transition: border-color 0.15s ease;
      box-sizing: border-box;
    }
    .app-input:focus {
      border-color: #38bdf8;
    }
    .app-textarea {
      width: 100%;
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      padding: 10px 12px;
      color: #ffffff;
      font-size: 0.85rem;
      font-family: var(--font-mono);
      line-height: 1.5;
      outline: none;
      resize: vertical;
      min-height: 110px;
      box-sizing: border-box;
    }
    .app-textarea:focus {
      border-color: #38bdf8;
    }"""

    new_app_comps = """    .app-input {
      width: 100%;
      background: #f8faf8;
      border: 1px solid #cbd5e1;
      border-radius: 10px;
      padding: 9px 12px;
      color: #1e293b;
      font-size: 0.88rem;
      outline: none;
      transition: border-color 0.15s ease;
      box-sizing: border-box;
    }
    .app-input:focus {
      border-color: #059669;
      box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.12);
    }
    .app-textarea {
      width: 100%;
      background: #f8faf8;
      border: 1px solid #cbd5e1;
      border-radius: 10px;
      padding: 10px 12px;
      color: #1e293b;
      font-size: 0.85rem;
      font-family: var(--font-mono);
      line-height: 1.5;
      outline: none;
      resize: vertical;
      min-height: 110px;
      box-sizing: border-box;
    }
    .app-textarea:focus {
      border-color: #059669;
      box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.12);
    }"""

    if old_app_comps in html:
        html = html.replace(old_app_comps, new_app_comps)
        print("Updated app input and textarea to light mode.")

    # .app-card and .app-btn-secondary
    html = html.replace(
        ".app-card {\n      background: rgba(255, 255, 255, 0.03);\n      border: 1px solid rgba(255, 255, 255, 0.08);",
        ".app-card {\n      background: #f8faf8;\n      border: 1px solid #e2ece3;"
    )
    html = html.replace(
        "background: rgba(255, 255, 255, 0.08);\n      border: 1px solid rgba(255, 255, 255, 0.12);\n      color: #ffffff;",
        "background: #f1f5f2;\n      border: 1px solid #dce8dd;\n      color: #1e293b;"
    )

    # 22. App Modal Overlay
    html = html.replace(
        "background: rgba(4, 6, 14, 0.88);\n      backdrop-filter: blur(18px);",
        "background: rgba(12, 28, 21, 0.45);\n      backdrop-filter: blur(14px);"
    )

    # 23. Close Button
    html = html.replace(
        "background: rgba(255, 255, 255, 0.06);\n      border: 1px solid rgba(255, 255, 255, 0.1);",
        "background: #f1f5f2;\n      border: 1px solid #dce8dd;"
    )

    # 24. Join Modal overlay and box
    html = html.replace(
        "background: rgba(18, 18, 34, 0.98);\n      border: 1px solid rgba(255, 255, 255, 0.12);",
        "background: #ffffff;\n      border: 1px solid #e2ece3; box-shadow: 0 25px 60px rgba(6, 78, 59, 0.2);"
    )
    html = html.replace(
        ".wp-modal-title {\n      font-size: 1.25rem;\n      font-weight: 700;\n      color: #ffffff;",
        ".wp-modal-title {\n      font-size: 1.25rem;\n      font-weight: 700;\n      color: #0c1c15;"
    )

    # 25. Dialpad Card in Phone Tab
    html = html.replace(
        ".dialpad-card {\n      background: var(--bg-surface);\n      border: 1px solid var(--border-hairline);\n      border-radius: 20px;\n      padding: 24px 20px;\n      width: 290px;",
        ".dialpad-card {\n      background: #ffffff;\n      border: 1px solid #e2ece3;\n      border-radius: 24px;\n      padding: 24px 20px;\n      width: 290px;\n      box-shadow: 0 4px 20px rgba(6, 78, 59, 0.06);"
    )
    html = html.replace(
        ".dialpad-screen {\n      width: 100%;\n      height: 48px;\n      background: rgba(0, 0, 0, 0.4);\n      border: 1px solid rgba(255, 255, 255, 0.12);\n      border-radius: 12px;\n      margin-bottom: 20px;\n      display: flex;\n      align-items: center;\n      justify-content: center;\n      font-size: 1.4rem;\n      font-family: var(--font-mono);\n      color: #38bdf8;",
        ".dialpad-screen {\n      width: 100%;\n      height: 48px;\n      background: #f4f8f4;\n      border: 1px solid #dce8dd;\n      border-radius: 12px;\n      margin-bottom: 20px;\n      display: flex;\n      align-items: center;\n      justify-content: center;\n      font-size: 1.4rem;\n      font-family: var(--font-mono);\n      color: #064e3b;\n      font-weight: 700;"
    )
    html = html.replace(
        ".dial-key {\n      width: 58px;\n      height: 58px;\n      border-radius: 50%;\n      background: rgba(255, 255, 255, 0.06);\n      border: 1px solid rgba(255, 255, 255, 0.1);\n      color: #ffffff;",
        ".dial-key {\n      width: 58px;\n      height: 58px;\n      border-radius: 50%;\n      background: #f4f8f4;\n      border: 1px solid #dce8dd;\n      color: #0c1c15;"
    )

    # 26. Replace inline styles in JavaScript templates inside index.html for the 11 modules:
    # color:#fff -> color:#0c1c15 or var(--text-primary)
    # background:rgba(255,255,255,0.03) -> background:#f8faf8
    # background:rgba(0,0,0,0.35) -> background:#f8faf8
    # border:1px solid rgba(255,255,255,0.08) -> border:1px solid #e2ece3
    html = html.replace("color:#fff;", "color:#0c1c15;")
    html = html.replace("color:#ffffff;", "color:#0c1c15;")
    html = html.replace("background:rgba(255,255,255,0.03);", "background:#f8faf8;")
    html = html.replace("background:rgba(255,255,255,0.04);", "background:#f4f8f4;")
    html = html.replace("border:1px solid rgba(255,255,255,0.08);", "border:1px solid #e2ece3;")
    html = html.replace("border-bottom:1px solid rgba(255,255,255,0.06);", "border-bottom:1px solid #edf4ee;")
    html = html.replace("border-bottom:1px solid rgba(255,255,255,0.08);", "border-bottom:1px solid #e2ece3;")
    html = html.replace("background:rgba(0,0,0,0.25);", "background:#f8faf8;")
    html = html.replace("background:rgba(0,0,0,0.3);", "background:#f4f8f4;")
    html = html.replace("background:rgba(0,0,0,0.4);", "background:#f4f8f4;")

    # Fix button and badge text colors where text was turned into dark on dark background
    html = html.replace(
        "app-btn-primary\" style=\"text-decoration:none;\">\n                      <span>🚀</span> Start Broadcast Room",
        "app-btn-primary\" style=\"text-decoration:none;color:#ffffff;\">\n                      <span>🚀</span> Start Broadcast Room"
    )
    html = html.replace(
        "class=\"app-btn-primary\"",
        "class=\"app-btn-primary\" style=\"color:#ffffff;\""
    )

    # Workvivo comments & author colors
    html = html.replace("color:#f1f5f9;", "color:#1e293b;")
    html = html.replace("color:#e2e8f0;", "color:#334155;")
    html = html.replace(
        "background:linear-gradient(135deg, #064e3b, #059669);display:flex;align-items:center;justify-content:center;font-weight:700;color:#0c1c15;",
        "background:linear-gradient(135deg, #064e3b, #059669);display:flex;align-items:center;justify-content:center;font-weight:700;color:#ffffff;"
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully applied Forest Green Light Theme to {path}!")

if __name__ == "__main__":
    transform_index()
