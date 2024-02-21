import warnings

from tabula.io import read_pdf

# Disable all warnings
warnings.filterwarnings("ignore")


# Read PDF into DataFrame
def readPdfWithTabula(pdfFilePath):
    try:
        df = read_pdf(pdfFilePath, pages='all')
        return df
    except Exception as e:
        print("An error occurred while extracting text with tabula:", str(e))
        return None
