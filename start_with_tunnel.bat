@echo off
title Syncra + Cloudflare HTTPS Tunnel
color 0B
cls
echo ==================================================================
echo   SYNCRA — DUAL STARTUP (SERVER + SECURE HTTPS TUNNEL)
echo   Unlocks camera, audio, and live streaming on all mobile devices
echo ==================================================================
echo.
if not exist "cloudflared.exe" (
    echo [*] Cloudflare tunnel binary not found. Downloading cloudflared.exe...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile 'cloudflared.exe'"
)
echo [*] Starting Cloudflare HTTPS Tunnel in background...
start "Cloudflare HTTPS Tunnel" cmd /k "cloudflared.exe tunnel --url http://127.0.0.1:8000"
timeout /t 3 /nobreak >nul
echo.
echo [*] Launching FastAPI backend on 0.0.0.0:8000...
start http://localhost:8000/app/
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
pause
