import PyPDF2
import logging

logger = logging.getLogger(__name__)


def print_metadata(pdf_file):
    # printing number of pages in pdf file
    logger.debug("Total number of pages: " + pdf_file.numPages.__str__())
    return pdf_file.numPages


def read_pdf(file_path):
    file = open(file_path, 'rb')
    pdf_file = PyPDF2.PdfFileReader(file)
    print_metadata(pdf_file)

    pdf_text = ""
    i = 0
    while i < pdf_file.numPages:
        pdf_page = pdf_file.getPage(i)
        pdf_text += pdf_page.extractText()
        i += 1
    file.close()
    return pdf_text
