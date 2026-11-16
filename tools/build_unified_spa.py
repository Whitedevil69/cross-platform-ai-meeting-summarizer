# tools/build_unified_spa.py
import re
import sys

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# ══════════════════════════════════════════════════════════════════════
# 1. UPGRADE POPOVER HTML (#wpMoreAppsPopover)
# ══════════════════════════════════════════════════════════════════════
new_popover_html = """  <!-- ⚡ Syncra Workplace "More Apps" Floating Popover Tray (Matching Dribbble Reference) -->
  <div class="wp-more-popover" id="wpMoreAppsPopover" style="display: none;" onclick="event.stopPropagation()">
    <div class="wp-more-popover-header">
      <div class="wp-more-popover-title">
        <span>⚡</span> Workplace Suite
      </div>
      <span class="wp-more-popover-count">11 Tools</span>
    </div>

    <div class="wp-apps-grid">
      <!-- 1. Mail -->
      <div class="wp-app-tile" onclick="openMoreApp('Mail')" title="Executive Meeting Digest &amp; Dispatcher">
        <div class="wp-app-tile-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect width="20" height="15" x="2" y="4" rx="2"></rect>
            <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
          </svg>
        </div>
        <span>Mail</span>
      </div>

      <!-- 2. Calendar -->
      <div class="wp-app-tile" onclick="openMoreApp('Calendar')" title="Schedule &amp; Upcoming Meetings">
        <div class="wp-app-tile-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect width="18" height="18" x="3" y="4" rx="3"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
        </div>
        <span>Calendar</span>
      </div>

      <!-- 3. Scheduler -->
      <div class="wp-app-tile" onclick="openMoreApp('Scheduler')" title="1-Click Instant Room Booker">
        <div class="wp-app-tile-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M8 2v4M16 2v4M3 10h18M5 4h14a2 2 0 0 1 2 2v5"></path>
            <circle cx="16" cy="16" r="5"></circle>
            <polyline points="16 13.5 16 16 18 17.5"></polyline>
            <path d="M3 10v10a2 2 0 0 0 2 2h6"></path>
          </svg>
        </div>
        <span>Scheduler</span>
      </div>

      <!-- 4. Surveys -->
      <div class="wp-app-tile" onclick="openMoreApp('Surveys')" title="Real-Time Consensus Polling">
        <div class="wp-app-tile-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="9" y1="6" x2="20" y2="6"></line>
            <line x1="9" y1="12" x2="16" y2="12"></line>
            <line x1="9" y1="18" x2="19" y2="18"></line>
            <circle cx="4.5" cy="6" r="1.5"></circle>
            <circle cx="4.5" cy="12" r="1.5"></circle>
            <circle cx="4.5" cy="18" r="1.5"></circle>
          </svg>
        </div>
        <span>Surveys</span>
      </div>

      <!-- 5. Apps -->
      <div class="wp-app-tile" onclick="openMoreApp('Apps')" title="Ecosystem Connectors &amp; Integrations">
        <div class="wp-app-tile-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M9 12a4 4 0 1 0-4-4"></path>
            <path d="M15 12a4 4 0 1 0 4 4"></path>
            <circle cx="6" cy="6" r="1.2"></circle>
            <circle cx="18" cy="18" r="1.2"></circle>
          </svg>
        </div>
        <span>Apps</span>
      </div>

      <!-- 6. Workspaces -->
      <div class="wp-app-tile" onclick="openMoreApp('Workspaces')" title="Multi-Project Department Switcher">
        <div class="wp-app-tile-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect width="6" height="6" x="3" y="3" rx="1.5"></rect>
            <rect width="6" height="6" x="15" y="3" rx="1.5"></rect>
            <rect width="6" height="6" x="3" y="15" rx="1.5"></rect>
            <rect width="6" height="6" x="15" y="15" rx="1.5"></rect>
            <path d="m13 14 3 3-1 1 2 2.5-1 1-2-2.5-1 1z"></path>
          </svg>
        </div>
        <span>Workspaces</span>
      </div>

      <!-- 7. Contacts -->
      <div class="wp-app-tile" onclick="openMoreApp('Contacts')" title="Team Directory &amp; Stakeholders">
        <div class="wp-app-tile-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect width="18" height="20" x="3" y="2" rx="3.5"></rect>
            <circle cx="12" cy="8.5" r="2.8"></circle>
            <path d="M7 17a5 5 0 0 1 10 0"></path>
          </svg>
        </div>
        <span>Contacts</span>
      </div>

      <!-- 8. Events -->
      <div class="wp-app-tile" onclick="openMoreApp('Events')" title="Townhalls &amp; Webinars">
        <div class="wp-app-tile-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M2 9a3 3 0 0 1 0 6v3a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-3a3 3 0 0 1 0-6V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2z"></path>
            <polygon points="12 8 13.2 10.5 16 10.9 14 12.8 14.5 15.5 12 14.2 9.5 15.5 10 12.8 8 10.9 10.8 10.5 12 8"></polygon>
          </svg>
        </div>
        <span>Events</span>
      </div>

      <!-- 9. Revenue Accelerator -->
      <div class="wp-app-tile" onclick="openMoreApp('Revenue Accelerator')" title="Conversational Deal Intelligence">
        <div class="wp-app-tile-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 3a9 9 0 0 0-9 9c0 3.8 2.4 7.1 5.9 8.3M21 12a9 9 0 0 0-2.5-6.4"></path>
            <circle cx="12" cy="12" r="2"></circle>
            <line x1="12" y1="12" x2="16.5" y2="7.5"></line>
          </svg>
        </div>
        <span>Revenue</span>
      </div>

      <!-- 10. Contact Center -->
      <div class="wp-app-tile" onclick="openMoreApp('Contact Center')" title="AI QA &amp; Supervisor Desk">
        <div class="wp-app-tile-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M4 11a8 8 0 0 1 16 0v4a3 3 0 0 1-3 3h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h2v-0.5a6 6 0 0 0-12 0V11h2a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5"></path>
            <path d="M10 19a2 2 0 0 0 2 2h1"></path>
          </svg>
        </div>
        <span>Contact</span>
      </div>

      <!-- 11. Workvivo -->
      <div class="wp-app-tile" onclick="openMoreApp('Workvivo')" title="Company Social Feed &amp; Recognition">
        <div class="wp-app-tile-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect width="18" height="18" x="3" y="3" rx="4.5"></rect>
            <path d="M8 8.5l1.8 7 1.7-5 1.7 5 1.8-7"></path>
          </svg>
        </div>
        <span>Workvivo</span>
      </div>
    </div>

    <div class="wp-more-popover-footer" onclick="openAppSuiteModal('Apps')">
      <span>Browse All Connectors &amp; Apps ↗</span>
    </div>
  </div>"""

