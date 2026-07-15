# CV Analyzer

A Python web app that analyzes CVs/resumes (PDF) and gives instant, structured feedback on formatting, wording, and common weaknesses — built after noticing my own CV needed exactly this kind of feedback while job hunting.



## The Problem

Job seekers rarely get direct, specific feedback on their CV before it's rejected by a recruiter or an automated screening system. Generic advice ("make it concise," "use action words") isn't actionable. This tool analyzes an actual CV and flags concrete, specific issues — missing sections, vague language, and a lack of measurable achievements — so the feedback can actually be acted on.

## Features

- **PDF upload & text extraction** — drag and drop a CV, text is extracted automatically using `pdfplumber`
- **Missing section detection** — checks for the presence of core CV sections (Contact Info, Education, Experience, Skills)
- **Weak phrase detection** — flags vague, low-impact language (e.g. "responsible for," "worked on") that weakens a CV
- **Length analysis** — flags CVs that are too short (lacking detail) or too long (losing the reader)
- **Quantified achievement detection** — checks whether claims are backed by real numbers (percentages, amounts) rather than vague descriptions
- **Instant, color-coded feedback** in a clean web interface — no installation needed for the end user beyond opening a browser

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Web framework | Streamlit |
| PDF processing | pdfplumber |

## Architecture

The app is deliberately split into independent layers, each one built and tested separately before being connected:

- **`pdf_extractor.py`** — input layer, converts an uploaded PDF into plain text
- **`rules_engine.py`** — logic layer, runs a set of independent checks against the extracted text and returns structured results
- **`app.py`** — display layer, Streamlit interface that ties the two together and renders results

This separation means each piece can be tested and debugged on its own — for example, `rules_engine.py` can be run directly from the command line against any PDF, without touching the web interface at all.

## Getting Started (Run It Locally)

### Prerequisites
- Python 3.10 or higher

### Setup
1. Clone the repository:
   ```
   git clone https://github.com/Zaneradebe6/cv_analyzer.git
   cd cv_analyzer
   ```
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   streamlit run app.py
   ```
5. It will automatically open in your browser at `localhost:8501`

## Roadmap

This project is actively being built out further:

- [ ] Integrate an LLM API (Claude/OpenAI) to give qualitative, nuanced feedback beyond rule-based checks — e.g. actual rewrite suggestions, not just flags
- [ ] Add an optional job description comparison — paste a job posting and get keyword-match feedback against it
- [ ] Deploy to Streamlit Community Cloud for a public live demo
- [ ] Expand the rules engine with more checks (formatting consistency, action-verb usage, etc.)

## Author

Built by **Zanele Radebe** — final-year BSc Information Technology student, North-West University.

- GitHub: [@Zaneradebe6](https://github.com/Zaneradebe6)
- Email: zaneradebe6@gmail.com

## License

This project is available under the MIT License.
