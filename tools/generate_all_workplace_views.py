# tools/generate_all_workplace_views.py
import re
import sys

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# ══════════════════════════════════════════════════════════════════════
# HTML DEFINITIONS FOR ALL 11 WORKPLACE SUITE VIEWS (Dribbble Layout)
# ══════════════════════════════════════════════════════════════════════

mail_view = """          <!-- ═════════ 7. MAIL TAB ═════════ -->
          <div class="wp-tab-view" id="view-mail" style="display:none;width:100%;">
            <div class="ref-three-cards-row">
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">📬</span> Briefings Sent</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">42 <span class="ref-pill-percent">98% Delivery Rate</span></div>
                  <div class="ref-metric-sub">/ 100 Stakeholders Reached</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">🎯</span> Evidence Grounding</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">100% <span class="ref-pill-percent">Verified ↗</span></div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">Audio Citations Back Every Sentence</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">Dispatch Executive<br>AI Meeting Digest<br>to Stakeholders ↗</div>
                  <div class="ref-dark-hero-sub">Instant formatted briefing dispatch</div>
                  <div class="ref-dark-hero-avatar">📬</div>
                </div>
                <button type="button" onclick="sendMailBriefing()" class="ref-btn-upgrade" style="cursor:pointer;border:none;">
                  <span>Send Digest ▷</span>
                </button>
              </div>
            </div>

            <div class="doc-card" style="margin-top:20px;">
              <div style="display:grid;grid-template-columns:1fr 280px;gap:20px;">
                <div>
                  <div style="font-size:0.8rem;font-weight:700;color:#64748b;text-transform:uppercase;margin-bottom:12px;letter-spacing:0.04em;">Draft Executive Briefing</div>
                  <div style="margin-bottom:12px;">
                    <label style="font-size:0.75rem;font-weight:700;color:var(--text-dark);display:block;margin-bottom:4px;">Recipients (comma separated):</label>
                    <input type="text" id="mailRecipientsMain" class="ref-search-input" value="lead@syncra.internal, rahul.s@syncra.internal, priya.p@syncra.internal">
                  </div>
                  <div style="margin-bottom:12px;">
                    <label style="font-size:0.75rem;font-weight:700;color:var(--text-dark);display:block;margin-bottom:4px;">Subject Line:</label>
                    <input type="text" id="mailSubjectMain" class="ref-search-input" value="[Executive Summary] Sprint Diarization &amp; Pipeline Architecture — Syncra Workplace">
                  </div>
                  <div style="margin-bottom:14px;">
                    <label style="font-size:0.75rem;font-weight:700;color:var(--text-dark);display:block;margin-bottom:4px;">Generated Executive Digest &amp; Action Items:</label>
                    <textarea id="mailBodyMain" class="app-textarea" style="min-height:160px;">Team,

Here is the executive digest and action items from today's meeting:

🎯 KEY DECISIONS:
• [00:03:12] Adopt Faster-Whisper on CUDA with fallback to Ollama llama3 for local offline environments.
• [00:07:45] Recall.ai bot bridge approved for Zoom, Google Meet, and Microsoft Teams.
• [00:12:30] Real-time decision graph enabled with D3.js NetworkX visualization.

⚡ ACTION ITEMS &amp; ASSIGNEES:
• @Gaurav: Deploy LiveKit SFU WebRTC room with dual audio/video streams (Due: Nov 18)
• @Rahul: Configure Recall.ai webhook endpoint &amp; bot lifecycle daemon (Due: Nov 19)
• @Priya: Benchmark speaker diarization accuracy on Hindi-English code-switched audio (Due: Nov 20)

Evidence verification links and audio citations are archived in Syncra Workplace.</textarea>
                  </div>
                  <div style="display:flex;gap:10px;flex-wrap:wrap;">
                    <button type="button" class="app-btn-primary" onclick="sendMailBriefing()"><span>🚀</span> Send AI Digest</button>
                    <button type="button" class="app-btn-secondary" onclick="copyMailBriefing()"><span>📋</span> Copy to Clipboard</button>
                    <button type="button" class="app-btn-secondary" onclick="openDefaultMailClient()"><span>✉️</span> Open Mail Client</button>
                  </div>
                </div>
                <div>
                  <div class="ref-card-metric" style="min-height:auto;padding:18px;margin-bottom:14px;">
                    <div style="font-size:0.8rem;font-weight:700;color:var(--text-dark);margin-bottom:10px;">Recent Dispatches</div>
                    <div style="padding:8px 0;border-bottom:1px solid #edf0ed;">
                      <div style="font-size:0.8rem;font-weight:700;color:var(--text-dark);">[Digest] Sprint Diarization Architecture</div>
                      <div style="font-size:0.72rem;color:#64748b;margin-top:2px;">To: team-leadership@syncra.internal</div>
                      <div style="display:flex;justify-content:space-between;align-items:center;margin-top:4px;">
                        <span class="app-badge-status app-badge-green">Delivered (200 OK)</span>
                        <span style="font-size:0.7rem;color:#8b95a5;">Today 10:14 AM</span>
                      </div>
                    </div>
                  </div>
                  <div class="ref-card-metric" style="min-height:auto;padding:18px;background:#fbfcfb;">
                    <div style="font-size:0.8rem;font-weight:700;color:var(--text-dark);margin-bottom:4px;">💡 AI Evidence Citation</div>
                    <div style="font-size:0.75rem;color:#64748b;line-height:1.45;">Every claim in this briefing includes exact timestamps linking directly to audio evidence stored in the SQLite database.</div>
                  </div>
                </div>
              </div>
            </div>
          </div>"""

