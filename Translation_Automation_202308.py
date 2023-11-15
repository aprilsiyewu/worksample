import pytesseract
from googletrans import Translator
import PyPDF2
import os
from pygtrans import Translate
from docx import Document
import openpyxl
import pandas as pd


# Set the path to the input PDF file and the output Word file
print(os.getcwd())
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
translator = Translator()
translation_tool = Translate()

for filename in os.listdir(directory_path):
    if filename.endswith(".pdf"):

        mypdf = open(os.path.join(directory_path, filename),mode='rb')
        pdf_doc = PyPDF2.PdfReader(mypdf)
        first_page = pdf_doc.pages[0]
        eng_lading = first_page.extract_text()

        # Set the language codes for translation (en for English, zh-CN for Simplified Chinese)
        source_lang = 'en'
        target_lang = 'zh-CN'

        # Initialize the OCR engine and translator

        # Translate the extracted text to Chinese
        chi_lading_1 = translator.translate(eng_lading, src=source_lang, dest=target_lang).text

        # Translate one more time to improve accuracy via pygtrans
        chi_lading = translation_tool.translate(chi_lading_1)

        # Modify specific words via replacing function manually
        chi_lading.translatedText = chi_lading.translatedText.replace("。", ".")
        chi_lading.translatedText = chi_lading.translatedText.replace("2.", "\n\n2.")
        chi_lading.translatedText = chi_lading.translatedText.replace("3.", "\n\n3.")
        chi_lading.translatedText = chi_lading.translatedText.replace("4.", "\n\n4.")
        chi_lading.translatedText = chi_lading.translatedText.replace("5.", "\n\n5.")
        chi_lading.translatedText = chi_lading.translatedText.replace("6.", "\n\n6.")
        chi_lading.translatedText = chi_lading.translatedText.replace("7.", "\n\n7.")
        chi_lading.translatedText = chi_lading.translatedText.replace("8.", "\n\n8.")
        chi_lading.translatedText = chi_lading.translatedText.replace("9.", "\n\n9.")
        chi_lading.translatedText = chi_lading.translatedText.replace("10.", "\n\n10.")
        chi_lading.translatedText = chi_lading.translatedText.replace("SAY", "\n")
        chi_lading.translatedText = chi_lading.translatedText.replace("11.", "\n\n11.")
        chi_lading.translatedText = chi_lading.translatedText.replace("/\n", "/")

        # Save the Word document
        chi_lading_doc = Document()
        paragraph = chi_lading_doc.add_paragraph(chi_lading.translatedText)
        word_filename = os.path.splitext(filename)[0]+'.docx'
        chi_lading_doc.save(os.path.join(directory_path,word_filename))

        # Convert Word document to text file
        MY_TEXT = docx2txt.process(os.path.join(directory_path,word_filename))
        with open("test.txt", "w") as text_file:
            print(MY_TEXT, file=text_file)

        #Define the Excel filename based on the original PDF filename
        excel_filename = os.path.splitext(filename)[0]+".xlsx"
        df = pd.DataFrame()
        df.to_excel(os.path.join(directory_path,excel_filename))
        mywb = openpyxl.load_workbook(os.path.join(directory_path,excel_filename))

        # Save to the Excel document
        mysheet = mywb['Sheet1']
        with open('test.txt', 'r') as file:
            for line in file:
                row_data = [line.strip()]
                mysheet.append(row_data)
        mywb.save("test.xlsx")

        # set the column width
        mysheet.column_dimensions['A'].width = 70.0
        mysheet.column_dimensions['B'].width = 70.0
        mywb.save("test.xlsx")

        #### Map to specific cells ####

        # Define the keyword if you want to move
        keyword1 = "a"
        keyword2 = "b"
        keyword3 = "5."
        keyword4 = "6."

        # if you need to move more than 1 rows, set up the below find & count parameters
        find = False
        count = 0
        find2 = False
        count2 = 0

        # Iterate through all the rows and columns in the worksheet
        for row in mysheet.iter_rows():
            for cell in row:
                # Check if the keyword is in the cell value
                if keyword1 in cell.value:
                    mysheet.move_range(cell.coordinate, cols=1, rows=-5)
                    print("Keyword found in cell", cell.coordinate, ":", cell.value)
                if keyword2 in cell.value:
                    mysheet.move_range(cell.coordinate, cols=1, rows=-5)
                    print("Keyword found in cell", cell.coordinate, ":", cell.value)
                if keyword3 in cell.value:
                    find = True
                if find == True and count < 3:
                    count += 1
                    mysheet.move_range(cell.coordinate, cols=1, rows=-3)
                    print("Keyword found in cell", cell.coordinate, ":", cell.value)
                if keyword4 in cell.value:
                    find2 = True
                if find2 == True and count2 < 3:
                    count2 += 1
                    mysheet.move_range(cell.coordinate, cols=2, rows=-8)
                    print("Keyword found in cell", cell.coordinate, ":", cell.value)

        mywb.save(os.path.join(directory_path, excel_filename))
