import fitz  # PyMuPDF


def readPdfWithFitz(pdf_file_path):
    doc = fitz.open(pdf_file_path)
    # Extract text from each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        if text is not None:
            return text
        else:
            return None