popover_pattern = re.compile(r'<div class="wp-more-popover" id="wpMoreAppsPopover".*?</div>\s*</div>(?=\s*<div class="wp-modal-overlay")', re.DOTALL)
if popover_pattern.search(text):
    text = popover_pattern.sub(new_popover_html, text, count=1)
    print("[OK] Replaced Popover HTML")
else:
    print("[WARN] Could not match Popover HTML")


# ══════════════════════════════════════════════════════════════════════
# 2. EXTRACT CURRENT HOME LEFT & RIGHT COLUMNS
# ══════════════════════════════════════════════════════════════════════
left_start = text.find('<div class="ref-left-col">')
right_start = text.find('<div class="ref-right-col">')
right_end = text.find('</div>\n        </div>\n      </div>\n\n      <!-- ════════════════════════════════════════════════════════════════')

if left_start == -1 or right_start == -1:
    print("[ERROR] Could not find left/right start")
    sys.exit(1)

# Extract inner left col (remove opening tag and closing </div>)
home_left_raw = text[left_start + len('<div class="ref-left-col">'):right_start].strip()
if home_left_raw.endswith('</div>'):
    home_left_raw = home_left_raw[:-6].strip()

# Extract persistent right column (inclusive of its opening <div class="ref-right-col"> and ending </div>)
# Notice right_end points to </div>\n        </div>\n      </div>
# The inner </div> terminates ref-right-col!
right_slice = text[right_start:text.find('<div class="wp-tab-view" id="view-chat"')]
# Find the exact end of ref-right-col
rc_closing_match = re.search(r'(<div class="ref-right-col">.*?</div>\s*</div>\s*</div>)', right_slice, re.DOTALL)
# Actually let's locate the exact end of ref-right-col:
# In check_rc, we saw:
# <div class="ref-vertical-link-card" style="background:#f4f7f4;border-color:#dce5dc;margin-top:6px;">...<div id="wpLiveResponse" ...></div></div></div>
rc_end_pos = right_slice.find('<div id="wpLiveResponse"')
rc_end_div = right_slice.find('</div>\n          </div>', rc_end_pos) + len('</div>\n          </div>')
persistent_right_col = right_slice[:rc_end_div].strip()
print(f"[OK] Extracted home left ({len(home_left_raw)} chars) and persistent right col ({len(persistent_right_col)} chars)")


# ══════════════════════════════════════════════════════════════════════
# 3. BUILD ALL 5 SIDEBAR VIEWS WITH HOMEPAGE TEMPLATE
# ══════════════════════════════════════════════════════════════════════

