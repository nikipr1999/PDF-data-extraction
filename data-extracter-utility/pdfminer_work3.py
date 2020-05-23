import io
import os
import json
import requests
from pathlib import Path
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


welcome="""
Hello,
Welcome to Data Extractor
This program is to extract text data from a PDF file.

You are requested to enter the url of your PDF file.
"""

def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    # close open handles
    converter.close()
    fake_file_handle.close()
    if text:
        return text

def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager() # #creates a resource manager instance
            fake_file_handle = io.StringIO()    #creates a file like object 
            converter = TextConverter(resource_manager, fake_file_handle) #creates a text converter 'loads all text disfiguratevetly'
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
            text = fake_file_handle.getvalue() #gets all the data regardles its position 
            yield text

            converter.close()
            fake_file_handle.close()

def export_as_txt(pdf_path):
    text = extract_text_from_pdf(pdf_path) #get string of text content of pdf
    textFilename = pdf_path.split(".")[0] + ".txt"
    textFile = open(textFilename, "w") #make text file
    textFile.write(text) #write text to text file
    #textFile.close


def export_as_json(pdf_path):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    data = {'Filename': filename}
    data['Pages'] = []
    counter = 1
    for page in extract_text_by_page(pdf_path):
        text = page[0:200]
        page = {'Page_{}'.format(counter): text}
        data['Pages'].append(page)
        counter += 1

    json_path=pdf_path.split(".")[0]+".json"
    with open(json_path, 'w') as fh:
        json.dump(data, fh)

def get_pdf_file():
    print(welcome)
    file_type=int(input('If you want to use a local file press 1 \
    \nIf you want to use an online file press 2\nEnter choice : '))

    if file_type==1:
      myfile=input('Enter the file path:  ');
      if Path(myfile).exists():
        return myfile
      else:
        print('Wrong file path.')

    elif file_type==2:
      url = input('Enter the url: ')
      myfile1 = requests.get(url)
      open('some_file.pdf', 'wb').write(myfile1.content)
      return "some_file.pdf"
      
    else:
      print('wrong entry.');


if __name__ == '__main__':
    pdf_path = get_pdf_file()
    export_as_txt(pdf_path)
    export_as_json(pdf_path)
    os.system("python pdf2txt.py -o "+pdf_path.split(".")[0] + ".html "+pdf_path)