import locale
from datetime import datetime
import logging
import dateparser

logger = logging.getLogger(__name__)


def sanitize_document_id(document_id):
    document_id = document_id.replace(' ', '')
    document_id = document_id.replace('\n', '')
    document_id = document_id.replace(' ', '_')
    return document_id


def sanitize_date(date):
    # Complete Abbreviations
    date = expand_date_abbreviation(date)
    # Normalize date from text
    normalized_date = dateparser.parse(date, languages=['de'])
    # Reformat date
    date = normalized_date.strftime("%Y-%m-%d")
    return date


def expand_date_abbreviation(date):
    if locale.getlocale()[0] == 'de_CH':
        if "Jan." in date: return date.replace('Jan.', 'Januar')
        if "Feb." in date: return date.replace('Feb.', 'Februar')
        if "Apr." in date: return date.replace('Apr.', 'April')
        if "Aug." in date: return date.replace('Aug.', 'August')
        if "Sept." in date: return date.replace('Sept.', 'September')
        if "Okt." in date: return date.replace('Okt.', 'Oktober')
        if "Nov." in date: return date.replace('Nov.', 'November')
        if "Dez." in date: return date.replace('Dez.', 'Dezember')
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
