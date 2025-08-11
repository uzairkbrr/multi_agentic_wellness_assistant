from typing import List, Dict, Any, Optional
import os

from together import Together
from utils.config import TOGETHER_API_KEY


MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"


def _client() -> Together:
    return Together(api_key=TOGETHER_API_KEY)


def get_mental_health_response(messages: List[Dict[str, str]]) -> str:
    client = _client()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.6,
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
