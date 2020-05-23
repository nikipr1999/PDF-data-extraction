from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt

#converts pdf, returns its text content as a string
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    print(text)
    return text 
   
def convertMultiple(pdf):
    text = convert(pdf) #get string of text content of pdf
    textFilename = pdf.split(".")[0] + ".txt"
    textFile = open(textFilename, "w") #make text file
    textFile.write(text) #write text to text file
	#textFile.close



########################################################
# driver code
########################################################

pdf=input('Enter the file name: ')
convertMultiple(pdf)