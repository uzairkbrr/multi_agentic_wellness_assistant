# Multi-Agentic Wellness Assistant

Streamlit app with three agents (Mental Health, Diet with Vision, Exercise) using Together AI.

## Setup

### For Localhost Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory with:
   ```
   TOGETHER_API_KEY=your_actual_together_api_key_here
   ```
   
   Get your API key from: https://api.together.xyz/settings/api-keys

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

### For Deployment (Streamlit Cloud)

1. **Set Streamlit secrets:**
   In your Streamlit Cloud dashboard, go to Settings → Secrets and add:
   ```toml
   TOGETHER_API_KEY = "your_actual_together_api_key_here"
   ```

2. **Deploy:**
   Connect your repository to Streamlit Cloud and deploy.

## Notes

- Uses SQLite at `data/wellness.db` created on first run.
- Vision analysis expects Together Vision model and returns raw JSON string; the UI attempts to parse.
- The app automatically detects whether it's running locally (uses .env) or deployed (uses Streamlit secrets).

