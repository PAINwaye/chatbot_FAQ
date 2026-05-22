import streamlit as st
from database.db import supabase
from chatbot.llm import generate_response
from chatbot.prompts import get_system_prompt

from chatbot.history import (
    create_chat,
    save_message,
    load_chats,
    load_messages,
    delete_chat
)

from auth.auth import (
    signup_user,
    login_user,
    logout_user,
    google_login
)

from ui.styles import load_css

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI FAQ Chatbot",
    layout="wide"
)

# ---------------- LOAD CSS ---------------- #

load_css()

# ---------------- GOOGLE OAUTH SESSION ---------------- #

query_params = st.query_params

if "code" in query_params and st.session_state.user is None:

    try:

        session = supabase.auth.exchange_code_for_session(
            {
                "auth_code": query_params["code"]
            }
        )

        if session.user:

            st.session_state.user = session.user

            st.query_params.clear()

            st.rerun()

    except Exception as e:

        st.error(e)
# ---------------- SESSION STATE ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- AUTH SCREEN ---------------- #

if st.session_state.user is None:

    st.markdown(
        """
        <div class="login-box">

        <h1>🤖 AI FAQ Chatbot</h1>

        <p>
        Generate intelligent FAQs for any topic instantly.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Login / Signup")

    auth_mode = st.radio(
        "Choose",
        ["Login", "Signup"]
    )

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    # ---------------- LOGIN ---------------- #

    if auth_mode == "Login":

        if st.button(
            "Login",
            use_container_width=True
        ):

            response = login_user(
                email,
                password
            )

            if response and response.user:

                st.session_state.user = response.user

                st.success("Login successful")

                st.rerun()

    # ---------------- SIGNUP ---------------- #

    else:

        if st.button(
            "Signup",
            use_container_width=True
        ):

            response = signup_user(
                email,
                password
            )

            if response and response.user:

                st.success(
                    "Signup successful. Please login."
                )

    st.divider()

    # ---------------- GOOGLE LOGIN ---------------- #

    if st.button(
        "Continue with Google",
        use_container_width=True
    ):

        auth_url = google_login()

        st.link_button(
            "Click here to continue",
            auth_url,
            use_container_width=True
        )

    st.stop()

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.markdown(
        "## 💬 Chat History"
    )

    st.markdown(
        f"""
        ### 👤 User

        {st.session_state.user.email}
        """
    )

    # ---------------- LOGOUT ---------------- #

    if st.button(
        "Logout",
        use_container_width=True
    ):

        logout_user()

        st.session_state.user = None
        st.session_state.messages = []
        st.session_state.session_id = None

        st.rerun()

    st.divider()

    # ---------------- NEW CHAT ---------------- #

    if st.button(
        "+ New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.session_id = None

        st.rerun()

    st.divider()

    # ---------------- LOAD USER CHATS ---------------- #

    chats = load_chats(
        st.session_state.user.id
    )

    for chat in chats:

        col1, col2 = st.columns([4, 1])

        # LOAD CHAT
        with col1:

            if st.button(
                chat["title"],
                key=chat["id"],
                use_container_width=True
            ):

                st.session_state.session_id = chat["id"]

                messages = load_messages(
                    chat["id"]
                )

                st.session_state.messages = [
                    {
                        "role": msg["role"],
                        "content": msg["content"],
                        "created_at": msg.get("created_at", "")
                    }
                    for msg in messages
                ]

                st.rerun()

        # DELETE CHAT
        with col2:

            if st.button(
                "🗑️",
                key=f"delete_{chat['id']}"
            ):

                delete_chat(chat["id"])

                if st.session_state.session_id == chat["id"]:

                    st.session_state.messages = []
                    st.session_state.session_id = None

                st.rerun()

# ---------------- MAIN CHAT UI ---------------- #

st.markdown(
    """
    <h1 style='margin-bottom:20px;'>
    🤖 AI FAQ Chatbot
    </h1>
    """,
    unsafe_allow_html=True
)

# ---------------- DISPLAY MESSAGES ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message.get("created_at"):

            st.caption(message["created_at"])

# ---------------- CHAT INPUT ---------------- #

prompt = st.chat_input(
    "Enter any topic to generate FAQs..."
)

# ---------------- CHAT LOGIC ---------------- #

if prompt:

    # CREATE NEW CHAT
    if st.session_state.session_id is None:

        title = prompt[:40]

        session_id = create_chat(
            st.session_state.user.id,
            title
        )

        st.session_state.session_id = session_id

    # USER MESSAGE
    user_message = {
        "role": "user",
        "content": prompt
    }

    st.session_state.messages.append(
        user_message
    )

    save_message(
        st.session_state.session_id,
        "user",
        prompt
    )

    # DISPLAY USER MESSAGE
    with st.chat_message("user"):

        st.markdown(prompt)

    # SYSTEM PROMPT
    system_prompt = get_system_prompt()

    # FINAL AI MESSAGE LIST
    ai_messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ] + [
        {
            "role": msg["role"],
            "content": msg["content"]
        }
        for msg in st.session_state.messages
    ]

    # GENERATE RESPONSE
    with st.spinner("Generating FAQs..."):

        response = generate_response(
            ai_messages
        )

    # ASSISTANT MESSAGE
    assistant_message = {
        "role": "assistant",
        "content": response
    }

    st.session_state.messages.append(
        assistant_message
    )

    save_message(
        st.session_state.session_id,
        "assistant",
        response
    )

    # DISPLAY RESPONSE
    with st.chat_message("assistant"):

        st.markdown(response)