calendar_view = """          <!-- ═════════ 8. CALENDAR TAB ═════════ -->
          <div class="wp-tab-view" id="view-calendar" style="display:none;width:100%;">
            <div class="ref-three-cards-row">
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">📅</span> Scheduled Meetings</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">8 <span class="ref-pill-percent">Upcoming ↗</span></div>
                  <div class="ref-metric-sub">/ 4 Synchronized Today</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">⚡</span> Sync Telemetry</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">Google + Outlook <span class="ref-pill-percent">Live ↗</span></div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">Recall.ai Auto-Notetaker Attached</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">Sync Schedule with<br>Google &amp; Outlook<br>Calendar Feeds ↗</div>
                  <div class="ref-dark-hero-sub">Export standard .ics meeting format</div>
                  <div class="ref-dark-hero-avatar">📅</div>
                </div>
                <button type="button" onclick="exportIcsSchedule()" class="ref-btn-upgrade" style="cursor:pointer;border:none;">
                  <span>Export .ics ▷</span>
                </button>
              </div>
            </div>

            <div class="doc-card" style="margin-top:20px;">
              <div style="display:grid;grid-template-columns:1fr 300px;gap:20px;">
                <div>
                  <div style="font-weight:800;font-size:1.1rem;color:var(--text-dark);margin-bottom:12px;">November 2026</div>
                  <div class="cal-grid">
                    <div class="cal-day-header">SUN</div><div class="cal-day-header">MON</div><div class="cal-day-header">TUE</div><div class="cal-day-header">WED</div><div class="cal-day-header">THU</div><div class="cal-day-header">FRI</div><div class="cal-day-header">SAT</div>
                    <div class="cal-cell"><span class="cal-date-num">1</span></div><div class="cal-cell"><span class="cal-date-num">2</span></div><div class="cal-cell"><span class="cal-date-num">3</span></div><div class="cal-cell"><span class="cal-date-num">4</span></div><div class="cal-cell"><span class="cal-date-num">5</span></div><div class="cal-cell"><span class="cal-date-num">6</span></div><div class="cal-cell"><span class="cal-date-num">7</span></div>
                    <div class="cal-cell"><span class="cal-date-num">8</span></div><div class="cal-cell"><span class="cal-date-num">9</span></div><div class="cal-cell"><span class="cal-date-num">10</span></div><div class="cal-cell"><span class="cal-date-num">11</span></div><div class="cal-cell"><span class="cal-date-num">12</span></div><div class="cal-cell"><span class="cal-date-num">13</span></div><div class="cal-cell"><span class="cal-date-num">14</span></div>
                    <div class="cal-cell today active"><span class="cal-date-num">15</span><span class="cal-event-dot"></span></div><div class="cal-cell"><span class="cal-date-num">16</span><span class="cal-event-dot"></span></div><div class="cal-cell"><span class="cal-date-num">17</span></div><div class="cal-cell"><span class="cal-date-num">18</span><span class="cal-event-dot"></span></div><div class="cal-cell"><span class="cal-date-num">19</span></div><div class="cal-cell"><span class="cal-date-num">20</span><span class="cal-event-dot"></span></div><div class="cal-cell"><span class="cal-date-num">21</span></div>
                  </div>
                </div>
                <div>
                  <div style="font-weight:700;font-size:0.85rem;color:var(--text-dark);margin-bottom:12px;text-transform:uppercase;letter-spacing:0.04em;">Upcoming AI Sessions</div>
                  <div style="display:flex;flex-direction:column;gap:10px;">
                    <div class="ref-card-metric" style="min-height:auto;padding:14px;">
                      <div style="font-size:0.75rem;font-weight:700;color:#059669;font-family:var(--font-mono);">TODAY • 02:00 PM</div>
                      <div style="font-weight:700;font-size:0.85rem;color:var(--text-dark);margin:2px 0;">Architecture Review &amp; Whisper CUDA</div>
                      <div style="font-size:0.72rem;color:#64748b;margin-bottom:8px;">LiveKit SFU + Recall.ai bot enabled</div>
                      <a href="/app/room.html?room=arch-review" target="_blank" class="app-btn-primary" style="padding:4px 12px;font-size:0.74rem;">Join Meeting</a>
                    </div>
                    <div class="ref-card-metric" style="min-height:auto;padding:14px;">
                      <div style="font-size:0.75rem;font-weight:700;color:#059669;font-family:var(--font-mono);">WED, NOV 18 • 11:00 AM</div>
                      <div style="font-weight:700;font-size:0.85rem;color:var(--text-dark);margin:2px 0;">Q4 Cross-Platform Roadmap</div>
                      <div style="font-size:0.72rem;color:#64748b;margin-bottom:8px;">Bilingual speech translation active</div>
                      <a href="/app/room.html?room=q4-roadmap" target="_blank" class="app-btn-primary" style="padding:4px 12px;font-size:0.74rem;">Join Meeting</a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>"""

