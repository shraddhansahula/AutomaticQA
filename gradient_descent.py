import sys
import os
import pickle
import nltk
import re

#[3.0000000000000013, 6.999999999999991, 6.799999999999992, 0.1, 0.2, 0.1, 1.6000000000000003, 1.0999999999999999, 33.90000000000021, 0.30000000000000004]

#[0.7, 9.299999999999983, 1.9000000000000006, 0.1, 0.4, 0.1, 2.800000000000001, 1.5000000000000002, 1.5000000000000002, 0.4]

#[24.1, 4.1, 15.1, 0.1, 2.1, 0.1, 30.1, 3.1, 4.1, 1.1] l
inp = open("featureVectors_NCERT_iess301_Q1", "rb")
features = pickle.load(inp)
inp.close()
l = .1
weights = [0.1 for x in range(0,10)]
for a,w in enumerate(weights):
	print "weight being updated is",a
	if a == 3 or a==5:
		continue 
	# if a>1:
	# 	break
	rg1 = 0
	rg2 = 0
	prev = 0
	
	while(1):
		#calculating score
		for k, f in enumerate(features):
			f = list(f)
			score = 0

			for i,j in enumerate(f[1]):
				score += weights[i]*j
			#print score
			f[0] = score
			#print f
			f = tuple(f)
			features[k] = f

		features = sorted(features, key=lambda x: -x[0])

		wordCount = 0
		i = 0
		summary = []
		#generating summary
		while(1):
			sentence = features[i][2]
			i += 1
			wordList = nltk.word_tokenize(sentence)
			wordCount += len(wordList)
			summary.append(sentence)
			if wordCount>450:
				break
		
		summaryFile = open("./DUC Dataset/NISTeval/ROUGE/peers/iess301.M.Q1.corpus.1", "w")
		for s in summary:
			summaryFile.write(s)
			summaryFile.write("\n")
			#print s
		summaryFile.close()
		#evaluating summary
		#./ROUGE-1.5.5.pl -2 -1 -u -r 1000 -t 0 -n 4 -w 1.2 -m -l 250 -a ../rougejk.input
		os.chdir("/home/shraddhan/Honors/DUC Dataset/NISTeval/ROUGE/rouge")
		os.system("./ROUGE-1.5.5.pl -2 -1 -u -r 1000 -t 0 -n 4 -w 1.2 -m -l 250 -a ../rougejk.input2 > rouge_results")
		os.system("mv rouge_results /home/shraddhan/Honors")
		os.chdir("/home/shraddhan/Honors")

		i = 0
		Fscores=[]
		with open("rouge_results") as f:
			for line in f:
				if i==7 or i==27:
					score = re.findall("\d+\.\d+", line)[0]
					score = float(score)
					Fscores.append(score)
				i += 1
		print Fscores
		rg2 = Fscores[1]
		print weights
		if rg1 <= rg2:
			prev = w
			w += l
			weights[a] = w
			print w
			rg1 = rg2
		else:
			break
		print rg1, rg2