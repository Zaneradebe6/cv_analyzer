import os
import sys

from openai import (
    OpenAI,
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    APITimeoutError,
)

MAX_CV_CHARS = 6000

PROMPT_INTRO = (
    "You are an experienced recruiter and CV coach. "
    "Review the following CV text and give specific, actionable feedback. "
    "Focus on: (1) your overall impression in 2-3 sentences, "
    "(2) the 3 most important improvements, with concrete examples, "
    "(3) one strength worth keeping. "
    "Be direct and specific. Avoid generic advice without showing exactly where."
)


class AIFeedbackError(Exception):
    """An error whose message is safe to show directly to the user."""


def _get_api_key():
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

    prompt = PROMPT_INTRO + "\n\nCV TEXT:\n" + cv_text[:MAX_CV_CHARS]

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        timeout=30,
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
        )
    except AuthenticationError:
        raise AIFeedbackError("AI feedback is temporarily unavailable. Please try again later.")
    except RateLimitError:
        raise AIFeedbackError("AI feedback is busy right now. Please try again in a minute.")
    except (APIConnectionError, APITimeoutError):
        raise AIFeedbackError("Couldn't reach the AI service. Please try again.")
    except Exception:
        raise AIFeedbackError("Something went wrong getting AI feedback. Please try again later.")

    return response.choices[0].message.content


if __name__ == "__main__":
    from pdf_extractor import extract_text_from_pdf

    if len(sys.argv) < 2:
        print("Usage: python ai_feedback.py path/to/cv.pdf")
        sys.exit(1)

    print(get_ai_feedback(extract_text_from_pdf(sys.argv[1])))
