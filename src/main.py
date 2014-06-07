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
                self.create_pdf()
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
			#print self.content[i]
			#names=re.findall(r'\w+\s(\w+),\s',self.content[i])
			name=''.join(names)
			#print name
			if names!='':
				pages=re.findall(r'\d+',self.content[i])
				print pages
				self.dictionary[name]=pages
			#	tree.add_topics("requirements models, ")
			#	tree.add_pages('556')
				tree.add_topics(name)
				tree.add_pages(self.dictionary[name])
				print self.dictionary[name]	
		tree.make()
		tree.search(str(sys.argv[1]))
		self.pages=tree.found_pages
	def create_pdf(self):
		self.pages=re.split(r'\d{1-5}',self.pages[0])
		for i in range(len(self.pages)):
			self.pages[i]=int(self.pages[i])+28
			subprocess.Popen(['pdfseparate','-f',str(int(self.pages[i])),'-l',str(int(self.pages[i])),'data/a.pdf','data/extract.pdf']).communicate()
Book1=Book("data/a.pdf")


