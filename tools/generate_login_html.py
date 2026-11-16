# tools/generate_login_html.py
import re
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sign In — Syncra Workplace</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
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
      --text-secondary: #475569;
      --text-muted: #8b95a5;
      --success: #10b981;
      --danger: #ef4444;
      --font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    html, body {
      width: 100%;
      min-height: 100vh;
      margin: 0;
      padding: 0;
      background-color: var(--canvas-sage);
      font-family: var(--font-family);
      color: var(--text-dark);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }

    /* Floating Shell Card */
    .login-container {
      width: 100%;
      max-width: 480px;
      margin: 24px auto;
      padding: 0 16px;
    }

    .login-card {
      background: var(--shell-white);
      border-radius: 28px;
      border: 1px solid rgba(0, 0, 0, 0.05);
      box-shadow: 0 25px 70px rgba(0, 0, 0, 0.12);
      padding: 38px 34px;
      position: relative;
    }

    .brand-header {
      text-align: center;
      margin-bottom: 24px;
    }

    .brand-icon {
      width: 52px;
      height: 52px;
      border-radius: 16px;
      background: var(--dock-dark);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      color: var(--highlight-lime);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.14);
      margin-bottom: 14px;
      transition: transform 0.2s ease;
    }
    .brand-icon:hover { transform: scale(1.05); }

    .brand-icon svg {
      width: 26px;
      height: 26px;
      stroke: var(--highlight-lime);
    }

    .meeting-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #eafaf1;
      border: 1px solid #c2eed5;
      color: #107e4a;
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.02em;
      margin-bottom: 8px;
    }

    .pulsing-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.3);
      animation: pulseDot 1.5s infinite;
    }
    @keyframes pulseDot {
      0% { opacity: 0.4; }
      50% { opacity: 1; }
      100% { opacity: 0.4; }
    }

    .brand-title {
      font-size: 22px;
      font-weight: 800;
      color: var(--text-dark);
      letter-spacing: -0.02em;
    }

    .brand-sub {
      font-size: 13.5px;
      color: var(--text-secondary);
      margin-top: 4px;
      line-height: 1.5;
    }

    /* Tab Switcher */
    .tab-switcher {
      display: flex;
      background: #f4f7f4;
      border: 1px solid var(--card-border);
      border-radius: 9999px;
      padding: 4px;
      margin-bottom: 24px;
    }

    .tab-btn {
      flex: 1;
      padding: 8px 16px;
      border-radius: 9999px;
      font-size: 12.5px;
      font-weight: 700;
      border: none;
      background: transparent;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: inherit;
    }

    .tab-btn.active {
      background: var(--dock-dark);
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    /* Alert Box */
    .alert-box {
      display: none;
      padding: 11px 16px;
      border-radius: 14px;
      font-size: 12.5px;
      font-weight: 700;
      margin-bottom: 18px;
      line-height: 1.45;
    }
    .alert-box.success {
      display: block;
      background: #eafaf1;
      border: 1px solid #c2eed5;
      color: #107e4a;
    }
    .alert-box.error {
      display: block;
      background: #fef2f2;
      border: 1px solid #fee2e2;
      color: #dc2626;
    }

    /* Form */
    .auth-form {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .form-label {
      font-size: 12px;
      font-weight: 700;
      color: var(--text-dark);
    }

    .form-input {
      width: 100%;
      padding: 11px 16px;
      border-radius: 14px;
      background: var(--card-bg);
      border: 1px solid #cbd5e1;
      font-size: 14px;
      font-family: inherit;
      color: var(--text-dark);
      outline: none;
      transition: all 0.18s ease;
    }

    .form-input:focus {
      border-color: var(--dock-dark);
      background: #ffffff;
      box-shadow: 0 0 0 3px rgba(24, 25, 27, 0.08);
    }

    .btn-submit {
      width: 100%;
      padding: 12px 20px;
      border-radius: 9999px;
      background: var(--dock-dark);
      color: #ffffff;
      font-size: 13.5px;
      font-weight: 800;
      border: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.14);
      transition: all 0.18s ease;
      font-family: inherit;
      margin-top: 4px;
    }

    .btn-submit:hover {
      background: #000000;
      transform: translateY(-1px);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
    }

    .btn-submit svg {
      width: 16px;
      height: 16px;
      stroke: var(--highlight-lime);
    }

    /* Divider */
    .divider-row {
      display: flex;
      align-items: center;
      gap: 12px;
      margin: 18px 0 14px;
      color: var(--text-muted);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .divider-line {
      flex: 1;
      height: 1px;
      background: var(--card-border);
    }

    /* Secondary Guest Button */
    .btn-guest {
      width: 100%;
      padding: 11px 20px;
      border-radius: 9999px;
      background: #f4f7f4;
      border: 1px solid #e2e8e2;
      color: var(--text-dark);
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.18s ease;
      font-family: inherit;
      text-decoration: none;
    }

    .btn-guest:hover {
      background: #e7ede7;
      color: #000000;
    }

    .footer-links {
      text-align: center;
      margin-top: 18px;
    }

    .footer-link {
      font-size: 12px;
      font-weight: 700;
      color: var(--text-secondary);
      text-decoration: none;
      transition: color 0.18s ease;
    }
    .footer-link:hover {
      color: var(--text-dark);
      text-decoration: underline;
    }
  </style>
</head>
<body>

  <div class="login-container">
    <div class="login-card">

      <!-- Brand Header -->
      <div class="brand-header">
        <div class="brand-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" x2="12" y1="19" y2="22"></line>
          </svg>
        </div>

        <div id="meetingBadge" class="meeting-tag" style="display: none;">
          <span class="pulsing-dot"></span>
          <span>Meeting Access Verification</span>
        </div>

        <h1 class="brand-title" id="pageTitle">Sign in to Syncra</h1>
        <p class="brand-sub" id="pageSub">
          AI Meeting Intelligence, Real-time Diarization &amp; Decision Systems
        </p>
      </div>

      <!-- Tab Switcher -->
      <div class="tab-switcher">
        <button type="button" id="tabLogin" class="tab-btn active" onclick="switchTab('login')">
          Sign In
        </button>
        <button type="button" id="tabRegister" class="tab-btn" onclick="switchTab('register')">
          Create Account
        </button>
      </div>

      <!-- Alert Box -->
      <div id="alertBox" class="alert-box"></div>

      <!-- Form -->
      <form id="authForm" onsubmit="handleAuth(event)" class="auth-form">
        <!-- Full Name field (always useful for meeting transcript attribution) -->
        <div class="form-group" id="nameGroup">
          <label for="userName" class="form-label">Full Name</label>
          <input id="userName" name="userName" type="text" placeholder="e.g. Gaurav Chakotiya" autocomplete="name" class="form-input">
        </div>

        <div class="form-group">
          <label for="email" class="form-label">Email address</label>
          <input id="email" name="email" type="email" required autocomplete="email" placeholder="you@company.internal" class="form-input">
        </div>

        <div class="form-group">
          <label for="password" class="form-label">Password</label>
          <input id="password" name="password" type="password" required autocomplete="current-password" placeholder="••••••••••••" class="form-input">
        </div>

        <button id="submitBtn" type="submit" class="btn-submit">
          <span id="submitBtnText">Sign In &amp; Proceed</span>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
        </button>
      </form>

      <div class="divider-row">
        <div class="divider-line"></div>
        <span>or</span>
        <div class="divider-line"></div>
      </div>

      <!-- Instant Guest / Direct Join Option -->
      <button type="button" class="btn-guest" id="btnGuestAccess" onclick="handleGuestAccess()">
        <span>Continue as Guest with Name</span>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
      </button>

      <div class="footer-links">
        <a href="/app/index.html" class="footer-link">
          ← Back to Workplace Dashboard
        </a>
      </div>

    </div>
  </div>

  <script>
    let mode = 'login';
    const params = new URLSearchParams(window.location.search);
    const redirectParam = params.get('redirect') || '';

    // Initialize UI on load
    document.addEventListener('DOMContentLoaded', () => {
      // Pre-fill existing user info if available
      const storedEmail = localStorage.getItem('user_email') || '';
      const storedName = localStorage.getItem('user_name') || '';
      if (storedEmail) document.getElementById('email').value = storedEmail;
      if (storedName) document.getElementById('userName').value = storedName;

      // If redirect points to meeting room, show meeting badge & customize text
      if (redirectParam && redirectParam.includes('room.html')) {
        const badge = document.getElementById('meetingBadge');
        if (badge) badge.style.display = 'inline-flex';
        document.getElementById('pageTitle').textContent = 'Sign In to Join Meeting';
        document.getElementById('pageSub').textContent = 'Enter your name and credentials to join the live intelligence session.';
        document.getElementById('submitBtnText').textContent = 'Sign In & Join Meeting';
        document.getElementById('btnGuestAccess').innerHTML = '<span>Join Meeting as Guest</span> <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>';
      }
    });

    function switchTab(newMode) {
      mode = newMode;
      const tabLogin = document.getElementById('tabLogin');
      const tabRegister = document.getElementById('tabRegister');
      const submitBtnText = document.getElementById('submitBtnText');
      const alertBox = document.getElementById('alertBox');
      alertBox.className = 'alert-box';
      alertBox.textContent = '';

      if (mode === 'login') {
        tabLogin.classList.add('active');
        tabRegister.classList.remove('active');
        submitBtnText.textContent = redirectParam.includes('room.html') ? 'Sign In & Join Meeting' : 'Sign In & Proceed';
      } else {
        tabRegister.classList.add('active');
        tabLogin.classList.remove('active');
        submitBtnText.textContent = redirectParam.includes('room.html') ? 'Create Account & Join Meeting' : 'Create Account & Proceed';
      }
    }

    function resolveRedirectUrl(userName) {
      if (!redirectParam) {
        return '/app/index.html';
      }
      let url = redirectParam;
      if (userName && !url.includes('name=')) {
        const sep = url.includes('?') ? '&' : '?';
        url = `${url}${sep}name=${encodeURIComponent(userName)}`;
      }
      return url;
    }

    function handleGuestAccess() {
      const nameInput = document.getElementById('userName');
      let name = nameInput.value.trim();
      if (!name) {
        const emailVal = document.getElementById('email').value.trim();
        name = emailVal ? emailVal.split('@')[0] : 'Gaurav Chakotiya';
      }
      localStorage.setItem('user_name', name);
      if (!localStorage.getItem('user_email')) {
        localStorage.setItem('user_email', `${name.toLowerCase().replace(/\\s+/g, '.')}@syncra.internal`);
      }
      window.location.href = resolveRedirectUrl(name);
    }

    async function handleAuth(e) {
      e.preventDefault();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;
      const userNameInput = document.getElementById('userName').value.trim();
      const userName = userNameInput || (email.split('@')[0] || 'User');
      const alertBox = document.getElementById('alertBox');
      const submitBtn = document.getElementById('submitBtn');

      alertBox.className = 'alert-box';
      alertBox.textContent = '';
      submitBtn.disabled = true;
      submitBtn.style.opacity = '0.7';

      const endpoint = mode === 'login' ? '/api/auth/login' : '/api/auth/register';

      try {
        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        });

        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.detail || 'Authentication failed');
        }

        if (mode === 'register') {
          // Auto login after registration
          const loginRes = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
          });
          const loginData = await loginRes.json();
          if (loginRes.ok && loginData.access_token) {
            localStorage.setItem('auth_token', loginData.access_token);
            localStorage.setItem('user_email', email);
            localStorage.setItem('user_name', userName);
            window.location.href = resolveRedirectUrl(userName);
            return;
          }
          alertBox.className = 'alert-box success';
          alertBox.textContent = 'Account created successfully! Please sign in.';
          switchTab('login');
        } else {
          localStorage.setItem('auth_token', data.access_token);
          localStorage.setItem('user_email', email);
          localStorage.setItem('user_name', userName);
          window.location.href = resolveRedirectUrl(userName);
        }
      } catch (err) {
        alertBox.className = 'alert-box error';
        alertBox.textContent = err.message || 'An error occurred';
      } finally {
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
      }
    }
  </script>
</body>
</html>
"""

with open("frontend/login.html", "w", encoding="utf-8") as f:
    f.write(LOGIN_HTML)

print("[OK] frontend/login.html successfully rewritten with Dribbble theme & meeting redirect logic!")
