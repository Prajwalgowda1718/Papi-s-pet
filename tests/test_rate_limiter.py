import sqlite3
import pytest

from app.monitoring.rate_limiter import is_rate_limited, record_request
from app.db.database import get_connection


def setup_test_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rate_limits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def test_rate_limit_trigger():
    setup_test_db()

    session_id = "test-session"

    # Insert maximum allowed requests
    for _ in range(10):
        record_request(session_id)

    assert is_rate_limited(session_id) is True
