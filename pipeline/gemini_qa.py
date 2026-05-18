import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = None
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def _get_client():
    global client
    if client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        client = genai.Client(api_key=api_key)
    return client

def answer_question(question: str, context: str) -> str:
    """
    Answer question using Gemini with podcast context
    """

    # 🛡️ Safety guard (VERY IMPORTANT)
    if not context or len(context.split()) < 100:
        return "I’m not confident enough to answer based on the available transcript."

    prompt = f"""
You are an assistant answering questions about a podcast.

Use ONLY the context below.
If the answer is not present, say: "Not enough information in the podcast."

Context:
{context}

Question:
{question}
"""

    try:
        response = _get_client().models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        return f"Gemini error: {str(e)}"
