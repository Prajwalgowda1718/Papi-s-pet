from app.db.database import get_connection
from app.utils.embedding_utils import (
    embed_text,
    serialize_embedding,
    deserialize_embedding,
    cosine_similarity,
)


SIMILARITY_THRESHOLD = 0.85


def get_cached_response(query: str):
    conn = get_connection()
    cursor = conn.cursor()

    query_vector = embed_text(query)

    cursor.execute("SELECT query, embedding, response FROM response_cache")
    rows = cursor.fetchall()

    for row in rows:
        stored_vector = deserialize_embedding(row["embedding"])
        similarity = cosine_similarity(query_vector, stored_vector)

        if similarity >= SIMILARITY_THRESHOLD:
            conn.close()
            return row["response"]

    conn.close()
    return None


def store_response_in_cache(query: str, response: str):
    conn = get_connection()
    cursor = conn.cursor()

    vector = embed_text(query)
    serialized = serialize_embedding(vector)

    cursor.execute(
        """
        INSERT OR REPLACE INTO response_cache (query, embedding, response)
        VALUES (?, ?, ?)
        """,
        (query.strip().lower(), serialized, response),
    )

    conn.commit()
    conn.close()
