from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import PorterStemmer as ps
from itertools import combinations

stopWords = ["?",".", "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]

index = {}
with open("inverted_index") as f:
	for line in f:
		line = line.strip("\n")
		line = line.split("=")
		index[line[0]] = line[1].split("||")

print "index created."

query = "Which groups of French society benefited from the revolution?"
query = query.lower()
queryWords = word_tokenize(query)
print "tokenised."
q = []
for i in queryWords:
	if i not in stopWords:
		q.append(ps().stem(i))

#print queryWords
#queryRel = q[:]
print q
print "queryWords created."
#print len(queryWords)
# queryWords = queryWords[0:8]
# print queryWords

queryRel = {}
for word in q:
	print word
	queryRel[word] = [word] 
	for i, j in enumerate(wn.synsets(word)):
		# print i, j.lemmas()
		for l in j.lemmas():
			queryRel[word].append(l.name())
print "queryRel created."

print queryRel

docList = {}

for word in queryRel:
	docList[word] = []
	for w in queryRel[word]:
		if w in index:
			docList[word] += index[w]

print docList

inter = []
i = 0
for w in docList:
	if i == 0:
		inter = docList[w]
	else:
		inter = list(set(inter)&set(docList[w]))
		print inter
	i += 1

print inter
# queryRel = list(set(queryRel))
# sentenceIDs = []

# inter = []
# inter2 = []
# j = 0
# for i in queryRel:
# 	if i in index:
# 		inter.append(index[i])
# 		inter2.append(i)
# 	# j+=1
	# if i in index and j == 1:
	# 	inter = set(index[i])
	# 	print i, index[i]
	# if i in index and j>1:
	# 	inter = list(set(inter)&set(index[i]))
	# 	print i, index[i]

# op2 = []
# for i in inter:
# 	op2 += i
# op2 = [i for i in sorted(op2) if int(i) > 211 and int(i) < 520]
# print set(op2), len(op2)
# #print inter
# for i,j in combinations(inter, r=2):
# 	op = set(i)&set(j)
# 	op = list(op)
# 	op = [i for i in sorted(op) if int(i) > 211 and int(i) < 520]
# 	print op, len(op)


# for i in queryRel:
# 	j += 1
# 	if i in index :
# 		sentenceIDs += index[i]

# sentenceIDs = [int(i) for i in sentenceIDs]
# relevantSent = [i for i in sorted(sentenceIDs) if i > 211 and i < 520]

# print sorted(relevantSent), len(relevantSent)