scheduler_view = """          <!-- ═════════ 9. SCHEDULER TAB ═════════ -->
          <div class="wp-tab-view" id="view-scheduler" style="display:none;width:100%;">
            <div class="ref-three-cards-row">
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">⚡</span> Instant Room Slots</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">1-Click <span class="ref-pill-percent">Pre-Attached</span></div>
                  <div class="ref-metric-sub">Ready to Dispatch with AI Notetaker</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">🤖</span> Bot Latency</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">180ms <span class="ref-pill-percent">CUDA Fast</span></div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">Zero Startup Lag on Room Join</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">Instant WebRTC<br>Video Conference<br>Launch Engine ↗</div>
                  <div class="ref-dark-hero-sub">Direct link with Recall.ai pre-attached</div>
                  <div class="ref-dark-hero-avatar">⚡</div>
                </div>
                <a href="/app/room.html" target="_blank" class="ref-btn-upgrade">
                  <span>Launch Room ▷</span>
                </a>
              </div>
            </div>

            <div class="doc-card" style="margin-top:20px;">
              <div style="max-width:680px;">
                <div style="font-weight:800;font-size:1.15rem;color:var(--text-dark);margin-bottom:6px;">Instant Meeting Booker</div>
                <div style="font-size:0.82rem;color:#64748b;margin-bottom:16px;">Generate instant room links pre-configured with autonomous recording, Faster-Whisper diarization, and evidence citations.</div>
                <div style="display:flex;gap:8px;margin-bottom:14px;">
                  <button type="button" class="app-btn-secondary" style="border-color:#18191b;color:#18191b;background:#e5f97e;font-weight:700;">15 min</button>
                  <button type="button" class="app-btn-secondary">30 min</button>
                  <button type="button" class="app-btn-secondary">45 min</button>
                  <button type="button" class="app-btn-secondary">60 min</button>
                </div>
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:18px;">
                  <input type="checkbox" id="schedBotToggleMain" checked style="width:18px;height:18px;accent-color:#18191b;">
                  <label for="schedBotToggleMain" style="font-size:0.82rem;font-weight:600;color:var(--text-dark);cursor:pointer;">Pre-attach Recall.ai AI Notetaker Bot to auto-transcribe &amp; ground decisions</label>
                </div>
                <div style="display:flex;gap:10px;">
                  <button type="button" class="app-btn-primary" onclick="window.location.href='/app/room.html'"><span>🚀</span> Start Instant Meeting</button>
                  <button type="button" class="app-btn-secondary" onclick="navigator.clipboard.writeText(window.location.origin + '/app/room.html');showToast('Room URL copied!','success')"><span>📋</span> Copy Shareable URL</button>
                </div>
              </div>
            </div>
          </div>"""

