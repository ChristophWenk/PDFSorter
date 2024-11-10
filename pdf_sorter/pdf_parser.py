import logging
import pymupdf
import easyocr
import os
import settings

logger = logging.getLogger(__name__)


def print_metadata(pdf_file):
    logger.debug(f"Total number of pages: {pdf_file.page_count}")
    logger.debug(f"Document Info: {pdf_file.metadata}")


def read_pdf(file_path):
    image_name = "pdf_page"

    # Convert PDF to images
    pdf_file = pymupdf.open(file_path)
    print_metadata(pdf_file)

    zoom = 4
    matrix = pymupdf.Matrix(zoom, zoom)
    for i in range(pdf_file.page_count):
        image_path = f"{settings.image_output_dir}/{image_name}_{i + 1}.png"
        page = pdf_file.load_page(i)
        image = page.get_pixmap(matrix=matrix)
        image.save(image_path)

    # Read text from images with OCR
    reader = easyocr.Reader(settings.ocr_languages)
    pdf_textblock_list = []
    for i in range(pdf_file.page_count):
        pdf_textblock_list += reader.readtext(f"{settings.image_output_dir}/{image_name}_{i + 1}.png", detail=0)
        os.remove(f"{settings.image_output_dir}/{image_name}_{i + 1}.png")
    pdf_file.close()

    pdf_text = "".join(pdf_textblock_list)
    logger.debug(f"PDF text: \n{pdf_text}")
    return pdf_text
