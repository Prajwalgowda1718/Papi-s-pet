from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from app.utils.fallbacks import out_of_scope, service_unavailable
from app.config import settings
from app.rag.vectorstore import get_retriever
from app.rag.reranker import rerank_documents
from app.rag.router import detect_target_section



_llm = None
_prompt = None
_chain = None


def build_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.2,
    )


def build_prompt():
    return ChatPromptTemplate.from_template(
        """
You are an AI assistant representing Prajwal K Madegowda.

Rules:
1. Always speak in third person.
2. Use ONLY provided context.
3. If information not present, respond:
   "He prefers not to share that information publicly."
4. Be concise and professional.

Context:
{context}

User Question:
{question}

Answer:
"""
    )


def get_chain():
    global _llm, _prompt, _chain

    if _chain is None:
        _llm = build_llm()
        _prompt = build_prompt()
        _chain = _prompt | _llm | StrOutputParser()

    return _chain






def generate_response(query: str):
    section = detect_target_section(query)
    retriever = get_retriever(section)

    docs = retriever.invoke(query)

    if not docs:
        return out_of_scope()

    ranked = rerank_documents(docs)
    context = "\n\n---\n\n".join(doc.page_content for doc in ranked)

    chain = get_chain()

    try:
        return chain.invoke({"context": context, "question": query})

    except ChatGoogleGenerativeAIError:
        return service_unavailable()

    except Exception:
        return service_unavailable()
