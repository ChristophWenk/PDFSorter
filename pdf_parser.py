import PyPDF2

def read_pdf(file):
    return PyPDF2.PdfFileReader(file)

def read_page(pdf_file, page_number):
    return pdf_file.getPage(page_number)

def print_metadata(pdf_file):
    # printing number of pages in pdf file
    print("Total number of pages in sample.pdf", pdf_file.numPages, '\n\n')


