from typing import List, Dict
from together import Together
from utils.config import TOGETHER_API_KEY


TEXT_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"


def _client() -> Together:
    return Together(api_key=TOGETHER_API_KEY)


def get_diet_suggestion(messages: List[Dict[str, str]]) -> str:
    client = _client()
    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=messages,
        temperature=0.5,
        max_tokens=512,
    )
    message = response.choices[0].message
    content = getattr(message, "content", None)
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                parts.append(part.get("text", ""))
            elif isinstance(part, str):
                parts.append(part)
        content = "\n".join([p for p in parts if p])
    # Strip any accidental code fences or JSON-looking wrappers
    if isinstance(content, str):
        content = content.strip()
        if content.startswith("```") and content.endswith("```"):
            content = content.strip("`")
        # Heuristic: if content looks like JSON, add a brief natural language preface
        if content.startswith("{") and content.endswith("}"):
            content = "Here is a concise suggestion based on your input:\n\n" + content
    if content is None:
        content = ""
    return content
