import PyPDF2


def readPdfWithPyPDF2(pdf_file_path):
    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        # Get the number of pages
        num_pages = len(reader.pages)
        # Extract text from each page
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            if text is not None:
                return text
            else:
                return None