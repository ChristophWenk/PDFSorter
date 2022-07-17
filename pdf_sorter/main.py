import logging
import os
import re
from os import listdir, makedirs
from os.path import isfile, join
from data_sanitizer import sanitize_attr
from json_parser import read_json
from pdf_parser import read_pdf
import settings
from file_manipulator import rename_file, move_file
from logger import setup_logger

logger = logging.getLogger(__name__)


def create_document_type_list(path):
    file_list = [f for f in listdir(path) if isfile(join(path, f))]
    document_type_list = {}

    for file in file_list:
        company, document_type, config_date = file.replace('.json', '').split('-')
        logger.debug("Company: " + company + ", Document Type: " + document_type + ", Config Date: " + config_date)
        if document_type_list.get(company):
            document_type_list.get(company).append(document_type)
        else:
            document_type_list.update({company: [document_type]})
    return document_type_list


# Check which document type is in scope
def get_document_type(text, document_type_list, company):
    # Companies may appear in documents of other companies. Therefore, filter for document types that belong to the
    # selected company.
    for document_type in document_type_list[company]:
        if document_type in text:
            logger.debug("Document Type retrieved from config file name: " + document_type)
            return document_type


# Check which company is in scope
def get_company(text, document_type_list):
    company = None
    document_type = None
    for company in document_type_list:
        if company in text:
            document_type = get_document_type(text, document_type_list, company)
            if document_type:
                logger.debug("Company retrieved from config file name: " + company)
                break
    return company, document_type


def get_attr_from_regex(config, regex, file_name, not_processed_list, pdf_text):
    regex_config = config['regex_patterns'][regex]
    compiled_regex = re.compile(regex_config)
    if compiled_regex.search(pdf_text) is not None:
        return compiled_regex.search(pdf_text).group()
    else:
        raise ValueError(regex)


def process_files(path, config_file_path):
    logger.info("##################################")
    logger.info("# Starting new PDF Sort Run      #")
    logger.info("##################################")
    if settings.dry_run is True:
        logger.warning("Dry Run active: Running in preview mode. No files will be renamed or moved.")

    document_type_list = create_document_type_list(config_file_path)
    file_path_list = [f for f in listdir(path) if isfile(join(path, f))]
    not_processed_list = []
    for file_name in file_path_list:
        logger.info('==============================================================================================')
        logger.info("Processing file... " + file_name)

        pdf_text = read_pdf(path + '/' + file_name)
        company, document_type = get_company(pdf_text, document_type_list)

        if company is not None and document_type is not None:
            try:
                # Get config values for current PDF
                config = read_json(config_file_path + '/' + company + '-' + document_type + '.json')
                logger.info("company_name: " + config['company_name'])
                logger.info("document_type: " + config['document_type'])
            except FileNotFoundError as exception:
                logging.warning("Config file not found: " + exception.filename + ". Skipping PDF file.")
                not_processed_list.append(file_name)
                continue

            try:
                # Read out attribute values from PDF, sanitize them and attach them to config
                for regex_key in config['regex_patterns']:
                    attribute_value = get_attr_from_regex(config, regex_key, file_name, not_processed_list,
                                                          pdf_text)
                    sanitized_attr = sanitize_attr(attribute_value, regex_key)
                    config.update({regex_key: sanitized_attr})

                # Rename file
                renamed_file = rename_file(path, file_name, config)

                # Move file to target folder
                target_directory = config['target_directory'] + "\\" + config['date'][0:4]
                makedirs(os.path.dirname(target_directory + "\\" + renamed_file),
                         exist_ok=True)
                move_file(path, renamed_file, target_directory)
            except ValueError as exception:
                logger.warning("Value for Regular Expression " + exception.args[0] + " not found. Skipping PDF file.")
                not_processed_list.append(file_name)
                continue
            except PermissionError as exception:
                logging.warning("File not accessible: " + exception.filename + ". PDF file was not renamed or moved.")
                not_processed_list.append(file_name)
                continue
        else:
            logger.warning("Company name and/or document type not found. Skipping PDF file.")
            not_processed_list.append(file_name)
            continue

    logger.info('==============================================================================================')
    logger.info("##################################")
    logger.info("# PDF Sort Run completed         #")
    logger.info("##################################")

    if not_processed_list:
        logger.warning("The following PDF files could not be processed or have just been partially processed:")
        for file_name in not_processed_list:
            logger.warning(file_name)


# Main Function
if __name__ == '__main__':
    setup_logger()

    process_files(settings.pdf_files_dir, settings.config_files_dir)