surveys_view = """          <!-- ═════════ 10. SURVEYS TAB ═════════ -->
          <div class="wp-tab-view" id="view-surveys" style="display:none;width:100%;">
            <div class="ref-three-cards-row">
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">📊</span> Active Polls</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">4 <span class="ref-pill-percent">Live Consensus</span></div>
                  <div class="ref-metric-sub">/ 38 Team Responses Registered</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">⚡</span> Consensus Accuracy</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">94% <span class="ref-pill-percent">Real-Time ↗</span></div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">Direct Vote Telemetry Stream</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">Create Live Team<br>Consensus Poll<br>and Surveys ↗</div>
                  <div class="ref-dark-hero-sub">Gather instant stakeholder alignment</div>
                  <div class="ref-dark-hero-avatar">📊</div>
                </div>
                <button type="button" onclick="showToast('Poll created and broadcasted!','success')" class="ref-btn-upgrade" style="cursor:pointer;border:none;">
                  <span>Create Poll ▷</span>
                </button>
              </div>
            </div>

            <div class="doc-card" style="margin-top:20px;">
              <div style="font-weight:800;font-size:1.15rem;color:var(--text-dark);margin-bottom:14px;">Active Team Consensus Polls</div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
                <div class="ref-card-metric" style="min-height:auto;padding:18px;">
                  <div style="font-weight:700;font-size:0.9rem;color:var(--text-dark);margin-bottom:10px;">Should we freeze the Sprint release on Thursday or Friday?</div>
                  <div style="margin-bottom:10px;">
                    <div style="display:flex;justify-content:space-between;font-size:0.78rem;font-weight:600;"><span>Thursday 5 PM</span> <span style="color:#059669;">65% (13 votes)</span></div>
                    <div class="poll-bar-bg"><div class="poll-bar-fill" style="width:65%;"></div></div>
                  </div>
                  <div style="margin-bottom:14px;">
                    <div style="display:flex;justify-content:space-between;font-size:0.78rem;font-weight:600;"><span>Friday 2 PM</span> <span style="color:#059669;">35% (7 votes)</span></div>
                    <div class="poll-bar-bg"><div class="poll-bar-fill" style="width:35%;"></div></div>
                  </div>
                  <button type="button" class="app-btn-primary" onclick="showToast('Vote registered!','success')" style="padding:6px 14px;font-size:0.75rem;">Submit Vote</button>
                </div>
                <div class="ref-card-metric" style="min-height:auto;padding:18px;">
                  <div style="font-weight:700;font-size:0.9rem;color:var(--text-dark);margin-bottom:10px;">Adopt Faster-Whisper on CUDA as default STT?</div>
                  <div style="margin-bottom:10px;">
                    <div style="display:flex;justify-content:space-between;font-size:0.78rem;font-weight:600;"><span>Yes, enable CUDA</span> <span style="color:#059669;">90% (18 votes)</span></div>
                    <div class="poll-bar-bg"><div class="poll-bar-fill" style="width:90%;"></div></div>
                  </div>
                  <div style="margin-bottom:14px;">
                    <div style="display:flex;justify-content:space-between;font-size:0.78rem;font-weight:600;"><span>No, CPU fallback only</span> <span style="color:#059669;">10% (2 votes)</span></div>
                    <div class="poll-bar-bg"><div class="poll-bar-fill" style="width:10%;"></div></div>
                  </div>
                  <button type="button" class="app-btn-primary" onclick="showToast('Vote registered!','success')" style="padding:6px 14px;font-size:0.75rem;">Submit Vote</button>
                </div>
              </div>
            </div>
          </div>"""

apps_view = """          <!-- ═════════ 11. APPS TAB ═════════ -->
          <div class="wp-tab-view" id="view-apps" style="display:none;width:100%;">
            <div class="ref-three-cards-row">
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">🧩</span> Connected Apps</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">6 <span class="ref-pill-percent">Active</span></div>
                  <div class="ref-metric-sub">Slack, Jira, Recall.ai, Zoom, Teams</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">⚡</span> Webhook Health</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">200 OK <span class="ref-pill-percent">0 Errors</span></div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">Real-Time Webhook Lifecycle Stream</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">Connect Enterprise<br>Integrations &amp;<br>Cloud Webhooks ↗</div>
                  <div class="ref-dark-hero-sub">Synchronize tickets and alerts</div>
                  <div class="ref-dark-hero-avatar">🧩</div>
                </div>
                <button type="button" onclick="testSlackWebhook()" class="ref-btn-upgrade" style="cursor:pointer;border:none;">
                  <span>Test All ▷</span>
                </button>
              </div>
            </div>

            <div class="doc-card" style="margin-top:20px;">
              <div style="font-weight:800;font-size:1.15rem;color:var(--text-dark);margin-bottom:14px;">Ecosystem Connectors &amp; Webhooks</div>
              <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:16px;">
                <div class="ref-card-metric" style="min-height:auto;padding:18px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <div style="font-weight:700;font-size:0.95rem;">Slack Bot</div>
                    <span class="app-badge-status app-badge-green">Connected</span>
                  </div>
                  <div style="font-size:0.75rem;color:#64748b;margin-bottom:12px;">Auto-dispatches executive digests to #general &amp; #engineering.</div>
                  <button type="button" class="app-btn-secondary" onclick="testSlackWebhook()" style="padding:4px 10px;font-size:0.72rem;">Test Ping</button>
                </div>
                <div class="ref-card-metric" style="min-height:auto;padding:18px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <div style="font-weight:700;font-size:0.95rem;">Jira Software</div>
                    <span class="app-badge-status app-badge-green">Connected</span>
                  </div>
                  <div style="font-size:0.75rem;color:#64748b;margin-bottom:12px;">Converts spoken meeting action items into trackable Jira tasks.</div>
                  <button type="button" class="app-btn-secondary" onclick="syncJiraTickets()" style="padding:4px 10px;font-size:0.72rem;">Sync Issues</button>
                </div>
                <div class="ref-card-metric" style="min-height:auto;padding:18px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <div style="font-weight:700;font-size:0.95rem;">Recall.ai Bridge</div>
                    <span class="app-badge-status app-badge-green">Connected</span>
                  </div>
                  <div style="font-size:0.75rem;color:#64748b;margin-bottom:12px;">Autonomous notetaker bot for external Zoom, Meet, &amp; Teams.</div>
                  <button type="button" class="app-btn-secondary" onclick="pingRecallBot()" style="padding:4px 10px;font-size:0.72rem;">Health Check</button>
                </div>
              </div>
            </div>
          </div>"""

