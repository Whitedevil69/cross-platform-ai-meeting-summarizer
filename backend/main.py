"""
FastAPI — central hub for the Meeting Intelligence System.

Routes:
  POST   /api/meetings/upload          Upload audio/video file → full pipeline
  GET    /api/meetings/{id}            Get meeting record JSON
  GET    /api/meetings/{id}/status     SSE stream for pipeline progress
  POST   /api/meetings/{id}/confirm    Submit read-back decisions
  GET    /api/meetings/{id}/report     Final report (confirmed items + stats)
  GET    /api/meetings/{id}/audio/{seg} Serve audio clip WAV
  GET    /api/rooms/token              LiveKit join token
  POST   /api/rooms/create             Create a new room (live meeting)
  WS     /ws/room/{room_id}            WebSocket audio stream (live room)
  GET    /api/graph                    Decision graph JSON for D3
  GET    /api/graph/impact/{item_id}   Impact analysis for an item
"""
from __future__ import annotations

import asyncio
import io
import json
import logging
import os
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import AsyncGenerator

import aiofiles
from fastapi import (
    BackgroundTasks, FastAPI, File, Form, HTTPException, Request,
    UploadFile, WebSocket, WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ── local imports ─────────────────────────────────────────────────────────────
from .audio_store import (
    clip_path_absolute, load_meeting_record,
    meeting_dir, save_audio, save_meeting_record,
)
from .evidence import evidence_summary, verify_items
from .extraction import extract_items
from .graph import get_graph
from .livekit_manager import generate_token, get_livekit_url, room_name_for_meeting
from .meeting_record import Item, MeetingRecord, ItemStatus

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Syncra Workplace — Meeting Intelligence System",
    description="Cross-platform, evidence-linked AI meeting intelligence for Hindi–English teams.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_no_cache_headers(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/app"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

# Serve frontend
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/app", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

# Serve meeting audio clips
MEETINGS_DIR = Path(os.getenv("MEETINGS_DIR", "meetings"))

# ── In-memory status store (keyed by meeting_id) ─────────────────────────────
_status: dict[str, dict] = {}


def _set_status(meeting_id: str, stage: str, progress: int, message: str = ""):
    _status[meeting_id] = {"stage": stage, "progress": progress, "message": message}


# ── Pipeline helpers ──────────────────────────────────────────────────────────

async def _run_pipeline(meeting_id: str, audio_path: Path, title: str | None, owner_id: str = "dev-user", workspace_id: str = "ws-engineering"):
    """
    Full offline pipeline (run in background thread):
    ASR → translation → extraction → evidence check → save.
    """
    import asyncio
    loop = asyncio.get_event_loop()

    try:
        _set_status(meeting_id, "transcribing", 10, "Running speech recognition…")

        # 1. ASR (CPU-bound — run in thread pool)
        from .asr import transcribe
        segments = await loop.run_in_executor(
            None, transcribe, str(audio_path), meeting_id
        )
        _set_status(meeting_id, "transcribed", 35, f"Transcribed {len(segments)} segments")

        # 1b. Speaker Diarization (Phase B — optional)
        from .diarization import assign_speakers
        if os.getenv("DIARIZATION_ENABLED", "false").lower() == "true":
            _set_status(meeting_id, "diarizing", 38, "Assigning speaker labels…")
            segments = await loop.run_in_executor(
                None, assign_speakers, segments, audio_path
            )
            speaker_count = len(set(s.speaker for s in segments if s.speaker != "Unknown"))
            _set_status(meeting_id, "diarized", 42, f"Detected {speaker_count} speaker(s)")

        # 2. Translation (optional — only if Hindi segments exist)
        hindi_segs = [s for s in segments if s.language in ("hi", "hin_Deva")]
        if hindi_segs:
            _set_status(meeting_id, "translating", 45, f"Translating {len(hindi_segs)} Hindi segment(s)…")
            from .translation import is_translation_available, translate_segments_to_english
            if is_translation_available():
                segments = await loop.run_in_executor(
                    None, translate_segments_to_english, segments
                )
            _set_status(meeting_id, "translated", 55, "Translation complete")

        # 3. LLM extraction
        _set_status(meeting_id, "extracting", 60, "Extracting decisions and actions (LLM)…")
        items = await loop.run_in_executor(
            None, extract_items, segments, meeting_id
        )
        _set_status(meeting_id, "extracted", 75, f"Extracted {len(items)} item(s)")

        # 4. Evidence checking
        _set_status(meeting_id, "checking", 80, "Verifying evidence citations…")
        items = await loop.run_in_executor(
            None, verify_items, items, segments
        )
        summary = evidence_summary(items)
        _set_status(meeting_id, "checked", 88, f"Evidence accuracy: {summary['evidence_accuracy']*100:.0f}%")

        # 5. Populate clip_path in evidence
        for item in items:
            for ev in item.evidence:
                clip = clip_path_absolute(meeting_id, ev.segment_id)
                if clip.exists():
                    ev.clip_path = f"/api/meetings/{meeting_id}/audio/{ev.segment_id}"

        # 6. Build and save Meeting Record
        record = MeetingRecord(
            meeting_id=meeting_id,
            title=title or f"Meeting {meeting_id[:8]}",
            source="upload",
            audio_path=str(audio_path),
            segments=segments,
            items=items,
        )
        _set_status(meeting_id, "saving", 95, "Saving meeting record…")
        save_meeting_record(meeting_id, record.model_dump_json(indent=2), owner_id=owner_id, workspace_id=workspace_id)
        _set_status(meeting_id, "done", 100, "Pipeline complete")
        logger.info("Pipeline complete for meeting %s — %d items", meeting_id, len(items))

    except Exception as e:
        logger.exception("Pipeline failed for meeting %s", meeting_id)
        _set_status(meeting_id, "error", 0, str(e))


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {"message": "Meeting Intelligence API", "docs": "/docs", "app": "/app"}


# ── Auth endpoints ────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/api/auth/register", tags=["auth"])
async def register(req: RegisterRequest):
    """Register a new user account."""
    from .auth import UserDB
    db = UserDB()
    if db.get_user(req.email):
        raise HTTPException(400, "Email already registered")
    user = db.create_user(req.email, req.password)
    return {"user_id": user["user_id"], "email": user["email"]}


@app.post("/api/auth/login", tags=["auth"])
async def login(req: LoginRequest):
    """Login and receive a JWT access token."""
    from .auth import UserDB, create_access_token
    db = UserDB()
    if not db.verify_password(req.email, req.password):
        raise HTTPException(401, "Invalid email or password")
    user = db.get_user(req.email)
    token = create_access_token(user["user_id"], user["email"])
    return {"access_token": token, "token_type": "bearer", "user_id": user["user_id"]}


@app.get("/api/auth/me", tags=["auth"])
async def me(request: Request):
    """Get current user info."""
    from .auth import get_current_user_id
    auth = request.headers.get("Authorization")
    user_id = get_current_user_id(auth)
    return {"user_id": user_id, "auth_enabled": os.getenv("AUTH_ENABLED", "false").lower() == "true"}

@app.post("/api/upload")
@app.post("/api/meetings/upload")
async def upload_meeting(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str | None = Form(None),
    workspace_id: str | None = Form(None),
):
    """Upload an audio/video file and start the AI pipeline with workspace isolation."""
    from .auth import get_current_user_id
    owner_id = get_current_user_id(request.headers.get("Authorization"))
    meeting_id = str(uuid.uuid4())
    ext = Path(file.filename or "audio.wav").suffix or ".wav"

    # Save uploaded file
    audio_bytes = await file.read()
    audio_path = save_audio(meeting_id, audio_bytes, ext)
    _set_status(meeting_id, "queued", 5, "File received, pipeline starting…")

    background_tasks.add_task(
        _run_pipeline,
        meeting_id,
        audio_path,
        title,
        owner_id,
        workspace_id or "ws-engineering",
    )

    return {
        "meeting_id": meeting_id,
        "status_url": f"/api/meetings/{meeting_id}/status",
        "record_url":  f"/api/meetings/{meeting_id}",
    }


@app.get("/api/meetings/{meeting_id}")
async def get_meeting(meeting_id: str):
    """Return the full Meeting Record JSON."""
    raw = load_meeting_record(meeting_id)
    if raw is None:
        raise HTTPException(404, "Meeting not found")
    return JSONResponse(content=json.loads(raw))


@app.get("/api/meetings/{meeting_id}/status")
async def stream_status(meeting_id: str):
    """
    Server-Sent Events stream for pipeline progress.
    Client listens until stage == 'done' or 'error'.
    """
    async def generator() -> AsyncGenerator[str, None]:
        for _ in range(300):  # max 5 minutes
            status = _status.get(meeting_id, {"stage": "unknown", "progress": 0, "message": ""})
            yield f"data: {json.dumps(status)}\n\n"
            if status["stage"] in ("done", "error"):
                break
            await asyncio.sleep(1)

    return StreamingResponse(generator(), media_type="text/event-stream")


class ConfirmRequest(BaseModel):
    decisions: list[dict]  # [{id, status, edited_text?, note?}]


@app.post("/api/meetings/{meeting_id}/confirm")
async def confirm_items(meeting_id: str, req: ConfirmRequest):
    """Submit read-back decisions (confirm / edit / reject) for each item."""
    raw = load_meeting_record(meeting_id)
    if raw is None:
        raise HTTPException(404, "Meeting not found")

    record = MeetingRecord.model_validate_json(raw)

    confirmed_count = 0
    for decision in req.decisions:
        item = record.get_item(decision["id"])
        if item is None:
            continue
        new_status: ItemStatus = decision.get("status", "confirmed")
        if new_status in ("confirmed", "edited", "rejected"):
            item.status = new_status
            if new_status == "edited" and decision.get("edited_text"):
                item.edited_text = decision["edited_text"]
            item.note = decision.get("note")
            if new_status in ("confirmed", "edited"):
                confirmed_count += 1

    # Update graph with confirmed items
    graph = get_graph()
    graph.add_meeting(record)

    save_meeting_record(meeting_id, record.model_dump_json(indent=2))

    return {
        "meeting_id": meeting_id,
        "confirmed": confirmed_count,
        "total": len(record.items),
        "report_url": f"/api/meetings/{meeting_id}/report",
    }


@app.get("/api/meetings/{meeting_id}/report")
async def get_report(meeting_id: str):
    """Return final report with confirmed items, stats, and evidence summary."""
    raw = load_meeting_record(meeting_id)
    if raw is None:
        raise HTTPException(404, "Meeting not found")

    record = MeetingRecord.model_validate_json(raw)

    confirmed = [i for i in record.items if i.status in ("confirmed", "edited")]
    rejected  = [i for i in record.items if i.status == "rejected"]
    proposed  = [i for i in record.items if i.status == "proposed"]
    unsupported = [i for i in record.items if i.status == "unsupported"]

    return {
        "meeting_id":   record.meeting_id,
        "title":        record.title,
        "created_at":   str(record.created_at),
        "source":       record.source,
        "segment_count": len(record.segments),
        "items": {
            "confirmed":   [i.model_dump() for i in confirmed],
            "proposed":    [i.model_dump() for i in proposed],
            "rejected":    [i.model_dump() for i in rejected],
            "unsupported": [i.model_dump() for i in unsupported],
        },
        "stats": {
            "total_items": len(record.items),
            "confirmed":   len(confirmed),
            "rejected":    len(rejected),
            "unsupported": len(unsupported),
            **evidence_summary(record.items),
        },
        "segments": [s.model_dump() for s in record.segments],
    }


@app.get("/api/meetings/{meeting_id}/audio/{segment_id}")
async def serve_clip(meeting_id: str, segment_id: int):
    """Serve WAV audio clip for a transcript segment."""
    clip = clip_path_absolute(meeting_id, segment_id)
    if not clip.exists():
        raise HTTPException(404, "Clip not found")
    return FileResponse(str(clip), media_type="audio/wav")


# ── LiveKit / Room endpoints ──────────────────────────────────────────────────

class CreateRoomRequest(BaseModel):
    title: str | None = None


@app.post("/api/rooms/create")
async def create_room(req: CreateRoomRequest):
    """Create a new live meeting room and return meeting_id + LiveKit URL."""
    meeting_id = str(uuid.uuid4())
    room_name  = room_name_for_meeting(meeting_id)
    _set_status(meeting_id, "live", 0, "Room created, waiting for participants")

    # Pre-create a blank Meeting Record
    record = MeetingRecord(
        meeting_id=meeting_id,
        title=req.title or f"Live Meeting {meeting_id[:8]}",
        source="browser_room",
    )
    save_meeting_record(meeting_id, record.model_dump_json(indent=2))

    return {
        "meeting_id":  meeting_id,
        "room_name":   room_name,
        "livekit_url": get_livekit_url(),
        "join_url":    f"/app/room.html?meeting={meeting_id}",
    }


@app.get("/api/rooms/token")
async def get_room_token(meeting_id: str, name: str):
    """Generate a LiveKit JWT token for a participant."""
    if not name.strip():
        raise HTTPException(400, "Name is required")
    room_name = room_name_for_meeting(meeting_id)
    try:
        token = generate_token(room_name, name.strip())
    except Exception as e:
        logger.error("Token generation failed: %s", e)
        raise HTTPException(500, f"Token error: {e}")
    return {
        "token":       token,
        "room_name":   room_name,
        "livekit_url": get_livekit_url(),
    }


# ── WebSocket — live audio processing ────────────────────────────────────────

@app.websocket("/ws/room/{meeting_id}")
async def websocket_audio(ws: WebSocket, meeting_id: str):
    """
    Receive raw audio chunks from browser (PCM/WebM), transcribe with Whisper,
    and stream back transcript segments in real time.
    Audio is also accumulated for final pipeline run when room ends.
    """
    await ws.accept()
    from .asr import _get_model
    from .meeting_record import Segment

    logger.info("WS connected: meeting %s", meeting_id)
    audio_buffer = bytearray()
    segments_all: list[Segment] = []
    seg_id_counter = 0

    try:
        while True:
            msg = await ws.receive()

            if "bytes" in msg and msg["bytes"]:
                audio_buffer.extend(msg["bytes"])

                # Process when we have ~3 seconds of audio (48kHz stereo webm ≈ 24KB chunks)
                if len(audio_buffer) >= 48000:
                    chunk = bytes(audio_buffer)
                    audio_buffer.clear()

                    # Write to temp file, transcribe
                    loop = asyncio.get_event_loop()
                    segs = await loop.run_in_executor(
                        None, _transcribe_chunk, chunk, meeting_id, seg_id_counter
                    )
                    seg_id_counter += len(segs)
                    segments_all.extend(segs)

                    # Stream back to client
                    for seg in segs:
                        await ws.send_text(json.dumps({
                            "type": "segment",
                            "data": seg.model_dump(),
                        }))

            elif "text" in msg:
                try:
                    data = json.loads(msg["text"])
                except Exception:
                    continue

                if data.get("type") == "end_meeting":
                    # Run full extraction pipeline on accumulated audio
                    await ws.send_text(json.dumps({"type": "status", "message": "Processing meeting…"}))
                    # Save accumulated segments to record
                    raw = load_meeting_record(meeting_id)
                    if raw:
                        record = MeetingRecord.model_validate_json(raw)
                        record.segments = segments_all
                        save_meeting_record(meeting_id, record.model_dump_json(indent=2))

                    # Run extraction + evidence in background
                    asyncio.create_task(_finalize_live_meeting(meeting_id, segments_all))
                    await ws.send_text(json.dumps({
                        "type": "pipeline_started",
                        "readback_url": f"/app/readback.html?meeting={meeting_id}",
                    }))
                    break

    except WebSocketDisconnect:
        logger.info("WS disconnected: meeting %s", meeting_id)
    except Exception as e:
        logger.error("WS error: %s", e)
        try:
            await ws.send_text(json.dumps({"type": "error", "message": str(e)}))
        except Exception:
            pass


def _transcribe_chunk(chunk: bytes, meeting_id: str, id_offset: int) -> list:
    """Transcribe a raw audio chunk (runs in thread pool)."""
    import tempfile
    from .asr import _get_model
    from .meeting_record import Segment

    model = _get_model()
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
        f.write(chunk)
        tmp_path = f.name

    try:
        segments_raw, info = model.transcribe(
            tmp_path,
            beam_size=3,
            language=None,
            multilingual=True,
            vad_filter=True,
        )
        result = []
        for i, raw in enumerate(segments_raw):
            seg = Segment(
                id=id_offset + i,
                start=round(raw.start, 3),
                end=round(raw.end, 3),
                text=raw.text.strip(),
                language=raw.language or info.language,
            )
            result.append(seg)
    finally:
        os.unlink(tmp_path)

    return result


async def _finalize_live_meeting(meeting_id: str, segments: list):
    """Run extraction + evidence check on live meeting segments."""
    import asyncio
    loop = asyncio.get_event_loop()

    _set_status(meeting_id, "extracting", 60, "Extracting decisions…")
    items = await loop.run_in_executor(None, extract_items, segments, meeting_id)
    items = await loop.run_in_executor(None, verify_items, items, segments)

    # Attach clip paths
    for item in items:
        for ev in item.evidence:
            clip = clip_path_absolute(meeting_id, ev.segment_id)
            if clip.exists():
                ev.clip_path = f"/api/meetings/{meeting_id}/audio/{ev.segment_id}"

    raw = load_meeting_record(meeting_id)
    if raw:
        record = MeetingRecord.model_validate_json(raw)
        record.items = items
        save_meeting_record(meeting_id, record.model_dump_json(indent=2))

    _set_status(meeting_id, "done", 100, "Ready for read-back")


class CreateWorkspaceRequest(BaseModel):
    name: str
    description: str = ""
    icon: str = "💼"
    department: str = "General"
    members_count: int = 1


@app.get("/api/workspaces", tags=["workspaces"])
async def list_workspaces_endpoint():
    """List all department workspaces with real meeting, decision, and storage metrics."""
    from .database import get_db
    workspaces = get_db().list_workspaces()
    return {"workspaces": workspaces, "count": len(workspaces)}


@app.post("/api/workspaces", tags=["workspaces"])
async def create_workspace_endpoint(req: CreateWorkspaceRequest):
    """Create a new department workspace with isolated meeting storage."""
    from .database import get_db
    if not req.name.strip():
        raise HTTPException(400, "Workspace name cannot be empty")
    ws = get_db().create_workspace(
        name=req.name,
        description=req.description,
        icon=req.icon or "💼",
        department=req.department or "General",
        members_count=req.members_count or 1,
    )
    return {"status": "ok", "workspace": ws}


@app.get("/api/workspaces/{workspace_id}", tags=["workspaces"])
async def get_workspace_endpoint(workspace_id: str):
    """Get single workspace details and metrics."""
    from .database import get_db
    ws = get_db().get_workspace(workspace_id)
    if not ws:
        raise HTTPException(404, "Workspace not found")
    return {"workspace": ws}


@app.get("/api/meetings", tags=["meetings"])
async def list_meetings(
    limit: int = 20,
    offset: int = 0,
    search: str | None = None,
    workspace_id: str | None = None,
):
    """List all meetings with pagination, optional search, and workspace isolation."""
    from .database import get_db
    db = get_db()
    if search:
        meetings = db.search_meetings(search, workspace_id=workspace_id)
    else:
        meetings = db.list_meetings(workspace_id=workspace_id, limit=limit, offset=offset)
    return {
        "meetings": meetings,
        "limit": limit,
        "offset": offset,
        "count": len(meetings),
        "workspace_id": workspace_id or "all",
    }


@app.delete("/api/meetings/{meeting_id}", tags=["meetings"])
async def delete_meeting_endpoint(meeting_id: str):
    """Delete a meeting record and its audio files."""
    from .database import get_db
    deleted_db = get_db().delete_meeting(meeting_id)
    # also delete audio folder
    folder = MEETINGS_DIR / meeting_id
    deleted_files = False
    if folder.exists():
        shutil.rmtree(folder)
        deleted_files = True
    if not deleted_db and not deleted_files:
        raise HTTPException(404, "Meeting not found")
    return {"deleted": meeting_id}


# ── Platform Connectors (Phase E — Recall.ai) ─────────────────────────────────

class JoinMeetingRequest(BaseModel):
    meeting_url: str
    title: str | None = None


@app.post("/api/connectors/join", tags=["connectors"])
async def join_external_meeting(req: JoinMeetingRequest):
    """
    Send a Recall.ai recording bot into a Zoom, Google Meet, or Microsoft Teams meeting.
    """
    from .connectors.recallai import create_bot
    from .connectors.router import detect_platform, parse_meeting_url

    platform = detect_platform(req.meeting_url)
    if platform == "unknown":
        raise HTTPException(400, "Unsupported meeting URL. Must be Zoom, Google Meet, or Teams.")

    parsed = parse_meeting_url(req.meeting_url)
    meeting_id = str(uuid.uuid4())
    meeting_title = req.title or f"{platform.replace('_', ' ').title()} Meeting"

    # Pre-create Meeting Record
    record = MeetingRecord(
        meeting_id=meeting_id,
        title=meeting_title,
        source="connector",
    )
    save_meeting_record(meeting_id, record.model_dump_json(indent=2))
    _set_status(meeting_id, "connecting", 10, f"Dispatching bot to {platform} meeting...")

    try:
        bot_data = await create_bot(req.meeting_url, meeting_title, meeting_id)
    except Exception as e:
        logger.error("Failed to create Recall.ai bot: %s", e)
        _set_status(meeting_id, "error", 0, str(e))
        raise HTTPException(502, f"Recall.ai error: {e}")

    bot_id = bot_data.get("bot_id") or bot_data.get("id")
    _set_status(meeting_id, "bot_joined", 25, "Bot active in meeting")

    return {
        "meeting_id": meeting_id,
        "bot_id": bot_id,
        "platform": platform,
        "details": parsed,
        "status": "bot_dispatched",
        "is_simulation": bot_data.get("is_simulation", False),
        "record_url": f"/api/meetings/{meeting_id}",
    }


@app.get("/api/connectors/bots/{bot_id}/status", tags=["connectors"])
async def get_bot_status_endpoint(bot_id: str):
    """Get the current live status of a Recall.ai bot."""
    from .connectors.recallai import get_bot_status
    try:
        status_data = await get_bot_status(bot_id)
        return status_data
    except Exception as e:
        logger.error("Failed to fetch bot status: %s", e)
        raise HTTPException(500, f"Error fetching bot status: {e}")


@app.delete("/api/connectors/bots/{bot_id}", tags=["connectors"])
async def remove_bot_endpoint(bot_id: str):
    """Stop and remove a Recall.ai bot from a meeting."""
    from .connectors.recallai import delete_bot
    try:
        success = await delete_bot(bot_id)
        return {"bot_id": bot_id, "removed": success}
    except Exception as e:
        logger.error("Failed to remove bot: %s", e)
        raise HTTPException(500, f"Error deleting bot: {e}")


@app.post("/api/webhooks/recall", tags=["connectors"])
async def recall_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Receive webhook callbacks from Recall.ai (transcript chunks or bot completion).
    """
    from .connectors.recallai import parse_transcript_webhook, verify_webhook_signature

    body = await request.body()
    secret = os.getenv("RECALL_WEBHOOK_SECRET", "")
    if secret:
        sig = request.headers.get("X-Recall-Signature", "")
        if not verify_webhook_signature(body, sig, secret):
            raise HTTPException(401, "Invalid webhook signature")

    try:
        payload = json.loads(body)
    except Exception:
        raise HTTPException(400, "Invalid JSON payload")

    event = payload.get("event")
    data = payload.get("data", {})
    bot_metadata = data.get("bot", {}).get("metadata", {})
    meeting_id = bot_metadata.get("meeting_id") or payload.get("meeting_id")

    if not meeting_id:
        return {"status": "ignored", "reason": "no meeting_id in payload"}

    if event == "transcript.data":
        segments = parse_transcript_webhook(payload, meeting_id)
        raw = load_meeting_record(meeting_id)
        if raw:
            record = MeetingRecord.model_validate_json(raw)
            # Merge or append segments
            record.segments.extend(segments)
            save_meeting_record(meeting_id, record.model_dump_json(indent=2))
        return {"status": "ok", "segments_received": len(segments)}

    elif event in ("bot.done", "bot.status_change") and data.get("code") in ("done", "fatal"):
        raw = load_meeting_record(meeting_id)
        if raw:
            record = MeetingRecord.model_validate_json(raw)
            if record.segments:
                background_tasks.add_task(_finalize_live_meeting, meeting_id, record.segments)
        return {"status": "finalizing_pipeline"}

    return {"status": "event_received", "event": event}


# ── Decision Graph endpoints ──────────────────────────────────────────────────

@app.get("/api/graph")
async def get_decision_graph():
    """Return the full decision graph as node-link JSON for D3."""
    graph = get_graph()
    return graph.to_dict()


@app.get("/api/graph/impact/{item_id}")
async def impact_analysis(item_id: str):
    """Return impact analysis for a given item."""
    graph = get_graph()
    return {
        "item_id": item_id,
        "affected": graph.impact_analysis(item_id),
        "what_if": graph.what_if_deadline_changes(item_id),
    }


@app.get("/api/graph/conflicts")
async def check_conflicts(meeting_id: str, item_id: str):
    """Check a proposed item for conflicts with existing confirmed decisions."""
    raw = load_meeting_record(meeting_id)
    if not raw:
        raise HTTPException(404, "Meeting not found")
    record = MeetingRecord.model_validate_json(raw)
    item = record.get_item(item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    graph = get_graph()
    return {"conflicts": graph.flag_conflicts(item)}


# ── AI Companion QA / Cross-Meeting Intelligence ─────────────────────────────

class AICompanionRequest(BaseModel):
    query: str
    meeting_id: str | None = None


@app.post("/api/ai/companion", tags=["ai"])
async def ai_companion_query(req: AICompanionRequest):
    """
    Interactive AI Companion: answers questions about past meetings, decisions,
    assigned owners, deadlines, and platform capabilities with exact evidence.
    """
    query_text = req.query.strip()
    if not query_text:
        raise HTTPException(400, "Query cannot be empty")

    lower_q = query_text.lower()

    # 1. Architectural & cross-platform questions
    if any(k in lower_q for k in ["cross platform", "cross-platform", "how do we", "how does it work", "recall", "bot"]):
        return {
            "answer": (
                "**Cross-Platform Meeting Intelligence** connects Zoom, Google Meet, and Microsoft Teams through 3 core pillars:\n\n"
                "1. **Headless Bot Dispatcher (Recall.ai)**: Dispatches an autonomous recording bot to any meeting URL with zero software install required for participants.\n"
                "2. **Canonical Schema (MeetingRecord)**: Ingests audio from any platform into a unified JSON format with sub-segment timestamps, Hindi-English translation (NLLB-200), and speaker diarization.\n"
                "3. **Zero-Install WebRTC Rooms**: Allows participants to join directly from any browser with video, microphone, and live transcript streaming.\n\n"
                "Every extracted claim cites exact audio timestamps and transcript quotes."
            ),
            "citations": [],
            "source": "system_knowledge"
        }

    # 2. Database search across meeting records
    from .database import get_db
    db = get_db()
    all_meetings = db.list_meetings()
    relevant_items = []

    tokens = [t for t in lower_q.split() if len(t) > 2]

    for m in all_meetings:
        m_id = m.get("meeting_id")
        try:
            rec_str = db.load_meeting(m_id)
            if not rec_str:
                continue
            rec_data = json.loads(rec_str)
            for it in rec_data.get("items", []):
                text = (it.get("text") or "").lower()
                owner = (it.get("owner") or "").lower()
                evidence_text = " ".join([ev.get("quote", "") for ev in it.get("evidence", [])]).lower()

                if any(t in text or t in owner or t in evidence_text for t in tokens) or not tokens:
                    relevant_items.append({
                        "meeting_title": rec_data.get("title", "Untitled Meeting"),
                        "meeting_id": m_id,
                        "item": it
                    })
        except Exception as e:
            logger.debug("Failed reading meeting for companion query: %s", e)

    # 3. If items found in DB, return them with citations
    if relevant_items:
        lines = []
        citations = []
        for ri in relevant_items[:6]:
            it = ri["item"]
            typ = (it.get("type") or "item").upper()
            txt = it.get("text", "")
            own = it.get("owner")
            dl = it.get("deadline")
            m_title = ri["meeting_title"]

            line = f"• **[{typ}]** {txt}"
            if own:
                line += f" — *Assigned to: {own}*"
            if dl:
                line += f" *(Deadline: {dl})*"
            line += f"  \n  ↳ *Meeting: {m_title}*"
            lines.append(line)

            for ev in it.get("evidence", []):
                citations.append({
                    "meeting_title": m_title,
                    "meeting_id": ri["meeting_id"],
                    "segment_id": ev.get("segment_id"),
                    "quote": ev.get("quote")
                })

        answer = f"Found **{len(relevant_items)} relevant decision/action items** for your question:\n\n" + "\n\n".join(lines)
        return {
            "answer": answer,
            "citations": citations,
            "source": "meeting_records",
            "matches_count": len(relevant_items)
        }

    # 4. Fallback to local Ollama LLM if available (non-blocking thread)
    try:
        import ollama
        def _chat():
            return ollama.chat(
                model=os.getenv("OLLAMA_MODEL", "qwen3:8b"),
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are the AI Companion in Meeting Intelligence. "
                            "Answer the user's question directly and informatively in 2-4 sentences. "
                            "Focus on meeting insights, action items, decisions, and Hindi-English multi-platform collaboration."
                        )
                    },
                    {"role": "user", "content": query_text}
                ],
                options={"temperature": 0.2, "num_predict": 200}
            )
        resp = await asyncio.wait_for(asyncio.to_thread(_chat), timeout=8.0)
        return {
            "answer": resp.message.content,
            "citations": [],
            "source": "ollama_llm"
        }
    except Exception as e:
        logger.debug("Ollama chat fallback skipped: %s", e)

    # 5. Default informative response
    return {
        "answer": (
            f"I searched your meeting records for '{query_text}', but did not find matching decisions or action items. "
            "You can upload a meeting recording, dispatch a bot to Zoom/Meet/Teams, or start a live room to extract new intelligence!"
        ),
        "citations": [],
        "source": "search_empty"
    }
