from fastapi import FastAPI
from app.config import settings
from app.db.database import init_db
from app.rag.loader import load_documents
from app.rag.vectorstore import index_documents, query_collection
from app.llm.gemini_client import generate_response


app=FastAPI(title="Papi's pet API")

@app.get("/")
def root():
    return {
        "message": "Papi's Pet is running",
        "environment": settings.APP_ENV,
        "debug": settings.DEBUG,
        
    }


@app.get("/health")
def health_check():
    return {"Status": "OK"}

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/debug/documents")
def debug_documents():
    docs = load_documents()
    return {
        "count": len(docs),
        "documents": docs
    }

@app.post("/debug/index")
def debug_index():
    index_documents()
    return {"status": "indexed"}


@app.get("/debug/query")
def debug_query(q: str):
    results = query_collection(q)
    return results

@app.get("/ask")
def ask(q: str):
    results = query_collection(q, n_results=5)

    retrieved_docs = results.get("documents", [[]])[0]

    context = "\n\n---\n\n".join(retrieved_docs)

    answer = generate_response(context=context, query=q)

    return {
        "answer": answer
    }
