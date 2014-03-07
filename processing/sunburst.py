import nltk
import json
from nltk.corpus import wordnet as wn
from nltk.corpus import words
from nltk.book import *

from nltk.corpus import PlaintextCorpusReader

def tag_chapter(chapter):
	text_raw = open("ofk_ch" + str(chapter) + ".txt").read()
	tokens = nltk.word_tokenize(text_raw)
	tokens = [w.lower() for w in tokens] #change to lower case
	tokens = [w for w in tokens if w.isalpha()] #just keep words
	fd = FreqDist(tokens)
	tokens = fd.keys()
	freqs = fd.values()
	# print [x for x in freqs]
	pos_tuples = nltk.pos_tag(tokens)
	list_pos = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNP', 'NNPS', 'NNS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB']
	pos_names = ['Conjunction', 'Numerical', 'Determiner', 'Existential There', 'Foreign Word', 'Preposition or Conjunction, Subordinating', 'Adjective or Numeral', 'adjective, comparative', 'adjective, superlative', 'List Item Marker', 'Modal Auxiliary', ' Noun, Common', 'Noun, Proper, Singular', 'Noun, Proper, Plural', 'Noun, Common, Plural', 'Pre-Determiner', 'Genitive Marker', 'Pronoun, Personal', 'Pronoun, Possessive', 'Adverb', 'Adverb, Comparitive', 'Adverb, Superlative', 'Particle', 'Symbol', '"to" as preposition', 'Interjection', 'Verb, Base Form', 'Verb, Past Tense', 'Verb, Present Participle', 'Verb, Past Participle', 'Verb, Present Tense, Not 3rd Person Singular', 'Verb, Present Tense, 3rd Person Singular', 'WH-Determiner', 'WH-Pronoun', 'WH-Pronoun, Possessive', 'WH-Adverb']
	results = [0] * 36
	resultWord = [[dict(name="", size=0)] for x in range(36)]

	for p in pos_tuples:
	# p = pos_tuples[0]
		for x in range(36):
			if list_pos[x] == p[1]:
				results[x] = results[x] + 1
				inDict = False
				# for q in range(len(resultWord[x])):
				# 	if((resultWord[x][q])["name"] == p[0]):
				# 		inDict = True
				# if not inDict:		
				(resultWord[x]).append(dict(name=p[0], size=fd[p[0]]))

	# for x in resultWord:
	# 	print x[:5]
	a = lambda e1, e2: int(1000000*(e1["size"] - e2["size"]))
	for x in range(len(resultWord)):
		resultWord[x] = sorted(resultWord[x], cmp = a, reverse=True)

	result_dict = [dict(name=list_pos[n], children=resultWord[n][:5]) for n in range(36) if results[n] > 100]
 	return result_dict



listthing = [tag_chapter(1), tag_chapter(2), tag_chapter(3), tag_chapter(4)]
listdict = dict(name="OFK", children=[dict(name="Chapter " + str(w+1), children=listthing[w]) for w in range(len(listthing))])

with open("sunburst.json",'w') as outfile:
	json.dump(listdict,outfile, sort_keys = True, indent = 4, ensure_ascii=False)
