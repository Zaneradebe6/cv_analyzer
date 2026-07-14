import re
EXPECTED_SECTIONS = {
    "Contact Info": ["email", "phone","@" ],
    "Education": ["education", "university", "degree", "bsc", "bachelor"],
    "Experience": ["experience", "work history", "employment"],
    "Skills": ["skills", "technologies", "proficiencies"],

}

WEAK_PHRASES = [
    "responsible for",
    "worked on",
    "helped with",
    "duties included",
    "tasked with",
    "various tasks",
    "things related to",
]

def check_missing_sections(text):
    text_lower = text.lower()
    missing = []

    for section_name, keywords in EXPECTED_SECTIONS.items():
        found = any(keyword in text_lower for keyword in keywords)
        if not found:
            missing.append(section_name)

    return missing
def check_weak_phrases(text):
    text_lower = text.lower()
    found_phrases = [phrase for phrase in WEAK_PHRASES if phrase in text_lower]
    return found_phrases

def check_word_count(text):
    word_count = len(text.split())

    if word_count < 150:
        verdict = "Too short — likely missing detail recruiters need"
    elif word_count > 1000:
        verdict = "Quite long — consider trimming to the most relevant points"
    else:
        verdict = "Reasonable length"

    return {"word_count": word_count, "verdict": verdict}


def check_quantified_achievements(text):
    numbers_found = re.findall(r"\d+%|\d+\+|\bR\d+|\$\d+", text)
    return len(numbers_found)


def run_all_checks(text):
    return {
        "missing_sections": check_missing_sections(text),
        "weak_phrases": check_weak_phrases(text),
        "length": check_word_count(text),
        "quantified_achievements": check_quantified_achievements(text),
    }


if __name__ == "__main__":
    from pdf_extractor import extract_text_from_pdf

    text = extract_text_from_pdf("Cv .pdf")
    results = run_all_checks(text)

    print("=== CV Analysis Results ===\n")
    print(f"Missing sections: {results['missing_sections']}")
    print(f"Weak phrases found: {results['weak_phrases']}")
    print(f"Length check: {results['length']}")
    print(f"Quantified achievements found: {results['quantified_achievements']}")
