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


def create_document_type_dictionary(path):
    file_list = [f for f in listdir(path) if isfile(join(path, f))]
    document_type_dictionary = {}

    for file in file_list:
        company, document_type, config_date = file.replace('.json', '').split('-')
        logger.debug("Company: " + company + ", Document Type: " + document_type + ", Config Date: " + config_date)
        # Add document type to company if it exists in the dictionary already
        if document_type_dictionary.get(company):
            document_type_dictionary.get(company).get('document_type_configurations').append(
                {
                    'document_type': document_type,
                    'config_date': config_date
                }
            )
        # Add company to dictionary
        else:
            document_type_dictionary.update(
                {
                    company:
                        {
                            'document_type_configurations':
                                [{
                                    'document_type': document_type,
                                    'config_date': config_date
                                }]
                        }
                }
            )
    return document_type_dictionary


# Create a list of all companies in the config files
def get_all_companies(document_type_dictionary):
    company_list = set()
    for company in document_type_dictionary:
        company_list.add(company)
    return company_list


# Check which companies might be in scope
def get_company_candidates(text, company_list):
    company_candidates = set()
    for company in company_list:
        if company in text:
            company_candidates.add(company)
    if company_candidates:
        # logger.info(f"Company candidates found in text: {str(company_candidates)}")
        logger.debug(f"Company candidates found in text: {', '.join(company_candidates)}")
        return company_candidates
    else:
        logger.warning("No company candidates found in text.")
        return None


# Check which document type is in scope
def get_document_type_for_company(text, document_type_dictionary, company):
    # Companies may appear in documents of other companies. Therefore, filter for document types that belong to the
    # selected company.
    for document_type_config in document_type_dictionary[company].get('document_type_configurations'):
        if document_type_config.get('document_type') in text:
            logger.info(f"Matched company name \"{company}\" to document type \"{document_type_config.get('document_type')}\"")
            return document_type_config.get('document_type')
    return None

# Check which company and document type is in scope
def get_document_types_for_company_list(text, document_type_dictionary, company_list):
    for company in company_list:
        if company in text:
            document_type = get_document_type_for_company(text, document_type_dictionary, company)
            if document_type:
                return company, document_type
    logger.warning("Did not find matching combination of company and document type.")
    return None, None


def get_attr_from_regex(config, regex, text):
    regex_config = config['regex_patterns'][regex]
    compiled_regex = re.compile(regex_config)
    if compiled_regex.search(text) is not None:
        return compiled_regex.search(text).group()
    else:
        raise ValueError(regex)


def get_document_type_configurations_for_company(company, document_type_dictionary):
    document_type_configuration_list = []
    for document_type_configuration in document_type_dictionary.get(company).get('document_type_configurations'):
        document_type_configuration_list.append(document_type_configuration)
    return document_type_configuration_list


def get_dates_for_document_types(document_type, document_type_configuration_list):
    document_type_dates_list = []
    for document_type_configuration in document_type_configuration_list:
        if document_type_configuration.get('document_type') == document_type:
            document_type_dates_list.append(document_type_configuration.get('config_date'))
    return document_type_dates_list


def process_files(path, config_file_path):
    if settings.dry_run is True:
        logger.warning("Dry Run active: Running in preview mode. No files will be renamed or moved.")
    logger.info("##################################")
    logger.info("# Starting new PDF Sort Run      #")
    logger.info("##################################")

    document_type_dictionary = create_document_type_dictionary(config_file_path)
    company_list = get_all_companies(document_type_dictionary)
    file_path_list = [f for f in listdir(path) if isfile(join(path, f))]
    not_processed_list = []
    for file_name in file_path_list:
        logger.info("\n")
        logger.info('==============================================================================================')
        logger.info("Processing file... " + file_name)

        pdf_text = read_pdf(f"{path}/{file_name}")

        company_candidates = get_company_candidates(pdf_text, company_list)
        if company_candidates is None:
            logger.warning("No suitable company candidates found. Skipping PDF file.")
            not_processed_list.append(file_name)
            continue

        company, document_type = get_document_types_for_company_list(pdf_text, document_type_dictionary,
                                                                     company_candidates)
        if company is None or document_type is None:
            logger.warning("Company name and/or document type not found. Skipping PDF file.")
            not_processed_list.append(file_name)
            continue

        document_types_configuration_list = get_document_type_configurations_for_company(company,
                                                                                         document_type_dictionary)
        # Sort by current dates because they are the ones that we need the most
        document_type_dates_list = sorted(get_dates_for_document_types(document_type,
                                                                       document_types_configuration_list))

        try:
            config = update_config_from_regex(pdf_text, document_type_dates_list, config_file_path, company,
                                              document_type)
            if not config:
                logger.warning("One or more values for regular expressions not found. Skipping PDF file.")
                not_processed_list.append(file_name)
                continue

        except FileNotFoundError as exception:
            logging.warning("Config file not found: " + exception.filename + ". Skipping PDF file.")
            not_processed_list.append(file_name)
            continue

        try:
            # Rename file
            renamed_file = rename_file(path, file_name, config)

            # Move file to target folder
            target_directory = config['target_directory'] + "\\" + config['date'][0:4]
            makedirs(os.path.dirname(target_directory + "\\" + renamed_file),
                     exist_ok=True)
            move_file(path, renamed_file, target_directory)

        except PermissionError as exception:
            logging.warning("File not accessible: " + exception.filename + ". PDF file was not renamed or moved.")
            not_processed_list.append(file_name)
            continue

    logger.info("\n")
    logger.info('==============================================================================================')
    logger.info("##################################")
    logger.info("# PDF Sort Run completed         #")
    logger.info("##################################")

    if not_processed_list:
        logger.warning("The following PDF files could not be processed or have just been partially processed:")
        for file_name in not_processed_list:
            logger.warning(file_name)


# Read out attribute values from PDF, sanitize them and attach them to config
def update_config_from_regex(pdf_text, document_type_dates_list, config_file_path, company, document_type):
    config_file_name = ''
    try:
        if document_type_dates_list:
            # Get newest config date
            config_date = document_type_dates_list.pop()

            config_file_name = f"{config_file_path}/{company}-{document_type}-{config_date}.json"
            config = read_json(config_file_name)
            for regex_key in config['regex_patterns']:
                attribute_value = get_attr_from_regex(config, regex_key, pdf_text)
                sanitized_attr = sanitize_attr(attribute_value, regex_key)
                config.update({regex_key: sanitized_attr})
            logging.debug("Config file used: " + config_file_name)
            return config
    except ValueError as exception:
        logging.warning("Could not parse Regex " + exception.args[0] + " in config file: " + config_file_name)
        return update_config_from_regex(pdf_text, document_type_dates_list, config_file_path, company, document_type)


# Main Function
if __name__ == '__main__':
    setup_logger()
    makedirs(os.path.dirname(settings.image_output_dir),
             exist_ok=True)

    process_files(settings.pdf_files_dir, settings.config_files_dir)
