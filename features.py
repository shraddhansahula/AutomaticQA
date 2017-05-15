# -*- coding: utf-8 -*-
import sys
sys.path.append('./LCS')
sys.path.append('./headRelated')
sys.path.append('./ngramOverlap')
sys.path.append('./skipBigram')
sys.path.append('./synHypOverlap')
sys.path.append('./treeKernel')
import os
import re
	
from lxml import etree
from lcs import lcs_wlcs #returns lcs, wlcs
from head import head_related #returns relHeadScore, exactHeadScore
from ngram import ngram_overlap #returns 1gram score
from skip import skip_bigram #returns skip score
from syn import syn_hyp_overlap #returns synOverlap, hypOverlap, glossOverlap
from synTreeKernel import syn_tree_kernel #returns treekernel score
import pickle
import multiprocessing as mp
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize, word_tokenize

def extract_sentences():
	# sentences = []
	# os.chdir("/home/shraddhan/Honors/DUC Dataset/DUC2006_Summarization_Documents/duc2006_docs/D0601A")
	# listOfFiles = os.listdir(".")
	# for file in listOfFiles:
	# 	print file
	# 	inp = etree.parse(file)
	# 	root = inp.getroot()
	# 	for child in root.iter():
	# 		if child.tag == "P":
	# 			text = child.text.split(".")
	# 			for i,j in enumerate(text):
	# 				text[i] = text[i].replace("\n", " ")
	# 				text[i] = text[i].replace("\t", " ")
	# 				if text[i] and not text[i].isspace():
	# 					sentences.append(text[i])
	# return sentences
	file = open("/home/shraddhan/Honors/Dataset_NCERT/Dataset-txt/iess306.txt")
	sentences = file.read()
	file.close()
	sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', sentences)
	for i, s in enumerate(sentences):
		s = s.replace("\n", " ")
		sentences[i] = s
	return sentences

def extract_sentences_anurag(query):
	f = open("stop_words.txt", "r")
	stopWords = [word for word in f.readlines()]
	f.close()

	index = {}
	with open("inverted_index") as f:
		for line in f:
			line = line.strip("\n").split("=")
			index[line[0]] = line[1].split("||")

	queryWords = word_tokenize(query)
	
	q = [word for word in queryWords if word not in stopWords]

	queryRel = q[:]
	
	for word in q:
		for i, j in enumerate(wn.synsets(word)):
			for l in j.lemmas():
				queryRel.append(l.name())
	
	queryRel = list(set(queryRel))
	sentenceIDs = []

	for i in queryRel:
		if i in index:
			sentenceIDs += index[i]

	sentenceIDs = [int(i) for i in sentenceIDs]
	relevantSent = [i for i in sorted(sentenceIDs) if i > 211 and i < 520]

	f = open("sentences.txt", "r")
	sentence_list = [sent.strip("\n") for sent in f.readlines()]
	f.close()

	final_list = [sentence_list[i] for i in relevantSent]
	return final_list

query = "Who was Captain Swing and What did the name symbolise or represent?"
# candidate = "Europe's new currency, the euro, will rival the U.S. dollar as an international currency over the long term, Der Speigel magazine reported Sunday."

#print query

# print feature_vector
#candidates = extract_sentences_anurag(query)
#print candidates
candidates = extract_sentences()
print len(candidates)
#candidates = candidates[5:13]
score_feature_candidate = []
global i
i = 0
def extract_features(candidate):
	feature_vector = []
	global i
	i += 1
	print "finding features for", i
	try:
		feature_vector += list(lcs_wlcs(query, candidate))
		feature_vector += list(head_related(query, candidate))
		feature_vector.append(ngram_overlap(query, candidate))
		feature_vector.append(skip_bigram(query, candidate))
		feature_vector += list(syn_hyp_overlap(query, candidate))
		feature_vector.append(syn_tree_kernel(query, candidate))
	except:
		feature_vector = [0,0,0,0,0,0,0,0,0,0]
	#score_feature_candidate.append((0,feature_vector,candidate
	print "processed", i
	return (0, feature_vector, candidate)

pool = mp.Pool(processes=4)
results = pool.map(extract_features, candidates)
#print results
# i = 0
# for candidate in candidates:
# 	i=i+1
# 	print i
# 	feature_vector = []
# 	try:
# 		feature_vector += list(lcs_wlcs(query, candidate))
# 		feature_vector += list(head_related(query, candidate))
# 		feature_vector.append(ngram_overlap(query, candidate))
# 		feature_vector.append(skip_bigram(query, candidate))
# 		feature_vector += list(syn_hyp_overlap(query, candidate))
# 		feature_vector.append(syn_tree_kernel(query, candidate))
# 	except:
# 		feature_vector = [0,0,0,0,0,0,0,0,0,0]
# 	score_feature_candidate.append((0,feature_vector,candidate))
# 	print feature_vector
	# if i==3:
	# 	break
	
os.chdir("/home/shraddhan/Honors/")
out = open("featureVectors_NCERT_iess306_Q6", "wb")
pickle.dump(results, out)
out.close()
