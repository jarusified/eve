import optparse 
import sys
import re
from worder import *
import os
from subprocess_caller import subprocess_cmd
global question, keywords

def split_by_lines(keywords):
	print "in"
	subprocess_cmd("cat extract.txt | tr -d ',' |tr '\n' ' ' | tr '.?!' '\n' > lines.txt")
	line=file("lines.txt","rb").read()
        lines=re.findall(r'(.*?)\n',line)
        keys=re.findall(r'(.*?),',keywords)
        answer=[]
        for l in range(1,len(lines)):
		for key in keys:
			if key in lines[l]:
			        answer.append(lines[l])
				for i in range(1,9):
					if l+i < len(lines):
						answer.append(lines[l+i])
					else: 
						pass
      	if not answer:
		for l in range(1,len(lines)):
			answer.append(lines[l])
        print '.\n'.join(answer)

def parseques(ques,keywords):
	worder=Worder()
	stems=[]
	stripped_entities=[]
	search=[]
	named_ent=worder.named_entities(ques)
	#print named_ent
	entities=re.findall(r'\s(.*?)/NN',str(named_ent)) #regex spliting about NN
	entities+=re.findall(r'\s(.*?)/VB',str(named_ent))
	for entity in entities:
		stripped_entities.append(entity.strip())
	print "entities are :%s " %entities
	for entity in entities: # for loop for finding the stems
		stems.append(worder.stemmer(entity))
	print "stems are :%s" %stems
	descriptives= ','.join(re.findall(r'\s(.*?)/WP',str(named_ent)))
	print "descriptive or type of question is : %s" %(descriptives)
	#print stripped_entities
	find_keyword(stripped_entities)

def find_keyword(list):
	for item in list:
		parsekeyword(item)
	for item1 in list:
		for item2 in list:
			parsekeyword(item1+' '+item2)
def parsekeyword(keyword):
	try:
		if keyword != None:
			command='python main.py'+ " "+'\"'+keyword+','+' '+'\"'
			print "searching for the keyword '%s'" %keyword
			os.system(command)
	except:
		print " No ouput recieved from the passing of keywords"
		print "----------------------------------------------"
		parseques(question)
	
def main():
	parser=optparse.OptionParser('usage %prog -q'+'<question> -k<keywords>{optional}')
	parser.add_option('-q',dest='question',type='string',help='You must specify the question')
	parser.add_option('-k',dest='keywords',type='string',help="specify the keywords")
	(options,args)=parser.parse_args()
	if (options.question == None):
		print parser.usage
		exit(0)
	question=options.question
	keywords=options.keywords
	print options.question
	if options.keywords != None:
		print "KEYWORDS : %s" %options.keywords
		print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
		print "checking for answers using the given keywords"
		parsekeyword(options.keywords)
	elif options.question != None:
		parseques(question,keywords)	

if __name__ =='__main__':
	main()
