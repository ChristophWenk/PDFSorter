import PyPDF2

file = open('test_files/Swica_Leistungsabrechnung.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(file)

# printing number of pages in pdf file
print("Total number of pages in sample.pdf", pdfReader.numPages)

# creating a page object
pageObj = pdfReader.getPage(0)
# extracting text from page
print(pageObj.extractText())

# closing the pdf file object
file.close()
