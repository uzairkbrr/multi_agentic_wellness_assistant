from typing import List, Dict
from together import Together
from utils.config import TOGETHER_API_KEY


TEXT_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"


def _client() -> Together:
    if not TOGETHER_API_KEY:
        raise ValueError(
            "❌ TOGETHER_API_KEY is missing. "
            "For localhost: Create a .env file with TOGETHER_API_KEY=your_key_here\n"
            "For deployment: Set TOGETHER_API_KEY in Streamlit secrets"
        )
    return Together(api_key=TOGETHER_API_KEY)


def get_exercise_plan(messages: List[Dict[str, str]]) -> str:
    client = _client()
    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=messages,
        temperature=0.5,
        max_tokens=512,
    )
    message = response.choices[0].message
    content = getattr(message, "content", None)
    # Handle potential structured content (e.g., list of parts)
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                parts.append(part.get("text", ""))
            elif isinstance(part, str):
                parts.append(part)
        content = "\n".join([p for p in parts if p])
    if content is None:
        content = ""
    return content
