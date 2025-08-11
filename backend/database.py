import os
import sqlite3

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "wellness.db")


def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    # Enable row factory for dict-like access
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password_hash TEXT,
            age INTEGER,
            gender TEXT,
            height_cm REAL,
            weight_kg REAL,
            fitness_goal TEXT,
            activity_level TEXT,
            dietary_preferences TEXT,
            mental_health_background TEXT,
            daily_schedule TEXT,
            medical_conditions TEXT,
            profile_photo_path TEXT,
            avatar_choice TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS mental_health_memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tags TEXT,
            summary TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS workout_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            routine TEXT NOT NULL,
            calories_burned REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS meal_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            image_path TEXT,
            calories_est REAL,
            macros_json TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            goal_type TEXT, -- e.g., weight_loss, muscle_gain, mental_health
            difficulty TEXT, -- e.g., beginner, intermediate, advanced
            duration_days INTEGER
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            challenge_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'active', -- active, completed, dropped
            progress INTEGER NOT NULL DEFAULT 0, -- percent
            started_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(challenge_id) REFERENCES challenges(id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS activity_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            type TEXT NOT NULL, -- e.g., meal_log, workout_log, challenge_update, profile_update
            payload TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    conn.commit()
    # Run lightweight migrations to ensure new columns exist on older DBs
    _run_migrations(conn)
    conn.close()


def _run_migrations(conn: sqlite3.Connection) -> None:
    """Add any missing columns to existing tables without destroying data.

    This is a minimal, idempotent migration helper suitable for SQLite.
    """
    cursor = conn.cursor()

    def ensure_column_exists(table: str, column: str, coltype: str) -> None:
        cursor.execute(f"PRAGMA table_info({table})")
        cols = {row[1] for row in cursor.fetchall()}  # row[1] is the column name
        if column not in cols:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {coltype}")

    # Users table migrations
    ensure_column_exists("users", "profile_photo_path", "TEXT")
    ensure_column_exists("users", "avatar_choice", "TEXT")
    # Meal logs migrations
    ensure_column_exists("meal_logs", "meal_name", "TEXT")

    conn.commit()
