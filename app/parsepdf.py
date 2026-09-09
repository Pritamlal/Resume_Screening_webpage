import PyPDF2 as pypdf


def parse_pdf(file) -> str:
    print("INFO: Parsing PDF file...")
    try:
        reader = pypdf.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"

        cleaned_text = text.strip()
        print(f"INFO: PDF parsed successfully. Extracted {len(cleaned_text)} characters.")
        return cleaned_text
    except Exception as e:
        print(f"ERROR: Failed to parse PDF: {str(e)}")
        return str(e)