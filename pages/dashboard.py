import random
import streamlit as st
from utils.styles import inject_landing_theme
from backend.crud import list_workout_logs, list_meal_logs, list_activity

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

col1, col2 = st.columns(2)
with col1:
    st.subheader("Recent Meals")
    for log in list_meal_logs(st.session_state.user["id"], limit=5):
        st.markdown(f"- {log['date']}: {log.get('description') or ''} {('~' + str(log['calories_est']) + ' kcal') if log.get('calories_est') else ''}")
with col2:
    st.subheader("Recent Workouts")
    for log in list_workout_logs(st.session_state.user["id"], limit=5):
        st.markdown(f"- {log['date']}: {log['routine']} {('~' + str(log['calories_burned']) + ' kcal') if log.get('calories_burned') else ''}")

st.subheader("Activity Stream")
for a in list_activity(st.session_state.user["id"], limit=15):
    st.markdown(f"- {a['created_at']} [{a['type']}]: {a['payload']}")
