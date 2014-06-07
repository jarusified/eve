from subprocess_caller import subprocess_cmd
import re
import sys
from questions import keyword
def split_by_lines():
	subprocess_cmd("cat output/extract.txt | tr -d ',' |tr '\n' ' ' | tr '.?!' '\n' > output/lines.txt")
	line=file("output/lines.txt","rb").read()
        lines=re.findall(r'(.*?)\n',line)
        keywords=re.findall(r'(.*?),',keyword)
        answer=[]
#	for l in range(2,len(lines)):
#		for keyword in keywords:
#			if keyword.isdigit():
#				breakpoint=l;
#			else if 
        for l in range(1,len(lines)):
		for keyword in keywords:
			if keyword in lines[l]:
	#			print "success"
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
split_by_lines()