# ── View 2: Live Chat Hub ──
chat_view_html = """          <!-- ═════════ 2. CHAT TAB ═════════ -->
          <div class="wp-tab-view" id="view-chat" style="display:none;width:100%;">
            <!-- Top 3 Cards Row (Matching Homepage Reference) -->
            <div class="ref-three-cards-row">
              <!-- Card 1: Channels Metric Card -->
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag">
                      <span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">💬</span>
                      Live Channels
                    </span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">
                    3 <span class="ref-pill-percent">100% Online</span>
                  </div>
                  <div class="ref-metric-sub">/ 12 Team Members Active</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>

              <!-- Card 2: Lime Highlight Card -->
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag">
                      <span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">🌐</span>
                      AI Translation
                    </span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">
                    Hindi + En <span class="ref-pill-percent">Real-Time ↗</span>
                  </div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">Faster-Whisper CUDA Diarized</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>

              <!-- Card 3: Dark Feature Hero Card -->
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">
                    Syncra AI<br>Chat Assistant<br>Live Stream ↗
                  </div>
                  <div class="ref-dark-hero-sub">Summarize conversations in 1-click</div>
                  <div class="ref-dark-hero-avatar">💬</div>
                </div>
                <button type="button" onclick="askCompanion('Summarize all recent chat messages and key discussions')" class="ref-btn-upgrade" style="cursor:pointer;border:none;">
                  <span>AI Summarize ▷</span>
                </button>
              </div>
            </div>

            <!-- Main Interactive Chat Card -->
            <div class="chat-layout" style="margin-top:20px;">
              <div class="chat-sidebar">
                <div style="font-size:0.75rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;margin-bottom:6px;letter-spacing:0.04em;">Channels</div>
                <div class="chat-channel-item active" onclick="switchChatChannel('live')">
                  <span>💬</span>
                  <div>
                    <div style="font-weight:700;">Active Session Chat</div>
                    <div style="font-size:11px;opacity:0.75;">Syncra Live Intelligence</div>
                  </div>
                </div>
                <div class="chat-channel-item" onclick="switchChatChannel('architecture')">
                  <span>⚡</span>
                  <div>
                    <div style="font-weight:700;">Architecture Review</div>
                    <div style="font-size:11px;opacity:0.75;">Decisions &amp; Deadlines</div>
                  </div>
                </div>
                <div class="chat-channel-item" onclick="switchChatChannel('cross_platform')">
                  <span>🤖</span>
                  <div>
                    <div style="font-weight:700;">AI Bot Stream</div>
                    <div style="font-size:11px;opacity:0.75;">Zoom/Meet/Teams Sync</div>
                  </div>
                </div>
              </div>

              <div class="chat-main-area">
                <div class="chat-header-bar">
                  <div style="display:flex;align-items:center;gap:10px;">
                    <span>💬</span>
                    <span id="currentChatChannelName">Active Session Chat</span>
                    <span style="font-size:11px;padding:3px 9px;border-radius:9999px;background:#eafaf1;color:#107e4a;font-weight:700;">● Connected</span>
                  </div>
                  <button type="button" onclick="askCompanion('Summarize this meeting chat')" class="app-btn-primary" style="padding:6px 14px;font-size:0.78rem;">
                    ✨ AI Summarize
                  </button>
                </div>

                <div class="chat-messages-scroll" id="chatMessagesScroll">
                  <div class="chat-msg">
                    <div class="chat-msg-avatar">AI</div>
                    <div class="chat-msg-bubble">
                      <strong>Syncra Bot:</strong> Welcome to the meeting chat stream! All speech segments from Hindi and English are live-streamed with timestamp citations.
                    </div>
                  </div>
                  <div class="chat-msg">
                    <div class="chat-msg-avatar" style="background:#18191b;">G</div>
                    <div class="chat-msg-bubble">
                      <strong>Gaurav [00:12]:</strong> Hum sprint release ko Friday tak finalize karenge. Architecture review report ready hai.
                      <div style="font-size:11px;color:#059669;margin-top:4px;font-weight:600;">[En Translation]: We will finalize the sprint release by Friday. Architecture review report is ready.</div>
                    </div>
                  </div>
                  <div class="chat-msg">
                    <div class="chat-msg-avatar" style="background:#2b2d31;">R</div>
                    <div class="chat-msg-bubble">
                      <strong>Rahul [00:28]:</strong> I will deploy the Kubernetes clusters and verify the database failovers before Thursday 5 PM.
                    </div>
                  </div>
                </div>

                <form class="chat-input-bar" onsubmit="sendChatMessage(event)">
                  <input type="text" id="chatInputText" class="ref-search-input" placeholder="Type a message or note to team…" autocomplete="off">
                  <button type="submit" class="app-btn-primary" style="padding:8px 22px;">Send</button>
                </form>
              </div>
            </div>
          </div>"""


