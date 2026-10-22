"""Privacy-minimal SQLite audit log for API executions (never stores API keys or bodies)."""
from __future__ import annotations

import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "audit_logs.db"


def audit_db_path() -> Path:
    configured = os.getenv("BIDSENTRY_AUDIT_DB_PATH", "").strip()
    return Path(configured).expanduser() if configured else DEFAULT_PATH


def record_api_call(*, audit_id: str, method: str, endpoint: str, status_code: int, duration_ms: float) -> None:
    path = audit_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS audit_runs (
            audit_id TEXT PRIMARY KEY,
            timestamp_utc TEXT NOT NULL,
            method TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            status_code INTEGER NOT NULL,
            duration_ms REAL NOT NULL
        )""")
        conn.execute(
            "INSERT INTO audit_runs(audit_id,timestamp_utc,method,endpoint,status_code,duration_ms) VALUES(?,?,?,?,?,?)",
            (audit_id, datetime.now(timezone.utc).isoformat(), method, endpoint, int(status_code), round(float(duration_ms), 2)),
        )


def recent_api_calls(limit: int = 20) -> list[dict[str, Any]]:
    path = audit_db_path()
    if not path.exists():
        return []
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        exists = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='audit_runs'").fetchone()
        if not exists:
            return []
        rows = conn.execute(
            "SELECT audit_id,timestamp_utc,method,endpoint,status_code,duration_ms FROM audit_runs ORDER BY timestamp_utc DESC LIMIT ?",
            (max(1, min(int(limit), 100)),),
        ).fetchall()
    return [dict(row) for row in rows]


def new_audit_id() -> str:
    return "AUD-" + uuid.uuid4().hex[:10].upper()
