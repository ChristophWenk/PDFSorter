import json_parser
import pdf_parser
import re
from os import listdir
from os.path import isfile, join


# Read in all config files and create a list of document types for each company
def create_document_type_list(path):
    file_list = [f for f in listdir(path) if isfile(join(path, f))]
    document_type_list = []
    for file in file_list:
        document_type_list.append(file.replace('.json', '').split('-'))
    return document_type_list


def evaluate_document_type(text, document_type_list):
    for document_type_tuple in document_type_list:
        if document_type_tuple[1] in text:
            print("Document Type:", document_type_tuple[1])
            return document_type_tuple[1]


# Check which company is in scope
def evaluate_company(text, document_type_list):
    company = None
    document_type = None
    for document_type_tuple in document_type_list:
        if document_type_tuple[0] in text:
            print("Company:", document_type_tuple[0])
            company = document_type_tuple[0]
            document_type = evaluate_document_type(text, document_type_list)
            break
    return company, document_type


def get_config_file(company, document_type, config_file_path):
    return json_parser.read_json(config_file_path + '/' + company + '-' + document_type + '.json')


def process_files(path, config_file_path):
    file_path_list = [f for f in listdir(path) if isfile(join(path, f))]
    for file_path in file_path_list:
        print("Processing file...", file_path)
        file = open(path + '/' + file_path, 'rb')

        pdf_file = pdf_parser.read_pdf(file)
        pdf_parser.print_metadata(pdf_file)

        pdf_page = pdf_parser.read_page(pdf_file, 0)
        pdf_text = pdf_page.extractText()

        document_type_list = create_document_type_list(config_file_path)
        company, document_type = evaluate_company(pdf_text, document_type_list)

        if company is not None and document_type is not None:

            # if document_type == 'Leistungsabrechnung':
            #     f = open("demofile2.txt", "a")
            #     f.write(pdf_text)
            #     f.close()
            if document_type == 'Leistungsabrechnung':
                config = get_config_file(company, document_type, config_file_path)
                date_regex_config = config['regex_paterns']['date']
                date_regex = re.compile(date_regex_config)
                date = date_regex.search(pdf_text)
                print('Found: ' + date.group())



        file.close()

        print('======================================================')


# Main Function
if __name__ == '__main__':
    file_path = 'resources/test_files'
    config_file_path = 'F:/Christoph/Sonstiges/Development/PDFSorter/resources/config_files'

    process_files(file_path, config_file_path)
