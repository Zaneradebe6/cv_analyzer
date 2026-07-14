import pdfplumber
def extract_text_from_pdf(pdf_file):
    full_text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    return full_text.strip()
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text = extract_text_from_pdf(sys.argv[1])
        print(f"Extracted {len(text)} characters:\n")
        print(text[:500])
    else:
        print("Usage: python pdf_extractor.py <path_to_pdf>")