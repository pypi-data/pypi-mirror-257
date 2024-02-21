import warnings

import PyPDF2

# Disable all warnings
warnings.filterwarnings("ignore")


def readPdfWithPyPDF2(pdfFilePath):
    try:
        with open(pdfFilePath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            all_text = ""
            # Extract text from each page
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                all_text += text + "\n"
            return all_text
    except Exception as e:
        print("An error occurred while extracting text with PyPDF2:", str(e))
        return None
