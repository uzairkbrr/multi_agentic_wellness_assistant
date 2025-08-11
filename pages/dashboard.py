import random
from datetime import datetime, timedelta
import streamlit as st
from utils.styles import inject_landing_theme
from backend.crud import list_workout_logs, list_meal_logs, list_activity, list_user_challenges


if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access this page.")
    st.stop()

inject_landing_theme()
st.title("Dashboard")
st.write(f"Hello, {st.session_state.user['name']}! Here’s your wellness overview.")
st.page_link("pages/challenges.py", label="Go to Challenges ➜", icon="🔥")
st.page_link("pages/report.py", label="Generate Report ➜", icon="📄")

quotes = [
    "Small steps every day lead to big changes.",
    "Your only limit is you.",
    "Progress over perfection.",
    "Be kind to your mind and body.",
    "Consistency beats intensity when intensity fails.",
]
st.info(random.choice(quotes))
st.markdown("<hr>", unsafe_allow_html=True)

# Highlights
hl1, hl2, hl3 = st.columns(3)
with hl1:
    meals_count = len(list_meal_logs(st.session_state.user["id"], limit=50))
    st.metric("Meals Logged (last 50)", meals_count)
with hl2:
    workouts_count = len(list_workout_logs(st.session_state.user["id"], limit=50))
    st.metric("Workouts Logged (last 50)", workouts_count)
with hl3:
    challenges = list_user_challenges(st.session_state.user["id"]) or []
    active = sum(1 for c in challenges if c.get("status") == "active")
    st.metric("Active Challenges", active)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Recent Meals")
    for log in list_meal_logs(st.session_state.user["id"], limit=5):
        meal_name = log.get("meal_name") or (log.get("description") or "Meal")
        kc = f" · {log['calories_est']} kcal" if log.get("calories_est") else ""
        st.markdown(f"- {log['date']}: {meal_name}{kc}")
with col2:
    st.subheader("Recent Workouts")
    for log in list_workout_logs(st.session_state.user["id"], limit=5):
        kc = f" · {log['calories_burned']} kcal" if log.get("calories_burned") else ""
        st.markdown(f"- {log['date']}: {log['routine']}{kc}")

st.subheader("Weekly Exercise Checklist")
today = datetime.utcnow().date()
monday = today - timedelta(days=today.weekday())
week_days = [monday + timedelta(days=i) for i in range(7)]
logs = list_workout_logs(st.session_state.user["id"], limit=200)
done_by_day = {str(l["date"]): True for l in logs}
cols = st.columns(7)
for i, day in enumerate(week_days):
    label = day.strftime("%a\n%m-%d")
    checked = done_by_day.get(day.isoformat(), False)
    cols[i].checkbox(label, value=checked, key=f"wk_{day.isoformat()}", disabled=True)

st.subheader("Activity Stream")
for a in list_activity(st.session_state.user["id"], limit=15):
    st.markdown(f"- {a['created_at']} [{a['type']}]: {a['payload']}")

 