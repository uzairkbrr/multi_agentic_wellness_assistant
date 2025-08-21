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


def analyze_meal_text(meal_text: str) -> str:
    """Analyze a text-based meal description and provide nutritional analysis.
    
    Similar to vision analysis but for text descriptions. Provides estimated
    calories, macros, and portion sizes based on the meal description.
    """
    if not meal_text:
        return "Unable to analyze nutrition for this meal."
    
    client = _client()
    system = {
        "role": "system",
        "content": (
            "You are a nutrition analyst. Given a meal description, identify foods, estimate portion sizes, "
            "and provide a rough calorie and macro breakdown. Format your response like this:\n\n"
            "The meal consists of [food items].\n\n"
            "To estimate the portion sizes and provide a rough calorie and macro breakdown, we can make the following assumptions:\n\n"
            "[List assumptions about portion sizes]\n\n"
            "Based on these assumptions, we can estimate the portion sizes as follows:\n\n"
            "[List estimated portions]\n\n"
            "To calculate the total calories, we can use the following approximate values:\n\n"
            "[List calorie estimates]\n\n"
            "Total calories: [X] calories\n\n"
            "To calculate the macros, we can use the following approximate values:\n\n"
            "[List macro estimates]"
        ),
    }
    user = {"role": "user", "content": f"Meal description: {meal_text}\nProvide nutritional analysis:"}
    try:
        response = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[system, user],
            temperature=0.2,
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
        if isinstance(content, str):
            return content.strip()
    except Exception:
        pass
    return "Unable to analyze nutrition for this meal."


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