workspaces_view = """          <!-- ═════════ 12. WORKSPACES TAB ═════════ -->
          <div class="wp-tab-view" id="view-workspaces" style="display:none;width:100%;">
            <div class="ref-three-cards-row">
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">🗂️</span> Workspaces</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">4 <span class="ref-pill-percent">Isolated</span></div>
                  <div class="ref-metric-sub">Engineering, Product, Sales, Exec</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">🔒</span> Storage Quota</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">12.4 GB <span class="ref-pill-percent">Encrypted</span></div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">AES-256 Storage Isolation Vault</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">Provision New<br>Department<br>Workspace ↗</div>
                  <div class="ref-dark-hero-sub">Isolate meeting intelligence &amp; access</div>
                  <div class="ref-dark-hero-avatar">🗂️</div>
                </div>
                <button type="button" onclick="showToast('Workspace creation wizard opened!','info')" class="ref-btn-upgrade" style="cursor:pointer;border:none;">
                  <span>New Workspace ▷</span>
                </button>
              </div>
            </div>

            <div class="doc-card" style="margin-top:20px;">
              <div style="font-weight:800;font-size:1.15rem;color:var(--text-dark);margin-bottom:14px;">Active Workspaces</div>
              <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:16px;">
                <div class="ref-card-metric" style="min-height:auto;padding:18px;border-color:var(--dock-dark);">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="font-weight:800;font-size:1rem;color:var(--text-dark);">Engineering &amp; Core Platform</div>
                    <span class="app-badge-status app-badge-green">● Active</span>
                  </div>
                  <div style="font-size:0.75rem;color:#64748b;margin:6px 0 12px;">12 Members • 48 Indexed Meetings • Faster-Whisper GPU cluster</div>
                  <button type="button" class="app-btn-primary" style="padding:5px 12px;font-size:0.72rem;">Current Workspace</button>
                </div>
                <div class="ref-card-metric" style="min-height:auto;padding:18px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="font-weight:800;font-size:1rem;color:var(--text-dark);">Product &amp; Design Strategy</div>
                    <span class="app-badge-status app-badge-purple">Isolated</span>
                  </div>
                  <div style="font-size:0.75rem;color:#64748b;margin:6px 0 12px;">6 Members • 18 Indexed Meetings • Bilingual Hindi-English models</div>
                  <button type="button" class="app-btn-secondary" onclick="showToast('Switched to Product &amp; Design!','success')" style="padding:5px 12px;font-size:0.72rem;">Switch Workspace</button>
                </div>
              </div>
            </div>
          </div>"""

contacts_view = """          <!-- ═════════ 13. CONTACTS TAB ═════════ -->
          <div class="wp-tab-view" id="view-contacts" style="display:none;width:100%;">
            <div class="ref-three-cards-row">
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">👥</span> Team Directory</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">18 <span class="ref-pill-percent">Online</span></div>
                  <div class="ref-metric-sub">Team Members &amp; Task Assignees</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">🎯</span> Action Owners</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">100% <span class="ref-pill-percent">Assigned</span></div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">Every Spoken Action Item Has An Owner</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">Invite New Team<br>Member to Syncra<br>Directory ↗</div>
                  <div class="ref-dark-hero-sub">Direct workspace collaboration invite</div>
                  <div class="ref-dark-hero-avatar">👥</div>
                </div>
                <button type="button" onclick="showToast('Invitation dialog opened!','info')" class="ref-btn-upgrade" style="cursor:pointer;border:none;">
                  <span>Add Contact ▷</span>
                </button>
              </div>
            </div>

            <div class="doc-card" style="margin-top:20px;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
                <div style="font-weight:800;font-size:1.15rem;color:var(--text-dark);">Team Directory &amp; Decision Assignees</div>
                <input type="text" class="ref-search-input" placeholder="Filter team members..." style="max-width:240px;padding:6px 14px;">
              </div>
              <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:14px;">
                <div class="ref-card-metric" style="min-height:auto;padding:16px;">
                  <div style="font-weight:700;font-size:0.95rem;color:var(--text-dark);">Gaurav Chakotiya</div>
                  <div style="font-size:0.75rem;color:#059669;font-weight:600;margin:2px 0 8px;">Lead Architect &amp; ML Engineer</div>
                  <a href="/app/room.html?room=call-gaurav" target="_blank" class="app-btn-primary" style="padding:4px 10px;font-size:0.72rem;">📞 Call</a>
                </div>
                <div class="ref-card-metric" style="min-height:auto;padding:16px;">
                  <div style="font-weight:700;font-size:0.95rem;color:var(--text-dark);">Rahul Sharma</div>
                  <div style="font-size:0.75rem;color:#059669;font-weight:600;margin:2px 0 8px;">DevOps &amp; Infrastructure Lead</div>
                  <a href="/app/room.html?room=call-rahul" target="_blank" class="app-btn-primary" style="padding:4px 10px;font-size:0.72rem;">📞 Call</a>
                </div>
                <div class="ref-card-metric" style="min-height:auto;padding:16px;">
                  <div style="font-weight:700;font-size:0.95rem;color:var(--text-dark);">Priya Patel</div>
                  <div style="font-size:0.75rem;color:#059669;font-weight:600;margin:2px 0 8px;">Frontend &amp; UX Lead</div>
                  <a href="/app/room.html?room=call-priya" target="_blank" class="app-btn-primary" style="padding:4px 10px;font-size:0.72rem;">📞 Call</a>
                </div>
              </div>
            </div>
          </div>"""

