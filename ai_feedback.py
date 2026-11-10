import os
import sys

from openai import (
    OpenAI,
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    APITimeoutError,
)

# Limit how much CV text is sent to the API (keeps costs and rate limits in check)
MAX_CV_CHARS = 6000


class AIFeedbackError(Exception):
    """An error whose message is safe to show directly to the user."""


def _get_api_key():
    """Look for the key in Streamlit Secrets first, then environment, then a local .env file."""
    key = None

    try:
        import streamlit as st
        key = st.secrets["GROQ_API_KEY"]
    except Exception:
        key = None

    if not key:
        key = os.getenv("GROQ_API_KEY")

    if not key:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            key = os.getenv("GROQ_API_KEY")
        except ImportError:
            pass

    return key.strip() if key else None


def get_ai_feedback(cv_text):
    api_key = _get_api_key()
    if not api_key:
        raise AIFeedbackError(
            "AI feedback isn't set up right now. The rule-based results above still work."
        )

    cv_text = cv_text[:MAX_CV_CHARS]

    prompt = f"""You are an
