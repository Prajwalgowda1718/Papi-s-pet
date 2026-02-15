from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.config import settings
from app.rag.vectorstore import get_retriever
from app.rag.reranker import rerank_documents
from app.rag.router import detect_target_section


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


def generate_response(query: str):
    section = detect_target_section(query)
    retriever = get_retriever(section)

    docs = retriever.invoke(query)

    if not docs:
        return {
            "This assistant is designed to provide only non sensitive information "
            "only about Prajwal K Madegowda."
        }

    ranked = rerank_documents(docs)

    context = "\n\n---\n\n".join(doc.page_content for doc in ranked)

    llm = build_llm()
    prompt = build_prompt()

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"context": context, "question": query})
