# 🤖 AI Handover & Continuation Guide
> **Purpose**: This document preserves 100% of the project context, design decisions, architectural invariants, conversation history, and current development state. If this folder is moved to any other AI model (Claude, ChatGPT/GPT-4o, Cursor, Gemini, DeepSeek, Qwen, Windsurf, etc.), feed this file to the model to continue development seamlessly without losing any progress.

---

## ⚡ Quick-Start Prompt for Your Next AI Assistant
When starting a conversation with a new AI model, **copy & paste this single block**:

```text
I am continuing development on the "Meeting Intelligence System" (Platform-Independent, Evidence-Linked AI Meeting Intelligence for Hindi–English Teams).
Please read `AI_CONTINUATION_GUIDE.md` and `ARCHITECTURE_AND_STRUCTURE.md` in the workspace root.
All core files for Phase A, C, and D are implemented in /backend and /frontend.
We left off with the full stack operational (FastAPI + faster-whisper + NLLB-200 + Ollama + LiveKit + read-back UI + D3 decision graph).
Acknowledge that you have loaded the context, state the current status, and tell me what the next recommended step is (e.g. testing with sample audio, Phase B PyAnnote diarization, or cloud LLM toggles).
```

---

## 📌 Project Identity & Overview
- **Project Name**: AI-Powered Real-Time Meeting Decision Intelligence System
- **Lead Developer / Author**: Gaurav (B.Tech CSE, ITM University, Gwalior)
- **Academic Foundation**: White Paper — *"Platform-Independent, Evidence-Linked Meeting Intelligence for Hindi–English Teams"* (October 2026).
- **Core Philosophy**: All AI outputs are **decision support only**. The system never makes binding commitments for participants without explicit human read-back confirmation.

### The 4 Non-Negotiable Architectural Commitments
1. **One Open Meeting Record**: Every input (uploaded audio/video file, live microphone, or browser WebRTC room) normalizes into the exact same JSON schema (`MeetingRecord`).
2. **Evidence-Linked Accountability**: Every extracted decision, action item, or question MUST cite transcript `segment_id` and exact quotes. Owners and deadlines must be left `null` if unstated—**never hallucinated or guessed**.
3. **Participant Read-Back**: Before finalization, participants review proposed items on a dedicated UI: Confirm ✅, Edit ✏️, or Reject ❌. Only confirmed items enter the official record and decision graph.
4. **Local-First & Bilingual (Hindi-English)**: Designed to run locally using open-weights models (`faster-whisper`, `nllb-200-distilled-600M`, `ollama llama3.1:8b`). Handles mixed Hindi-English (Hinglish) code-switching gracefully.

---

## 🗺️ Current Roadmap & Implementation Status

| Phase | Description | Status | Implementation Details |
|---|---|---|---|
| **Phase A** | Core Pipeline, Evidence Checking, Read-back, Metrics | **✅ Completed** | Full backend pipeline: `asr.py`, `translation.py`, `extraction.py`, `evidence.py`, `audio_store.py`. Full UI: `index.html`, `readback.html`, `report.html`. |
| **Phase B** | Speaker Diarization for Mixed Single-Channel Audio | **✅ Completed** | Implemented in `backend/diarization.py`. Supports `pyannote/speaker-diarization-3.1` (via HF_TOKEN) and a zero-dependency energy-based silence threshold fallback. |
| **Phase C** | Cross-Meeting Decision Graph & Impact Analysis | **✅ Completed** | NetworkX directed graph in `backend/graph.py`. Tracks `depends_on`, `supersedes`, `assigned_to`, `due_on`. Visualized via D3.js in `report.html`. API endpoints `/api/graph` and `/api/graph/impact/{item_id}`. |
| **Phase D** | Zero-Install Browser Meeting Room | **✅ Completed** | LiveKit WebRTC server (`docker-compose.yml`, `livekit.yaml`), token manager (`livekit_manager.py`), WebSocket audio streamer, and client room UI (`frontend/room.html`). |
| **Phase E** | External Platform Connectors (Zoom / Meet / Teams) | **✅ Completed** | Full connector suite in `backend/connectors/` (`recallai.py`, `zoom.py`, `meet.py`, `teams.py`, `router.py`). Dispatches Recall.ai recording bots via `/api/connectors/join` with HMAC-verified webhooks. |
| **Database** | SQLite Relational Storage & Fast Querying | **✅ Completed** | `backend/database.py` with thread-safe connection pooling, meeting search, item tracking, and automatic file migration. |
| **Auth** | Multi-User Authentication & JWT | **✅ Completed** | Pure stdlib PBKDF2 password hashing & HS256 JWT in `backend/auth.py`, login/register UI at `frontend/login.html`. |
| **Cloud LLMs** | Multi-Provider LLM Extraction | **✅ Completed** | `backend/extraction.py` with runtime lazy adapter for Ollama, OpenAI, Google Gemini, and Anthropic Claude. |
| **Evaluation** | Automated Empirical Benchmark Suite | **✅ Completed** | `eval/benchmark.py` measuring WER, Extraction F1, Evidence Precision, Correction Rate, and Latency on role-played samples. |
| **Deployment**| Multi-Container Production Docker Stack | **✅ Completed** | Multi-stage `Dockerfile`, `docker-compose.prod.yml` (FastAPI + LiveKit + Ollama), and `DEPLOY.md`. |

---

## 🛠️ Tech Stack & Key Components

