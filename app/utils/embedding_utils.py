import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Reuse same model used in vectorstore
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str):
    vector = _model.encode(text)
    return vector


def serialize_embedding(vector):
    return json.dumps(vector.tolist())


def deserialize_embedding(vector_str):
    return np.array(json.loads(vector_str))


def cosine_similarity(vec1, vec2):
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
