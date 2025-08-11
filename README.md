# Multi-Agentic Wellness Assistant

Streamlit app with three agents (Mental Health, Diet with Vision, Exercise) using Together AI.

Setup
- Create `.env` with:
  - `TOGETHER_API_KEY=...`
- Install deps:
  - `pip install -r requirements.txt`
- Run:
  - `streamlit run app.py`

Notes
- Uses SQLite at `data/wellness.db` created on first run.
- Vision analysis expects Together Vision model and returns raw JSON string; the UI attempts to parse.

