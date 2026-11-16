import sys

with open("frontend/room.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update showConsentModal & handleConsentAgreed & handleConsentDeclined
old_consent = """      function showConsentModal() {
        modalConsent.classList.add('active');
      }

      function handleConsentAgreed() {
        modalConsent.classList.remove('active');
        startMeetingSession();
      }

      function handleConsentDeclined() {
        modalConsent.classList.remove('active');
        window.location.href = (window.location.pathname.startsWith('/app')) ? '/app/index.html' : 'index.html';
      }"""

new_consent = """      function showConsentModal() {
        modalConsent.classList.add('active');
        modalConsent.classList.add('open');
      }

      function handleConsentAgreed() {
        modalConsent.classList.remove('active');
        modalConsent.classList.remove('open');
        startMeetingSession();
      }

      function handleConsentDeclined() {
        modalConsent.classList.remove('active');
        modalConsent.classList.remove('open');
        window.location.href = (window.location.pathname.startsWith('/app')) ? '/app/index.html' : 'index.html';
      }"""

if old_consent in text:
    text = text.replace(old_consent, new_consent, 1)
    print("[OK] Updated consent modal methods")

# 2. Update showNameModal & handleNameSubmitted
old_name_flow = """      function showNameModal() {
        modalNameEntry.classList.add('active');
        setTimeout(() => inputUserName.focus(), 150);
      }

      function handleNameSubmitted() {
        const val = inputUserName.value.trim();
        if (!val) {
          inputUserName.style.borderColor = 'var(--danger)';
          inputUserName.focus();
          return;
        }

        participantName = val;
        modalNameEntry.classList.remove('active');"""

new_name_flow = """      function showNameModal() {
        modalNameEntry.classList.add('active');
        modalNameEntry.classList.add('open');
        setTimeout(() => inputUserName.focus(), 150);
      }

      function handleNameSubmitted() {
        const val = inputUserName.value.trim();
        if (!val) {
          inputUserName.style.borderColor = 'var(--danger)';
          inputUserName.focus();
          return;
        }

        participantName = val;
        localStorage.setItem('user_name', val);
        modalNameEntry.classList.remove('active');
        modalNameEntry.classList.remove('open');"""

if old_name_flow in text:
    text = text.replace(old_name_flow, new_name_flow, 1)
    print("[OK] Updated name modal methods")

# 3. Update openShareModal & closeShareModal
old_share = """      function openShareModal() {
        shareUrlInput.value = window.location.href;
        modalShareLink.classList.add('active');
      }

      function closeShareModal() {
        modalShareLink.classList.remove('active');
      }"""

new_share = """      function openShareModal() {
        shareUrlInput.value = window.location.href;
        modalShareLink.classList.add('active');
        modalShareLink.classList.add('open');
      }

      function closeShareModal() {
        modalShareLink.classList.remove('active');
        modalShareLink.classList.remove('open');
      }"""

if old_share in text:
    text = text.replace(old_share, new_share, 1)
    print("[OK] Updated share modal methods")

# 4. Update name resolution in init()
old_name_resolve = """        // 2. Resolve Participant Name
        if (params.name && params.name.trim()) {
          participantName = params.name.trim();
          showConsentModal();
        } else {
          showNameModal();
        }"""

new_name_resolve = """        // 2. Resolve Participant Name
        if (params.name && params.name.trim()) {
          participantName = params.name.trim();
          localStorage.setItem('user_name', participantName);
          showConsentModal();
        } else {
          const storedName = localStorage.getItem('user_name');
          const storedEmail = localStorage.getItem('user_email');
          if (storedName && storedName.trim()) {
            participantName = storedName.trim();
            showConsentModal();
          } else if (storedEmail && storedEmail.trim()) {
            participantName = storedEmail.split('@')[0];
            showConsentModal();
          } else {
            showNameModal();
          }
        }"""

if old_name_resolve in text:
    text = text.replace(old_name_resolve, new_name_resolve, 1)
    print("[OK] Updated name resolution in init()")

# 5. Add Sign In link to modal-name-entry in HTML
old_modal_btns = """      <div class="modal-btn-row">
        <button class="modal-btn modal-btn-primary" id="btn-name-continue">
          <span>Continue to Room</span>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"></line>
            <polyline points="12 5 19 12 12 19"></polyline>
          </svg>
        </button>
      </div>"""

new_modal_btns = """      <div class="modal-btn-row">
        <a href="/app/login.html" id="link-name-login" class="modal-btn modal-btn-secondary" style="text-decoration:none;">
          <span>Sign In / Register</span>
        </a>
        <button class="modal-btn modal-btn-primary" id="btn-name-continue">
          <span>Continue to Room</span>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"></line>
            <polyline points="12 5 19 12 12 19"></polyline>
          </svg>
        </button>
      </div>"""

if old_modal_btns in text:
    text = text.replace(old_modal_btns, new_modal_btns, 1)
    print("[OK] Added login link to name modal HTML")

# 6. Set link-name-login href in JS
old_setup_events = """      function setupEventListeners() {
        // Name modal
        btnNameContinue.addEventListener('click', handleNameSubmitted);"""

new_setup_events = """      function setupEventListeners() {
        // Name modal
        const linkNameLogin = document.getElementById('link-name-login');
        if (linkNameLogin) {
          linkNameLogin.href = `/app/login.html?redirect=${encodeURIComponent(window.location.href)}`;
        }
        btnNameContinue.addEventListener('click', handleNameSubmitted);"""

if old_setup_events in text:
    text = text.replace(old_setup_events, new_setup_events, 1)
    print("[OK] Configured link-name-login in JS")

with open("frontend/room.html", "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] frontend/room.html fully updated!")
