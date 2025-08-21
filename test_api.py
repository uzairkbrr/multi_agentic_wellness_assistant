#!/usr/bin/env python3
"""
Test script to verify Together AI API key is working
"""

import sys
import os

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.config import TOGETHER_API_KEY
from together import Together

def test_api_key():
    """Test if the API key is working"""
    print("🔍 Testing Together AI API Key...")
    print("=" * 40)
    
    # Check if API key is set
    if not TOGETHER_API_KEY:
        print("❌ TOGETHER_API_KEY is not set!")
        print("\nTo fix this:")
        print("1. For localhost: Create a .env file with TOGETHER_API_KEY=your_key_here")
        print("2. For deployment: Set TOGETHER_API_KEY in Streamlit secrets")
        print("\nGet your API key from: https://api.together.xyz/settings/api-keys")
        return False
    
    print(f"✅ API Key found: {TOGETHER_API_KEY[:8]}...{TOGETHER_API_KEY[-4:]}")
    
    # Test the API
    try:
        client = Together(api_key=TOGETHER_API_KEY)
        
        # Simple test request
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            messages=[{"role": "user", "content": "Say 'Hello, API is working!'"}],
            max_tokens=50,
            temperature=0.1
        )
        
        message = response.choices[0].message
        content = getattr(message, "content", "")
        
        if "Hello" in content or "working" in content.lower():
            print("✅ API test successful!")
            print(f"Response: {content}")
            return True
        else:
            print("⚠️  API responded but with unexpected content")
            print(f"Response: {content}")
            return True
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        print("\nPossible issues:")
        print("1. Invalid API key")
        print("2. Network connectivity issues")
        print("3. API service temporarily unavailable")
        return False

if __name__ == "__main__":
    success = test_api_key()
    if success:
        print("\n🎉 Your API key is working! You can now run the app.")
    else:
        print("\n💡 Please fix the issues above and try again.")
        sys.exit(1)
