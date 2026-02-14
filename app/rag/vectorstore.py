from pathlib import Path
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

from app.rag.loader import load_documents


VECTOR_DB_PATH = Path("data/vectorstore/chromadb")
COLLECTION_NAME = "papis_pet"

# Initialize embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_chroma_client():
    VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)
    return PersistentClient(path=str(VECTOR_DB_PATH))


def get_or_create_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name=COLLECTION_NAME)


def index_documents():
    client = get_chroma_client()

    # Delete existing collection if exists
    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    documents = load_documents()

    for idx, doc in enumerate(documents):
        embedding = embedding_model.encode(doc["content"]).tolist()

        collection.upsert(
            documents=[doc["content"]],
            embeddings=[embedding],
            metadatas=[doc["metadata"]],
            ids=[f"doc_{idx}"]
        )



def query_collection(query: str, n_results: int = 5):
    collection = get_or_create_collection()

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results
