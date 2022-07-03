import json_parser
import pdf_parser

document_type_set = ''

# Main Function
if __name__ == '__main__':
    # Read in PDF page content
    file_path = 'test_files/Helsana_Leistungsabrechnung.pdf'
    file = open(file_path, 'rb')

    pdf_file = pdf_parser.read_pdf(file)
    print(pdf_parser.print_metadata(pdf_file))

    pdf_page = pdf_parser.read_page(pdf_file, 0)
    pdf_text = pdf_page.extractText()
    file.close()
    print(pdf_text)

    # Read in configuration files
    json_file = json_parser.read_json()
    print(json_file['company_name'])



def create_document_type_list():
    print('')

def evaluate_company():
    print('')

def evaluate_document_type():
    print('')