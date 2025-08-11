import os
import streamlit as st
from backend.crud import update_user_profile, upsert_profile_media, log_activity
from backend.database import init_db


# Ensure database and migrations are applied even when navigating directly to this page
init_db()

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
    col1, col2 = st.columns([1,3])
    with col1:
        if u.get("profile_photo_path"):
            st.image(u["profile_photo_path"], width=140)
        elif u.get("avatar_choice"):
            st.markdown(f"<div style='font-size:96px'>{u['avatar_choice']}</div>", unsafe_allow_html=True)
        else:
            st.markdown("No photo/avatar")
    with col2:
        st.markdown(f"**Name**: {u.get('name','-')}")
        st.markdown(f"**Age**: {u.get('age','-')}  |  **Gender**: {u.get('gender','-')}")
        st.markdown(f"**Height**: {u.get('height_cm','-')} cm  |  **Weight**: {u.get('weight_kg','-')} kg")
        st.markdown(f"**Goal**: {u.get('fitness_goal','-')}  |  **Activity**: {u.get('activity_level','-')}")
        st.markdown(f"**Diet**: {u.get('dietary_preferences','-')}")
        st.markdown(f"**Preferred Start**: {u.get('daily_schedule','-')}")
        st.markdown(f"**Medical**: {u.get('medical_conditions','-')}")
    st.divider()
    st.page_link("pages/challenges.py", label="View Challenges ➜", icon="🔥")

 