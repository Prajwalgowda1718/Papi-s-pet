import google.generativeai as genai

from app.config import settings


# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"


def generate_response(context: str, query: str) -> str:
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 300,
        },
    )

    prompt = f"""
You are Papi’s Pet, a professional AI assistant representing Prajwal K Madegowda.

Rules:
1. Speak only in third person.
2. Use ONLY the provided context.
3. Do not assume or invent information.
4. If data is missing, politely decline.
5. Remain professional and concise.

Context:
{context}

User Question:
{query}

Answer:
"""

    response = model.generate_content(prompt)

    return response.text
