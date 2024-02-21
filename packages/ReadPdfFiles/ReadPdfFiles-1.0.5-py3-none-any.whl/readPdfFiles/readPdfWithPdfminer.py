import warnings

from pdfminer.high_level import extract_text

# Disable all warnings
warnings.filterwarnings("ignore")


def readPdfWithPdfMiner(pdfFilePath):
    try:
        text = extract_text(pdfFilePath)
        return text
    except Exception as e:
        print("An error occurred while extracting text with PdfMiner:", str(e))
        return None
