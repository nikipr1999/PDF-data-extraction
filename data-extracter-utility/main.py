# importing required modules 
import PyPDF2 
from pathlib import Path

welcome="""
Hello,
Welcome to Data Extractor
This program is to extract text data from a PDF file.

You are requested to enter the url of your PDF file.
"""

def print_data(myfile):
  # creating a pdf file object 
  pdfFileObj = open(myfile,'rb');

  # creating a pdf reader object 
  pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

  print('\n\nThe information about the document:\n',pdfReader.getDocumentInfo())
  print('\n\nThe number of pages in your pdf is : ', pdfReader.numPages) 
  print('\n\n\nThe text from the given pdf is following: \n');

  print('\nThis is the text from first page of the pdf\n\n\n')
  pageObj = pdfReader.getPage(0) 

  # extracting text from page 
  text=pageObj.extractText()
  print(text) 

  if(pdfReader.numPages>1):
    get_complete_pdf=int(input('\n\nIf you want to get complete pdf press 1 : '))
    if(get_complete_pdf==1):
      for i in range(pdfReader.numPages):
        print('\n\nThe text of page ',i,' is :\n')
        pageObj=pdfReader.getPage(i)
        print(pageObj.extractText())
  # closing the pdf file object 
  pdfFileObj.close() 



print(welcome);

file_type=int(input('If you want to use a local file press 1 \
  \nIf you want to use an online file press 2\nEnter choice : '))

if file_type==1:
  myfile=Path(input('Enter the file path:  '));
  if myfile.exists():
    print_data(myfile);
  else:
    print('Wrong file path.')

elif file_type==2:
  import requests
  url = input('Enter the url: ')
  # for example url:
  # https://www.adobe.com/support/products/enterprise/knowledgecenter/media/c4611_sample_explain.pdf
  myfile1 = requests.get(url)
  open('some_file.pdf', 'wb').write(myfile1.content)
  print_data('some_file.pdf')
  
else:
  print('wrong entry.');
