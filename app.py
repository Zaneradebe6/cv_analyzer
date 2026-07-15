import streamlit as st
from ai_feedback import get_ai_feedback
from pdf_extractor import extract_text_from_pdf
from rules_engine import run_all_checks

st.set_page_config(page_title="CV Analyzer", page_icon="📄")

st.title("📄 CV Analyzer")
st.write("Upload your CV as a PDF and get instant feedback on structure, wording, and common weaknesses recruiters look for.")

uploaded_file = st.file_uploader("Upload your CV (PDF only)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Reading your CV..."):
        text = extract_text_from_pdf(uploaded_file)

    if not text:
        st.error("Couldn't extract any text from this PDF. It might be a scanned image rather than real text.")
    else:
        results = run_all_checks(text)

        st.subheader("Results")

        if results["missing_sections"]:
            st.warning(f"**Missing sections:** {', '.join(results['missing_sections'])}")
        else:
            st.success("All expected sections found.")

        if results["weak_phrases"]:
            st.warning("**Weak phrases found:** " + ", ".join(results["weak_phrases"]))
        else:
            st.success("No common weak phrases detected.")

        st.info(f"**Word count:** {results['length']['word_count']} — {results['length']['verdict']}")

        count = results["quantified_achievements"]
        if count == 0:
            st.warning("No quantified achievements found. Try adding measurable impact where possible.")
        else:
            st.success(f"Found {count} quantified achievement(s).")

        with st.expander("See extracted text"):
            st.text(text)

        st.subheader("AI-Powered Feedback")
        st.write("Get personalized, in-depth feedback from an AI reviewer, beyond the rule-based checks above.")

        if st.button("Get AI Feedback"):
            with st.spinner("Analyzing your CV with AI... this can take a few seconds"):
                try:
                    ai_result = get_ai_feedback(text)
                    st.markdown(ai_result)
                except Exception as e:
                    st.error(f"Something went wrong getting AI feedback: {e}")
        