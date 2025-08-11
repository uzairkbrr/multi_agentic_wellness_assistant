from typing import Optional

from .crud import get_user_by_email, get_user_by_id, create_user
from utils.security import hash_password, verify_password


def register_user(name: str, email: str, password: str) -> int:
    password_hash = hash_password(password)
    return create_user(name, email, password_hash)


def login_user(email: str, password: str) -> Optional[dict]:
    user = get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return user


def fetch_user(user_id: int) -> Optional[dict]:
    return get_user_by_id(user_id)

