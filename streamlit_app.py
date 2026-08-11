"""Streamlit interface for the medical RAG assistant.

This file deliberately calls the existing RAG functions directly.  The FastAPI
application and all retrieval/generation logic remain independent and unchanged.
"""

import logging
import os
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Medical AI | Health assistant",
    page_icon=":material/medical_services:",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def configure_credentials() -> None:
    """Let Streamlit Cloud secrets provide the existing environment variables."""
    for key in ("mistral", "Pinecone_key"):
        if not os.getenv(key):
            try:
                secret_value = st.secrets.get(key)
            except FileNotFoundError:
                secret_value = None
            if secret_value:
                os.environ[key] = str(secret_value)


configure_credentials()

# Imports intentionally happen after secret fallback setup: the backend modules
# continue to use their existing environment-variable configuration unchanged.
from src.llm import generate_response
from src.query_rewrite import rewrite_query
from src.retrival import retrieve_documents


logger = logging.getLogger(__name__)
PROFILE_IMAGE = Path("data/shayanbaig.png")


def clear_conversation() -> None:
    st.session_state.messages = []


def history_for_pipeline() -> str:
    """Format only completed, prior turns like the FastAPI memory layer does."""
    return "\n".join(
        f"{message['role']}: {message['content']}"
        for message in st.session_state.messages
    )


def run_rag(question: str, previous_history: str) -> str:
    try:
        rewritten_question = rewrite_query(previous_history, question)
        logger.info(f"Rewritten question: {rewritten_question}")

        try:
            context = retrieve_documents(rewritten_question)
            logger.info("Document retrieval successful")
        except Exception as e:
            logger.exception("Document retrieval failed")
            context = ""

        logger.info("Calling generate_response...")
        answer = generate_response(context, question, previous_history)
        logger.info("generate_response successful")

        return getattr(answer, "content", str(answer))

    except Exception as e:
        logger.exception("Medical assistant response generation failed")
        return f"ERROR: {str(e)}"


st.session_state.setdefault("messages", [])

st.markdown(
    """
    <style>
      .stApp { background: #f8fbff; }
      .block-container { max-width: 980px; padding-top: 2rem; padding-bottom: 7rem; }
      [data-testid="stHeader"] { background: rgba(248, 251, 255, 0.88); }
      .st-key-app_header {
        background: #ffffff; border: 1px solid #e3edf7; border-radius: 18px;
        padding: 1rem 1.2rem; box-shadow: 0 8px 24px rgba(33, 74, 120, 0.05);
      }
      .st-key-chat_panel {
        background: #ffffff; border: 1px solid #e3edf7; border-radius: 22px;
        padding: 0.65rem 0.45rem; box-shadow: 0 12px 34px rgba(33, 74, 120, 0.06);
      }
      .st-key-about_section {
        background: #ffffff; border: 1px solid #e3edf7; border-radius: 20px;
        padding: 1.4rem; box-shadow: 0 8px 24px rgba(33, 74, 120, 0.04);
      }
      .st-key-new_conversation button {
        min-width: 42px; min-height: 42px; border-radius: 12px; border-color: #d5e5f5;
        color: #1666a8; background: #f4f9fe;
      }
      .st-key-new_conversation button:hover { border-color: #8dbde6; background: #eaf5ff; }
      [data-testid="stChatMessage"] { border-radius: 16px; padding: 0.3rem 0.2rem; }
      [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: #edf7ff; margin-left: 18%;
      }
      [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        background: #fbfdff; border: 1px solid #edf3f9; margin-right: 8%;
      }
      [data-testid="stChatInput"] { border: 1px solid #cddfee; border-radius: 16px; box-shadow: 0 8px 24px rgba(33, 74, 120, 0.10); }
      [data-testid="stChatInput"] textarea { font-size: 1rem; }
      [data-testid="stChatInput"] button { background: #1769aa; color: #ffffff; border-radius: 10px; }
      [data-testid="stImage"] img { border-radius: 14px; }
      @media (max-width: 640px) {
        .block-container { padding: 1rem 0.8rem 6rem; }
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) { margin-left: 4%; }
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) { margin-right: 0; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.container(key="app_header"):
    brand_column, action_column = st.columns([10, 1], vertical_alignment="center")
    with brand_column:
        st.title("Medical AI", anchor=False)
        st.caption("Your AI health assistant")
    with action_column:
        st.button(
            "+",
            key="new_conversation",
            help="Start a new conversation",
            on_click=clear_conversation,
        )

st.space("medium")

chat_panel = st.container(key="chat_panel", height=500)
with chat_panel:
    if not st.session_state.messages:
        st.markdown("### How can I help today?")
        st.caption("Ask a medical question and I’ll search the available medical knowledge base.")
    for message in st.session_state.messages:
        avatar = (
            ":material/account_circle:"
            if message["role"] == "user"
            else ":material/medical_services:"
        )
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

st.space("large")

with st.container(key="about_section"):
    st.subheader("About the creator", anchor=False)
    image_column, bio_column = st.columns([1, 4], vertical_alignment="center")
    with image_column:
        if PROFILE_IMAGE.exists():
            st.image(str(PROFILE_IMAGE), width="stretch")
    with bio_column:
        st.markdown("#### Muhammad Shayan Baig")
        st.caption("Aspiring AI & full-stack developer.")
        st.write(
            "Building AI applications,AI Automations ,RAG systems, chatbots, and intelligent software solutions."
        )

prompt = st.chat_input(
    "Ask a medical question...",
    key="medical_chat_input",
    submit_mode="disable",
)

if prompt and prompt.strip():
    question = prompt.strip()
    previous_history = history_for_pipeline()
    st.session_state.messages.append({"role": "user", "content": question})

    with chat_panel:
        with st.chat_message("user", avatar=":material/account_circle:"):
            st.markdown(question)

        with st.chat_message("assistant", avatar=":material/medical_services:"):
            with st.spinner("Medical AI is preparing a response..."):
                response = run_rag(question, previous_history)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
