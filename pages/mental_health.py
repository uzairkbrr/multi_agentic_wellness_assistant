import streamlit as st
from agents.mental_health import get_mental_health_response
from utils.memory_manager import summarize_messages
from utils.styles import inject_landing_theme
from backend.crud import insert_memory, list_memories, log_activity
from utils.token_manager import trim_messages_to_token_limit


if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in to access this page.")
    st.stop()

inject_landing_theme()
st.title("Mental Health Assistant")

if "mh_messages" not in st.session_state:
    st.session_state.mh_messages = [
        {"role": "system", "content": "You are a supportive, empathetic mental health assistant. Keep responses concise and gentle."}
    ]

# Recall past insights at the top
with st.expander("Recall past insights"):
    memories = list_memories(st.session_state.user["id"], limit=20)
    for m in memories:
        st.markdown(f"- {m['created_at']}: {m['summary']}")

col1, col2 = st.columns([3, 1])
with col1:
    enable_memory = st.toggle("Store key insights to long-term memory")
with col2:
    if st.button("Summarize & Trim Context"):
        # Summarize older messages excluding system
        summary = summarize_messages(st.session_state.mh_messages[1:])
        st.session_state.mh_messages = st.session_state.mh_messages[:1] + [
            {"role": "system", "content": f"Conversation summary so far: {summary}"}
        ]

left, right = st.columns([1,3])
with left:
    # Past Insights section removed
    pass
with right:
    for msg in st.session_state.mh_messages[1:]:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        elif msg["role"] == "assistant":
            st.chat_message("assistant").write(msg["content"])

prompt = st.chat_input("Share what's on your mind...")
if prompt:
    st.session_state.mh_messages.append({"role": "user", "content": prompt})
    limited = trim_messages_to_token_limit(st.session_state.mh_messages, 2000)
    reply = get_mental_health_response(limited)
    st.session_state.mh_messages.append({"role": "assistant", "content": reply})
    st.chat_message("user").write(prompt)
    st.chat_message("assistant").write(reply)

    if enable_memory:
        try:
            insert_memory(
                user_id=st.session_state.user["id"],
                summary=reply[:800],
                tags="check-in",
            )
        except Exception as e:
            st.warning(f"Memory save failed: {e}")
    log_activity(st.session_state.user["id"], "mh_chat", {"prompt": prompt[:120], "reply_len": len(reply)})

 