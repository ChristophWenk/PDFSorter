import json
import logging
import os
import re
from operator import itemgetter
from itertools import groupby
from os import listdir, makedirs
from os.path import isfile, join
from pathlib import Path
from data_sanitizer import sanitize_document_id, sanitize_date, sanitize_attr
from pdf_parser import read_pdf
from json_parser import read_json
from pdf_sorter.file_manipulator import rename_file, move_file
from pdf_sorter.logger import setup_logger

logger = logging.getLogger(__name__)


def create_document_type_list(path):
    file_list = [f for f in listdir(path) if isfile(join(path, f))]
    document_type_list = {}

    for file in file_list:
        company, document_type = file.replace('.json', '').split('-')
        if document_type_list.get(company):
            document_type_list.get(company).append(document_type)
        else:
            document_type_list.update({company: [document_type]})
    return document_type_list


# Check which document type is in scope
def evaluate_document_type(text, document_type_list, company):
    # Companies may appear in documents of other companies. Therefore, filter for document types that belong to the
    # selected company.
    for document_type in document_type_list[company]:
        if document_type in text:
            logger.info("Document Type: " + document_type)
            return document_type


# Check which company is in scope
def evaluate_company(text, document_type_list):
    company = None
    document_type = None
    for company in document_type_list:
        if company in text:
            document_type = evaluate_document_type(text, document_type_list, company)
            if document_type:
                logger.info("Company: " + company)
                break
    return company, document_type


def process_files(path, config_file_path):
    logger.info("\n"
                "##################################\n"
                "# Starting new PDF Sort Run\n"
                "##################################")
    document_type_list = create_document_type_list(config_file_path)
    file_path_list = [f for f in listdir(path) if isfile(join(path, f))]
    not_processed_list = []
    for file_name in file_path_list:
        logger.info('======================================================')
        logger.info("Processing file... " + file_name)

        pdf_file_path = path + '/' + file_name
        pdf_text = read_pdf(pdf_file_path)
        company, document_type = evaluate_company(pdf_text, document_type_list)

        if company is not None and document_type is not None:
            try:
                config = read_json(config_file_path + '/' + company + '-' + document_type + '.json')
            except FileNotFoundError as exception:
                logging.warning("Config file not found: " + exception.filename + ". Skipping PDF file.")
                not_processed_list.append(file_name)
                continue

            try:
                for regex_key in config['regex_paterns']:
                    try:
                        attribute_value = get_attr_from_regex(config, regex_key, file_name, not_processed_list, pdf_text)
                        sanitized_attr = sanitize_attr(attribute_value, regex_key)
                        config.update({regex_key: sanitized_attr})
                    except ValueError:
                        raise ValueError
            except ValueError:
                break

            try:
                renamed_file = rename_file(path, file_name, config)
            except PermissionError as exception:
                logging.warning("File not accessible: " + exception.filename + ". PDF file was not renamed.")
                not_processed_list.append(file_name)
                continue

            # try:
            #     target_directory = config['target_directory'] + "\\" + sanitized_date[0:4]
            #     makedirs(os.path.dirname(target_directory + "\\" + renamed_file),
            #              exist_ok=True)
            #     move_file(path, renamed_file, target_directory)
            # except PermissionError as exception:
            #     logging.warning("File not accessible: " + exception.filename + ". PDF file was not moved.")
            #     not_processed_list.append(renamed_file)
            #     continue

        else:
            logger.warning("Company name and document type not found. Skipping PDF file.")
            not_processed_list.append(file_name)
            continue

    logger.info('======================================================')
    logger.info("\n"
                "##################################\n"
                "# PDF Sort Run completed\n"
                "##################################")
    if not_processed_list:
        output_list = ""
        for file_name in not_processed_list:
            output_list += "\n" + file_name
        logger.warning("The following PDF files could not be processed or have just been partially processed:" +
                       output_list)


def get_attr_from_regex(config, regex, file_name, not_processed_list, pdf_text):
    regex_config = config['regex_paterns'][regex]
    compiled_regex = re.compile(regex_config)
    if compiled_regex.search(pdf_text) is not None:
        return compiled_regex.search(pdf_text).group()
    else:
        logger.warning("Value for Regular Expression " + regex + " not found. Skipping PDF file.")
        not_processed_list.append(file_name)
        raise ValueError(regex + ' not found')


# Main Function
if __name__ == '__main__':
    setup_logger()
    file_path = '../resources/test_files'
    config_file_path = '../resources/config_files'

    process_files(file_path, config_file_path)
