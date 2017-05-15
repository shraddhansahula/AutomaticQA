import sys
import os
import pickle
import nltk
import re
# Used for whole corpus method and query union method.
inp = open("featureVectors_NCERT_iess301_Q1_new_method", "rb")
features = pickle.load(inp) #Three tuple of score, feature vector and sentence
inp.close()
weights = [3.0000000000000013, 6.999999999999991, 6.799999999999992, 0.1, 0.2, 0.1, 1.6000000000000003, 1.0999999999999999, 33.90000000000021, 0.30000000000000004]
for k, f in enumerate(features):
	f = list(f)
	score = 0

	for i,j in enumerate(f[1]):
		score += weights[i]*j
	#print score
	f[0] = score
	#print f
	f[:0] = [k]
	f = tuple(f) 

	features[k] = f #four tuple of sid, score, feature vector and sentence 

features = sorted(features, key=lambda x: -x[1])
query = "Describe the circumstances leading to the outbreak of revolutionary protest in France."
print query
wordCount = 0
i = 0
summary = []
#generating summary
while(1):
	sentence = features[i][3]
	i += 1
	wordList = nltk.word_tokenize(sentence)
	wordCount += len(wordList)
	summary.append((features[i][0], features[i][3]))

	if wordCount>350:
	 	break
	# if i>28:
	# 	break

summary = sorted(summary, key = lambda x : x[0])
answer = ""
for s in summary:
	answer += s[1]

print answer