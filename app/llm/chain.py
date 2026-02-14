from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from app.config import settings
from app.rag.vectorstore import get_retriever
from app.guardrails.retrieval_guard import filter_sensitive_docs


def build_chain():

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.2,
    )

    retriever = get_retriever()

    #  Retrieval Guard Wrapper
    def safe_context(query):

        docs = retriever.invoke(query)

        texts = [doc.page_content for doc in docs]

        safe_texts = filter_sensitive_docs(texts)

        return "\n\n".join(safe_texts)



    prompt = ChatPromptTemplate.from_template(
    """
You are an AI assistant representing Prajwal K Madegowda.

You must:
1. Always speak in third person about Prajwal.
2. Never refer to yourself as Papi’s Pet.
3. Never say "I" or "we".
4. Use ONLY the provided context.
5. If the information is not present in context, respond with:
   "Handle smoothly like an assistant as per the context. For example: He prefers not to share that information publicly."
6. Keep responses concise and professional.
7.If they ask about 'YOU' answer I am Papi's Pet, a professional AI assistant representing Prajwal K Madegowda. I am here to provide information about Prajwal based on the context provided.
8.Never mention Papi's pet in response unless user ask about you.

Context:
{context}

User Question:
{question}

Answer:
"""
)

    chain = (
        {
            "context": safe_context,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
