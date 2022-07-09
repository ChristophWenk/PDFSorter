from datetime import datetime
import logging
import dateparser

logger = logging.getLogger(__name__)


def sanitize_document_id(document_id):
    document_id = document_id.replace(' ', '')
    document_id = document_id.replace('\n', '')
    return document_id


def sanitize_date(date):
    # Normalize date from text
    normalized_date = dateparser.parse(date, languages=['de'])
    # Reformat date
    date = normalized_date.strftime("%Y-%m-%d")
    return date


def sanitize_attr(attribute_value, regex_key):
    match regex_key:
        case "document_id":
            sanitized_value = sanitize_document_id(attribute_value)
        case "date":
            sanitized_value = sanitize_date(attribute_value)
        case "month":
            sanitized_value = datetime.strptime(attribute_value, '%d.%m.%Y').strftime("%B")
        case _:
            sanitized_value = attribute_value
            logging.debug("Regex Key " + regex_key + " has not been sanitized as there is no definition for it.")
    logger.info(regex_key + ": " + sanitized_value)
    return sanitized_value
