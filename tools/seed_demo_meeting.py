import sys, os
sys.path.insert(0, os.path.abspath('.'))
import json
from datetime import datetime, timezone
from backend.database import get_db
from backend.meeting_record import MeetingRecord, Segment, Item, Evidence, Edge

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

db = get_db()

meeting_id = "sprint-sync-2026"
now = datetime.now(timezone.utc).isoformat()

segments = [
    Segment(id=0, start=0.0, end=4.2, speaker="Vikram", text="Toh humne decide kiya ki hum PostgreSQL use karenge database ke liye.", language="hi"),
    Segment(id=1, start=4.2, end=9.0, speaker="Vikram", text="Aur authentication ke liye hum OAuth2 with Google login implement karenge.", language="hi"),
    Segment(id=2, start=9.0, end=14.5, speaker="Priya", text="Priya will handle the backend API integration by Wednesday.", language="en"),
    Segment(id=3, start=14.5, end=20.3, speaker="Rahul", text="Amit ko deployment script likhna hai before the release on Thursday.", language="hi"),
    Segment(id=4, start=20.3, end=26.0, speaker="Priya", text="Kya hume GraphQL bhi consider karna chahiye instead of REST?", language="hi"),
    Segment(id=5, start=26.0, end=31.4, speaker="Vikram", text="We will use Docker Compose for the local development environment — final decision.", language="en")
]

items = [
    Item(
        id="dec-001",
        type="decision",
        text="Adopt PostgreSQL with pgvector for the primary database",
        status="proposed",
        evidence=[Evidence(segment_id=0, quote="Toh humne decide kiya ki hum PostgreSQL use karenge database ke liye.", timestamp=0.0)]
    ),
    Item(
        id="dec-002",
        type="decision",
        text="Standardize on Docker Compose for local microservices orchestration",
        status="proposed",
        evidence=[Evidence(segment_id=5, quote="We will use Docker Compose for the local development environment — final decision.", timestamp=26.0)]
    ),
    Item(
        id="act-001",
        type="action",
        text="Integrate OAuth2 Google sign-in and backend JWT session verification",
        owner="Priya Sharma",
        deadline="Wednesday 5 PM",
        status="proposed",
        evidence=[Evidence(segment_id=1, quote="Aur authentication ke liye hum OAuth2 with Google login implement karenge.", timestamp=4.2)]
    ),
    Item(
        id="act-002",
        type="action",
        text="Create automated deployment pipeline script for staging release",
        owner="Amit Kumar",
        deadline="Thursday",
        status="proposed",
        evidence=[Evidence(segment_id=3, quote="Amit ko deployment script likhna hai before the release on Thursday.", timestamp=14.5)]
    ),
    Item(
        id="que-001",
        type="question",
        text="Should we evaluate GraphQL endpoints alongside REST APIs for mobile client?",
        status="proposed",
        evidence=[Evidence(segment_id=4, quote="Kya hume GraphQL bhi consider karna chahiye instead of REST?", timestamp=20.3)]
    )
]

rec = MeetingRecord(
    meeting_id=meeting_id,
    title="Executive Sprint Planning — Architecture & Pipelines",
    owner_id="dev-user",
    source="upload",
    created_at=now,
    segments=segments,
    items=items,
    edges=[]
)

db.save_meeting(meeting_id, rec.model_dump_json(indent=2), "dev-user")
print("[OK] Demo meeting sprint-sync-2026 saved successfully!")
