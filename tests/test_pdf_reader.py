import os
from os import makedirs

from pdf_sorter.pdf_parser import read_pdf

if __name__ == '__main__':
    file_name = "Helsana-Leistungsabrechnung"
    pdf_file_path = "../resources/test_files/" + file_name + ".pdf"
    pdf_text = read_pdf(pdf_file_path)

    pdf_text_file_path = "../generated/tests/" + file_name + ".txt"
    makedirs(os.path.dirname(pdf_text_file_path),
             exist_ok=True)
    f = open(pdf_text_file_path, "w", encoding='utf-8')
    f.write(pdf_text)
    f.close()
