import streamlit as st
from backend.database import init_db
from backend.auth import register_user, login_user, fetch_user
from utils.styles import inject_landing_theme


st.set_page_config(page_title="Multi-Agentic Wellness Assistant", layout="wide")


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
                st.switch_page("pages/profile_setting.py")
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
    st.title("Multi-Agentic Wellness Assistant")
    st.caption("Your personal hub for mind, nutrition, and movement")
    if st.session_state.user:
        cols = st.columns([3, 1])
        with cols[0]:
            st.success(f"Logged in as {st.session_state.user['name']}")
        with cols[1]:
            if st.button("Logout"):
                st.session_state.user = None
                st.session_state.user_id = None
                st.rerun()
    else:
        st.info("Please log in to use the features.")
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
    # Logged in: show app header as usual
    header()


if __name__ == "__main__":
    main()
