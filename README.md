# 🧠 Meeting Intelligence System

**Platform-Independent, Evidence-Linked AI Meeting Intelligence for Hindi–English Teams**

> Author: Gaurav · B.Tech CSE, ITM University, Gwalior · October 2026  
> Status: Phase A + D implementation

---

> 🤖 **Moving to another AI model or assistant?**  
> Everything is fully documented and structured for zero-context-loss migration:  
> - 📄 **[AI Continuation & Handover Guide](AI_CONTINUATION_GUIDE.md)**: Drop-in master prompt, conversation history, design decisions, and immediate next steps.  
> - 🏗️ **[Architecture & Structure Guide](ARCHITECTURE_AND_STRUCTURE.md)**: File-by-file anatomy, data schemas, API routes, and pipeline flowcharts.

---

## What This Does

This system records/uploads meetings → transcribes with faster-whisper → detects Hindi/English language per segment → translates with NLLB-200 → extracts decisions, actions and questions via a local LLM (Ollama) → verifies every AI claim against the actual transcript → lets participants confirm/edit/reject before anything becomes official → saves a structured Meeting Record → visualises a decision graph.

**The pipeline:**
```
Guests (browser, no install)
        │ WebRTC
        ▼
   LiveKit room ──audio──► FastAPI ──► faster-whisper (per-segment language ID)
                               │             │
                               │             ▼
                               │        NLLB translation
                               ▼             │
                     Local LLM (Ollama) ◄───┘   → JSON: decisions, tasks, owner,
                               │                   deadline, evidence{line, time, clip}
                               ▼
                    Read-back confirmation ─► Meeting Record (JSON) ─► Report / graph
```

---

## Quick Start

### 1 — Prerequisites

| Tool | How to get it |
|------|--------------|
| Python 3.10+ | python.org |
| Docker Desktop | docker.com |
| Ollama | ollama.com |

### 2 — Install Python deps

```powershell
python -m pip install -r requirements.txt
```

### 3 — Pull an Ollama model

```powershell
# Recommended (good JSON accuracy, 5GB):
ollama pull llama3.1:8b

# Better quality if you have RAM:
ollama pull qwen2.5:14b
```

### 4 — Copy and configure .env

```powershell
copy .env.example .env
# Edit .env to match your chosen Ollama model etc.
```

### 5 — Start LiveKit (Docker)

```powershell
docker compose up -d
```

Or download `livekit-server.exe` from [github.com/livekit/livekit/releases](https://github.com/livekit/livekit/releases) and run:
```powershell
.\livekit-server.exe --config livekit.yaml
```

### 6 — Start the FastAPI server

```powershell
# From the project root:
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 7 — Open the app

Open your browser to: **http://localhost:8000/app/index.html**

---

## Usage

### Upload a Recording
1. Go to `index.html`
2. Drag-and-drop an audio/video file (MP3, WAV, MP4, WebM…)
3. Add a meeting title (optional)
4. Click **Process Meeting**
5. Watch the pipeline progress (ASR → Translation → Extraction → Evidence Check)
6. Review items in the **Read-back** screen — Confirm ✅ / Edit ✏️ / Reject ❌
7. View your **Final Report** with decision graph

### Start a Live Room
1. Click **Start Live Room** → enter a title
2. Share the join link with participants (they need no install — just a browser)
3. All audio is transcribed in real time
4. Click **End Meeting & Review** to trigger extraction
5. Complete read-back → report

---

## Project Structure

```
├── backend/
│   ├── main.py              FastAPI app (all routes + WebSocket)
│   ├── meeting_record.py    Pydantic models (open JSON schema)
│   ├── asr.py               faster-whisper transcription
│   ├── translation.py       NLLB-200 Hindi↔English translation
│   ├── extraction.py        Ollama LLM → structured JSON extraction
│   ├── evidence.py          Evidence citation verification
│   ├── graph.py             NetworkX decision graph
│   ├── audio_store.py       Audio file management + clip extraction
│   └── livekit_manager.py   LiveKit JWT token generation
├── frontend/
│   ├── index.html           Landing page (upload + create room)
│   ├── room.html            Live meeting room (WebRTC)
│   ├── readback.html        Read-back confirmation UI
│   └── report.html          Final report + D3 decision graph
├── meetings/                Runtime data (created automatically)
├── docker-compose.yml       LiveKit server
├── livekit.yaml             LiveKit configuration
├── requirements.txt
└── .env.example
```

---

## Environment Variables

See `.env.example` for all options. Key ones:

| Variable | Default | Description |
|----------|---------|-------------|
| `WHISPER_MODEL` | `small` | Model size: tiny/base/small/medium/large-v3 |
| `OLLAMA_MODEL` | `llama3.1:8b` | Local LLM for extraction |
| `NLLB_MODEL` | `facebook/nllb-200-distilled-600M` | Translation model |
| `LIVEKIT_URL` | `ws://localhost:7880` | LiveKit server URL |
| `MEETINGS_DIR` | `meetings` | Where to store meeting data |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/meetings/upload` | Upload audio/video file |
| GET  | `/api/meetings/{id}` | Get full Meeting Record JSON |
| GET  | `/api/meetings/{id}/status` | SSE progress stream |
| POST | `/api/meetings/{id}/confirm` | Submit read-back decisions |
| GET  | `/api/meetings/{id}/report` | Final report |
| GET  | `/api/meetings/{id}/audio/{seg}` | Serve audio clip |
| POST | `/api/rooms/create` | Create LiveKit room |
| GET  | `/api/rooms/token` | Get LiveKit join token |
| WS   | `/ws/room/{id}` | Live audio WebSocket |
| GET  | `/api/graph` | Decision graph JSON |
| GET  | `/api/graph/impact/{item_id}` | Impact analysis |

Docs: **http://localhost:8000/docs**

---

## Roadmap (per whitepaper)

| Phase | Status | Content |
|-------|--------|---------|
| A | ✅ Done | Core pipeline, evidence checking, read-back, evaluation |
| B | 🔲 Stub | Speaker diarization (pyannote.audio) for mixed audio |
| C | ✅ Done | Decision graph, conflict flagging, impact analysis |
| D | ✅ Done | Browser meeting room (LiveKit WebRTC) |
| E | 🔲 Planned | Platform connectors (Zoom/Meet/Teams via Recall.ai) |

---

## Evaluation Metrics (Phase A)

Per the whitepaper, measure on 8–10 role-played Hindi/English/Hinglish meetings:

| Metric | Target |
|--------|--------|
| Word Error Rate | Report honestly with Devanagari/Roman normalisation |
| Extraction F1 | Precision/recall of decisions vs hand labels |
| Evidence accuracy | Share of items with verified citations |
| Read-back correction rate | Share of items edited/rejected by participants |
| Latency (P50 / P95) | Speech → on-screen text |

---

*All AI outputs are decision support. The system never makes binding decisions for participants.*