# ── View 3: Voice Phone Hub ──
phone_view_html = """          <!-- ═════════ 3. PHONE TAB ═════════ -->
          <div class="wp-tab-view" id="view-phone" style="display:none;width:100%;">
            <!-- Top 3 Cards Row (Matching Homepage Reference) -->
            <div class="ref-three-cards-row">
              <!-- Card 1: Metric Card -->
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag">
                      <span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">📞</span>
                      Telephony Gateway
                    </span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">
                    SIP Trunk <span class="ref-pill-percent">Active ↗</span>
                  </div>
                  <div class="ref-metric-sub">WebRTC 24kHz HD Audio Inbound</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>

              <!-- Card 2: Lime Highlight Card -->
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag">
                      <span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">🔊</span>
                      Audio Fidelity
                    </span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">
                    4.8 <span class="ref-pill-percent">MOS Score</span>
                  </div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">0% Packet Loss / Opus Codec</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>

              <!-- Card 3: Dark Feature Hero Card -->
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">
                    Instant Voice<br>Conference<br>Room ↗
                  </div>
                  <div class="ref-dark-hero-sub">Direct audio-only WebRTC bridge</div>
                  <div class="ref-dark-hero-avatar">🎙️</div>
                </div>
                <a href="/app/room.html?audio_only=true" target="_blank" class="ref-btn-upgrade">
                  <span>Voice Room ▷</span>
                </a>
              </div>
            </div>

            <!-- Main Interactive Phone Layout Card -->
            <div class="phone-container" style="margin-top:20px;">
              <!-- Left: Dialpad -->
              <div class="dialpad-card">
                <div style="font-size:0.8rem;color:var(--text-muted);margin-bottom:8px;align-self:flex-start;font-weight:700;text-transform:uppercase;letter-spacing:0.04em;">Keypad DTMF</div>
                <div class="dialpad-screen" id="dialScreen"></div>

                <div class="dialpad-grid">
                  <button class="dial-btn" onclick="pressDial('1', 697, 1209)"><span class="dial-num">1</span><span class="dial-sub"></span></button>
                  <button class="dial-btn" onclick="pressDial('2', 697, 1336)"><span class="dial-num">2</span><span class="dial-sub">ABC</span></button>
                  <button class="dial-btn" onclick="pressDial('3', 697, 1477)"><span class="dial-num">3</span><span class="dial-sub">DEF</span></button>
                  <button class="dial-btn" onclick="pressDial('4', 770, 1209)"><span class="dial-num">4</span><span class="dial-sub">GHI</span></button>
                  <button class="dial-btn" onclick="pressDial('5', 770, 1336)"><span class="dial-num">5</span><span class="dial-sub">JKL</span></button>
                  <button class="dial-btn" onclick="pressDial('6', 770, 1477)"><span class="dial-num">6</span><span class="dial-sub">MNO</span></button>
                  <button class="dial-btn" onclick="pressDial('7', 852, 1209)"><span class="dial-num">7</span><span class="dial-sub">PQRS</span></button>
                  <button class="dial-btn" onclick="pressDial('8', 852, 1336)"><span class="dial-num">8</span><span class="dial-sub">TUV</span></button>
                  <button class="dial-btn" onclick="pressDial('9', 852, 1477)"><span class="dial-num">9</span><span class="dial-sub">WXYZ</span></button>
                  <button class="dial-btn" onclick="pressDial('*', 941, 1209)"><span class="dial-num">*</span><span class="dial-sub"></span></button>
                  <button class="dial-btn" onclick="pressDial('0', 941, 1336)"><span class="dial-num">0</span><span class="dial-sub">+</span></button>
                  <button class="dial-btn" onclick="pressDial('#', 941, 1477)"><span class="dial-num">#</span><span class="dial-sub"></span></button>
                </div>

                <div class="dial-actions-row">
                  <button type="button" class="dial-call-btn" onclick="startPhoneCall()">
                    <span>📞</span> Call Room
                  </button>
                  <button type="button" class="dial-del-btn" onclick="clearDial()" title="Backspace">⌫</button>
                </div>
              </div>

              <!-- Right: Telephony Status & Recent Voice Calls Desk -->
              <div style="display:flex;flex-direction:column;gap:16px;">
                <div class="ref-card-metric" style="min-height:auto;padding:20px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <div style="font-weight:700;font-size:0.95rem;color:var(--text-dark);">SIP Audio Inbound Gateway</div>
                    <span class="app-badge-status app-badge-green">● Connected</span>
                  </div>
                  <div style="font-size:0.82rem;color:var(--text-secondary);line-height:1.5;">
                    Live SIP trunk mapped directly to Faster-Whisper CUDA engine. High-definition 24kHz stream is recorded with instant evidence grounding.
                  </div>
                </div>

                <div class="ref-card-metric" style="min-height:auto;padding:20px;">
                  <div style="font-weight:700;font-size:0.9rem;color:var(--text-dark);margin-bottom:12px;">Recent Voice Room Calls</div>
                  <table class="rm-table">
                    <thead>
                      <tr>
                        <th>Room / Caller</th>
                        <th>Duration</th>
                        <th>Status</th>
                        <th style="text-align:right;">Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td style="font-weight:600;color:var(--text-dark);">Room #73eb-prod</td>
                        <td style="font-family:var(--font-mono);font-size:0.75rem;">18m 42s</td>
                        <td><span class="app-badge-status app-badge-green">Transcribed</span></td>
                        <td style="text-align:right;"><button type="button" class="app-btn-secondary" style="padding:4px 10px;font-size:0.72rem;" onclick="pressDial('73eb', 697, 1209)">Redial</button></td>
                      </tr>
                      <tr>
                        <td style="font-weight:600;color:var(--text-dark);">Room #arch-sprint</td>
                        <td style="font-family:var(--font-mono);font-size:0.75rem;">34m 10s</td>
                        <td><span class="app-badge-status app-badge-green">Transcribed</span></td>
                        <td style="text-align:right;"><button type="button" class="app-btn-secondary" style="padding:4px 10px;font-size:0.72rem;" onclick="pressDial('arch', 697, 1209)">Redial</button></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>"""


