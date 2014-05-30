from pyPdf import PdfFileWriter,PdfFileReader
import sys
import subprocess
import string 
import re
import unicodedata
from search import * 

class Book:	
	def __init__(self,path):
		self.content=""
                output=PdfFileWriter()
                pdf=PdfFileReader(file(path,"rb"))
                self.appendix_content(pdf)
                self.sort()
#                self.search()
                self.display()

	def appendix_content(self,pdf):
		for i in range(883,888):
			self.content+=pdf.getPage(i).extractText()
		self.content+=pdf.getPage(887).extractText()	
		self.content=self.content.splitlines()
		for i in range(len(self.content)):	
			self.content[i]=self.content[i].encode('ascii','ignore').lower()
	def sort(self):
		tree=searchTree()
		self.dictionary={}
		for i in range(len(self.content)):	
			names=''.join(re.findall(r'(?!,)(?! )(?!\')\D+',self.content[i]))
			name=''.join(names)
			if name!='':
				pages=re.findall(r'\d+',self.content[i])
				self.dictionary[name]=pages
				tree.add_topics(name)
				tree.add_pages(self.dictionary[name])
		tree.make()
		tree.search(str(sys.argv[1]))
		self.pages=tree.found_pages
	def display(self):
		self.pages=re.split(r'\W+',self.pages[0])
		for i in range(len(self.pages)):
			self.pages[i]=int(self.pages[i])+28
			subprocess.Popen(['pdfseparate','-f',str(int(self.pages[i])),'-l',str(int(self.pages[i])),'data/a.pdf','data/extract.pdf']).communicate()
Book1=Book("data/a.pdf")


		
