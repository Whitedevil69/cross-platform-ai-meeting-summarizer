@echo off
title Syncra — AI Meeting Intelligence
color 0A
cls
echo ==================================================================
echo   SYNCRA — CROSS-PLATFORM AI MEETING INTELLIGENCE
echo   Multi-Device Presence, Real-Time Transcription, Evidence Grounding
echo ==================================================================
echo.
echo [*] Checking system diagnostics...
python doctor.py
if %ERRORLEVEL% NEQ 0 (
    echo [!] Diagnostic warning detected, but proceeding with startup.
)
echo.
echo [*] Launching FastAPI backend on 0.0.0.0:8000...
start http://localhost:8000/app/
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
pause