events_view = """          <!-- ═════════ 14. EVENTS TAB ═════════ -->
          <div class="wp-tab-view" id="view-events" style="display:none;width:100%;">
            <div class="ref-three-cards-row">
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">🎟️</span> Scheduled Townhalls</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">3 <span class="ref-pill-percent">High-Capacity</span></div>
                  <div class="ref-metric-sub">500+ Concurrent Viewers Supported</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">⚡</span> Broadcast Quality</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">1080p60 <span class="ref-pill-percent">WebRTC SFU</span></div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">Sub-300ms Global Distribution Latency</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">Start Live Studio<br>Webinar &amp; Broadcast<br>Session ↗</div>
                  <div class="ref-dark-hero-sub">Multi-party video with live translation</div>
                  <div class="ref-dark-hero-avatar">🎟️</div>
                </div>
                <a href="/app/room.html?role=broadcaster" target="_blank" class="ref-btn-upgrade">
                  <span>Go Live ▷</span>
                </a>
              </div>
            </div>

            <div class="doc-card" style="margin-top:20px;">
              <div style="font-weight:800;font-size:1.15rem;color:var(--text-dark);margin-bottom:14px;">Webinar &amp; Townhall Schedule</div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
                <div class="ref-card-metric" style="min-height:auto;padding:18px;">
                  <div style="font-size:0.75rem;font-weight:700;color:#059669;font-family:var(--font-mono);">NOV 24 • 04:00 PM UTC</div>
                  <div style="font-weight:800;font-size:1rem;color:var(--text-dark);margin:4px 0;">Q4 Global Engineering Townhall</div>
                  <div style="font-size:0.75rem;color:#64748b;margin-bottom:12px;">320 Registered • Faster-Whisper live Hindi/English captioning</div>
                  <a href="/app/room.html?room=townhall-q4&amp;role=broadcaster" target="_blank" class="app-btn-primary" style="padding:5px 14px;font-size:0.74rem;">Join as Host</a>
                </div>
                <div class="ref-card-metric" style="min-height:auto;padding:18px;">
                  <div style="font-size:0.75rem;font-weight:700;color:#059669;font-family:var(--font-mono);">DEC 02 • 06:30 PM UTC</div>
                  <div style="font-weight:800;font-size:1rem;color:var(--text-dark);margin:4px 0;">AI Notetaker &amp; D3 Architecture Deep Dive</div>
                  <div style="font-size:0.75rem;color:#64748b;margin-bottom:12px;">180 Registered • Real-time Decision Graph streaming</div>
                  <a href="/app/room.html?room=ai-deepdive&amp;role=broadcaster" target="_blank" class="app-btn-primary" style="padding:5px 14px;font-size:0.74rem;">Join as Host</a>
                </div>
              </div>
            </div>
          </div>"""

