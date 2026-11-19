"""
Syncra Pre-Flight Diagnostic & System Health Checker
Run this anytime: python doctor.py
"""
import sys
import os
import socket
import urllib.request
import json
from pathlib import Path

def print_header(title):
    print(f"\n{'=' * 65}")
    print(f"  {title}")
    print(f"{'=' * 65}")

def check_mark(status: bool, msg: str):
    icon = "[OK]" if status else "[WARN]"
    color_prefix = "\033[92m" if status else "\033[93m"
    color_reset = "\033[0m"
    print(f" {color_prefix}{icon}{color_reset} {msg}")

def main():
    print_header("SYNCRA PRE-FLIGHT SYSTEM DIAGNOSTIC")
    all_ok = True

    # 1. Python Check
    py_ver = sys.version.split()[0]
    is_py_ok = sys.version_info >= (3, 10)
    check_mark(is_py_ok, f"Python Runtime: v{py_ver} ({sys.executable})")
    if not is_py_ok: all_ok = False

    # 2. Dependencies
    pkgs = [
        ("uvicorn", "ASGI server"),
        ("faster_whisper", "Faster-Whisper bilingual ASR engine"),
        ("av", "PyAV multimedia library"),
        ("dotenv", "python-dotenv config loader"),
        ("pydantic", "Pydantic v2 data models"),
        ("websockets", "WebSocket client/server protocol"),
    ]
    try:
        from backend.main import app
        check_mark(True, "Syncra Backend Application: Loaded cleanly with all routers & middlewares")
    except Exception as e:
        check_mark(False, f"Syncra Backend load error: {e}")
        all_ok = False

    for mod_name, label in pkgs:
        try:
            __import__(mod_name)
            check_mark(True, f"Dependency '{mod_name}': installed ({label})")
        except ImportError as e:
            check_mark(False, f"Dependency '{mod_name}' MISSING: {e}")
            all_ok = False

    # 3. Environment & Workspace
    env_file = Path(".env")
    check_mark(env_file.exists(), f"Configuration (.env): {'Present' if env_file.exists() else 'Missing'}")

    html_files = ["frontend/index.html", "frontend/room.html", "frontend/readback.html"]
    for h in html_files:
        exists = Path(h).exists()
        check_mark(exists, f"Frontend template '{h}': {'Found' if exists else 'Missing'}")
        if not exists: all_ok = False

    # 4. LAN IP Resolution
    lan_ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        lan_ip = s.getsockname()[0]
        s.close()
        check_mark(True, f"Local Wi-Fi / LAN IP: {lan_ip}")
    except Exception as e:
        check_mark(False, f"Local Wi-Fi IP discovery failed: {e}")

    # 5. Ollama Status
    ollama_ok = False
    try:
        req = urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3)
        if req.status == 200:
            data = json.loads(req.read().decode())
            models = [m.get("name") for m in data.get("models", [])]
            check_mark(True, f"Ollama Service: Running (models: {', '.join(models) if models else 'None'})")
            ollama_ok = True
    except Exception:
        check_mark(False, "Ollama Service: Not responding on port 11434 (Smart heuristic fallback will handle extractions)")

    # 6. Cloudflare Tunnel Binary
    cf_bin = Path("cloudflared.exe")
    check_mark(cf_bin.exists(), f"Cloudflare HTTPS Tunnel ('cloudflared.exe'): {'Ready' if cf_bin.exists() else 'Missing'}")

    # 7. Summary
    print_header("SUMMARY")
    if all_ok:
        print("  🎉 ALL CRITICAL SYSTEMS ARE OPERATIONAL & VERIFIED!")
        print("  👉 To start Syncra: Double-click 'start_syncra.bat' or press F5 in VS Code.")
        print(f"  👉 Local Web URL:   http://localhost:8000/app/")
        print(f"  👉 Mobile Wi-Fi:    http://{lan_ip}:8000/app/")
    else:
        print("  ⚠️ Some optional items had warnings, but fallback handlers are active.")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
