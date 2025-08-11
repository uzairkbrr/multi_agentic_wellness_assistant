from typing import List, Dict


def count_tokens(text: str) -> int:
    # Heuristic token count ~ whitespace-separated words
    return len(text.split())


def trim_messages_to_token_limit(messages: List[Dict[str, str]], max_tokens: int = 2000) -> List[Dict[str, str]]:
    total = 0
    trimmed: List[Dict[str, str]] = []
    # keep most recent by traversing reversed
    for msg in reversed(messages):
        t = count_tokens(msg.get("content", ""))
        if total + t > max_tokens:
            break
        trimmed.append(msg)
        total += t
    return list(reversed(trimmed))
