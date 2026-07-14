import streamlit as st
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