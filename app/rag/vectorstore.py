from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

from app.rag.loader import load_documents


VECTOR_DB_PATH = Path("data/vectorstore/chromadb")
COLLECTION_NAME = "papis_pet"

embedding_function = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


def get_vectorstore() -> Chroma:
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_function,
        persist_directory=str(VECTOR_DB_PATH),
    )


def index_documents():
    documents = load_documents()

    texts = [doc["content"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]

    # Delete existing collection safely
    vectorstore = get_vectorstore()
    try:
        vectorstore.delete_collection()
    except Exception:
        pass

    vectorstore = get_vectorstore()

    vectorstore.add_texts(texts=texts, metadatas=metadatas)
    vectorstore.persist()


def get_retriever():
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(
        search_kwargs={
            "k": 5,
            "filter": {"access_level": "public"}
        }
    )