# ── View 4: Docs & Reports Hub ──
docs_view_html = """          <!-- ═════════ 4. DOCS TAB ═════════ -->
          <div class="wp-tab-view" id="view-docs" style="display:none;width:100%;">
            <!-- Top 3 Cards Row (Matching Homepage Reference) -->
            <div class="ref-three-cards-row">
              <!-- Card 1: Metric Card -->
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag">
                      <span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">📑</span>
                      Briefings Generated
                    </span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">
                    14 <span class="ref-pill-percent">Indexed ↗</span>
                  </div>
                  <div class="ref-metric-sub">Executive Markdown Briefings</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>

              <!-- Card 2: Lime Highlight Card -->
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag">
                      <span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">🎯</span>
                      Evidence Grounding
                    </span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">
                    100% <span class="ref-pill-percent">Verified</span>
                  </div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">Audio Timestamps &amp; Speaker Citations</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>

              <!-- Card 3: Dark Feature Hero Card -->
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">
                    Export All<br>Meeting Records<br>in Markdown ↗
                  </div>
                  <div class="ref-dark-hero-sub">Download formatted AI briefings</div>
                  <div class="ref-dark-hero-avatar">📄</div>
                </div>
                <button type="button" onclick="exportCurrentDoc('md')" class="ref-btn-upgrade" style="cursor:pointer;border:none;">
                  <span>Export .md ▷</span>
                </button>
              </div>
            </div>

            <!-- Main Interactive Docs Card -->
            <div class="doc-card" style="margin-top:20px;">
              <div class="doc-header-row">
                <div>
                  <div class="doc-title" id="docViewerTitle">Sprint Diarization &amp; Pipeline Architecture Review</div>
                  <div class="doc-meta" id="docViewerMeta">Meeting ID: 73ebc603 • Source: Multi-Party LiveKit WebRTC</div>
                </div>
                <div style="display:flex;gap:8px;">
                  <button type="button" onclick="exportCurrentDoc('md')" class="app-btn-primary" style="padding:7px 16px;font-size:0.78rem;">
                    📄 Export Markdown
                  </button>
                  <button type="button" onclick="exportCurrentDoc('json')" class="app-btn-secondary" style="padding:7px 16px;font-size:0.78rem;">
                    { } Export JSON
                  </button>
                </div>
              </div>

              <div class="doc-section-title">Executive Summary</div>
              <p class="doc-summary-text" id="docExecutiveSummary">
                The engineering team conducted a comprehensive architecture review of the cross-platform meeting summarization pipeline. Core discussion focused on migrating the Whisper transcription and diarization topology from on-premise infrastructure to Kubernetes clusters, validating speech segment grounding, and verifying SQLite audio timestamps.
              </p>

              <div class="doc-section-title">Decisions &amp; Action Items</div>
              <table class="doc-items-table">
                <thead>
                  <tr>
                    <th>Type</th>
                    <th>Description</th>
                    <th>Owner</th>
                    <th>Deadline</th>
                    <th>Citation</th>
                  </tr>
                </thead>
                <tbody id="docItemsTableBody">
                  <tr>
                    <td><span class="app-badge-status app-badge-purple">DECISION</span></td>
                    <td style="font-weight:600;">Migrate microservices to production Kubernetes clusters before sprint freeze.</td>
                    <td>Team Lead</td>
                    <td>Friday</td>
                    <td><span style="color:#059669;font-family:var(--font-mono);font-weight:600;">Segment #12</span></td>
                  </tr>
                  <tr>
                    <td><span class="app-badge-status" style="background:#18191b;color:#fff;">ACTION</span></td>
                    <td style="font-weight:600;">Execute database failover validation test scripts.</td>
                    <td>Rahul</td>
                    <td>Friday 5 PM</td>
                    <td><span style="color:#059669;font-family:var(--font-mono);font-weight:600;">Segment #15</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>"""


