import logging
import os
import warnings
from datetime import datetime
from os import makedirs

from PyPDF2.errors import PdfReadWarning
import settings


def setup_logger():
    logging_format = '%(asctime)-25s %(module)-18s %(levelname)-10s %(message)-8s'
    log_file_name = 'pdf_sorter_' + datetime.now().strftime("%Y-%m-%d") + '.log'

    makedirs(os.path.dirname(settings.log_files_dir),
             exist_ok=True)

    logging.basicConfig(level=settings.log_level, format=logging_format, handlers=[
        logging.FileHandler(f"{settings.log_files_dir}/{log_file_name}", encoding='utf-8'),  # Write to file
        logging.StreamHandler()  # Write to console
    ])

    # Log filters
    warnings.filterwarnings("ignore", category=PdfReadWarning)
