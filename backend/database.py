"""
SQLite database layer — replaces file-based record.json storage.
Database file: meetings/meetings.db (created automatically).

Tables:
  meetings: meeting_id, title, owner_id, source, status, created_at, updated_at, record_json
  items:    item_id, meeting_id, type, status, owner, deadline, text, created_at
"""
from __future__ import annotations

import json
import logging
import os
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Thread-safe SQLite database manager for meeting records and items."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self.conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            isolation_level=None,  # Autocommit mode
        )
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        """Create necessary tables and indices if they do not exist."""
        with self._lock:
            cur = self.conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS meetings (
                    meeting_id TEXT PRIMARY KEY,
                    title TEXT,
                    owner_id TEXT DEFAULT 'dev-user',
                    source TEXT DEFAULT 'upload',
                    status TEXT DEFAULT 'done',
                    created_at TEXT,
                    updated_at TEXT,
                    record_json TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    item_id TEXT PRIMARY KEY,
                    meeting_id TEXT,
                    type TEXT,
                    status TEXT,
                    owner TEXT,
                    deadline TEXT,
                    text TEXT,
                    created_at TEXT,
                    FOREIGN KEY(meeting_id) REFERENCES meetings(meeting_id) ON DELETE CASCADE
                )
            """)
            cur.execute("CREATE INDEX IF NOT EXISTS idx_items_meeting ON items(meeting_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_meetings_owner ON meetings(owner_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_meetings_created ON meetings(created_at)")

    def save_meeting(self, meeting_id: str, record_json: str, owner_id: str = "dev-user") -> None:
        """Upsert meeting record and its individual items."""
        now = datetime.now(timezone.utc).isoformat()
        try:
            data = json.loads(record_json)
        except Exception:
            data = {}

        title = data.get("title") or f"Meeting {meeting_id[:8]}"
        source = data.get("source", "upload")
        status = data.get("status", "done")
        created_at = data.get("created_at") or now
        items = data.get("items", [])

        with self._lock:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO meetings (meeting_id, title, owner_id, source, status, created_at, updated_at, record_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(meeting_id) DO UPDATE SET
                    title=excluded.title,
                    owner_id=coalesce(excluded.owner_id, meetings.owner_id),
                    source=excluded.source,
                    status=excluded.status,
                    updated_at=excluded.updated_at,
                    record_json=excluded.record_json
            """, (meeting_id, title, owner_id, source, status, created_at, now, record_json))

            # Replace items for this meeting
            cur.execute("DELETE FROM items WHERE meeting_id = ?", (meeting_id,))
            for it in items:
                item_id = it.get("id") or str(len(items))
                cur.execute("""
                    INSERT INTO items (item_id, meeting_id, type, status, owner, deadline, text, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item_id,
                    meeting_id,
                    it.get("type", "decision"),
                    it.get("status", "proposed"),
                    it.get("owner"),
                    it.get("deadline"),
                    it.get("text", ""),
                    created_at,
                ))

    def load_meeting(self, meeting_id: str) -> str | None:
        """Fetch raw JSON string for a meeting."""
        with self._lock:
            cur = self.conn.cursor()
            cur.execute("SELECT record_json FROM meetings WHERE meeting_id = ?", (meeting_id,))
            row = cur.fetchone()
            if row:
                return row["record_json"]
        return None

    def list_meetings(self, owner_id: str | None = None, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        """List meetings with summary statistics (item counts)."""
        with self._lock:
            cur = self.conn.cursor()
            params: list[Any] = []
            query = """
                SELECT m.meeting_id, m.title, m.owner_id, m.source, m.status, m.created_at, m.updated_at,
                       COUNT(i.item_id) as total_items,
                       SUM(CASE WHEN i.status IN ('confirmed', 'edited') THEN 1 ELSE 0 END) as confirmed_items,
                       SUM(CASE WHEN i.type = 'decision' THEN 1 ELSE 0 END) as decisions_count,
                       SUM(CASE WHEN i.type = 'action' THEN 1 ELSE 0 END) as actions_count
                FROM meetings m
                LEFT JOIN items i ON m.meeting_id = i.meeting_id
            """
            if owner_id:
                query += " WHERE m.owner_id = ? "
                params.append(owner_id)

            query += " GROUP BY m.meeting_id ORDER BY m.created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])

            cur.execute(query, tuple(params))
            rows = cur.fetchall()

            result = []
            for r in rows:
                result.append({
                    "meeting_id": r["meeting_id"],
                    "title": r["title"],
                    "owner_id": r["owner_id"],
                    "source": r["source"],
                    "status": r["status"],
                    "created_at": r["created_at"],
                    "updated_at": r["updated_at"],
                    "item_counts": {
                        "total": r["total_items"] or 0,
                        "confirmed": r["confirmed_items"] or 0,
                        "decisions": r["decisions_count"] or 0,
                        "actions": r["actions_count"] or 0,
                    }
                })
            return result

    def delete_meeting(self, meeting_id: str) -> bool:
        """Delete a meeting and its cascading items."""
        with self._lock:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM items WHERE meeting_id = ?", (meeting_id,))
            cur.execute("DELETE FROM meetings WHERE meeting_id = ?", (meeting_id,))
            return cur.rowcount > 0

    def search_meetings(self, query: str, owner_id: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
        """Search meetings by title or text in extracted items."""
        pattern = f"%{query.strip()}%"
        with self._lock:
            cur = self.conn.cursor()
            sql = """
                SELECT DISTINCT m.meeting_id, m.title, m.owner_id, m.source, m.status, m.created_at
                FROM meetings m
                LEFT JOIN items i ON m.meeting_id = i.meeting_id
                WHERE (m.title LIKE ? OR i.text LIKE ? OR i.owner LIKE ?)
            """
            params: list[Any] = [pattern, pattern, pattern]
            if owner_id:
                sql += " AND m.owner_id = ?"
                params.append(owner_id)
            sql += " ORDER BY m.created_at DESC LIMIT ?"
            params.append(limit)

            cur.execute(sql, tuple(params))
            rows = cur.fetchall()

            result = []
            for r in rows:
                result.append({
                    "meeting_id": r["meeting_id"],
                    "title": r["title"],
                    "owner_id": r["owner_id"],
                    "source": r["source"],
                    "status": r["status"],
                    "created_at": r["created_at"],
                })
            return result

    def migrate_from_files(self, meetings_dir: Path) -> int:
        """Scan folder for existing record.json files not yet in DB and import them."""
        migrated = 0
        if not meetings_dir.exists():
            return 0

        for m_folder in meetings_dir.iterdir():
            if m_folder.is_dir():
                rec_path = m_folder / "record.json"
                if rec_path.exists():
                    meeting_id = m_folder.name
                    if not self.load_meeting(meeting_id):
                        try:
                            content = rec_path.read_text(encoding="utf-8")
                            self.save_meeting(meeting_id, content)
                            migrated += 1
                        except Exception as e:
                            logger.warning("Could not auto-migrate %s: %s", rec_path, e)
        return migrated


# ── Singleton Access ─────────────────────────────────────────────────────────

_DB_INSTANCE: DatabaseManager | None = None


def get_db() -> DatabaseManager:
    """Return the global DatabaseManager instance."""
    global _DB_INSTANCE
    if _DB_INSTANCE is None:
        meetings_dir = Path(os.getenv("MEETINGS_DIR", "meetings"))
        meetings_dir.mkdir(parents=True, exist_ok=True)
        db_path = meetings_dir / "meetings.db"
        _DB_INSTANCE = DatabaseManager(db_path)
        # Run one-time migration check for existing files
        migrated = _DB_INSTANCE.migrate_from_files(meetings_dir)
        if migrated:
            logger.info("Migrated %d existing JSON records into SQLite", migrated)
    return _DB_INSTANCE
