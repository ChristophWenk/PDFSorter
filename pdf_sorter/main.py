import logging
import re
from os import listdir
from os.path import isfile, join
from data_sanitizer import sanitize_document_id, sanitize_date
from pdf_parser import read_pdf
from json_parser import read_json
from pdf_sorter.logger import setup_logger

logger = logging.getLogger(__name__)


def create_document_type_list(path):
    file_list = [f for f in listdir(path) if isfile(join(path, f))]
    document_type_list = []
    for file in file_list:
        document_type_list.append(file.replace('.json', '').split('-'))
    return document_type_list


def evaluate_document_type(text, document_type_list):
    for document_type_tuple in document_type_list:
        if document_type_tuple[1] in text:
            logger.info("Document Type: " + document_type_tuple[1])
            return document_type_tuple[1]


# Check which company is in scope
def evaluate_company(text, document_type_list):
    company = None
    document_type = None
    for document_type_tuple in document_type_list:
        if document_type_tuple[0] in text:
            logger.info("Company: " + document_type_tuple[0])
            company = document_type_tuple[0]
            document_type = evaluate_document_type(text, document_type_list)
            break
    return company, document_type


def get_config_file(company, document_type, config_file_path):
    return read_json(config_file_path + '/' + company + '-' + document_type + '.json')


def process_files(path, config_file_path):
    logger.info("\n"
                "##################################\n"
                "# Starting new PDF Sort Run\n"
                "##################################")
    file_path_list = [f for f in listdir(path) if isfile(join(path, f))]
    for file_name in file_path_list:
        logger.info('======================================================')
        logger.info("Processing file... " + file_name)
        pdf_file_path = path + '/' + file_name
        pdf_text = read_pdf(pdf_file_path)

        document_type_list = create_document_type_list(config_file_path)
        company, document_type = evaluate_company(pdf_text, document_type_list)

        if company is not None and document_type is not None:
            config = get_config_file(company, document_type, config_file_path)

            document_id_regex_config = config['regex_paterns']['document_id']
            document_id_regex = re.compile(document_id_regex_config)

            if document_id_regex.search(pdf_text) is not None:
                document_id = document_id_regex.search(pdf_text).group()
            else:
                logger.warning("Document ID not found. Skipping file.")
                continue
            sanitized_document_id = sanitize_document_id(document_id)
            logger.info("Document ID: " + sanitized_document_id)

            date_regex_config = config['regex_paterns']['date']
            date_regex = re.compile(date_regex_config)
            if date_regex.search(pdf_text) is not None:
                date = date_regex.search(pdf_text).group()
            else:
                logger.warning("Date not found. Skipping file.")
                continue
            sanitized_date = sanitize_date(date)
            logger.info("Date: " + sanitized_date)

            # renamed_file = rename_file(path, file_name, company, document_type, sanitized_date,
            #                            sanitized_document_id)
            # move_file(path, renamed_file, config['target_location'])

        else:
            logger.warning("Company name and document type not found. Skipping file.")
            continue



# Main Function
if __name__ == '__main__':
    setup_logger()
    file_path = '../resources/test_files'
    config_file_path = '../resources/config_files'

    process_files(file_path, config_file_path)
