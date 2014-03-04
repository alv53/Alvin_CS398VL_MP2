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
	tokens = fd.keys()[:20]
	pos_tuples = nltk.pos_tag(tokens)
	list_pos = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNP', 'NNPS', 'NNS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB']
	pos_names = ['Conjunction', 'Numerical', 'Determiner', 'Existential There', 'Foreign Word', 'Preposition or Conjunction, Subordinating', 'Adjective or Numeral', 'adjective, comparative', 'adjective, superlative', 'List Item Marker', 'Modal Auxiliary', ' Noun, Common', 'Noun, Proper, Singular', 'Noun, Proper, Plural', 'Noun, Common, Plural', 'Pre-Determiner', 'Genitive Marker', 'Pronoun, Personal', 'Pronoun, Possessive', 'Adverb', 'Adverb, Comparitive', 'Adverb, Superlative', 'Particle', 'Symbol', '"to" as preposition', 'Interjection', 'Verb, Base Form', 'Verb, Past Tense', 'Verb, Present Participle', 'Verb, Past Participle', 'Verb, Present Tense, Not 3rd Person Singular', 'Verb, Present Tense, 3rd Person Singular', 'WH-Determiner', 'WH-Pronoun', 'WH-Pronoun, Possessive', 'WH-Adverb']
	result = [None] * len(list_pos)
	for p in range(len(list_pos)):
		result[p] = [dict(name=w[0]) for w in pos_tuples if w[1] == list_pos[p]]
	result_dict = [dict(name=pos_names[n], children=result[n]) for n in range(len(list_pos)) if result[n]]
 	return result_dict



listthing = [tag_chapter(1), tag_chapter(2), tag_chapter(3), tag_chapter(4)]
listdict = dict(name="Once and Future King", children=[dict(name="Chapter " + str(w+1), children=listthing[w]) for w in range(4)])

with open("pos_by_chapter.json",'w') as outfile:
	json.dump(listdict,outfile, sort_keys = True, indent = 4, ensure_ascii=False)
