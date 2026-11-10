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

    prompt = f"""You are an experienced recruiter and CV coach. Review the following CV text
and give specific, actionable feedback. Focus on:
1. Overall impression (2-3 sentences)
2. The 3 most important improvements to make, with concrete examples
3. One strength worth keeping

Be direct and specific. Avoid generic advice like "use action verbs" without showing exactly where.

CV TEXT:
{cv_text}
"""

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
        raise AIFeedbackError(
            "AI feedback is temporarily unavailable (configuration problem). Please try again later."
        )
    except RateLimitError:
        raise AIFeedbackError(
            "AI feedback is busy right now. Please try again in a minute."
        )
    except (APIConnectionError, APITimeoutError):
        raise AIFeedbackError(
            "Couldn't reach the AI service. Please check your connection and try again."
        )
    except Exception:
        raise AIFeedbackError(
            "Something went wrong getting AI feedback. Please try again later."
        )

    return response.choices[0].message.content


if __name__ == "__main__":
    # Usage: python ai_feedback.py path/to/cv.pdf
    from pdf_extractor import extract_text_from_pdf

    if len(sys.argv) < 2:
        print("Usage: python ai_feedback.py path/to/cv.pdf")
        sys.exit(1)

    text = extract_text_from_pdf(sys.argv[1])
    print(get_ai_feedback(text))
