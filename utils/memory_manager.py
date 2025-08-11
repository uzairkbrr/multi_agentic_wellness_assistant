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
    return resp.choices[0].message["content"]
