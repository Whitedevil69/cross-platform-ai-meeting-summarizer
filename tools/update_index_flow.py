import sys

with open("frontend/index.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update header create meeting button
old_btn = """          <a href="/app/room.html" class="ref-btn-create" id="btnHeaderCreateMeeting" title="Start Instant WebRTC Video Room">
            <span>+ Create a New Meeting</span>
          </a>"""

new_btn = """          <a href="/app/login.html?redirect=/app/room.html" class="ref-btn-create" id="btnHeaderCreateMeeting" title="Start Instant WebRTC Video Room" onclick="startNewMeetingFlow(event)">
            <span>+ Create a New Meeting</span>
          </a>"""

if old_btn in text:
    text = text.replace(old_btn, new_btn, 1)
    print("[OK] Replaced btnHeaderCreateMeeting")
else:
    print("[WARN] old_btn not matched directly")

# 2. Add window.startNewMeetingFlow
old_func_anchor = """      function getAppUrl(path) {
        if (window.location.protocol.startsWith('http') && window.location.port === '8000') {
          return `/app/${path}`;
        }
        return `http://localhost:8000/app/${path}`;
      }"""

new_func = """      function getAppUrl(path) {
        if (window.location.protocol.startsWith('http') && window.location.port === '8000') {
          return `/app/${path}`;
        }
        return `http://localhost:8000/app/${path}`;
      }

      window.startNewMeetingFlow = function(e) {
        if (e && e.preventDefault) e.preventDefault();
        const storedEmail = localStorage.getItem('user_email');
        const storedName = localStorage.getItem('user_name') || (storedEmail ? storedEmail.split('@')[0] : '');
        const newMeetingId = (typeof crypto !== 'undefined' && crypto.randomUUID) ? crypto.randomUUID() : 'meet-' + Date.now();
        
        if (!storedEmail && !storedName) {
          window.location.href = `/app/login.html?redirect=${encodeURIComponent('/app/room.html?meeting=' + newMeetingId)}`;
        } else {
          window.location.href = `/app/room.html?meeting=${newMeetingId}&name=${encodeURIComponent(storedName || 'Gaurav')}`;
        }
      };"""

if old_func_anchor in text:
    text = text.replace(old_func_anchor, new_func, 1)
    print("[OK] Added window.startNewMeetingFlow")
else:
    print("[WARN] old_func_anchor not matched directly")

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] frontend/index.html updated successfully!")
