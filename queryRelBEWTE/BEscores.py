from __future__ import division
from nltk.corpus import wordnet as wn
from nltk.corpus import treebank
from itertools import chain
import os
import collections
from math import log
import pickle
from lxml import etree
import nltk.data

inp = open("BEcounts", "rb")
BEcounts = pickle.load(inp)
inp.close()


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

inp = etree.parse('./APW19990707.0181')

root = inp.getroot()

candidates = []
for child in root.iter():
	if child.tag == "P":
		
		child = child.text.split(".")
		for i in child:
			i = i.replace("\n", " ")
			i = i.replace("\t", " ")
			candidates.append(i)


data = "Discuss conditions on American Indian reservations or among Native American communities. Include the benefits and drawbacks of the reservation system. Include legal privileges and problems."
print "Query Sentence"
print data
print "\n"
data = data.split(" ")
queryRel = [] 
for word in data: 
	for i,j in enumerate(wn.synsets(word)):
		for l in j.lemmas():
			queryRel.append(l.name())
		#queryRel.append(l.lemma_names() for l in j.hypernyms())
		for l in j.hypernyms():
			for k in l.lemma_names():
				queryRel.append(k)
		for l in j.hyponyms():
			for k in l.lemma_names():
				queryRel.append(k)


def LLR(e):
	N = 0
	for i in e:
		for j in i:
			N = N+j

	row1 = e[0][0] + e[0][1]
	row2 = e[1][0] + e[1][1]
	col1 = e[0][0] + e[1][0]
	col2 = e[0][1] + e[1][1]

	rowSum = row1 + row2
	colSum = col1 + col2
	rowH = (row1/rowSum)*log(row1/rowSum) + (row2/rowSum)*log(row2/rowSum)
	colH = (col1/colSum)*log(col1/colSum) + (col2/colSum)*log(col2/colSum)

	H = 0
	for i in e:
		for j in i:
			if j != 0:
				H = H + (j/N)*log(j/N)
	return 2*N*(H - rowH - colH)

listOfTags = []
for word, tag in treebank.tagged_words():
	if tag not in listOfTags:
		listOfTags.append(tag)

prepositions = ['when','whenever','where','wherever','while','even','though','lest','since','that','though','till','unless','until','than','because','before','after','although','long','much','soon','though','if','so','aboard','about','above','across','after','against','along','amid','among','anti','around','as','at','before','behind','below','beneath','beside','besides','between','beyond','but','by','concerning','considering','despite','down','during','except','excepting','excluding','following','for','from','in','inside','into','like','minus','near','of','off','on','onto','opposite','outside','over','past','per','plus','regarding','round','save','since','than','through','to','toward','towards','under','underneath','unlike','until','up','upon','versus','via','with','within','without']																																																																																																																																				

def find_BEs(sent):
	BE = []
	os.chdir("../bewte/input")
	out = open("sent.1.1", "wb")
	out.write(sent)
	out.close()
	os.chdir("../build")
	os.system("ant Step1")
	print "step1"
	os.system("ant Step2")
	print "step2"
	os.system("ant Step3")
	print "step3"
	os.chdir("../output/BEXs/00000000")
	with open("sent.1.1", "r") as f:
		for line in f:
			line = line.replace("","|")
			line = line.split("|")
			line = line[1:-1]
			line = [w for w in line if w not in listOfTags]
			line = [w for w in line if w not in prepositions]
			BE.append(zip(line,line[1:]))
	os.chdir("../../../../queryRelBEWTE")
	return BE

def match_BE(can):
	BE = []
	for i in can:
		if i[0] in queryRel or i[1] in queryRel:
			BE.append(i)

	return BE
#useless = "Clinton was going to the Pine Ridge Reservation for a visit with  the Oglala Sioux nation and to participate in a conference on Native American homeownership and economic development."
for can in candidates:
	matchedBE = []
	print can
	if can != ' ':
		canBEs = find_BEs(can)
	print canBEs
	matchedBE = match_BE(canBEs)																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																											
	# print len(matchedBE)

	for i in matchedBE:
		event = [[0,0],[0,0]]
		event[0][0] = BEcounts[i]
		a = i[0]
		b = i[1]
		aCount = 0
		bCount = 0
		abCount = 0
		for be in BEcounts:
			if a in be and b not in be:
				aCount = aCount + BEcounts[be]
			elif b in be and a not in be:
				bCount = bCount + BEcounts[be]
			elif a not in be and b not in be:
				abCount = abCount + BEcounts[be]
		event[0][1] = aCount
		event[1][0] = bCount
		event[1][1] = abCount
		beLLR = LLR(event)
		print i
		print beLLR