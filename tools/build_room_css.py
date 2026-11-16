# build_room_css.py
"""
Build the modern Dribbble template stylesheet for frontend/room.html
Aesthetic:
- Outer background: #a9b8aa (matte sage green)
- Main container: #ffffff shell, border-radius: 28px, box-shadow: 0 25px 70px rgba(0,0,0,0.12)
- Inner surfaces: #ffffff and #fbfcfb
- Hairline borders: #edf0ed
- Dark accents & capsules: #18191b
- Lime chartreuse accents: #e5f97e
- Typography: Plus Jakarta Sans
"""

NEW_CSS = """
    /* ── Reset & Global Variables ─────────────────────────────────────── */
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    :root {
      --canvas-sage: #a9b8aa;
      --shell-white: #ffffff;
      --dock-dark: #18191b;
      --highlight-lime: #e5f97e;
      --card-bg: #fbfcfb;
      --card-border: #edf0ed;
      --card-border-hover: #dbe2db;
      
      --text-dark: #18191b;
      --text-primary: #18191b;
      --text-secondary: #475569;
      --text-muted: #8b95a5;
      --text-heading: #18191b;
      
      --success: #10b981;
      --success-bg: #eafaf1;
      --success-border: #c2eed5;
      --danger: #ef4444;
      --danger-hover: #dc2626;
      --danger-bg: #fef2f2;
      --danger-border: #fee2e2;
      --warning: #f59e0b;
      --secondary: #18191b;
      
      --font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --topbar-height: 72px;
      --bottombar-height: 78px;
    }

    html, body {
      width: 100%;
      height: 100%;
      margin: 0;
      padding: 0;
      overflow: hidden;
      font-family: var(--font-family);
      background-color: var(--canvas-sage);
      color: var(--text-dark);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    /* Ambient radial orbs hidden for clean Dribbble light aesthetic */
    body::before, body::after, .ambient-orb-center {
      display: none !important;
    }

    /* ── Application Layout ───────────────────────────────────────────── */
    #app-container {
      position: relative;
      width: calc(100vw - 32px);
      max-width: 1720px;
      height: calc(100vh - 32px);
      margin: 16px auto;
      background: var(--shell-white);
      border-radius: 28px;
      border: 1px solid rgba(0, 0, 0, 0.05);
      box-shadow: 0 25px 70px rgba(0, 0, 0, 0.12);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      z-index: 1;
    }

    /* ── Top Bar ──────────────────────────────────────────────────────── */
    header.top-bar {
      height: var(--topbar-height);
      padding: 0 28px;
      background: #ffffff;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      z-index: 20;
    }

    .top-left {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .brand-logo {
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-icon {
      width: 44px;
      height: 44px;
      border-radius: 14px;
      background: var(--dock-dark);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--highlight-lime);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease;
    }

    .brand-icon:hover {
      transform: scale(1.04);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18);
    }

    .brand-icon svg {
      width: 22px;
      height: 22px;
      stroke: var(--highlight-lime);
    }

    .meeting-info-group {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }

    .meeting-title-row {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .meeting-title {
      font-size: 17px;
      font-weight: 800;
      color: var(--text-dark);
      letter-spacing: -0.02em;
    }

    .meeting-id-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #f4f7f4;
      border: 1px solid #e2e8e2;
      border-radius: 9999px;
      padding: 5px 12px;
      font-size: 12px;
      font-weight: 700;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      color: var(--text-dark);
      cursor: pointer;
      transition: all 0.2s ease;
      user-select: none;
    }

    .meeting-id-pill:hover {
      background: #e7ede7;
      border-color: #cbd5e1;
    }

    .meeting-id-pill svg {
      width: 13px;
      height: 13px;
      stroke: var(--text-muted);
      transition: stroke 0.2s ease;
    }

    .meeting-id-pill:hover svg {
      stroke: var(--text-dark);
    }

    .meeting-id-pill.copied {
      background: var(--highlight-lime);
      border-color: #d1ea64;
      color: var(--dock-dark);
    }

    /* Top Center: Recording Indicator & Timer */
    .top-center {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .recording-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: var(--danger-bg);
      border: 1px solid var(--danger-border);
      border-radius: 9999px;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 700;
      color: #dc2626;
      letter-spacing: -0.01em;
    }

    .pulsing-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--danger);
      box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
      animation: pulseRecord 1.8s infinite;
    }

    @keyframes pulseRecord {
      0% {
        transform: scale(0.95);
        box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
      }
      70% {
        transform: scale(1);
        box-shadow: 0 0 0 8px rgba(239, 68, 68, 0);
      }
      100% {
        transform: scale(0.95);
        box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
      }
    }

    .timer-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--dock-dark);
      color: #ffffff;
      border-radius: 9999px;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 700;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .timer-badge svg {
      width: 14px;
      height: 14px;
      stroke: var(--highlight-lime);
    }

    /* Top Right: Stats & Navigation */
    .top-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .participants-counter {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #f4f7f4;
      border: 1px solid #e2e8e2;
      border-radius: 9999px;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 700;
      color: var(--text-dark);
    }

    .participants-counter svg {
      width: 14px;
      height: 14px;
      stroke: var(--text-dark);
    }

    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #f4f7f4;
      border: 1px solid #e2e8e2;
      border-radius: 9999px;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 700;
      color: var(--text-muted);
    }

    .status-pill.connected {
      background: var(--success-bg);
      border-color: var(--success-border);
      color: #107e4a;
    }

    .status-pill .indicator-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #94a3b8;
    }

    .status-pill.connected .indicator-dot {
      background: #10b981;
      box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25);
    }

    .top-nav-link {
      text-decoration: none;
      font-size: 12px;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 9999px;
      background: #f4f7f4;
      color: var(--text-dark);
      border: 1px solid #e2e8e2;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.18s ease;
    }

    .top-nav-link:hover {
      background: var(--dock-dark);
      border-color: var(--dock-dark);
      color: #ffffff;
      transform: translateY(-1px);
    }

    .top-nav-link svg {
      stroke: currentColor;
    }

    /* ── Main Workspace: Two-Column Layout ────────────────────────────── */
    .main-workspace {
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 20px;
      padding: 20px 28px;
      flex: 1;
      overflow: hidden;
      background: #f8faf8;
    }

    /* ── Left Column: Participant Tiles ───────────────────────────────── */
    .left-panel {
      display: flex;
      flex-direction: column;
      overflow: hidden;
      background: #ffffff;
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 22px;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.02);
    }

    .panel-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 18px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--card-border);
      flex-shrink: 0;
    }

    .panel-title {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 15px;
      font-weight: 800;
      color: var(--text-dark);
      letter-spacing: -0.01em;
    }

    .panel-title svg {
      width: 18px;
      height: 18px;
      stroke: var(--text-dark);
    }

    #tiles-count-hint {
      font-size: 12px;
      font-weight: 700;
      color: var(--text-muted);
      background: #f4f7f4;
      padding: 4px 12px;
      border-radius: 9999px;
    }

    .tiles-grid-container {
      flex: 1;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      align-content: start;
      overflow-y: auto;
      padding-right: 4px;
    }

    /* Participant Tile Card */
    .participant-tile {
      position: relative;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 22px;
      min-height: 250px;
      padding: 24px 20px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
      overflow: hidden;
    }

    .participant-tile:hover {
      transform: translateY(-2px);
      border-color: var(--card-border-hover);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
    }

    .participant-tile.speaking {
      border: 2px solid var(--dock-dark);
      box-shadow: 0 0 0 3px rgba(229, 249, 126, 0.65), 0 8px 25px rgba(0, 0, 0, 0.06);
    }

    /* Video inside tile */
    .tile-video {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: none;
      z-index: 1;
      background: #000000;
      border-radius: 22px;
    }

    .tile-video.active {
      display: block;
    }

    .participant-tile.has-video {
      padding: 0;
      min-height: 260px;
      background: #000000;
    }

    .participant-tile.has-video .avatar-wrapper {
      display: none !important;
    }

    .participant-tile.has-video .participant-name-row {
      position: absolute;
      bottom: 14px;
      left: 14px;
      z-index: 3;
      background: rgba(24, 25, 27, 0.75);
      backdrop-filter: blur(8px);
      padding: 5px 12px;
      border-radius: 9999px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      flex-direction: row;
      gap: 6px;
    }

    .participant-tile.has-video .participant-name {
      color: #ffffff;
      font-size: 13px;
    }

    .participant-tile.has-video .tile-status-row {
      position: absolute;
      top: 14px;
      right: 14px;
      z-index: 3;
    }

    .participant-tile.has-video .speaking-badge {
      position: absolute;
      top: 14px;
      left: 14px;
      z-index: 3;
    }

    /* Avatar styling */
    .avatar-wrapper {
      position: relative;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .participant-avatar {
      width: 90px;
      height: 90px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 26px;
      font-weight: 800;
      color: #ffffff;
      border: 4px solid #ffffff;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
      z-index: 2;
      position: relative;
    }

    .speaking-rings {
      position: absolute;
      top: -8px;
      left: -8px;
      right: -8px;
      bottom: -8px;
      border-radius: 50%;
      border: 2.5px solid var(--highlight-lime);
      opacity: 0;
      transform: scale(0.9);
      transition: all 0.3s ease;
      z-index: 1;
    }

    .participant-tile.speaking .speaking-rings {
      opacity: 1;
      animation: pulseAvatarRing 1.5s infinite;
    }

    @keyframes pulseAvatarRing {
      0% { transform: scale(0.95); opacity: 0.9; }
      50% { transform: scale(1.18); opacity: 0.4; }
      100% { transform: scale(1.35); opacity: 0; }
    }

    /* Speaking badge pill */
    .speaking-badge {
      position: absolute;
      top: 14px;
      right: 14px;
      display: none;
      align-items: center;
      gap: 6px;
      background: var(--dock-dark);
      color: var(--highlight-lime);
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.02em;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
      z-index: 3;
    }

    .participant-tile.speaking .speaking-badge {
      display: inline-flex;
    }

    .sound-bars {
      display: flex;
      align-items: center;
      gap: 2px;
      height: 12px;
    }

    .sound-bar {
      width: 2.5px;
      height: 4px;
      background: var(--highlight-lime);
      border-radius: 2px;
      animation: soundBarBounce 0.8s ease-in-out infinite alternate;
    }

    .sound-bar:nth-child(1) { animation-delay: 0.1s; height: 10px; }
    .sound-bar:nth-child(2) { animation-delay: 0.3s; height: 6px; }
    .sound-bar:nth-child(3) { animation-delay: 0.2s; height: 12px; }
    .sound-bar:nth-child(4) { animation-delay: 0.4s; height: 8px; }

    @keyframes soundBarBounce {
      0% { height: 3px; }
      100% { height: 12px; }
    }

    .participant-name-row {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      z-index: 2;
      margin-bottom: 10px;
    }

    .participant-name {
      font-size: 15px;
      font-weight: 800;
      color: var(--text-dark);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .you-pill {
      background: var(--highlight-lime);
      color: var(--dock-dark);
      font-size: 11px;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 9999px;
      letter-spacing: 0.02em;
    }

    .tile-status-row {
      display: flex;
      align-items: center;
      gap: 8px;
      z-index: 2;
    }

    .mic-status-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      background: var(--success-bg);
      border: 1px solid var(--success-border);
      color: #107e4a;
      transition: all 0.2s ease;
      cursor: pointer;
    }

    .mic-status-pill.muted {
      background: var(--danger-bg);
      border-color: var(--danger-border);
      color: #dc2626;
    }

    .mic-status-pill svg {
      width: 12px;
      height: 12px;
      stroke: currentColor;
    }

    /* Waiting for colleagues card */
    .waiting-card {
      border: 1.5px dashed #cbd5e1;
      background: var(--card-bg);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 30px 24px;
      border-radius: 22px;
      min-height: 250px;
      transition: all 0.2s ease;
    }

    .waiting-card:hover {
      border-color: #94a3b8;
      background: #ffffff;
    }

    .waiting-icon {
      width: 52px;
      height: 52px;
      border-radius: 16px;
      background: #f4f7f4;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text-dark);
      margin-bottom: 14px;
    }

    .waiting-icon svg {
      stroke: var(--text-dark);
    }

    .waiting-title {
      font-size: 15px;
      font-weight: 800;
      color: var(--text-dark);
      margin-bottom: 6px;
    }

    .waiting-subtitle {
      font-size: 12px;
      color: var(--text-secondary);
      line-height: 1.5;
      max-width: 260px;
      margin-bottom: 18px;
    }

    .waiting-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: var(--dock-dark);
      color: #ffffff;
      font-size: 12px;
      font-weight: 700;
      padding: 9px 18px;
      border-radius: 9999px;
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
      transition: all 0.18s ease;
    }

    .waiting-btn:hover {
      background: #000000;
      transform: translateY(-1px);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18);
    }

    .waiting-btn svg {
      stroke: var(--highlight-lime);
    }

    /* ── Right Column: Live Transcript Panel ──────────────────────────── */
    .right-panel {
      display: flex;
      flex-direction: column;
      overflow: hidden;
      background: #ffffff;
      border: 1px solid var(--card-border);
      border-radius: 24px;
      padding: 22px;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.02);
    }

    .transcript-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 14px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--card-border);
      flex-shrink: 0;
    }

    .transcript-title-wrap {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .transcript-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 16px;
      font-weight: 800;
      color: var(--text-dark);
      letter-spacing: -0.02em;
    }

    .transcript-title svg {
      width: 18px;
      height: 18px;
      stroke: var(--text-dark);
    }

    .live-stream-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--highlight-lime);
      color: var(--dock-dark);
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.04em;
    }

    .green-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--dock-dark);
      animation: pulseDot 1.5s infinite;
    }

    @keyframes pulseDot {
      0% { opacity: 0.4; }
      50% { opacity: 1; }
      100% { opacity: 0.4; }
    }

    .transcript-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .transcript-action-btn {
      width: 36px;
      height: 36px;
      border-radius: 12px;
      background: #f4f7f4;
      border: 1px solid #e2e8e2;
      color: var(--text-dark);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.18s ease;
    }

    .transcript-action-btn:hover {
      background: var(--dock-dark);
      border-color: var(--dock-dark);
      color: #ffffff;
      transform: translateY(-1px);
    }

    .transcript-action-btn svg {
      width: 15px;
      height: 15px;
      stroke: currentColor;
    }

    /* Transcript Subbar: Language filter & Auto-scroll */
    .transcript-subbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
      gap: 10px;
      flex-shrink: 0;
    }

    .lang-pills-group {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .lang-filter-pill {
      padding: 5px 14px;
      border-radius: 9999px;
      background: #f4f7f4;
      border: 1px solid #e2e8e2;
      color: var(--text-secondary);
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.18s ease;
      user-select: none;
    }

    .lang-filter-pill:hover {
      background: #edf1ed;
      color: var(--text-dark);
    }

    .lang-filter-pill.active {
      background: var(--dock-dark);
      border-color: var(--dock-dark);
      color: #ffffff;
    }

    .auto-scroll-toggle {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-secondary);
      cursor: pointer;
      user-select: none;
    }

    .auto-scroll-toggle input {
      accent-color: var(--dock-dark);
      cursor: pointer;
    }

    /* Scrolling Segment Feed */
    .transcript-feed {
      flex: 1;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding-right: 4px;
    }

    /* Empty State */
    .transcript-empty-state {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 60px 24px;
      margin: auto 0;
    }

    .speech-radar {
      position: relative;
      width: 72px;
      height: 72px;
      border-radius: 50%;
      background: rgba(229, 249, 126, 0.3);
      border: 2px solid var(--highlight-lime);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--dock-dark);
      margin-bottom: 18px;
    }

    .speech-radar svg {
      width: 26px;
      height: 26px;
      stroke: var(--dock-dark);
    }

    .radar-pulse {
      position: absolute;
      top: -12px;
      left: -12px;
      right: -12px;
      bottom: -12px;
      border-radius: 50%;
      border: 2px solid rgba(229, 249, 126, 0.7);
      animation: radarWave 2s cubic-bezier(0, 0.2, 0.8, 1) infinite;
    }

    @keyframes radarWave {
      0% { transform: scale(0.85); opacity: 0.9; }
      100% { transform: scale(1.45); opacity: 0; }
    }

    .empty-title {
      font-size: 16px;
      font-weight: 800;
      color: var(--text-dark);
      margin-bottom: 6px;
    }

    .empty-desc {
      font-size: 12.5px;
      color: var(--text-secondary);
      line-height: 1.55;
      max-width: 320px;
    }

    /* Segment Cards */
    .segment-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 14px 16px;
      transition: all 0.18s ease;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
    }

    .segment-card:hover {
      background: #ffffff;
      border-color: var(--card-border-hover);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
    }

    .segment-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }

    .segment-speaker-info {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .segment-speaker-avatar {
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: var(--dock-dark);
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 10px;
      font-weight: 800;
    }

    .segment-speaker-name {
      font-size: 13px;
      font-weight: 800;
      color: var(--text-dark);
    }

    .segment-meta {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .timestamp-badge {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted);
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }

    .lang-badge {
      font-size: 10px;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 9999px;
      background: #f4f7f4;
      border: 1px solid #e2e8e2;
      color: var(--text-dark);
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .segment-body {
      font-size: 13.5px;
      line-height: 1.5;
      color: #1e293b;
      word-break: break-word;
    }

    .segment-translation {
      margin-top: 10px;
      padding: 8px 12px;
      background: #f4fdf7;
      border-left: 3px solid #10b981;
      border-radius: 8px;
      font-size: 12.5px;
      color: #065f46;
      line-height: 1.45;
    }

    .segment-translation-label {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #047857;
      margin-bottom: 3px;
    }

    /* ── Bottom Bar ───────────────────────────────────────────────────── */
    footer.bottom-bar {
      height: var(--bottombar-height);
      padding: 0 28px;
      background: #ffffff;
      border-top: 1px solid var(--card-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      z-index: 20;
    }

    .bottom-left, .bottom-center, .bottom-right {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .control-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 18px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 700;
      background: #f4f7f4;
      border: 1px solid #e2e8e2;
      color: var(--text-dark);
      cursor: pointer;
      transition: all 0.18s ease;
      font-family: inherit;
    }

    .control-btn:hover {
      background: #e7ede7;
      transform: translateY(-1px);
    }

    .control-btn svg {
      width: 16px;
      height: 16px;
      stroke: currentColor;
    }

    .control-btn.active-control {
      background: var(--dock-dark);
      border-color: var(--dock-dark);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
    }

    .control-btn.active-control svg {
      stroke: var(--highlight-lime);
    }

    .control-btn.muted-control {
      background: var(--danger-bg);
      border-color: var(--danger-border);
      color: #dc2626;
    }

    .control-btn.muted-control svg {
      stroke: #dc2626;
    }

    .mini-meter-wrap {
      display: flex;
      align-items: center;
      gap: 3px;
      height: 22px;
      padding: 0 8px;
      background: #f4f7f4;
      border: 1px solid #e2e8e2;
      border-radius: 9999px;
    }

    .mini-meter-bar {
      width: 3px;
      height: 6px;
      background: #cbd5e1;
      border-radius: 2px;
      transition: height 0.1s ease, background-color 0.1s ease;
    }

    .mini-meter-bar.active {
      background: var(--dock-dark);
    }

    .end-meeting-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 22px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 800;
      background: var(--danger);
      border: none;
      color: #ffffff;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35);
      transition: all 0.18s ease;
      font-family: inherit;
    }

    .end-meeting-btn:hover {
      background: var(--danger-hover);
      transform: translateY(-1px);
      box-shadow: 0 6px 18px rgba(239, 68, 68, 0.45);
    }

    .end-meeting-btn svg {
      width: 16px;
      height: 16px;
      stroke: #ffffff;
    }

    /* ── Modals & Dialogs ─────────────────────────────────────────────── */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(24, 25, 27, 0.45);
      backdrop-filter: blur(8px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }

    .modal-overlay.open {
      display: flex;
    }

    .modal-box {
      background: #ffffff;
      border: 1px solid var(--card-border);
      border-radius: 26px;
      padding: 32px;
      width: 90%;
      max-width: 480px;
      box-shadow: 0 25px 70px rgba(0, 0, 0, 0.18);
      position: relative;
      animation: modalPop 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes modalPop {
      0% { transform: scale(0.95); opacity: 0; }
      100% { transform: scale(1); opacity: 1; }
    }

    .modal-header-icon {
      width: 54px;
      height: 54px;
      border-radius: 18px;
      background: #f4f7f4;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text-dark);
      margin-bottom: 18px;
    }

    .modal-header-icon svg {
      width: 24px;
      height: 24px;
      stroke: currentColor;
    }

    .modal-header-icon.red {
      background: var(--danger-bg);
      color: var(--danger);
    }

    .modal-header-icon.cyan, .modal-header-icon.purple {
      background: #f4f7f4;
      color: var(--text-dark);
    }

    .modal-title {
      font-size: 20px;
      font-weight: 800;
      color: var(--text-dark);
      margin-bottom: 8px;
      letter-spacing: -0.02em;
    }

    .modal-desc {
      font-size: 13.5px;
      color: var(--text-secondary);
      line-height: 1.55;
      margin-bottom: 22px;
    }

    .modal-input-group {
      margin-bottom: 22px;
    }

    .modal-label {
      display: block;
      font-size: 12px;
      font-weight: 700;
      color: var(--text-dark);
      margin-bottom: 6px;
    }

    .modal-input {
      width: 100%;
      padding: 12px 16px;
      border-radius: 14px;
      background: var(--card-bg);
      border: 1px solid #cbd5e1;
      font-size: 14px;
      font-family: inherit;
      color: var(--text-dark);
      outline: none;
      transition: all 0.18s ease;
    }

    .modal-input:focus {
      border-color: var(--dock-dark);
      background: #ffffff;
      box-shadow: 0 0 0 3px rgba(24, 25, 27, 0.08);
    }

    .consent-bullet-box {
      background: #f8faf8;
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 14px 16px;
      margin-bottom: 22px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .consent-bullet {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      font-size: 12.5px;
      color: #334155;
      line-height: 1.45;
    }

    .consent-bullet svg {
      width: 16px;
      height: 16px;
      stroke: #10b981;
      flex-shrink: 0;
      margin-top: 1px;
    }

    .modal-btn-row {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      gap: 10px;
    }

    .modal-btn {
      padding: 11px 22px;
      border-radius: 9999px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.18s ease;
      font-family: inherit;
    }

    .modal-btn svg {
      stroke: currentColor;
    }

    .modal-btn-secondary {
      background: #f4f7f4;
      border: 1px solid #e2e8e2;
      color: var(--text-dark);
    }

    .modal-btn-secondary:hover {
      background: #e7ede7;
    }

    .modal-btn-primary {
      background: var(--dock-dark);
      border: 1px solid var(--dock-dark);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
    }

    .modal-btn-primary:hover {
      background: #000000;
      border-color: #000000;
    }

    .modal-btn-danger {
      background: var(--danger);
      border: 1px solid var(--danger);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35);
    }

    .modal-btn-danger:hover {
      background: var(--danger-hover);
    }

    .modal-close-btn {
      position: absolute;
      top: 20px;
      right: 20px;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: #f4f7f4;
      border: none;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.18s ease;
    }

    .modal-close-btn:hover {
      background: var(--dock-dark);
      color: #ffffff;
    }

    .modal-close-btn svg {
      width: 14px;
      height: 14px;
      stroke: currentColor;
    }

    .copy-url-container {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 20px;
    }

    .copy-url-input {
      flex: 1;
      padding: 10px 14px;
      border-radius: 12px;
      background: #f8faf8;
      border: 1px solid #cbd5e1;
      font-size: 12px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      color: var(--text-dark);
      outline: none;
    }

    .copy-action-btn {
      padding: 10px 18px;
      border-radius: 12px;
      background: var(--dock-dark);
      color: #ffffff;
      border: none;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.18s ease;
      font-family: inherit;
    }

    .copy-action-btn:hover {
      background: #000000;
    }

    .copy-action-btn svg {
      stroke: var(--highlight-lime);
    }

    /* ── Ending Processing Overlay ────────────────────────────────────── */
    .ending-overlay {
      position: fixed;
      inset: 0;
      background: rgba(255, 255, 255, 0.94);
      backdrop-filter: blur(12px);
      display: none;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      z-index: 2000;
      padding: 24px;
    }

    .ending-overlay.active {
      display: flex;
    }

    .spinner-disc {
      width: 56px;
      height: 56px;
      border-radius: 50%;
      border: 4px solid var(--card-border);
      border-top-color: var(--dock-dark);
      border-right-color: var(--highlight-lime);
      animation: spinRing 0.9s linear infinite;
      margin-bottom: 22px;
    }

    @keyframes spinRing {
      to { transform: rotate(360deg); }
    }

    .ending-title {
      font-size: 22px;
      font-weight: 800;
      color: var(--text-dark);
      margin-bottom: 8px;
      letter-spacing: -0.02em;
    }

    .ending-subtitle {
      font-size: 14px;
      color: var(--text-secondary);
      max-width: 440px;
      line-height: 1.55;
    }

    /* ── Toast Notifications ─────────────────────────────────────────── */
    .toast-container {
      position: fixed;
      bottom: 24px;
      right: 24px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      z-index: 3000;
      pointer-events: none;
    }

    .toast {
      pointer-events: auto;
      background: #ffffff;
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 12px 18px;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-dark);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
      display: flex;
      align-items: center;
      gap: 10px;
      animation: toastSlideIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes toastSlideIn {
      0% { transform: translateY(16px); opacity: 0; }
      100% { transform: translateY(0); opacity: 1; }
    }

    .toast.success {
      border-left: 4px solid #10b981;
    }

    .toast.success svg {
      stroke: #10b981;
    }

    .toast.danger {
      border-left: 4px solid var(--danger);
    }

    .toast.danger svg {
      stroke: var(--danger);
    }

    .toast.info {
      border-left: 4px solid var(--dock-dark);
    }

    .toast.info svg {
      stroke: var(--dock-dark);
    }

    /* ── Custom Scrollbar ─────────────────────────────────────────────── */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }

    ::-webkit-scrollbar-track {
      background: transparent;
    }

    ::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
      background: #94a3b8;
    }

    /* ── Responsive adjustments ───────────────────────────────────────── */
    @media (max-width: 1024px) {
      .main-workspace {
        grid-template-columns: 1fr;
        grid-template-rows: 1fr 1fr;
      }
      header.top-bar {
        padding: 0 16px;
      }
      footer.bottom-bar {
        padding: 0 16px;
      }
    }
"""

print(f"Generated CSS size: {len(NEW_CSS)} characters")
