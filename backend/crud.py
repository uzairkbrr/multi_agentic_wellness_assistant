from typing import Optional, List, Dict, Any
from datetime import datetime
import json

from .database import get_connection


def create_user(name: str, email: str, password_hash: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    user_id = cur.lastrowid
    conn.commit()
    conn.close()
    return user_id


def get_user_by_email(email: str) -> Optional[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id: int) -> Optional[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def update_user_profile(user_id: int, fields: Dict[str, Any]) -> None:
    if not fields:
        return
    conn = get_connection()
    cur = conn.cursor()
    assignments = ", ".join([f"{k} = ?" for k in fields.keys()])
    values = list(fields.values()) + [user_id]
    cur.execute(f"UPDATE users SET {assignments} WHERE id = ?", values)
    conn.commit()
    conn.close()


def log_activity(user_id: int, type_: str, payload: Dict[str, Any]) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO activity_stream (user_id, created_at, type, payload) VALUES (?, ?, ?, ?)",
        (user_id, datetime.utcnow().isoformat(), type_, json.dumps(payload)),
    )
    aid = cur.lastrowid
    conn.commit()
    conn.close()
    return aid


def list_activity(user_id: int, limit: int = 50) -> List[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM activity_stream WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def upsert_profile_media(user_id: int, photo_path: Optional[str], avatar_choice: Optional[str]) -> None:
    fields: Dict[str, Any] = {}
    if photo_path is not None:
        fields["profile_photo_path"] = photo_path
    if avatar_choice is not None:
        fields["avatar_choice"] = avatar_choice
    update_user_profile(user_id, fields)


def insert_memory(user_id: int, summary: str, tags: str = "") -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO mental_health_memories (user_id, tags, summary, created_at) VALUES (?, ?, ?, ?)",
        (user_id, tags, summary, datetime.utcnow().isoformat()),
    )
    memory_id = cur.lastrowid
    conn.commit()
    conn.close()
    return memory_id


def list_memories(user_id: int, limit: int = 50) -> List[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM mental_health_memories WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def insert_workout_log(user_id: int, date: str, routine: str, calories_burned: float | None) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO workout_logs (user_id, date, routine, calories_burned) VALUES (?, ?, ?, ?)",
        (user_id, date, routine, calories_burned),
    )
    log_id = cur.lastrowid
    conn.commit()
    conn.close()
    return log_id


def list_workout_logs(user_id: int, limit: int = 100) -> List[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM workout_logs WHERE user_id = ? ORDER BY date DESC LIMIT ?",
        (user_id, limit),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def insert_meal_log(
    user_id: int,
    date: str,
    description: str | None,
    image_path: str | None,
    calories_est: float | None,
    macros_json: str | None,
) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO meal_logs (user_id, date, description, image_path, calories_est, macros_json)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, date, description, image_path, calories_est, macros_json),
    )
    log_id = cur.lastrowid
    conn.commit()
    conn.close()
    return log_id


def list_meal_logs(user_id: int, limit: int = 100) -> List[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM meal_logs WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT ?",
        (user_id, limit),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Challenges

def create_challenge(title: str, description: str, goal_type: str, difficulty: str, duration_days: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO challenges (title, description, goal_type, difficulty, duration_days) VALUES (?, ?, ?, ?, ?)",
        (title, description, goal_type, difficulty, duration_days),
    )
    cid = cur.lastrowid
    conn.commit()
    conn.close()
    return cid


def list_relevant_challenges(goal_type: Optional[str], difficulty: Optional[str], limit: int = 20) -> List[dict]:
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT * FROM challenges WHERE 1=1"
    params: List[Any] = []
    if goal_type:
        query += " AND goal_type = ?"
        params.append(goal_type)
    if difficulty:
        query += " AND difficulty = ?"
        params.append(difficulty)
    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def join_challenge(user_id: int, challenge_id: int) -> int:
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO user_challenges (user_id, challenge_id, status, progress, started_at, updated_at) VALUES (?, ?, 'active', 0, ?, ?)",
        (user_id, challenge_id, now, now),
    )
    ucid = cur.lastrowid
    conn.commit()
    conn.close()
    return ucid


def update_challenge_progress(user_id: int, challenge_id: int, progress: int, status: Optional[str] = None) -> None:
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    cur = conn.cursor()
    if status:
        cur.execute(
            "UPDATE user_challenges SET progress = ?, status = ?, updated_at = ? WHERE user_id = ? AND challenge_id = ?",
            (progress, status, now, user_id, challenge_id),
        )
    else:
        cur.execute(
            "UPDATE user_challenges SET progress = ?, updated_at = ? WHERE user_id = ? AND challenge_id = ?",
            (progress, now, user_id, challenge_id),
        )
    conn.commit()
    conn.close()


def list_user_challenges(user_id: int) -> List[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT uc.*, c.title, c.description FROM user_challenges uc JOIN challenges c ON uc.challenge_id = c.id WHERE uc.user_id = ? ORDER BY uc.updated_at DESC",
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def ensure_default_challenges() -> None:
    """Seed a small set of default challenges if the table is empty."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM challenges")
    count = cur.fetchone()[0]
    if count and count > 0:
        conn.close()
        return
    defaults = [
        ("7-Day Step Boost", "Hit 8,000 steps daily for a week.", "weight_loss", "beginner", 7),
        ("Core Strength Sprint", "10-minute core routine daily.", "muscle_gain", "beginner", 14),
        ("Mindful Mornings", "5 minutes of morning meditation.", "mental_health", "beginner", 10),
        ("Protein Focus", "Hit your protein goal each day.", "muscle_gain", "intermediate", 14),
        ("Sugar-Lite Week", "Limit added sugars for 7 days.", "weight_loss", "beginner", 7),
    ]
    cur.executemany(
        "INSERT INTO challenges (title, description, goal_type, difficulty, duration_days) VALUES (?, ?, ?, ?, ?)",
        defaults,
    )
    conn.commit()
    conn.close()
