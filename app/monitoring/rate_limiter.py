from app.db.database import get_connection
from app.config import settings


def is_rate_limited(session_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM rate_limits
        WHERE session_id = ?
        AND created_at >= datetime('now', '-1 minute')
    """, (session_id,))

    count = cursor.fetchone()[0]
    conn.close()

    return count >= settings.MAX_REQUESTS_PER_MINUTE



def record_request(session_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO rate_limits (session_id)
        VALUES (?)
    """, (session_id,))

    conn.commit()
    conn.close()
