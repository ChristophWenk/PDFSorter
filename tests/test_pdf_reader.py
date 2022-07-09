from pdf_sorter.pdf_parser import read_pdf

if __name__ == '__main__':
    file_path = '../resources/test_files/Aquilana_Prämienabrechung.pdf'
    pdf_text = read_pdf(file_path)
    f = open("../target/tests/test_pdf_reader.txt", "w", encoding='utf-8')
    f.write(pdf_text)
    f.close()
