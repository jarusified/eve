import re
from stemming.porter2 import stem
import nltk
class Worder:
	def stemmer(self,word):
		word=stem(word)
		return word
	def named_entities(self,text):
		tokens=nltk.word_tokenize(text)
		tags=nltk.pos_tag(tokens)
		named_ent=nltk.ne_chunk(tags,binary=True)
		return named_ent

