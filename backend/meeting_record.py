"""
Meeting Record — open JSON schema (Pydantic v2)
Every pipeline stage reads/writes these models.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field


# ── Transcript ──────────────────────────────────────────────────────────────

class Segment(BaseModel):
    id: int
    start: float
    end: float
    speaker: str = "Unknown"
    text: str
    language: str = "en"          # ISO 639-1 or Whisper lang code
    translated_text: Optional[str] = None   # populated if NLLB ran


# ── Evidence ─────────────────────────────────────────────────────────────────

class Evidence(BaseModel):
    segment_id: int
    quote: str                    # exact words cited by LLM
    timestamp: float              # start time of segment
    clip_path: Optional[str] = None  # relative path to .wav clip


# ── Extracted items ──────────────────────────────────────────────────────────

ItemType   = Literal["decision", "action", "question"]
ItemStatus = Literal["proposed", "confirmed", "edited", "rejected", "unsupported"]

class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: ItemType
    text: str
    owner: Optional[str] = None
    deadline: Optional[str] = None
    evidence: list[Evidence] = Field(default_factory=list)
    status: ItemStatus = "proposed"
    edited_text: Optional[str] = None   # filled in during read-back if edited
    note: Optional[str] = None          # reviewer's note


# ── Decision graph edges ─────────────────────────────────────────────────────

EdgeType   = Literal["depends_on", "supersedes", "assigned_to", "due_on"]
EdgeStatus = Literal["proposed", "confirmed"]

class Edge(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    from_id: str
    to_id: str
    type: EdgeType
    status: EdgeStatus = "proposed"
    evidence: list[Evidence] = Field(default_factory=list)


# ── Top-level Meeting Record ─────────────────────────────────────────────────

SourceType = Literal["upload", "microphone", "browser_room", "connector"]

class MeetingRecord(BaseModel):
    meeting_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = None
    owner_id: str = "dev-user"
    source: SourceType = "upload"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    audio_path: Optional[str] = None    # original audio file
    segments: list[Segment] = Field(default_factory=list)
    items: list[Item] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)

    # convenience helpers
    def confirmed_items(self) -> list[Item]:
        return [i for i in self.items if i.status in ("confirmed", "edited")]

    def proposed_items(self) -> list[Item]:
        return [i for i in self.items if i.status == "proposed"]

    def get_item(self, item_id: str) -> Optional[Item]:
        return next((i for i in self.items if i.id == item_id), None)

    def get_segment(self, seg_id: int) -> Optional[Segment]:
        return next((s for s in self.segments if s.id == seg_id), None)
