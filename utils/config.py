import os
from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/wellness.db")
