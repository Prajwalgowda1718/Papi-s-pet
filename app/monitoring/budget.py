from app.db.database import get_connection


DAILY_COST_LIMIT = 5


def get_today_cost() -> float:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(cost) FROM cost_tracking
        WHERE DATE(created_at) = DATE('now')
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result if result is not None else 0.0


def is_budget_exceeded() -> bool:
    return get_today_cost() >= DAILY_COST_LIMIT
