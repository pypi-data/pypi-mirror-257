from pdfminer.high_level import extract_text


# Extract text from the PDF file

def readPdfWithPdfMiner(pdf_file_path):
    text = extract_text(pdf_file_path)
    if text is not None:
        return text
    else:
        return None


print(readPdfWithPdfMiner(r'D:\python\document\pdf\sample.pdf'))