revenue_view = """          <!-- ═════════ 15. REVENUE TAB ═════════ -->
          <div class="wp-tab-view" id="view-revenue" style="display:none;width:100%;">
            <div class="ref-three-cards-row">
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">📈</span> Pipeline Value</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">$480K <span class="ref-pill-percent">3 Deals</span></div>
                  <div class="ref-metric-sub">Enterprise Telemetry Monitored</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">⚡</span> Rep Talk Ratio</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">41% / 59% <span class="ref-pill-percent">Optimal ↗</span></div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">Customer-Led Discovery Conversation</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">AI Deal Intelligence<br>&amp; Next Best Action<br>Recommendations ↗</div>
                  <div class="ref-dark-hero-sub">Automated buyer sentiment scoring</div>
                  <div class="ref-dark-hero-avatar">📈</div>
                </div>
                <button type="button" onclick="copyDealSummary()" class="ref-btn-upgrade" style="cursor:pointer;border:none;">
                  <span>Copy Telemetry ▷</span>
                </button>
              </div>
            </div>

            <div class="doc-card" style="margin-top:20px;">
              <div style="font-weight:800;font-size:1.15rem;color:var(--text-dark);margin-bottom:14px;">Conversational Deal Intelligence</div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;">
                <div class="ref-card-metric" style="min-height:auto;padding:18px;">
                  <div style="font-weight:700;font-size:0.9rem;color:var(--text-dark);margin-bottom:8px;">Acme Corp ($240,000 ARR)</div>
                  <div style="font-size:0.75rem;color:#059669;font-weight:600;margin-bottom:8px;">Stage: Solution Validation &amp; Security Review</div>
                  <div style="margin-bottom:10px;">
                    <div style="display:flex;justify-content:space-between;font-size:0.78rem;"><span>Talk Ratio</span> <span style="color:#059669;font-weight:600;">Rep 41% / Prospect 59%</span></div>
                    <div class="poll-bar-bg"><div class="poll-bar-fill" style="width:41%;"></div></div>
                  </div>
                  <div style="font-size:0.75rem;color:#64748b;line-height:1.45;">Buyer Sentiment: <strong style="color:var(--text-dark);">Strong Positive (84%)</strong>. Prospect validated Faster-Whisper offline security model.</div>
                </div>
                <div class="ref-card-metric" style="min-height:auto;padding:18px;background:#fbfcfb;">
                  <div style="font-weight:700;font-size:0.85rem;color:var(--text-dark);margin-bottom:6px;">🎯 AI Next Best Action</div>
                  <div style="font-size:0.78rem;color:#334155;line-height:1.55;margin-bottom:12px;">"Send architecture whitepaper covering Kubernetes offline failover to VP Engineering before Friday 5 PM."</div>
                  <button type="button" class="app-btn-primary" onclick="copyDealSummary()" style="padding:5px 14px;font-size:0.74rem;">Copy Action Briefing</button>
                </div>
              </div>
            </div>
          </div>"""

contactcenter_view = """          <!-- ═════════ 16. CONTACT CENTER TAB ═════════ -->
          <div class="wp-tab-view" id="view-contactcenter" style="display:none;width:100%;">
            <div class="ref-three-cards-row">
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">🎧</span> Supervisor QA</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">94.6% <span class="ref-pill-percent">Compliance</span></div>
                  <div class="ref-metric-sub">Monitored Across Live Voice Streams</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">⚡</span> Active Voice Queues</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">12 <span class="ref-pill-percent">Live Calls</span></div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">0 Escalations Pending / Normal Load</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">Real-Time Audio<br>Whisper Coaching<br>&amp; Supervisor Desk ↗</div>
                  <div class="ref-dark-hero-sub">Direct audio whisper to agent ear</div>
                  <div class="ref-dark-hero-avatar">🎧</div>
                </div>
                <button type="button" onclick="showToast('Whisper channel ready!','success')" class="ref-btn-upgrade" style="cursor:pointer;border:none;">
                  <span>Send Whisper ▷</span>
                </button>
              </div>
            </div>

            <div class="doc-card" style="margin-top:20px;">
              <div style="font-weight:800;font-size:1.15rem;color:var(--text-dark);margin-bottom:14px;">Live Contact Center Queue &amp; Coaching</div>
              <table class="rm-table">
                <thead>
                  <tr>
                    <th>Call ID</th>
                    <th>Agent</th>
                    <th>Duration</th>
                    <th>Sentiment</th>
                    <th>QA Compliance</th>
                    <th style="text-align:right;">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="font-family:var(--font-mono);color:#059669;font-weight:600;">#CC-4910</td>
                    <td style="font-weight:700;">Agent Ankit</td>
                    <td style="font-family:var(--font-mono);font-size:0.75rem;">04m 18s</td>
                    <td><span class="app-badge-status app-badge-green">Positive (92%)</span></td>
                    <td><span class="app-badge-status app-badge-green">Compliant</span></td>
                    <td style="text-align:right;"><button type="button" class="app-btn-secondary" onclick="showToast('Barge-in channel connected','info')" style="padding:4px 10px;font-size:0.72rem;">Barge-In</button></td>
                  </tr>
                  <tr>
                    <td style="font-family:var(--font-mono);color:#059669;font-weight:600;">#CC-4911</td>
                    <td style="font-weight:700;">Agent Neha</td>
                    <td style="font-family:var(--font-mono);font-size:0.75rem;">11m 40s</td>
                    <td><span class="app-badge-status app-badge-amber">Neutral (74%)</span></td>
                    <td><span class="app-badge-status app-badge-green">Compliant</span></td>
                    <td style="text-align:right;"><button type="button" class="app-btn-secondary" onclick="showToast('Whisper channel connected','info')" style="padding:4px 10px;font-size:0.72rem;">Whisper</button></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>"""

