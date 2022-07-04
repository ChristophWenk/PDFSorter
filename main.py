import json_parser
import pdf_parser
from os import listdir
from os.path import isfile, join

# Read in all config files and create a list of document types for each company
def create_document_type_list(path):
    file_list = [f for f in listdir(path) if isfile(join(path, f))]
    document_type_list = []
    for file in file_list:
        document_type_list.append(file.split('-'))
    return document_type_list

def evaluate_document_type(text, document_type_list):
    for document_type_tuple in document_type_list:
        if document_type_tuple[1] in text:
            print("Document Type:", document_type_tuple[1])
            return document_type_tuple[1]

# Check which company is in scope
def evaluate_company(text, document_type_list):
    for document_type_tuple in document_type_list:
        if document_type_tuple[0] in text:
            print("Company:", document_type_tuple[0])
            return document_type_tuple[0], evaluate_document_type(text, document_type_list)

def process_files(path):
    file_path_list = [f for f in listdir(path) if isfile(join(path, f))]
    pdf_file_list = []
    for file_path in file_path_list:
        print("Processing file...", file_path)
        file = open(path + '/' + file_path, 'rb')

        pdf_file = pdf_parser.read_pdf(file)
        pdf_parser.print_metadata(pdf_file)

        pdf_page = pdf_parser.read_page(pdf_file, 0)
        pdf_text = pdf_page.extractText()

        evaluate_company(pdf_text, document_type_list)

        file.close()

        print('======================================================')

# Main Function
if __name__ == '__main__':
    # Read in configuration files
    json_file = json_parser.read_json()
    #print(json_file['company_name'])

    document_type_list = create_document_type_list('F:/Christoph/Sonstiges/Development/PDFSorter/resources/config_files')

    file_path = 'resources/test_files'
    process_files(file_path)