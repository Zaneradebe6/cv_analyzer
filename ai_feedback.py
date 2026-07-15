import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def get_ai_feedback(cv_text):
    prompt = f"""You are an experienced recruiter and CV coach. Review the following CV text
and give specific, actionable feedback. Focus on:
1. Overall impression (2-3 sentences)
2. The 3 most important improvements to make, with concrete examples
3. One strength worth keeping

Be direct and specific — avoid generic advice like "use action verbs" without showing exactly where.

CV TEXT:
{cv_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
    )

    return response.choices[0].message.content
if __name__ == "__main__":
    from pdf_extractor import extract_text_from_pdf

    text = extract_text_from_pdf("Cv .pdf")
    feedback = get_ai_feedback(text)
    print(feedback)