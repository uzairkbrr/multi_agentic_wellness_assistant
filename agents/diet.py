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


def extract_meal_name(meal_text: str) -> str:
    """Return only the concise meal name for a given free-text description.

    The model is instructed to reply with the exact meal name only, without
    extra words, punctuation, emojis, or explanations. Falls back to the
    original text if the model cannot produce a response.
    """
    if not meal_text:
        return "Meal"
    client = _client()
    system = {
        "role": "system",
        "content": (
            "You extract a concise food dish name from user-provided text. "
            "Output ONLY the dish name, with no extra words, no punctuation, "
            "no quotes, no emojis. Examples: '\"I had a grilled chicken salad\"' -> 'Grilled Chicken Salad'; "
            "'2 eggs, toast and coffee' -> 'Eggs and Toast'."
        ),
    }
    user = {"role": "user", "content": f"Text: {meal_text}\nDish name:"}
    try:
        response = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[system, user],
            temperature=0.0,
            max_tokens=32,
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
        if isinstance(content, str):
            name = content.strip().strip('"').strip("'")
            # Guardrail: keep it short
            if 0 < len(name) <= 80:
                return name
    except Exception:
        pass
    return meal_text.strip()