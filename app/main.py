from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
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
from app.db.cache_manager import get_cached_response, store_response_in_cache
from app.monitoring.rate_limiter import is_rate_limited, record_request
from app.utils.logger import logger
from app.guardrails.input_guard import handle_malicious


app=FastAPI(title="Papi's pet API")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def frontend():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/info")
def api_info():
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
def ask(q: str, session_id: str | None = None):

    logger.info(f"Incoming query | session={session_id} | query={q}")

    # Budget check
    if is_budget_exceeded():
        logger.error("Daily budget exceeded")
        return {
            "answer": "Service temporarily unavailable due to daily usage limits. Please try again tomorrow."
        }

    # Create session if needed
    if session_id is None:
        session_id = create_session()
        logger.info(f"New session created | session={session_id}")

    # Rate limiting check
    if is_rate_limited(session_id):
        logger.warning(f"Rate limit triggered | session={session_id}")
        return {
            "answer": "Too many requests. Please slow down.",
            "session_id": session_id
        }

    # Record request
    record_request(session_id)

    # Log user message
    log_message(session_id, "user", q)

    # Input guard
    if is_malicious(q):
        logger.warning(f"Malicious query detected | session={session_id}")
        fallback = handle_malicious()
        log_message(session_id, "assistant", fallback)
        return {
            "answer": fallback,
            "session_id": session_id,
            "cached": False
        }

    # Check cache
    cached = get_cached_response(q)
    if cached:
        logger.info(f"Cache hit | session={session_id}")
        log_message(session_id, "assistant", cached)
        return {
            "answer": cached,
            "session_id": session_id,
            "cached": True
        }

    # Generate response
    logger.info(f"Calling LLM | session={session_id}")
    response = generate_response(q)

    # Output guard
    safe_response = validate_output(response)

    # Log assistant response
    log_message(session_id, "assistant", safe_response)

    # Estimate tokens and cost
    input_tokens = estimate_tokens(q)
    output_tokens = estimate_tokens(safe_response)
    total_tokens = input_tokens + output_tokens
    cost = total_tokens * settings.TOKEN_COST_RATE

    log_cost(session_id, total_tokens, cost)

    # Store in cache
    store_response_in_cache(q, safe_response)

    logger.info(f"Response completed | session={session_id} | tokens={total_tokens}")

    return {
        "answer": safe_response,
        "session_id": session_id,
        "cached": False
    }
