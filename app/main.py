from fastapi import FastAPI
from app.config import settings
from app.db.database import init_db
from app.rag.loader import load_documents
from app.rag.vectorstore import index_documents
from app.guardrails.input_guard import is_malicious
from app.guardrails.output_guard import validate_output
from app.db.session_manager import create_session, log_message
from app.db.cost_logger import estimate_tokens, log_cost
from app.monitoring.budget import is_budget_exceeded
from app.llm.chain import generate_response


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

from app.db.session_manager import create_session, log_message


@app.get("/ask")

def ask(q: str, session_id: str | None = None):

    if is_budget_exceeded():
        return {
            "answer": "Service temporarily unavailable due to daily usage limits. Please try again tomorrow."
        }


    # Create session if not provided
    if session_id is None:
        session_id = create_session()

    # Log user message
    log_message(session_id, "user", q)

    if is_malicious(q):
        fallback = "He prefers not to share that information publicly."
        log_message(session_id, "assistant", fallback)
        return {"answer": fallback, "session_id": session_id}

    response = generate_response(q)


    safe_response = validate_output(response)

    log_message(session_id, "assistant", safe_response)

    # Estimate tokens
    input_tokens = estimate_tokens(q)
    output_tokens = estimate_tokens(safe_response)
    total_tokens = input_tokens + output_tokens

    cost = total_tokens * 0.00002

    log_cost(session_id, total_tokens, cost)

    return {"answer": safe_response, "session_id": session_id}

