# Papi’s Pet

### Public-Facing AI Assistant with Guardrails, RAG, and Cost Control

Papi’s Pet is a production-oriented Retrieval-Augmented Generation system designed to represent a professional profile safely and reliably.

It answers questions strictly about Prajwal K Madegowda using verified structured data and enforces multiple layers of control to prevent hallucination, data leakage, and prompt injection.

This project demonstrates practical implementation of:

* RAG architecture using LangChain
* Section-based retrieval routing
* Input / Output guardrails
* Semantic caching
* Rate limiting
* Cost tracking
* Session management
* Logging and observability
* Automated testing

---

# System Architecture

User Query
→ Input Guard
→ Rate Limit Check
→ Budget Check
→ Semantic Cache
→ Section Router
→ Vector Retrieval
→ Retrieval Guard
→ Re-ranking
→ Prompt Construction
→ Gemini LLM
→ Output Guard
→ Logging + Cost Tracking
→ Response

---

# Core Design Principles

### 1. Strict Grounding

The LLM is forced to use only retrieved context.
If information is absent, it responds with a controlled fallback.

### 2. Multi-Layer Guardrails

* Input Guard: detects prompt injection patterns
* Retrieval Guard: filters sensitive documents
* Output Guard: blocks PII and first-person violations

### 3. Cost Awareness

* Token usage estimation
* Daily budget limit
* API quota handling
* Rate limiting per session

### 4. Performance Optimization

* Semantic cache using cosine similarity
* Section-aware retriever to reduce vector search scope
* Re-ranking of retrieved documents

---

# Tech Stack

Backend:

* FastAPI

RAG:

* LangChain
* ChromaDB
* SentenceTransformers

LLM:

* Google Gemini (gemini-2.5-flash)

Database:

* SQLite

Testing:

* Pytest

---

# Key Features

### Section-Based Retrieval Routing

Query intent detection limits vector search to relevant sections such as:

* skills
* education
* projects
* profile

Improves precision and reduces noise.

### Semantic Cache

Stores query embeddings in SQLite.
If cosine similarity > threshold, response is reused.
Reduces token usage and API calls.

### Rate Limiting

Per-session request throttling to prevent abuse.

### Budget Control

Daily cost ceiling prevents uncontrolled API spend.

---

# Example Queries

* What programming languages does he know?
* What is his CGPA?
* What machine learning frameworks does he use?
* What are his areas of interest?

---

# Testing

Run:

pytest

Includes:

* Input guard tests
* Output guard tests
* Semantic cache tests

---

# Limitations

* Depends on Gemini API quota
* Currently single-user SQLite backend
* No authentication layer
* Not horizontally scalable yet

---

# Future Improvements

* Replace deprecated LangChain imports
* Add evaluation benchmarking
* Containerize with Docker Compose
* Add CI pipeline
* Deploy with reverse proxy
* Add structured telemetry

---

# Why This Project Matters

This project demonstrates understanding of:

* RAG failure modes
* Hallucination control
* Prompt injection defense
* API cost management
* System-level design tradeoffs
* Production-minded AI engineering

