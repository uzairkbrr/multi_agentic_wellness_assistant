#!/usr/bin/env python3
"""
Setup script for Multi-Agentic Wellness Assistant
Helps users create the required .env file with their API keys.
"""

import os
import sys

def create_env_file():
    """Create .env file with user input"""
    print("🚀 Setting up Multi-Agentic Wellness Assistant")
    print("=" * 50)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    print("\n📋 You need a Together AI API key to use this app.")
    print("Get yours at: https://api.together.xyz/settings/api-keys")
    print()
    
    # Get API key from user
    api_key = input("Enter your Together AI API key: ").strip()
    
    if not api_key:
        print("❌ API key is required!")
        return
    
    # Create .env content
    env_content = f"""# Together AI API Key
TOGETHER_API_KEY={api_key}

# Optional: OpenAI API Key (if using OpenAI models)
# OPENAI_API_KEY=your_openai_api_key_here

# Database URL (optional, defaults to SQLite)
# DATABASE_URL=sqlite:///data/wellness.db
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("🔒 Remember: .env is in .gitignore and won't be committed to version control.")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return
    
    print("\n🎉 Setup complete!")
    print("You can now run: streamlit run app.py")

if __name__ == "__main__":
    create_env_file()