### Backend (Python 3.10+)
- **Framework**: `FastAPI` (Async endpoints, WebSocket, SSE progress streams, static files mounting).
- **Database & Persistence**: `sqlite3` (`database.py`) with thread-safe connection pooling, meeting search, item tracking, and JSON backup syncing.
- **Authentication**: stdlib PBKDF2 password hashing & HS256 JWT tokens (`auth.py`) with opt-in `AUTH_ENABLED` toggle.
- **ASR (Speech-to-Text)**: `faster-whisper` (CTranslate2 optimized; default model `small`, configurable to `medium` or `large-v3`).
- **Speaker Diarization**: `pyannote/speaker-diarization-3.1` with energy-based silence threshold fallback (`diarization.py`).
- **Translation**: HuggingFace `transformers` with Meta's `facebook/nllb-200-distilled-600M` (lazy-loaded; maps `hin_Deva` ↔ `eng_Latn`).
- **LLM Extraction**: Multi-provider adapter in `extraction.py` supporting `ollama` (default `llama3.1:8b`), `openai`, `gemini`, and `anthropic`.
- **Evidence Verification**: Deterministic Python text normalizer + unicode NFKC cleaner + 70% word overlap threshold (`evidence.py`).
- **Decision Graph**: `networkx` DiGraph with cycle/conflict detection and BFS downstream impact analysis (`graph.py`).
- **Platform Connectors**: Recall.ai bot dispatcher in `backend/connectors/` for Zoom, Google Meet, and Teams.
- **LiveKit Server**: `livekit-api` for room JWT token generation; connects to Dockerized LiveKit WebRTC server.

### Frontend (Vanilla JS + Tailwind CSS CDN + D3.js)
- `index.html`: Meeting dashboard, file drag-and-drop upload, pipeline progress bar with SSE (`EventSource`), quick-launch live room, and SQLite Recent Meetings history table.
- `room.html`: WebRTC video/audio conferencing room powered by `livekit-client` JS SDK, real-time live transcript feed, "End Meeting & Review" trigger.
- `readback.html`: Human-in-the-loop audit interface. Displays extracted items, audio playback snippet buttons, inline editing, confirmation/rejection toggles.
- `report.html`: Final immutable meeting record presentation, interactive D3.js decision graph visualization, audio clip playback, JSON export.
- `login.html`: Multi-user sign in / sign up page with dev-mode detection.

---

## 📂 Key Invariants & Rules for Any New Model

When modifying this repository, any AI assistant **must adhere to these rules**:

1. **Never Bypass Read-Back**: Extracted items start as `"proposed"`. Only user interaction sets them to `"confirmed"`, `"edited"`, or `"rejected"`. Do not auto-confirm items without human consent.
2. **Evidence Integrity**: Every item generated by the LLM must have an accompanying quote in `evidence`. If `_quote_in_segment` in `evidence.py` cannot verify the quote against the transcript, the item status MUST be set to `"unsupported"`.
3. **No Hallucinated Owners/Deadlines**: If a speaker did not mention a deadline or person responsible, leave `owner: null` and `deadline: null`.
4. **Preserve Open Schema**: `backend/meeting_record.py` defines the canonical Pydantic models (`Segment`, `Evidence`, `Item`, `Edge`, `MeetingRecord`). Any new feature must stay compatible with this JSON format.
5. **Windows Powershell Friendly**: Development is on Windows. Shell scripts and commands should run in standard PowerShell or Docker Desktop.

---

## 📋 Conversation History & Prior Decisions

### Why LiveKit instead of plain WebRTC peer-to-peer?
A WebRTC mesh network does not scale beyond 3-4 users and makes server-side audio capture difficult. LiveKit provides an SFU (Selective Forwarding Unit) that allows capturing each participant's audio track individually with known speaker identity, solving speaker attribution cleanly without needing heavy diarization.

### Why Ollama + local LLM?
Enterprise meetings often contain confidential financial, hiring, or technical data. Running Ollama locally ensures zero external data leakage and eliminates per-minute cloud API bills.

### Why Faster-Whisper instead of standard OpenAI Whisper?
`faster-whisper` uses CTranslate2, delivering 4x faster transcription speed and roughly 50% less RAM usage on CPU (int8 quantization) compared to standard PyTorch implementations.

### Why NLLB-200?
Hindi-English meetings frequently involve code-switching (Hinglish). NLLB-200 distilled provides specialized multi-lingual translation between Indian languages and English with minimal footprint (600M parameters).

---

## 🎯 Next Steps / Suggested Tasks for the Incoming Model

When the user is ready to continue, here are the immediate next milestones:

1. **Phase B Implementation (Speaker Diarization)**:
   - Integrate `pyannote.audio` or a lightweight clustering alternative for single audio files with multiple speakers where participant tracks are mixed into one channel.
   - Map diarization turn timestamps `[start, end]` onto Whisper segment timestamps.

2. **Cloud LLM / Alternate Provider Adapter**:
   - Add optional fallback provider in `backend/extraction.py` (e.g. OpenAI / Anthropic / Google Gemini API) via environment variable `LLM_PROVIDER=ollama|gemini|openai` for systems that do not have enough local RAM to run Ollama 8B.

3. **Evaluation Test Harness**:
   - Build a CLI benchmark script in `eval/` that runs sample Hindi/English audio files through the pipeline and calculates:
     - Word Error Rate (WER)
     - Decision Extraction F1 Score
     - Evidence Citation Precision
     - Processing Latency (P50/P95)

4. **Production Deployment Packaging**:
   - Provide a complete multi-container `docker-compose.yml` bundling FastAPI backend, LiveKit server, and Ollama runner for 1-click cloud or on-prem deployment.
