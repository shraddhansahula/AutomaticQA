# -*- coding: utf-8 -*-

import sys
import io, os
import math
import operator
from nltk import PorterStemmer as ps
from nltk.tokenize import word_tokenize
from practnlptools.tools import Annotator

annotator = Annotator()

def read_stop_words_set():
    """Read the stop words from a file into a python list."""
    stop_words_set = []
    f = io.open("../stop_words.txt", "r", encoding="utf-8")
    for word in f:
        if word[-1] == "\n":
            word = word[:-1]
        stop_words_set.append(word)
    stop_words_set = list(set(stop_words_set))
    f.close()
    return stop_words_set

def read_chapter_index():
    """Read the chapters and their starting and ending sentence ids"""
    chapter_index = []
    f = open("../chapter_index.txt", "r")
    for line in f.readlines():
        chapter, idx = line.split("=")
        start, end = idx.strip("\n").split(",")
        chapter_index.append((int(start), int(end), int(chapter)))
    chapter_index.sort()
    f.close()
    return chapter_index

def read_inverted_index():
    inverted_index = {}
    f = io.open("../inverted_index", "r", encoding = "utf-8")
    for line in f.readlines():
        term, idx = line.split("=")
        idx_list = [int(i) for i in idx.split("||")]
        inverted_index[term] = sorted(idx_list)
    f.close()
    return inverted_index

def ne_tagger(question):
    ne_tagged_list = annotator.getAnnotations(question)['ner']
    ne_tagged = {}
    for name, tag in ne_tagged_list:
        ne_tagged[ps().stem(name).lower()] = tag
    return ne_tagged

def detect_question_main(question):
    stop_words_set = read_stop_words_set()
    chapter_index = read_chapter_index()
    inverted_index = read_inverted_index()
    score = {}
    for i in range(16):
        score[i+1] = 0.0
    ne_tagged = ne_tagger(question)
    for term in word_tokenize(question):
        stem = ps().stem(term.lower())
        if stem in stop_words_set or stem not in inverted_index:
            continue
        if stem in ne_tagged and ne_tagged[stem] is not "O":
            # print stem, ne_tagged[stem]
            multiplier = 2.0
        else:
            multiplier = 1.0
        tf_counts = {}
        for sent_id in inverted_index[stem]:
            for rec in chapter_index:
                if sent_id >= rec[0] and sent_id <= rec[1]:
                    try:
                        tf_counts[rec[2]] += 1.0
                    except:
                        tf_counts[rec[2]] = 1.0
                    break
        # print(term, tf_counts)
        idf = [1 for ch in tf_counts if tf_counts[ch] > 0]
        idf = len(idf)
        if idf > 0:
            idf = math.log10(16.0/float(idf))
        # print term, idf
        for ch in tf_counts:
            # print term, ch, tf_counts[ch], idf, (math.log10(1 + tf_counts[ch])*idf*multiplier)
            score[ch] += (math.log10(1+tf_counts[ch])*idf*multiplier)
        # print term, score
    score = sorted(score.items(), key=operator.itemgetter(1))
    return score[-1][0]


if __name__ == '__main__':
    
    while True:
        question = raw_input()
        print detect_question_main(question)
    


