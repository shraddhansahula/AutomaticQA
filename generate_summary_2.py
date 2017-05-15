# -*- coding: utf-8 -*-
import sys
import os
import pickle
import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize

# Used for window on whole corpus method.
inp = open("featureVectors_NCERT_iess301_Q1", "rb")
features = pickle.load(inp) #Three tuple of score, feature vector and sentence
inp.close()
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

	if wordCount>550:
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

print answer