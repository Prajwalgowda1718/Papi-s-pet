from fastapi import FastAPI
from app.config import settings
from app.db.database import init_db
from app.rag.loader import load_documents
from app.rag.vectorstore import index_documents
from app.llm.chain import build_chain
from app.guardrails.input_guard import is_malicious
from app.guardrails.output_guard import is_sensitive_output




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


@app.get("/ask")
def ask(q: str):

    if is_malicious(q):
        return {
            "answer": "He prefers not to share that information publicly."
        }

    chain = build_chain()

    response = chain.invoke(q)

    if is_sensitive_output(response):
        return {
            "answer": "He prefers not to share that information publicly."
        }

    return {
        "answer": response
    }

