import json
import os
from datetime import datetime
import streamlit as st
from backend.database import init_db

from agents.diet import get_diet_suggestion
from agents.vision import analyze_meal_image
from backend.crud import insert_meal_log, list_meal_logs, log_activity
from utils.styles import inject_landing_theme


# Ensure DB is initialized when navigating directly
init_db()
inject_landing_theme()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in to access this page.")
    st.stop()

st.title("Diet Tracker")

tabs = st.tabs(["Log Meal (Text)", "Analyze Photo", "History"])

with tabs[0]:
    st.subheader("Text Log and Suggestions")
    user_text = st.text_area("Describe your meal or ask for a plan")
    if st.button("Get Suggestion") and user_text:
        msgs = [
            {
                "role": "system",
                "content": (
                    "You are a knowledgeable diet assistant. Provide practical, budget-aware suggestions. "
                    "Respond in clear English paragraphs only. Do not output JSON or code blocks."
                ),
            },
            {"role": "user", "content": user_text},
        ]
        reply = get_diet_suggestion(msgs)
        st.markdown(reply)
        # Save a simple log
        insert_meal_log(
            user_id=st.session_state.user["id"],
            date=datetime.utcnow().date().isoformat(),
            description=user_text,
            image_path=None,
            calories_est=None,
            macros_json=None,
        )
        log_activity(st.session_state.user["id"], "meal_log", {"description": user_text})

with tabs[1]:
    st.subheader("Upload Meal Photo for Vision Analysis")
    upload = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
    if upload:
        img_bytes = upload.read()
        os.makedirs("data/uploads", exist_ok=True)
        save_path = os.path.join("data", "uploads", f"{datetime.utcnow().timestamp()}_{upload.name}")
        with open(save_path, "wb") as f:
            f.write(img_bytes)
        st.image(save_path, caption="Uploaded meal")
        with st.spinner("Analyzing image..."):
            analysis = analyze_meal_image(save_path)
        # Show readable text instead of JSON
        raw_text = analysis.get("raw", "") if isinstance(analysis, dict) else str(analysis)
        st.markdown(raw_text)
        # Try to parse calorie/macros if provided in JSON text
        calories = None
        macros_json = None
        if isinstance(analysis, dict) and "raw" in analysis:
            try:
                parsed = json.loads(analysis["raw"]) if isinstance(analysis["raw"], str) else analysis["raw"]
                calories = parsed.get("total_calories")
                macros_json = json.dumps(parsed.get("macros")) if parsed.get("macros") else None
            except Exception:
                pass
        insert_meal_log(
            user_id=st.session_state.user["id"],
            date=datetime.utcnow().date().isoformat(),
            description=None,
            image_path=save_path,
            calories_est=calories,
            macros_json=macros_json,
        )
        log_activity(st.session_state.user["id"], "meal_log", {"image_path": save_path, "calories": calories})

with tabs[2]:
    st.subheader("Recent Meals")
    logs = list_meal_logs(st.session_state.user["id"], limit=20)
    for log in logs:
        st.markdown(f"- {log['date']}: {log.get('description') or ''} {('(image) ' + log['image_path']) if log.get('image_path') else ''} {('~' + str(log['calories_est']) + ' kcal') if log.get('calories_est') else ''}")