# ── View 5: Whiteboards D3 Studio ──
whiteboards_view_html = """          <!-- ═════════ 5. WHITEBOARDS TAB ═════════ -->
          <div class="wp-tab-view" id="view-whiteboards" style="display:none;width:100%;">
            <!-- Top 3 Cards Row (Matching Homepage Reference) -->
            <div class="ref-three-cards-row">
              <!-- Card 1: Metric Card -->
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag">
                      <span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">🕸️</span>
                      Graph Nodes
                    </span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">
                    28 <span class="ref-pill-percent">Active ↗</span>
                  </div>
                  <div class="ref-metric-sub">Connected Decisions &amp; Owners</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>

              <!-- Card 2: Lime Highlight Card -->
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag">
                      <span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">⚡</span>
                      Graph Resolution
                    </span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">
                    0 Blocked <span class="ref-pill-percent">Optimal</span>
                  </div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">Critical Architecture Path Resolved</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>

              <!-- Card 3: Dark Feature Hero Card -->
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">
                    Interactive D3<br>Force Simulation<br>Graph Studio ↗
                  </div>
                  <div class="ref-dark-hero-sub">Drag, zoom, and inspect dependencies</div>
                  <div class="ref-dark-hero-avatar">🎨</div>
                </div>
                <button type="button" onclick="loadWhiteboardsView()" class="ref-btn-upgrade" style="cursor:pointer;border:none;">
                  <span>Reset Graph ▷</span>
                </button>
              </div>
            </div>

            <!-- Main Interactive Whiteboard Card -->
            <div class="whiteboard-container" style="margin-top:20px;">
              <div class="whiteboard-toolbar">
                <div style="display:flex;align-items:center;gap:12px;">
                  <span style="font-weight:800;color:var(--text-dark);font-size:0.95rem;">Decision Graph Whiteboard</span>
                  <span class="app-badge-status app-badge-purple">D3.js Force v7</span>
                </div>
                <div style="display:flex;gap:14px;align-items:center;font-size:0.75rem;font-weight:600;">
                  <span style="display:flex;align-items:center;gap:5px;"><span style="width:10px;height:10px;border-radius:50%;background:#e5f97e;border:1.5px solid #18191b;"></span> Decision</span>
                  <span style="display:flex;align-items:center;gap:5px;"><span style="width:10px;height:10px;border-radius:50%;background:#18191b;"></span> Action</span>
                  <span style="display:flex;align-items:center;gap:5px;"><span style="width:10px;height:10px;border-radius:50%;background:#059669;"></span> Topic</span>
                  <button type="button" onclick="loadWhiteboardsView()" class="app-btn-secondary" style="padding:4px 10px;font-size:0.72rem;">
                    ↻ Refresh
                  </button>
                </div>
              </div>
              <svg id="whiteboardSvg"></svg>
            </div>
          </div>"""


