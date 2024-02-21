import warnings

import fitz

# Disable all warnings
warnings.filterwarnings("ignore")


def readPdfWithFitz(pdfFilePath):
    try:
        pdfDocument = fitz.open(pdfFilePath)
        all_text = ""
        for pageNumber in range(len(pdfDocument)):
            page = pdfDocument[pageNumber]
            text = page.get_text()
            if text is not None:
                all_text += text + "\n"
        return all_text
    except Exception as e:
        print("An error occurred while extracting text with fitz:", str(e))
        return None
