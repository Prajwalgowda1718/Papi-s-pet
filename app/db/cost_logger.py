from app.db.database import get_connection


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def log_cost(session_id: str, tokens_used: int, cost: float):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO cost_tracking (session_id, tokens_used, cost)
        VALUES (?, ?, ?)
        """,
        (session_id, tokens_used, cost)
    )

    conn.commit()
    conn.close()
