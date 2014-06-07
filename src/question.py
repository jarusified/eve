import sys
import re
from worder import *
from  subprocess_caller import subprocess_cmd
def getques():
	try:
		ques=sys.argv[1]
		worder=Worder()
		stems=[]
		named_ent=worder.named_entities(ques)
		print named_ent
		entities=re.findall(r'\s(.*?)/NN',str(named_ent)) #regex spliting about NN
		entities+=re.findall(r'\s(.*?)/VB',str(named_ent))
		print "entities are : "
		print(entities)
		for entity in entities: # for loop for finding the stems
			stems.append(worder.stemmer(entity))
		print "stems are :"
		print stems
		descriptives= ','.join(re.findall(r'\s(.*?)/WP',str(named_ent)))
		print "descriptive or type of question is : %s" %(descriptives)
		print "searching using stems........"
		search=''.join(entities).strip()
		print search
		def keyword():
			return search
		subprocess_cmd('python src/main.py'+ " " +search+',')
		print 'python src/main.py'+ " " +search+','		
	except Exception ,e:
		print(str(e))
		print "traceback: error in getques() of question.py"
getques()		
