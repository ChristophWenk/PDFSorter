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


def sanitize_account_name(account_name):
    account_name = account_name.replace(' ', '_')
    return account_name


def sanitize_attr(attribute_value, regex_key):
    logger.debug("[PRE SANITIZATION] " + regex_key + ": " + attribute_value)
    match regex_key:
        case "document_id":
            sanitized_value = sanitize_document_id(attribute_value)
        case "date":
            sanitized_value = sanitize_date(attribute_value)
        case "account_name":
            sanitized_value = sanitize_account_name(attribute_value)
        case _:
            sanitized_value = attribute_value

    if regex_key.startswith("month_word"):
        sanitized_value = datetime.strptime(attribute_value, '%d.%m.%Y').strftime("%B")

    logger.info(regex_key + ": " + sanitized_value)
    return sanitized_value
