# import os
# from dotenv import load_dotenv

# load_dotenv()

# TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/wellness.db")


import os
from dotenv import load_dotenv

# Load .env file for local development (ignored if on Streamlit Cloud)
load_dotenv()

# API Keys
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Optional: if using OpenAI

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/wellness.db")

# Safety check
if not TOGETHER_API_KEY:
    print("⚠️ Warning: TOGETHER_API_KEY is not set. API calls will fail.")