workvivo_view = """          <!-- ═════════ 17. WORKVIVO TAB ═════════ -->
          <div class="wp-tab-view" id="view-workvivo" style="display:none;width:100%;">
            <div class="ref-three-cards-row">
              <div class="ref-card-metric">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#e5f97e;color:#18191b;font-size:11px;">✨</span> Celebrations</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val">24 <span class="ref-pill-percent">Milestones</span></div>
                  <div class="ref-metric-sub">Cross-Department Kudos &amp; Wins</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item solid-dark"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div><div class="ref-capsule-item dashed-light"></div>
                </div>
              </div>
              <div class="ref-card-highlight">
                <div>
                  <div class="ref-card-header">
                    <span class="ref-card-tag"><span style="display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:#18191b;color:#e5f97e;font-size:11px;">⚡</span> Engagement Rate</span>
                    <button type="button" class="ref-card-menu-btn">⋮</button>
                  </div>
                  <div class="ref-metric-val" style="color:#18191b;">88% <span class="ref-pill-percent">Active ↗</span></div>
                  <div class="ref-metric-sub" style="color:rgba(24,25,27,0.6);">Monthly Active Team Participation</div>
                </div>
                <div class="ref-capsules-row">
                  <div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item solid-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div><div class="ref-capsule-item dashed-lime"></div>
                </div>
              </div>
              <div class="ref-card-dark-hero">
                <div>
                  <div class="ref-dark-hero-title">Publish Milestone<br>or Team Shoutout<br>to Company ↗</div>
                  <div class="ref-dark-hero-sub">Celebrate sprint deliverables &amp; releases</div>
                  <div class="ref-dark-hero-avatar">✨</div>
                </div>
                <button type="button" onclick="showToast('Milestone posted to Workvivo feed!','success')" class="ref-btn-upgrade" style="cursor:pointer;border:none;">
                  <span>Post Kudos ▷</span>
                </button>
              </div>
            </div>

            <div class="doc-card" style="margin-top:20px;">
              <div style="font-weight:800;font-size:1.15rem;color:var(--text-dark);margin-bottom:14px;">Workvivo Activity &amp; Recognition Feed</div>
              <div class="ref-card-metric" style="min-height:auto;padding:18px;margin-bottom:14px;">
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
                  <div style="width:38px;height:38px;border-radius:50%;background:#18191b;color:#ffffff;display:grid;place-items:center;font-weight:700;">G</div>
                  <div>
                    <div style="font-weight:800;font-size:0.95rem;color:var(--text-dark);">Gaurav Chakotiya</div>
                    <div style="font-size:0.72rem;color:#64748b;">Today at 10:45 AM • Engineering</div>
                  </div>
                </div>
                <p style="font-size:0.85rem;line-height:1.55;color:var(--text-dark);margin-bottom:12px;">
                  Huge shoutout to the engineering team for validating the Faster-Whisper CUDA diarization pipeline and integrating the Dribbble-inspired UI template across all options! 🚀
                  <span style="color:#059669;font-weight:600;">#SyncraWorkplace2</span> <span style="color:#059669;font-weight:600;">#WhisperCUDAOptimization</span>
                </p>
                <div style="display:flex;gap:8px;">
                  <button type="button" class="wv-reaction-btn" onclick="showToast('Reacted!','info')">🔥 12</button>
                  <button type="button" class="wv-reaction-btn" onclick="showToast('Clapped!','info')">👏 18</button>
                  <button type="button" class="wv-reaction-btn" onclick="showToast('Loved!','info')">❤️ 9</button>
                </div>
              </div>
            </div>
          </div>"""

# Insert all 11 views into <div class="ref-left-col"> right after clips_view
all_new_views = f"\n\n{mail_view}\n\n{calendar_view}\n\n{scheduler_view}\n\n{surveys_view}\n\n{apps_view}\n\n{workspaces_view}\n\n{contacts_view}\n\n{events_view}\n\n{revenue_view}\n\n{contactcenter_view}\n\n{workvivo_view}\n"

# Locate closing of view-clips
clips_end = text.find('</div>\n\n        </div>\n\n        <!-- RIGHT COLUMN:')
if clips_end != -1:
    text = text[:clips_end + len('</div>')] + all_new_views + text[clips_end + len('</div>'):]
    print("[OK] Inserted all 11 workplace views into ref-left-col")
else:
    print("[WARN] Could not find clips_end position")

# ══════════════════════════════════════════════════════════════════════
# 2. UPDATE JAVASCRIPT: switchMainTab & openMoreApp & openAppSuiteModal
# ══════════════════════════════════════════════════════════════════════

# Update switchMainTab to support all views
new_switch_all = """    window.switchMainTab = function(tabKey) {
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
    };"""

switch_pattern = re.compile(r'window\.switchMainTab\s*=\s*function\(tabKey\)\s*\{.*?\};\s*', re.DOTALL)
if switch_pattern.search(text):
    text = switch_pattern.sub(lambda m: new_switch_all + "\n\n", text, count=1)
    print("[OK] Replaced switchMainTab and routed openMoreApp/openAppSuiteModal to switchMainTab")
else:
    print("[WARN] Could not match switchMainTab regex")

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("[COMPLETE] Successfully integrated all 11 workplace views directly into the Dribbble homepage template!")
