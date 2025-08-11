import streamlit as st
from datetime import datetime
from backend.crud import (
    list_relevant_challenges,
    join_challenge,
    list_user_challenges,
    update_challenge_progress,
    log_activity,
)
from utils.styles import inject_landing_theme
from backend.crud import ensure_default_challenges


inject_landing_theme()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in to access this page.")
    st.stop()

ensure_default_challenges()

st.title("Challenges")
st.caption("Join challenges tailored to your goals and share your progress.")

u = st.session_state.user
mine = list_user_challenges(u["id"]) or []
joined_ids = {m["challenge_id"] for m in mine}

st.subheader("Suggested Challenges")
goal = (u.get("fitness_goal") or "").replace(" ", "_").lower()
activity = (u.get("activity_level") or "").lower()
suggested = list_relevant_challenges(goal_type=goal if goal else None, difficulty=None, limit=10)
for c in suggested:
    with st.container():
        st.markdown(f"**{c['title']}** — {c.get('description') or ''}")
        cols = st.columns([1,1,1])
        with cols[0]:
            st.caption(f"Goal: {c.get('goal_type') or '-'}")
        with cols[1]:
            st.caption(f"Difficulty: {c.get('difficulty') or '-'}")
        with cols[2]:
            st.caption(f"Duration: {c.get('duration_days') or '-'} days")
        if c["id"] in joined_ids:
            st.info("Already joined ✅")
        else:
            if st.button(f"Join #{c['id']}", key=f"join_{c['id']}"):
                join_challenge(u["id"], c["id"])
                log_activity(u["id"], "challenge_update", {"action": "join", "challenge_id": c["id"]})
                st.success("Joined challenge.")

st.subheader("My Challenges")
for m in mine:
    with st.expander(f"{m['title']} — {m['status']} — {m['progress']}%"):
        new_progress = st.slider("Update progress", 0, 100, m["progress"], key=f"pr_{m['id']}")
        new_status = st.selectbox("Status", ["active", "completed", "dropped"], index=["active", "completed", "dropped"].index(m["status"]), key=f"st_{m['id']}")
        if st.button(f"Save Update {m['challenge_id']}", key=f"save_{m['id']}"):
            update_challenge_progress(u["id"], m["challenge_id"], new_progress, new_status)
            log_activity(u["id"], "challenge_update", {
                "action": "update",
                "challenge_id": m["challenge_id"],
                "progress": new_progress,
                "status": new_status,
            })
            st.success("Progress updated.")


