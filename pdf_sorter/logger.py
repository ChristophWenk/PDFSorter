import logging
import warnings
from datetime import datetime
from PyPDF2.errors import PdfReadWarning
from pdf_sorter import settings


def setup_logger():
    logging_format = '%(asctime)-25s %(module)-18s %(levelname)-10s %(message)-8s'
    log_file_name = 'pdf_sorter_' + datetime.now().strftime("%Y-%m-%d") + '.log'
    log_file_path = '../target/logs/'

    logging.basicConfig(level=settings.log_level, format=logging_format, handlers=[
        logging.FileHandler(log_file_path + log_file_name, encoding='utf-8'),  # Write to file
        logging.StreamHandler()  # Write to console
    ])

    # Log filters
    warnings.filterwarnings("ignore", category=PdfReadWarning)
