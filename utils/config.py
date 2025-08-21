import os
import streamlit as st
from dotenv import load_dotenv

# Load .env file for local development (ignored if on Streamlit Cloud)
load_dotenv()

def get_api_key():
    """Get API key from multiple sources in order of preference"""
    # 1. Try Streamlit secrets (for deployment)
    try:
        if hasattr(st, 'secrets') and st.secrets:
            api_key = st.secrets.get("TOGETHER_API_KEY", "")
            if api_key:
                return api_key
    except Exception:
        pass
    
    # 2. Try environment variable (for localhost)
    api_key = os.getenv("TOGETHER_API_KEY", "")
    if api_key:
        return api_key
    
    # 3. Return empty string if not found
    return ""

# API Keys
TOGETHER_API_KEY = get_api_key()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Optional: if using OpenAI

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/wellness.db")

# Safety check
if not TOGETHER_API_KEY:
    print("⚠️ Warning: TOGETHER_API_KEY is not set. API calls will fail.")
    print("   For localhost: Create a .env file with TOGETHER_API_KEY=your_key_here")
    print("   For deployment: Set TOGETHER_API_KEY in Streamlit secrets")
