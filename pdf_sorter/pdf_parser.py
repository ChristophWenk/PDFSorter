import logging
import settings
import pymupdf
import easyocr

logger = logging.getLogger(__name__)


def print_metadata(pdf_file):
    # printing number of pages in pdf file
    logger.debug(f"Total number of pages: {pdf_file.page_count}")
    logger.debug(f"Document Info: {pdf_file.metadata}")


def read_pdf(file_path):
    pdf_file = pymupdf.open(file_path)
    print_metadata(pdf_file)

    # Convert PDF to images
    zoom = 4
    matrix = pymupdf.Matrix(zoom, zoom)
    for i in range(pdf_file.page_count):
            image_path = f"{settings.image_output_dir}/image_{i + 1}.png"
            page = pdf_file.load_page(i)
            image = page.get_pixmap(matrix=matrix)
            image.save(image_path)

    # Read text from images with OCR
    reader = easyocr.Reader(settings.ocr_languages)
    pdf_textblock_list = []
    for i in range(pdf_file.page_count):
        pdf_textblock_list += reader.readtext(f"{settings.image_output_dir}/image_{i + 1}.png", detail=0)

    pdf_text = "".join(pdf_textblock_list)
    logger.debug(pdf_text)
    return pdf_text