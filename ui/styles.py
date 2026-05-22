import streamlit as st


def load_css():

    st.markdown(
        """
        <style>

        /* MAIN BACKGROUND */

        .stApp {
            background-color: #0b1020;
            color: white;
        }

        /* SIDEBAR */

        section[data-testid="stSidebar"] {
            background-color: #111827;
            border-right: 1px solid #1f2937;
        }

        /* SIDEBAR BUTTONS */

        .stButton button {
            border-radius: 10px;
            border: 1px solid #374151;
            background-color: #1f2937;
            color: white;
            transition: 0.3s;
        }

        .stButton button:hover {
            background-color: #374151;
            border-color: #60a5fa;
        }

        /* CHAT INPUT */

        .stChatInput {
            position: fixed;
            bottom: 20px;
            left: 320px;
            right: 30px;
        }

        /* CHAT MESSAGE */

        .stChatMessage {
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 15px;
        }

        /* USER MESSAGE */

        [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
        ) {
            background-color: #1e293b;
        }

        /* ASSISTANT MESSAGE */

        [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
        ) {
            background-color: #111827;
        }

        /* INPUT BOX */

        textarea {
            background-color: #1f2937 !important;
            color: white !important;
            border-radius: 12px !important;
        }

        /* LOGIN CARD */

        .login-box {
            background-color: #111827;
            padding: 30px;
            border-radius: 16px;
            border: 1px solid #1f2937;
            margin-top: 30px;
        }

        /* TITLES */

        h1, h2, h3 {
            color: white !important;
        }

        /* SCROLLBAR */

        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-thumb {
            background: #374151;
            border-radius: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )