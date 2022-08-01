import win32com.client
import os
inputFolder = r'F:\Downloads\msgs'
outputFolder = r'F:\Downloads\02_pdf_sorter'

if __name__ == '__main__':
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    for file in os.listdir(inputFolder):
        if file.endswith(".msg"):
            filePath = inputFolder + '\\' + file
            msg = outlook.OpenSharedItem(filePath)
            att = msg.Attachments
            for i in att:
                # Saves the file with the attachment name
                i.SaveAsFile(os.path.join(outputFolder, i.FileName))
