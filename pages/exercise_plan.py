from datetime import datetime
import streamlit as st
from agents.exercise import get_exercise_plan
from utils.styles import inject_landing_theme
from backend.crud import insert_workout_log, list_workout_logs, log_activity


if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in to access this page.")
    st.stop()

inject_landing_theme()
st.title("Exercise Plan")

st.subheader("Generate Routine")
prompt = st.text_area("Any constraints or goals for this week? (e.g., 3 days, knee-friendly)")
if st.button("Generate Plan"):
    msgs = [
        {"role": "system", "content": "You are an experienced personal trainer. Provide a 1-week plan with sets, reps, and rest. Consider user's goals and limitations."},
        {"role": "user", "content": prompt or "Create a balanced 3-day routine for weight loss and strength."},
    ]
    plan = get_exercise_plan(msgs)
    st.markdown(plan)

st.subheader("Log Completed Workout")
with st.form("log_workout_form"):
    routine = st.text_area("What did you do?")
    calories = st.number_input("Estimated calories burned (kcal)", min_value=0.0, value=0.0)
    submitted = st.form_submit_button("Save Log")
    if submitted and routine:
        insert_workout_log(
            user_id=st.session_state.user["id"],
            date=datetime.utcnow().date().isoformat(),
            routine=routine,
            calories_burned=float(calories) if calories else None,
        )
        st.success("Workout logged.")
        log_activity(st.session_state.user["id"], "workout_log", {"routine": routine, "calories": float(calories) if calories else None})

st.subheader("Recent Workout Logs")
logs = list_workout_logs(st.session_state.user["id"], limit=30)
for log in logs:
    st.markdown(f"- {log['date']}: {log['routine']} {('~' + str(log['calories_burned']) + ' kcal') if log.get('calories_burned') else ''}")
