import os
import base64
import streamlit as st
from backend.crud import update_user_profile, upsert_profile_media, log_activity
from backend.database import init_db
from utils.styles import inject_landing_theme


# Ensure database and migrations are applied even when navigating directly to this page
init_db()
inject_landing_theme()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in to access this page.")
    st.stop()


st.title("Profile")
st.caption("Set up your profile once, then review and tweak anytime.")

u = st.session_state.user
# Default to Edit for new/incomplete profiles
is_incomplete = not any([u.get("age"), u.get("fitness_goal"), u.get("activity_level")])
mode = st.radio("Mode", ["View", "Edit"], index=(1 if is_incomplete else 0), horizontal=True)

if mode == "Edit":
    st.subheader("Profile Photo / Avatar")
    colA, colB = st.columns(2)
    with colA:
        upload = st.file_uploader("Upload Profile Photo", type=["jpg", "jpeg", "png"], key="profile_photo")
        if upload is not None:
            try:
                os.makedirs("data/profile", exist_ok=True)
                filename = f"user_{u['id']}_{upload.name}"
                save_path = os.path.join("data", "profile", filename)
                with open(save_path, "wb") as f:
                    f.write(upload.getbuffer())
                upsert_profile_media(u["id"], photo_path=save_path, avatar_choice=None)
                st.session_state.user["profile_photo_path"] = save_path
                log_activity(u["id"], "profile_update", {"photo": True})
                st.success("Photo updated.")
                st.image(save_path, width=160)
            except Exception as e:
                st.error(f"Upload failed: {e}")
    with colB:
        st.write("Or choose an avatar")
        avatars = ["🧘", "🏋️", "🥗", "🏃", "🌟", "💪", "😊"]
        choice = st.selectbox("Avatar", avatars, key="avatar_choice")
        if st.button("Set Avatar"):
            upsert_profile_media(u["id"], photo_path=None, avatar_choice=choice)
            st.session_state.user["avatar_choice"] = choice
            log_activity(u["id"], "profile_update", {"avatar": choice})
            st.success("Avatar set.")
            st.markdown(f"Current avatar: {choice}")

if mode == "Edit":
    with st.form("profile_form"):
        row1 = st.columns(3)
        with row1[0]:
            name = st.text_input("Name", value=u.get("name", ""))
        with row1[1]:
            age = st.number_input("Age", min_value=0, max_value=120, value=int(u.get("age") or 0))
        with row1[2]:
            gender = st.selectbox("Gender", ["", "Male", "Female", "Non-binary", "Prefer not to say"], index=0)

        row2 = st.columns(3)
        with row2[0]:
            height_cm = st.number_input("Height (cm)", min_value=0.0, value=float(u.get("height_cm") or 0.0))
        with row2[1]:
            weight_kg = st.number_input("Weight (kg)", min_value=0.0, value=float(u.get("weight_kg") or 0.0))
        with row2[2]:
            fitness_goal = st.selectbox("Fitness Goal", ["", "Weight loss", "Muscle gain", "Maintenance"])

        row3 = st.columns(3)
        with row3[0]:
            activity_level = st.selectbox("Activity Level", ["", "Sedentary", "Lightly active", "Active", "Very active"])
        with row3[1]:
            dietary_options = ["", "None", "Vegan", "Vegetarian", "Pescatarian", "Keto", "Paleo", "Gluten-free", "Dairy-free", "Nut allergy", "Halal", "Kosher"]
            dietary_preferences = st.selectbox("Dietary Preferences", options=dietary_options, index=0)
        with row3[2]:
            time_options = [f"{h:02d}:00" for h in range(0,24)]
            start_time = st.selectbox("Preferred Start Time", time_options, index=8)

        mental_health_background = st.text_area("Mental Health Background (optional)", value=u.get("mental_health_background") or "")
        medical_conditions = st.text_area("Medical conditions (if any)", value=u.get("medical_conditions") or "", placeholder="e.g., asthma, hypertension, knee pain")

        submitted = st.form_submit_button("Save Profile")
        if submitted:
            fields = {
                "name": name,
                "age": int(age) if age else None,
                "gender": gender or None,
                "height_cm": float(height_cm) if height_cm else None,
                "weight_kg": float(weight_kg) if weight_kg else None,
                "fitness_goal": fitness_goal or None,
                "activity_level": activity_level or None,
                "dietary_preferences": dietary_preferences or None,
                "mental_health_background": mental_health_background or None,
                "daily_schedule": start_time or None,
                "medical_conditions": medical_conditions or None,
            }
            fields = {k: v for k, v in fields.items() if v is not None}
            update_user_profile(u["id"], fields)
            st.session_state.user.update(fields)
            log_activity(u["id"], "profile_update", {"fields": list(fields.keys())})
            st.success("Profile updated.")

