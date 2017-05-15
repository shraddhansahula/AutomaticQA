import sys
import os

qType = 0
chapNum = sys.argv[1]
question = sys.argv[2]

#print question

if qType == 0:
	os.chdir("./factoid_qa/NLP-Question-Answer-System/stanford-corenlp-python/")
	os.system('python answer_factoid.py'+ " "+ str(chapNum)+ " " + "'" +question + "'" + '')
else:
	os.system('python answer_desc.py 1 "Describe the circumstances leading to the outbreak of revolutionary protest in France."')

