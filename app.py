import streamlit as st
from backend.database import init_db
from backend.auth import register_user, login_user, fetch_user
from utils.styles import inject_landing_theme


st.markdown("""
<style>
.st-emotion-cache-8fjoqp,
.st-emotion-cache-vqhohv p,
.st-ba, 
.st-emotion-cache-9ajs8n h1 {
    max-width: 900px;
    width: 100%;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="Wellness Assistant", layout="wide")


def _ensure_user_state():
    if "user" not in st.session_state:
        st.session_state.user = None
    # persist only the user id in session cookie to survive refresh
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    # hydrate user from id on refresh
    if not st.session_state.user and st.session_state.user_id:
        user = fetch_user(st.session_state.user_id)
        if user:
            st.session_state.user = user


def login_register_ui():
    cols = st.columns([1,2,1])
    with cols[1]:
        tabs = st.tabs(["Login", "Register"])
    with tabs[0]:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state.user = user
                st.session_state.user_id = user["id"]
                st.success("Logged in")
                st.switch_page("pages/unified_chatbot.py")
            else:
                st.error("Invalid credentials")
    with tabs[1]:
        st.subheader("Register")
        name = st.text_input("Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        if st.button("Create Account"):
            try:
                uid = register_user(name, email, password)
                st.success("Account created. Please login.")
            except Exception as e:
                st.error(f"Registration failed: {e}")


def header():
    st.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
    st.title("🤖 Wellness Assistant")
    st.caption("Your personal AI companion for health, nutrition, and fitness")
    if st.session_state.user:
        st.success(f"Welcome back, {st.session_state.user['name']}!")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Start Chatting", type="primary", use_container_width=True):
                st.switch_page("pages/unified_chatbot.py")
        with col3:
            if st.button("👤 Profile"):
                st.switch_page("pages/profile.py")
        with col1:
            if st.button("Logout"):
                st.session_state.user = None
                st.session_state.user_id = None
                st.rerun()
    else:
        st.info("Please log in to access your personal wellness assistant.")
    st.markdown("</div>", unsafe_allow_html=True)


def main():
    init_db()
    _ensure_user_state()
    inject_landing_theme()
    
    # If not logged in and no signup query, show landing; if signup query present, show auth UI
    if not st.session_state.user:
        if st.query_params.get("signup"):
            header()
            login_register_ui()
        else:
            st.switch_page("pages/landing_page.py")
        # Hide pages when not logged in via navigation links only
        st.markdown("<style>section[data-testid='stSidebarNav'] ul li { display:none; }</style>", unsafe_allow_html=True)
        return
    
    # Logged in: show app header and redirect to chatbot
    header()
    
    # Show features overview
    st.markdown("---")
    st.markdown("### 🎯 What I can help you with:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🍽️ Nutrition & Diet**
        - Food image analysis
        - Meal suggestions
        - Diet advice
        - Calorie tracking
        """)
    
    with col2:
        st.markdown("""
        **💪 Exercise & Fitness**
        - Workout plans
        - Exercise advice
        - Fitness tracking
        - Progress monitoring
        """)
    
    with col3:
        st.markdown("""
        **🧠 Mental Health**
        - Emotional support
        - Stress management
        - Mood tracking
        - Wellness guidance
        """)
    
    st.markdown("---")
    st.markdown("### 🚀 Ready to get started?")
    st.markdown("Click the **'Start Chatting'** button above to begin your wellness journey!")


if __name__ == "__main__":
    main()
