import base64
from typing import Dict, Any
from together import Together
from utils.config import TOGETHER_API_KEY


VISION_MODEL = "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"


def _client() -> Together:
    if not TOGETHER_API_KEY:
        raise ValueError(
            "❌ TOGETHER_API_KEY is missing. "
            "For localhost: Create a .env file with TOGETHER_API_KEY=your_key_here\n"
            "For deployment: Set TOGETHER_API_KEY in Streamlit secrets"
        )
    return Together(api_key=TOGETHER_API_KEY)


def analyze_meal_image(image_path: str) -> Dict[str, Any]:
    try:
        with open(image_path, "rb") as f:
            b64_image = base64.b64encode(f.read()).decode("utf-8")

        client = _client()
        prompt = (
            "You are a nutrition analyst. Given a meal photo, identify foods, estimate portion sizes, "
            "and provide a rough calorie and macro breakdown in JSON with keys: items (list of {name, grams, calories}),"
            " total_calories, macros {protein_g, carbs_g, fat_g}."
        )
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"},
                        },
                    ],
                }
            ],
            temperature=0.2,
            max_tokens=512,
        )
        message = response.choices[0].message
        content = getattr(message, "content", None)

        # Some SDKs may return structured content; coerce to string when needed
        if isinstance(content, list):
            # Join any text parts; ignore non-text types defensively
            parts = []
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    parts.append(part.get("text", ""))
                elif isinstance(part, str):
                    parts.append(part)
            content = "\n".join([p for p in parts if p])

        if content is None:
            content = ""

        # Prefer returning human-readable text, strip fenced code blocks (e.g., JSON snippets)
        text = content
        if isinstance(text, str) and "```" in text:
            # Keep only the portion before the first code fence
            text = text.split("```", 1)[0].strip()
        # Remove explicit section header if present
        for marker in ["JSON Output:", "JSON output:"]:
            text = text.replace(marker, "").strip()

        return {"raw": text}
    except ValueError as e:
        # API key missing error
        return {"error": str(e)}
    except Exception as e:
        # Other errors
        return {"error": f"Failed to analyze image: {str(e)}"}
