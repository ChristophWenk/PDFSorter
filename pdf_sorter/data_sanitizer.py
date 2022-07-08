import dateparser


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
