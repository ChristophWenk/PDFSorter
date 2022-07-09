import logging
from datetime import datetime


def setup_logger():
    logging_format = '%(asctime)-25s %(module)-12s %(levelname)-10s %(message)-8s'
    log_file_name = 'pdf_sorter_' + datetime.now().strftime("%Y-%m-%d") + '.log'
    log_file_path = '../target/logs/'
    logging.basicConfig(level=logging.INFO, format=logging_format, handlers=[
        logging.FileHandler(log_file_path + log_file_name, encoding='utf-8'),  # Write to file
        logging.StreamHandler()  # Write to console
    ])
