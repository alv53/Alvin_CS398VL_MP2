from __future__ import division
from math import log
from math import exp
import nltk
import json
import re, pprint
from nltk.corpus import stopwords

from nltk.book import *
from nltk.corpus import PlaintextCorpusReader

text1 = FreqDist(text1)
text2 = FreqDist(text2)
text3 = FreqDist(text3)
text4 = FreqDist(text4)
text5 = FreqDist(text5)
text6 = FreqDist(text6)
text7 = FreqDist(text7)
text8 = FreqDist(text8)
text9 = FreqDist(text9)
def importance(w, tokens_freq, tokens_10, text1, text2, text3, text4, text5, text6, text7, text8, text9):
	tf = 0.5 + (0.5 * tokens_freq[w])/(max(tokens_freq[w] for w in tokens_10))
	iter = 0
	if text1[w] > 0:
		iter+=1
	if text2[w] > 0:
		iter+=1
	if text3[w] > 0:
		iter+=1
	if text4[w] > 0:
		iter+=1
	if text5[w] > 0:
		iter+=1
	if text6[w] > 0:
		iter+=1
	if text7[w] > 0:
		iter+=1
	if text8[w] > 0:
		iter+=1
	if text9[w] > 0:
		iter+=1
	if(iter == 0):
		iter = exp(-320)
	idf = log(9/iter)
	return tf * idf
# select chapter to print, chapter 0 for whole book
# chapter = 4
def tag_chapter(chapter):
	text_raw = open("ofk_ch" + str(chapter) + ".txt").read()
	bad = ["ca", 'wo', 'thelmselves']
	tokens = nltk.word_tokenize(text_raw)
	# tokens = [w.lower() for w in tokens] #change to lower case
	tokens = [re.sub('\.','',w) for w in tokens] #remove periods
	tokens = [w for w in tokens if w.isalpha()] #just keep words
	tokens = [w for w in tokens if not w in stopwords.words('english')]
	tokens = [w for w in tokens if len(w) > 1]
	tokens_freq = FreqDist(tokens)
	tokens_10 = [w for w in tokens if tokens_freq[w] > 20]
	tokens_10 = [w for w in tokens_10 if w not in bad]
	tokens_freq = FreqDist(tokens_10)

	tokens_table = [(w, importance(w, tokens_freq, tokens_10, text1, text2, text3, text4, text5, text6, text7, text8, text9)) for w in tokens_freq]

	a = lambda e1, e2: int(1000000*(e1[1] - e2[1]))

	sorted_table = sorted(tokens_table, cmp = a, reverse=True)
	# The number of elements you want to dump
	nums = 20
	final_table = sorted_table[:nums];
	pos_tuples = []
	for x in final_table:
		token = nltk.word_tokenize(x[0])
		pos_tuples = pos_tuples + nltk.pos_tag(token)
	list_pos = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNP', 'NNPS', 'NNS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB']
	pos_names = ['Conjunction', 'Numerical', 'Determiner', 'Existential There', 'Foreign Word', 'Preposition or Conjunction, Subordinating', 'Adjective or Numeral', 'adjective, comparative', 'adjective, superlative', 'List Item Marker', 'Modal Auxiliary', ' Noun, Common', 'Noun, Proper, Singular', 'Noun, Proper, Plural', 'Noun, Common, Plural', 'Pre-Determiner', 'Genitive Marker', 'Pronoun, Personal', 'Pronoun, Possessive', 'Adverb', 'Adverb, Comparitive', 'Adverb, Superlative', 'Particle', 'Symbol', '"to" as preposition', 'Interjection', 'Verb, Base Form', 'Verb, Past Tense', 'Verb, Present Participle', 'Verb, Past Participle', 'Verb, Present Tense, Not 3rd Person Singular', 'Verb, Present Tense, 3rd Person Singular', 'WH-Determiner', 'WH-Pronoun', 'WH-Pronoun, Possessive', 'WH-Adverb']
	result = [None] * len(list_pos)
	for p in range(len(list_pos)):
		result[p] = [dict(name=w[0]) for w in pos_tuples if w[1] == list_pos[p]]
	result_dict = [dict(name=pos_names[n], children=result[n]) for n in range(len(list_pos)) if result[n]]
 	return result_dict


listthing = [tag_chapter(1), tag_chapter(2), tag_chapter(3), tag_chapter(4)]
listdict = dict(name="Once and Future King", children=[dict(name="Chapter " + str(w+1), children=listthing[w]) for w in range(4)])

with open("pos_tfidf.json",'w') as outfile:
	json.dump(listdict,outfile, sort_keys = True, indent = 4, ensure_ascii=False)
