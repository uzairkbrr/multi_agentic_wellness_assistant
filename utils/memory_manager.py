from typing import List, Dict
from together import Together
from utils.config import TOGETHER_API_KEY


MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"


def _client() -> Together:
    return Together(api_key=TOGETHER_API_KEY)


def summarize_messages(messages: List[Dict[str, str]]) -> str:
    client = _client()
    system = {
        "role": "system",
        "content": (
            "Summarize the following conversation into a short, factual bullet list with key events, needs, and action items."
        ),
    }
    msgs = [system] + messages
    resp = client.chat.completions.create(
        model=MODEL,
        messages=msgs,
        temperature=0.2,
        max_tokens=256,
    )
    message = resp.choices[0].message
    content = getattr(message, "content", None)
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                parts.append(part.get("text", ""))
            elif isinstance(part, str):
                parts.append(part)
        content = "\n".join([p for p in parts if p])
    return content or ""