if mode == "View":
    # Futuristic profile display
    name = u.get('name', '-')
    age = u.get('age', '-')
    gender = u.get('gender', '-')
    height_cm = u.get('height_cm', '-')
    weight_kg = u.get('weight_kg', '-')
    goal = u.get('fitness_goal', '-')
    activity = u.get('activity_level', '-')
    diet = u.get('dietary_preferences', '-')
    preferred = u.get('daily_schedule', '-')
    medical = u.get('medical_conditions', '-')

    photo_path = u.get("profile_photo_path")
    avatar_choice = u.get("avatar_choice", "🌟")

    st.markdown(
        """
<style>
.profile-card { position: relative; border-radius: 18px; padding: 24px; margin: 8px 0 16px 0; background: linear-gradient(135deg, rgba(30,144,255,0.12), rgba(168,85,247,0.12)); border: 1px solid rgba(255,255,255,0.18); box-shadow: 0 10px 30px rgba(0,0,0,0.15), inset 0 0 30px rgba(30,144,255,0.12); backdrop-filter: blur(10px) saturate(160%); -webkit-backdrop-filter: blur(10px) saturate(160%); }
.avatar-center { display: flex; justify-content: center; margin-bottom: 10px; }
.avatar-wrap { width: 160px; height: 160px; border-radius: 50%; overflow: hidden; border: 2px solid rgba(30,144,255,0.6); box-shadow: 0 8px 24px rgba(30,144,255,0.25), 0 0 0 6px rgba(30,144,255,0.08); display:flex; align-items:center; justify-content:center; background: rgba(255,255,255,0.6); }
.avatar-wrap img { width: 100%; height: 100%; object-fit: cover; display: block; }
.avatar-emoji { font-size: 96px; line-height: 1; }
.profile-name { font-weight: 900; font-size: 1.8rem; color: #0f172a; margin: 8px 0 0 0; text-align: center; }
.stat-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; justify-content: center; }
.chip { font-weight: 700; font-size: 0.85rem; padding: 6px 12px; border-radius: 999px; color: #1e293b; background: rgba(255,255,255,0.75); border: 1px solid rgba(30,144,255,0.25); box-shadow: 0 6px 16px rgba(0,0,0,0.06); }
.info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-top: 16px; }
.info-card { background: rgba(255,255,255,0.66); border: 1px solid rgba(30,144,255,0.16); border-radius: 14px; padding: 12px 14px; box-shadow: 0 8px 22px rgba(0,0,0,0.08); }
.info-label { color: #334155; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; font-weight: 800; opacity: 0.8; margin-bottom: 4px; }
.info-value { color: #0f172a; font-weight: 800; font-size: 1.05rem; }
</style>
        """,
        unsafe_allow_html=True,
    )

    # Build avatar/photo HTML using data URI to ensure proper rendering in the circular mask
    if photo_path and os.path.exists(photo_path):
        try:
            with open(photo_path, "rb") as _pf:
                b64 = base64.b64encode(_pf.read()).decode("utf-8")
            ext = os.path.splitext(photo_path)[1].lower()
            mime = "image/png" if ext == ".png" else "image/jpeg"
            img_src = f"data:{mime};base64,{b64}"
            avatar_html = f"<div class='avatar-wrap'><img src='{img_src}' alt='profile photo'/></div>"
        except Exception:
            avatar_html = f"<div class='avatar-wrap'><div class='avatar-emoji'>{avatar_choice}</div></div>"
    else:
        avatar_html = f"<div class='avatar-wrap'><div class='avatar-emoji'>{avatar_choice}</div></div>"

    # First row: profile picture centered, then subsequent rows for info
    st.markdown(
        f"""
<div class="profile-card">
  <div class="avatar-center">{avatar_html}</div>
  <h3 class="profile-name">{name}</h3>
  <div class="stat-chips">
    <div class="chip">Age: {age}</div>
    <div class="chip">Gender: {gender}</div>
    <div class="chip">Height: {height_cm} cm</div>
    <div class="chip">Weight: {weight_kg} kg</div>
  </div>
  <div class="info-grid">
    <div class="info-card"><div class="info-label">Goal</div><div class="info-value">{goal}</div></div>
    <div class="info-card"><div class="info-label">Activity</div><div class="info-value">{activity}</div></div>
    <div class="info-card"><div class="info-label">Diet</div><div class="info-value">{diet}</div></div>
    <div class="info-card"><div class="info-label">Preferred Start</div><div class="info-value">{preferred}</div></div>
    <div class="info-card"><div class="info-label">Medical</div><div class="info-value">{medical}</div></div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.page_link("pages/challenges.py", label="View Challenges ➜", icon="🔥")
    st.page_link("pages/dashboard.py", label="Go to Dashboard ➜", icon="🏠")

 