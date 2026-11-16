with open("frontend/report.html", "r", encoding="utf-8") as f:
    text = f.read()

old_btn = """      <button class="btn-export btn-export-primary" onclick="location.href='/app/index.html'">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        <span>New Meeting</span>
      </button>"""

new_btn = """      <button class="btn-export btn-export-primary" onclick="handleNewMeeting(event)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        <span>New Meeting</span>
      </button>"""

old_script_end = """function showToast(msg, type) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.style.borderColor = type === 'error' ? '#ef4444' : '#10b981';
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

init();"""

new_script_end = """function showToast(msg, type) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.style.borderColor = type === 'error' ? '#ef4444' : '#10b981';
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

function handleNewMeeting(e) {
  if (e && e.preventDefault) e.preventDefault();
  const storedEmail = localStorage.getItem('user_email');
  const storedName = localStorage.getItem('user_name') || (storedEmail ? storedEmail.split('@')[0] : '');
  const newMeetingId = (typeof crypto !== 'undefined' && crypto.randomUUID) ? crypto.randomUUID() : 'meet-' + Date.now();
  if (!storedEmail && !storedName) {
    window.location.href = `/app/login.html?redirect=${encodeURIComponent('/app/room.html?meeting=' + newMeetingId)}`;
  } else {
    window.location.href = `/app/room.html?meeting=${newMeetingId}&name=${encodeURIComponent(storedName || 'Gaurav')}`;
  }
}

init();"""

if old_btn in text:
    text = text.replace(old_btn, new_btn, 1)
    print("[OK] Replaced New Meeting button in report.html")

if old_script_end in text:
    text = text.replace(old_script_end, new_script_end, 1)
    print("[OK] Added handleNewMeeting in report.html")

with open("frontend/report.html", "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] report.html updated!")
