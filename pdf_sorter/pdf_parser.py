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

    # Only read the first page as it contains all necessary information
    pdf_page = pdf_file.getPage(0)
    pdf_text = pdf_page.extractText()
    file.close()
    return pdf_text
