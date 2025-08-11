from datetime import date
import streamlit as st

from backend.database import init_db
from backend.crud import insert_workout_log, list_workout_logs, log_activity
from utils.styles import inject_landing_theme

try:
    from agents.exercise import get_exercise_plan
except Exception:  # Optional dependency
    get_exercise_plan = None  # type: ignore


# Ensure DB is available and theme is applied
init_db()
inject_landing_theme()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in to access this page.")
    st.stop()

st.title("Workout Logger")
st.page_link("pages/dashboard.py", label="Back to Dashboard ➜", icon="🏠")

tabs = st.tabs(["Log Workout", "AI Plan", "History"])

with tabs[0]:
    st.subheader("Quick Log")
    log_date = st.date_input("Date", value=date.today())
    routine = st.text_input("Routine", placeholder="e.g., 30 min run + 20 push-ups")
    calories_burned = st.number_input("Calories burned (optional)", min_value=0, step=10)
    if st.button("Save Workout"):
        if routine.strip():
            cal_value = float(calories_burned) if calories_burned > 0 else None
            insert_workout_log(
                user_id=st.session_state.user["id"],
                date=log_date.isoformat(),
                routine=routine.strip(),
                calories_burned=cal_value,
            )
            log_activity(
                st.session_state.user["id"],
                "workout_log",
                {"date": log_date.isoformat(), "routine": routine.strip(), "calories_burned": cal_value},
            )
            st.success("Workout saved.")
        else:
            st.warning("Please enter a routine before saving.")

with tabs[1]:
    st.subheader("Generate an Exercise Plan")
    prefs = st.text_area(
        "Describe your goals or constraints",
        placeholder="e.g., 3-day weekly plan for fat loss, 30–40 minutes per session, no equipment",
    )
    disabled = get_exercise_plan is None
    if disabled:
        st.info("AI plan generation not available. Configure Together API to enable.")
    if st.button("Generate Plan", disabled=disabled) and prefs:
        try:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful fitness coach. Provide safe, progressive workouts. "
                        "Return clear, concise guidance in plain text."
                    ),
                },
                {"role": "user", "content": prefs},
            ]
            reply = get_exercise_plan(messages) if get_exercise_plan else ""
            st.markdown(reply or "No response.")
        except Exception as e:  # pragma: no cover
            st.error(f"Could not generate plan: {e}")

with tabs[2]:
    st.subheader("Recent Workouts")
    logs = list_workout_logs(st.session_state.user["id"], limit=20)
    if not logs:
        st.caption("No workouts logged yet.")
    for log in logs:
        kcal = f" · {log['calories_burned']} kcal" if log.get("calories_burned") else ""
        st.markdown(f"- {log['date']}: {log['routine']}{kcal}")

 