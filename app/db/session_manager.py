import uuid
from app.db.database import get_connection


def create_session():
    session_id = str(uuid.uuid4())

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO sessions (session_id) VALUES (?)",
        (session_id,)
    )

    conn.commit()
    conn.close()

    return session_id


def log_message(session_id: str, role: str, content: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages (session_id, role, content)
        VALUES (?, ?, ?)
        """,
        (session_id, role, content)
    )

    conn.commit()
    conn.close()
