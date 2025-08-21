import streamlit as st
import os
from datetime import datetime, timezone
from agents.unified_chatbot import generate_unified_response

# Page configuration
st.set_page_config(
    page_title="Wellness Assistant",
    page_icon="🤖",
    layout="wide"
)

# --- Authentication check ---
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access the Wellness Assistant.")
    st.stop()

# --- Session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

if "input_key" not in st.session_state:
    st.session_state.input_key = 0


def save_uploaded_file(uploaded_file):
    """Save uploaded file and return the path"""
    if uploaded_file is not None:
        upload_dir = os.path.join("data", "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        timestamp = datetime.now(timezone.utc).timestamp()
        file_path = os.path.join(upload_dir, f"{timestamp}_{uploaded_file.name}")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None


def main():
    # --- Custom CSS ---
    st.markdown("""
    <style>

    .st-emotion-cache-zy6yx3 {
        padding-top: 40px;
    }

    .st-emotion-cache-1permvm {
        position: fixed;
        bottom: 50px;
        left: 400px;
        width: 70%;    
    }


    body, .stApp {
        background-color: #343541;
        color: white;
        margin: 0;
    }

    /* Chat container fills screen */
    .chat-container {
        display: flex;
        flex-direction: column;
        width: 100%;
        # padding-bottom: 80px; /* reserve space for input bar */
    }

    /* Scrollable messages */
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        # padding: 1rem;
    }

    .message {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        line-height: 1.6;
        max-width: 80%;
        word-wrap: break-word;
    }
    .user-message {
        background-color: #10a37f;
        color: white;
        margin-left: auto;
        text-align: right;
    }
    .assistant-message {
        background-color: #444654;
        color: white;
        margin-right: auto;
        text-align: left;
    }

    /* FIXED input at bottom */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #343541;
        padding: 0.75rem 1rem;
        z-index: 100;
    }

    .input-wrapper {
        max-width: 800px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .input-field {
        flex: 1;
        background: #40414f;
        border: 1px solid #565869;
        border-radius: 8px;
        padding: 0.75rem;
        color: white;
        font-size: 1rem;
    }
    .input-field:focus {
        outline: none;
        border-color: #10a37f;
    }

    .send-button {
        background: #10a37f;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        cursor: pointer;
        font-size: 1rem;
    }
    .send-button:hover {
        background: #0d8a6f;
    }

    .disclaimer {
        text-align: center;
        color: #8e8ea0;
        font-size: 0.8rem;
        position: fixed;
        bottom: 20px;
        left: 650px;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Chat container ---
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Messages area (scrollable)
    st.markdown('<div class="chat-messages" id="chat-messages">', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        role_class = "user-message" if message["role"] == "user" else "assistant-message"
        st.markdown(f"""
        <div class="message {role_class}">
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # end chat-messages

    # Auto-scroll to latest message
    st.markdown("""
    <script>
    var chatBox = document.getElementById('chat-messages');
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    </script>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # chat-container

    # --- Input area (fixed bottom) ---
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns([8, 1])
        with col1:
            user_input = st.text_input(
                "Message Wellness Assistant...",
                placeholder="Message Wellness Assistant...",
                key=f"user_input_{st.session_state.input_key}",
                label_visibility="collapsed"
            )
        with col2:
            send_button = st.button("➤", key=f"send_button_{st.session_state.input_key}")

    st.markdown('</div>', unsafe_allow_html=True)  # input-container

    # --- Handle sending ---
    if send_button and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("🤖 Thinking..."):
            try:
                response_data = generate_unified_response(
                    user_message=user_input,
                    user_id=st.session_state.user["id"],
                    chat_history=st.session_state.chat_history,
                    image_path=st.session_state.uploaded_image
                )
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response_data["response"]
                })
                st.session_state.uploaded_image = None
                st.session_state.input_key += 1
                st.rerun()
            except Exception as e:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"❌ Sorry, I encountered an error: {str(e)}"
                })
                st.session_state.input_key += 1
                st.rerun()


if __name__ == "__main__":
    main()
