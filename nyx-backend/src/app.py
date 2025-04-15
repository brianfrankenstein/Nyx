from src.brain import Brain
import streamlit as st
import time

brain = Brain()  # our central processing unit

# Sidebar debug controls
with st.sidebar:
    st.title("🔧 Debug Settings")
    show_memory = st.checkbox("🗄️ Show Memory Retrieval", value=False)
    show_prompt_injection = st.checkbox("💉 Show Prompt Injection", value=False)
    show_self_insights = st.checkbox("👥 Show Self Insight", value=True)
    show_companion_insights = st.checkbox("👥 Show Companion Insight", value=True)

# Main UI
st.title("💬 Nyx Chat")

def chat_stream(prompt):
    for char in prompt:
        yield char
        time.sleep(0.01)


def save_feedback(index):
    st.session_state.history[index]["feedback"] = st.session_state[f"feedback_{index}"]

if "history" not in st.session_state:
    st.session_state.history = []


# Create a table with two columns
chat_table = st.container()

for i, message in enumerate(st.session_state.history):
    row_cols = chat_table.columns([2, 1])  # Each message gets its own row with two columns

    # Left column: Chat messages
    with row_cols[0]:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.write(message["content"].expressed_response)
                feedback = message.get("feedback", None)
                st.session_state[f"feedback_{i}"] = feedback
                st.feedback(
                    "thumbs",
                    key=f"feedback_{i}",
                    disabled=feedback is not None,
                )
            else:
                st.write(message["content"])

    # Right column: Additional information
    with row_cols[1]:
        if message["role"] == "assistant":
            if show_self_insights:
                st.write(message["content"].self_insights)
            if show_companion_insights:
                st.write(message["content"].companion_insights)

# Input area spans full width
if prompt := st.chat_input("Say something"):
    response = brain.handle_message(prompt)

    # User message row
    user_cols = chat_table.columns([2, 1])
    with user_cols[0]:
        with st.chat_message("user"):
            st.write(prompt)
    with user_cols[1]:
        st.text(f"Message #{len(st.session_state.history)+1}")
        st.text("Role: user")

    st.session_state.history.append({"role": "user", "content": prompt})

    # Assistant message row
    assistant_cols = chat_table.columns([2, 1])
    with assistant_cols[0]:
        with st.chat_message("assistant"):
            st.write_stream(chat_stream(response.expressed_response))
            st.feedback(
                "thumbs",
                key=f"feedback_{len(st.session_state.history)}",
                on_change=save_feedback,
                args=[len(st.session_state.history)],
            )
    with assistant_cols[1]:
        if show_self_insights:
            st.write(response.self_insights)
        if show_companion_insights:
            st.write(response.companion_insights)

    st.session_state.history.append({"role": "assistant", "content": response})