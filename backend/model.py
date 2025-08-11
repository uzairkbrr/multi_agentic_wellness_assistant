from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class User:
    id: Optional[int]
    name: str
    email: str
    password_hash: str
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    fitness_goal: Optional[str] = None
    activity_level: Optional[str] = None
    dietary_preferences: Optional[str] = None
    mental_health_background: Optional[str] = None
    daily_schedule: Optional[str] = None
    medical_conditions: Optional[str] = None
    profile_photo_path: Optional[str] = None
    avatar_choice: Optional[str] = None


@dataclass
class MentalHealthMemory:
    id: Optional[int]
    user_id: int
    tags: Optional[str]
    summary: str
    created_at: str


@dataclass
class WorkoutLog:
    id: Optional[int]
    user_id: int
    date: str
    routine: str
    calories_burned: Optional[float]


@dataclass
class MealLog:
    id: Optional[int]
    user_id: int
    date: str
    description: Optional[str]
    image_path: Optional[str]
    calories_est: Optional[float]
    macros_json: Optional[str]

