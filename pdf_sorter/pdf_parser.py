import PyPDF2
import logging

logger = logging.getLogger(__name__)


def print_metadata(pdf_file):
    # printing number of pages in pdf file
    logger.debug("Total number of pages: " + str(pdf_file.numPages))
    return pdf_file.numPages


def read_pdf(file_path):
    pdf_file = PyPDF2.PdfReader(file_path)
    print_metadata(pdf_file)

    pdf_text = ""
    i = 0
    while i < pdf_file.numPages:
        try:
            pdf_page = pdf_file.getPage(i)
            pdf_text += pdf_page.extractText()
        except IndexError:
            logger.warning("Page number " + str(i + 1) + " could not be read. Skipping page.")
        finally:
            i += 1
    return pdf_text