# ── View 6: Audio Clips Hub ──
clips_view_html = """          <!-- ═════════ 6. CLIPS TAB ═════════ -->
          <div class="wp-tab-view" id="view-clips" style="display:none;width:100%;">
            <!-- Top 3 Cards Row (Matching Homepage Reference) -->
            <div class="ref-three-cards-row">
              <!-- Card 1: Metric Card -->
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag">
                      <span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">🎙️</span>
                      Verbatim Evidence
                    </span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">
                    100% <span class="ref-pill-percent">Audio Grounded</span>
                  </div>
                  <div class="ref-metric-sub">Zero Hallucination Guarantee</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item solid-dark"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                  <div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>

              <!-- Card 2: Lime Highlight Card -->
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag">
                      <span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">🌐</span>
                      Diarization Engine
                    </span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">
                    En + Hi <span class="ref-pill-percent">Diarized</span>
                  </div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">Hindi-English Code-Switched Speech</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item solid-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                  <div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>

              <!-- Card 3: Dark Feature Hero Card -->
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">
                    High-Fidelity<br>Audio Evidence<br>Stream ↗
                  </div>
                  <div class="ref-dark-hero-sub">Instant playback of exact spoken citations</div>
                  <div class="ref-dark-hero-avatar">🎧</div>
                </div>
                <button type="button" onclick="playAudioClipDemo(1)" class="ref-btn-upgrade" style="cursor:pointer;border:none;">
                  <span>Play Clip ▷</span>
                </button>
              </div>
            </div>

            <!-- Main Clips Stream Card -->
            <div class="ref-card-metric" style="margin-top:20px;min-height:auto;padding:24px;">
              <div style="margin-bottom:16px;">
                <h2 style="font-size:1.25rem;font-weight:800;color:var(--text-dark);margin:0 0 4px;letter-spacing:-0.02em;">Evidence Audio Clips</h2>
                <p style="font-size:0.82rem;color:var(--text-secondary);margin:0;">Listen to the exact spoken sentences that back every decision claim with 100% precision.</p>
              </div>

              <div id="clipsFeedList" style="display:flex;flex-direction:column;gap:12px;">
                <!-- Clip 1 -->
                <div class="clip-card">
                  <button type="button" class="clip-play-btn" onclick="playAudioClipDemo(1)" title="Play Spoken Sentence">▶</button>
                  <div class="clip-info">
                    <div class="clip-quote">"Hum sprint release ko Friday tak finalize karenge. Architecture review report ready hai."</div>
                    <div class="clip-meta">Speaker: Gaurav • Time: 00:12 — 00:18 • Language: Hinglish • Citation: Decision #1</div>
                  </div>
                  <div class="clip-verified-badge">100% Verified Evidence</div>
                </div>

                <!-- Clip 2 -->
                <div class="clip-card">
                  <button type="button" class="clip-play-btn" onclick="playAudioClipDemo(2)" title="Play Spoken Sentence">▶</button>
                  <div class="clip-info">
                    <div class="clip-quote">"I will deploy the Kubernetes clusters and verify the database failovers before Thursday 5 PM."</div>
                    <div class="clip-meta">Speaker: Rahul • Time: 00:28 — 00:36 • Language: English • Citation: Action Item #2</div>
                  </div>
                  <div class="clip-verified-badge">100% Verified Evidence</div>
                </div>
              </div>
            </div>
          </div>"""


# ══════════════════════════════════════════════════════════════════════
# 4. ASSEMBLE NEW MAIN WORKSPACE STRUCTURE
# ══════════════════════════════════════════════════════════════════════
# In this structure:
# <main class="ref-main-container">
#   (header row)
#   (sub-header bar)
#   <div class="ref-dashboard-grid">
#     <div class="ref-left-col">
#       <div class="wp-tab-view" id="view-home">...home_left_raw...</div>
#       ...chat_view_html...
#       ...phone_view_html...
#       ...docs_view_html...
#       ...whiteboards_view_html...
#       ...clips_view_html...
#     </div>
#     (persistent_right_col)
#   </div>
# </main>

new_views_body = f"""      <!-- ══════════════════════════════════════════════════════════════════════ -->
      <!-- UNIFIED DASHBOARD GRID (Homepage Template across all Sidebar Options) -->
      <!-- ══════════════════════════════════════════════════════════════════════ -->
      <div class="ref-dashboard-grid">

        <!-- LEFT COLUMN: Hosts all active view components inside the same template -->
        <div class="ref-left-col">

          <!-- ═════════ 1. HOME TAB ═════════ -->
          <div class="wp-tab-view" id="view-home">
{home_left_raw}
          </div>

{chat_view_html}

{phone_view_html}

{docs_view_html}

{whiteboards_view_html}

{clips_view_html}

        </div>

        <!-- RIGHT COLUMN: Persistent Dribbble Companion Hub -->
        {persistent_right_col}
      </div>
    </main>"""

# Replace the region from <div class="wp-tab-view" id="view-home"> to </main>
old_views_region_start = text.find('<!-- ════════════════════════════════════════════════════════════════════ -->\n      <!-- VIEW 1: HOME DASHBOARD')
if old_views_region_start == -1:
    old_views_region_start = text.find('<div class="wp-tab-view" id="view-home">')

old_views_region_end = text.find('</main>') + len('</main>')

text = text[:old_views_region_start] + new_views_body + text[old_views_region_end:]
print("[OK] Replaced all Views HTML into the Unified Dashboard Grid structure")


# ══════════════════════════════════════════════════════════════════════
# 5. ENHANCE JAVASCRIPT: switchMainTab & D3 Whiteboard Node Colors
# ══════════════════════════════════════════════════════════════════════

