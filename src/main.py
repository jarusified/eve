from pyPdf import PdfFileWriter,PdfFileReader
import sys
import subprocess
import string 
import re
import unicodedata
from run import *
import os
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
			#names=re.findall(r'\w+\s(\w+),\s',self.content[i])
			name=''.join(names)
			if names!='':
				pages=re.findall(r'\d+',self.content[i])
				self.dictionary[name]=pages
				tree.add_topics(name)
				tree.add_pages(self.dictionary[name])
		tree.make()
		tree.search(str(sys.argv[1]))
		self.pages=tree.found_pages
	def create_pdf(self):
		try:
			for i in range(len(self.pages)):
				if self.pages[i]!="":
					self.pages[i]=int(self.pages[i])+28
					subprocess.Popen(['pdfseparate','-f',str(int(self.pages[i])),'-l',str(int(self.pages[i])),'a.pdf','extract.pdf']).communicate()
					os.system('make')
					split_by_lines(sys.argv[1])
		except:
			pass
Book1=Book("a.pdf")


