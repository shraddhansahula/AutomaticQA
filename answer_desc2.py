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
import pickle
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
	
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


"""
This code requires a chapter number and a question as first two arguments. Also needs a stop_words.txt.
"""
# iORj = 0 #0 if i else 1
# chapNum = int(sys.argv[1])
# if chapNum <=8:
# 	iORj = 0
# else:
# 	iORj = 1
# 	chapNum = chapNum - 8
# print chapNum, iORj

def extract_sentences(chapNum):
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
	classIdentifier = ""
	if chapNum <= 8:
		classIdentifier = "i"
	else:
		chapNum = chapNum - 8
		classIdentifier = "j"
	file = open("./Dataset_NCERT/Dataset-txt/"+classIdentifier+"ess30"+str(chapNum)+".txt")
	sentences = file.read()
	file.close()
	sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', sentences)
	for i, s in enumerate(sentences):
		s = s.replace("\n", " ")
		sentences[i] = s
	return sentences

# def extract_sentences_anurag(query):
# 	f = open("stop_words.txt", "r")
# 	stopWords = [word for word in f.readlines()]
# 	f.close()

# 	index = {}
# 	with open("inverted_index") as f:
# 		for line in f:
# 			line = line.strip("\n").split("=")
# 			index[line[0]] = line[1].split("||")

# 	queryWords = word_tokenize(query)
	
# 	q = [word for word in queryWords if word not in stopWords]

# 	queryRel = q[:]
	
# 	for word in q:
# 		for i, j in enumerate(wn.synsets(word)):
# 			for l in j.lemmas():
# 				queryRel.append(l.name())
	
# 	queryRel = list(set(queryRel))
# 	sentenceIDs = []

# 	for i in queryRel:
# 		if i in index:
# 			sentenceIDs += index[i]

# 	sentenceIDs = [int(i) for i in sentenceIDs]
# 	relevantSent = [i for i in sorted(sentenceIDs) if i > 211 and i < 520]

# 	f = open("sentences.txt", "r")
# 	sentence_list = [sent.strip("\n") for sent in f.readlines()]
# 	f.close()

# 	final_list = [sentence_list[i] for i in relevantSent]
# 	return final_list




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
	print feature_vector
	return (0, feature_vector, candidate)

with open("question.txt") as f:
	for line in f:
		line = line.split("|")
		chapNum = int(line[0])
		query = str(line[1])
		print chapNum, query
		candidates = extract_sentences(chapNum)
		print len(candidates)

		pool = mp.Pool(processes=12)
		features = pool.map(extract_features, candidates)
		features = [(x[0], x[1], unicode(x[2], "utf-8")) for x in features]
		weights = [3.0000000000000013, 6.999999999999991, 6.799999999999992, 0.1, 0.2, 0.1, 1.6000000000000003, 1.0999999999999999, 33.90000000000021, 0.30000000000000004]
		for k, f in enumerate(features):
			f = list(f)
			score = 0
			#print f
			for i,j in enumerate(f[1]):
				score += weights[i]*j
			#print score
			f[0] = score
			#print f
			f[:0] = [k]
			f = tuple(f)
			features[k] = f
		lenFeatures = len(features)
		windowFeature = []
		windowSize = 4

		for k, f in enumerate(features):
			if k > lenFeatures - windowSize:
				break
			windowScore = 0
			windowSentence = ""
			for i in xrange(0, windowSize):
				windowScore += features[k+i][1]
				windowSentence += features[k+i][3]+" "

			windowFeature.append((windowScore, windowSentence.strip()))

		windowFeature = sorted(windowFeature, key=lambda x: -x[0])

		# for i in xrange(0,5):
		# 	print windowFeature[i]
		wordCount = 0
		i = 0
		summary = []
		#generating summary
		while(1):
			sentence = windowFeature[i][1]
			i += 1
			wordList = nltk.word_tokenize(sentence)
			wordCount += len(wordList)
			summary.append(sentence)

			if wordCount>450:
				break

		new_summary = []
		for sent in summary:
			# print sent_tokenize(sent)
			# print ""
			temp_list = sent_tokenize(sent)
			for s in temp_list:
				if s not in new_summary:
					new_summary.append(s)

		# new_summary = list(set(new_summary))
		answer = ""
		for s in new_summary:
			answer += s

		fileName = open("answers.txt", "a+")
		fileName.write(query + "\n")
		fileName.write(answer + "\n\n")
		fileName.close()