# Update switchMainTab to dynamically update main title to match active option!
old_switch_tab = """    window.switchMainTab = function(tabKey) {
      // 1. Update left dock buttons
      document.querySelectorAll('.ref-dock-btn').forEach(btn => btn.classList.remove('active'));
      const activeDock = document.getElementById('dockNav-' + tabKey);
      if (activeDock) activeDock.classList.add('active');

      // 2. Update top horizontal capsule tabs
      document.querySelectorAll('.ref-tab-pill').forEach(btn => btn.classList.remove('active'));
      const activeTab = document.getElementById('navTab-' + tabKey);
      if (activeTab) activeTab.classList.add('active');

      // 3. Switch visible view
      const allViews = ['home', 'chat', 'phone', 'docs', 'whiteboards', 'clips'];
      allViews.forEach(v => {
        const viewEl = document.getElementById('view-' + v);
        if (viewEl) {
          viewEl.style.display = (v === tabKey) ? (v === 'home' ? 'block' : 'flex') : 'none';
        }
      });

      // 4. Trigger view-specific dynamic loaders
      if (tabKey === 'docs') loadDocsView();
      if (tabKey === 'chat') loadChatView();
      if (tabKey === 'whiteboards') loadWhiteboardsView();
      if (tabKey === 'clips') loadClipsView();
    };"""

new_switch_tab = """    window.switchMainTab = function(tabKey) {
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
        clips: { pre: 'Managing', badge: '🎙️', t1: 'Audio Evidence', sub: 'and', spark: '⚡', t2: 'Verbatim Quotes' }
      };
      const mainTitleEl = document.querySelector('.ref-main-title');
      if (mainTitleEl && viewTitles[tabKey]) {
        const vt = viewTitles[tabKey];
        mainTitleEl.innerHTML = `${vt.pre} <span class="ref-title-badge gear">${vt.badge}</span> ${vt.t1}<br>${vt.sub} <span class="ref-title-badge spark">${vt.spark}</span> ${vt.t2}`;
      }

      // 4. Switch visible view (all use display:block or display:flex inside ref-left-col)
      const allViews = ['home', 'chat', 'phone', 'docs', 'whiteboards', 'clips'];
      allViews.forEach(v => {
        const viewEl = document.getElementById('view-' + v);
        if (viewEl) {
          viewEl.style.display = (v === tabKey) ? 'flex' : 'none';
        }
      });

      // 5. Trigger view-specific dynamic loaders
      if (tabKey === 'docs') loadDocsView();
      if (tabKey === 'chat') loadChatView();
      if (tabKey === 'whiteboards') loadWhiteboardsView();
      if (tabKey === 'clips') loadClipsView();
    };"""

if old_switch_tab in text:
    text = text.replace(old_switch_tab, new_switch_tab)
    print("[OK] Enhanced switchMainTab in JavaScript")
else:
    print("[WARN] Could not find exact old_switch_tab string, trying regex")
    switch_regex = re.compile(r'window\.switchMainTab\s*=\s*function\(tabKey\)\s*\{.*?\};', re.DOTALL)
    if switch_regex.search(text):
        text = switch_regex.sub(new_switch_tab.strip(), text, count=1)
        print("[OK] Enhanced switchMainTab via regex")

# Enhance D3 Whiteboard Simulation colors to look stunning on the light background
# Line stroke, node colors, text colors
old_d3_link = ".attr('stroke', 'rgba(255,255,255,0.25)')"
new_d3_link = ".attr('stroke', '#cbd5e1')"
if old_d3_link in text:
    text = text.replace(old_d3_link, new_d3_link)

old_d3_text = ".attr('fill', '#ffffff')\n          .attr('font-size', '11px');"
new_d3_text = ".attr('fill', '#18191b')\n          .attr('font-size', '11px')\n          .attr('font-weight', '600');"
if old_d3_text in text:
    text = text.replace(old_d3_text, new_d3_text)

old_d3_node_fill = ".attr('fill', d => d.type === 'decision' ? '#10b981' : (d.type === 'action' ? '#38bdf8' : '#f59e0b'))\n          .attr('stroke', '#ffffff')"
new_d3_node_fill = ".attr('fill', d => d.type === 'decision' ? '#e5f97e' : (d.type === 'action' ? '#18191b' : '#059669'))\n          .attr('stroke', '#18191b')"
if old_d3_node_fill in text:
    text = text.replace(old_d3_node_fill, new_d3_node_fill)
    print("[OK] Updated D3 Whiteboard node & link colors for light canvas")


with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("[COMPLETE] Successfully rebuilt frontend/index.html with unified homepage template across all options!")
