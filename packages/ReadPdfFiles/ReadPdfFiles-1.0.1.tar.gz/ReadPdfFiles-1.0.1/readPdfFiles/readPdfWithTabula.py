from tabula.io import read_pdf


# Read PDF into DataFrame

def readPdfWithTabula(pdf_file_path):
    text = read_pdf(pdf_file_path, pages='all')
    if text is not None:
        return text
    else:
        return None


print(readPdfWithTabula(r'D:\python\document\pdf\sample.pdf'))
