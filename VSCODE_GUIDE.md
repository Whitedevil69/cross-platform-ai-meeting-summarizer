# Syncra — VS Code Setup & Showcase Guide

This workspace is fully pre-configured for Visual Studio Code on Windows.

---

## ⚡ 1-Step Quick Launch

### Option 1: The F5 Key (Recommended in VS Code)
1. Open this folder in VS Code (`File > Open Folder...`).
2. Press **`F5`** on your keyboard (or click the Run & Debug tab on the left and click the green play button).
3. The server starts immediately in your integrated terminal on `http://0.0.0.0:8000`.
4. Open `http://localhost:8000/app/` in your browser.

### Option 2: VS Code Tasks (`Ctrl + Shift + B`)
1. Press **`Ctrl + Shift + B`** in VS Code.
2. It automatically executes **"1. Start Syncra Server (FastAPI)"**.
3. To run other tasks, open the Command Palette (`Ctrl + Shift + P`) -> **`Tasks: Run Task`**:
   - `1. Start Syncra Server (FastAPI)`
   - `2. Start Secure HTTPS Tunnel (Cloudflare)` (unlocks mobile cameras)
   - `3. Run System Diagnostic (doctor.py)`
   - `4. Open Syncra Web Dashboard`

### Option 3: Double-Click Desktop Launchers
You can run Syncra directly without even opening VS Code:
- **`start_syncra.bat`**: Runs system diagnostics, starts the server, and automatically opens your browser.
- **`start_with_tunnel.bat`**: Starts the server **plus** a secure Cloudflare HTTPS tunnel for iPhone/Android camera streaming.

---

## 🩺 System Diagnostic Tool (`doctor.py`)

Run this anytime to verify all components, dependencies, and local network IPs:
```bash
python doctor.py
```
Outputs an instant status report confirming:
- Python 3.13 Runtime
- FastAPI & Uvicorn ASGI Server
- Faster-Whisper Bilingual ASR Engine
- Ollama LLM Service (`qwen3:8b`)
- Frontend templates (`index.html`, `room.html`, `readback.html`)
- Local Wi-Fi IP and Cloudflare Tunnel readiness

---

## 📱 Cross-Device Testing (For Tomorrow's Showcase)

1. **Host on Laptop:**
   - Go to `http://localhost:8000/app/`
   - Click **"Create Meeting Room"**
   - Click **"Share Meeting Link"** -> Click **Copy**
2. **Participant on Phone (iPhone / Android):**
   - Paste the link on your phone.
   - For plain Wi-Fi: `http://192.168.29.192:8000/app/room.html?meeting=...`
   - For full HTTPS camera + mic: Use the Cloudflare Tunnel link from `start_with_tunnel.bat`.
3. **During the Meeting:**
   - Both devices see each other in the room tiles.
   - Counter shows `Participants: 2`.
   - Speaking indicator pulses in real time.
   - Live Hindi & English captions stream across both screens simultaneously.
   - Clicking **"End Meeting & Review"** transitions both devices to the evidence-grounded review page.

---

## 🛠️ VS Code Configuration Files Included

- **`.vscode/settings.json`**: Pre-configured Python interpreter path, file associations, and terminal profile.
- **`.vscode/launch.json`**: Debug configurations for FastAPI and system diagnostics.
- **`.vscode/tasks.json`**: Automated build and background server tasks.
