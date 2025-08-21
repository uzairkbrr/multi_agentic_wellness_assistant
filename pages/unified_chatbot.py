import streamlit as st
import os
from datetime import datetime, timezone
from agents.unified_chatbot import generate_unified_response
from utils.styles import inject_landing_theme


# Page configuration
st.set_page_config(
    page_title="Wellness Assistant",
    page_icon="🤖",
    layout="wide"
)

# Check authentication
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access the Wellness Assistant.")
    st.stop()

# Initialize session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None


def save_uploaded_file(uploaded_file):
    """Save uploaded file and return the path"""
    if uploaded_file is not None:
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join("data", "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file with timestamp
        timestamp = datetime.now(timezone.utc).timestamp()
        file_path = os.path.join(upload_dir, f"{timestamp}_{uploaded_file.name}")
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    return None


def main():
    # ChatGPT-style dark theme
    st.markdown("""
    <style>
    .main {
        background-color: #343541;
        color: white;
    }
    .stApp {
        background-color: #343541;
    }
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 1rem;
        background-color: #343541;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }
    .chat-messages {
        flex: 1;
        padding: 1rem 0;
        margin-bottom: 120px;
    }
    .message {
        padding: 1rem;
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
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #343541;
        padding: 1rem;
        border-top: 1px solid #565869;
        z-index: 1000;
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
    .icon-button {
        background: none;
        border: none;
        color: #d1d5db;
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 4px;
        font-size: 1.2rem;
    }
    .icon-button:hover {
        background: #40414f;
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
    .file-upload {
        display: none;
    }
    .upload-icon {
        cursor: pointer;
        color: #d1d5db;
        font-size: 1.2rem;
    }
    .disclaimer {
        text-align: center;
        color: #8e8ea0;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Chat messages area
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="message user-message">
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message assistant-message">
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area (ChatGPT-style)
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
    
    # Hidden file upload
    uploaded_file = st.file_uploader(
        "Upload image", 
        type=['png', 'jpg', 'jpeg'],
        key="image_uploader",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.session_state.uploaded_image = save_uploaded_file(uploaded_file)
        st.success(f"✅ Image uploaded: {uploaded_file.name}")
    
    # Input field with icons
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col1:
        # Upload icon
        st.markdown("""
        <div class="upload-icon" onclick="document.getElementById('image_uploader').click()">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1H5C3.89 1 3 1.89 3 3V21C3 22.11 3.89 23 5 23H19C20.11 23 21 22.11 21 21V9M19 9H14V4H5V21H19V9Z"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Voice input button
        st.markdown("""
        <button class="icon-button" onclick="startVoiceRecognition()" title="Voice input">
            🎤
        </button>
        
        <script>
        function startVoiceRecognition() {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'en-US';
                
                recognition.onstart = function() {
                    console.log('Voice recognition started');
                };
                
                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    const input = document.querySelector('input[data-testid="stTextInput"]');
                    if (input) {
                        input.value = transcript;
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                };
                
                recognition.onerror = function(event) {
                    console.error('Speech recognition error:', event.error);
                };
                
                recognition.onend = function() {
                    console.log('Voice recognition ended');
                };
                
                recognition.start();
            } else {
                alert('Speech recognition not supported in this browser.');
            }
        }
        </script>
        """, unsafe_allow_html=True)
    
    with col3:
        # Text input
        user_input = st.text_input(
            "Message Wellness Assistant...",
            placeholder="Message Wellness Assistant...",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col4:
        # Send button
        send_button = st.button("➤", key="send_button", help="Send message")
    
    with col5:
        # Empty column for spacing
        st.markdown("&nbsp;", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown('<div class="disclaimer">Wellness Assistant can make mistakes. Check important info.</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle Enter key press
    st.markdown("""
    <script>
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            const sendButton = document.querySelector('button[data-testid="baseButton-secondary"]');
            if (sendButton) {
                sendButton.click();
            }
        }
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Process user input
    if send_button and user_input.strip():
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Show processing indicator
        with st.spinner("🤖 Thinking..."):
            try:
                # Generate response
                response_data = generate_unified_response(
                    user_message=user_input,
                    user_id=st.session_state.user["id"],
                    chat_history=st.session_state.chat_history,
                    image_path=st.session_state.uploaded_image
                )
                
                # Add assistant response to history
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": response_data["response"]
                })
                
                # Clear uploaded image after processing
                if st.session_state.uploaded_image:
                    st.session_state.uploaded_image = None
                
                st.rerun()
                
            except Exception as e:
                error_message = f"❌ Sorry, I encountered an error: {str(e)}"
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": error_message
                })
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
