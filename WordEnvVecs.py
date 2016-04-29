#!/usr/bin/python

import os
import sys
import nltk
import string
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize

class WordEnvironmentVectors(object):
	"""
	Create feature vectors for each word in a corpus.
	Features are determined based on the words surrounding each corpus word.

	self.word_vectors is a mapping of each unique word in training to a list of 
	the feature vector created for each instance of that word in training

	To create vectors from files in a directory:
	wev = WordEnvironmentVectors.create_vectors(indir)
	wev.save_vecs(file)
	"""

	def __init__(self, word_list, vocab=None, window_size=5):
		#https://en.wiktionary.org/wiki/Appendix:Basic_English_word_list
		self.words = word_list
		self.vocab = vocab
		self.window_size = window_size
		self.word_vectors = defaultdict(list)
		self.punctuation = string.punctuation
		self.stopwords = stopwords.words('english')

	def clear_vectors(self):
		self.word_vectors = defaultdict(list)

	def get_file_text(self, f):
		words = []
		for line in f:
			if line.split():
				line = line.lower().split()
				for i, word in enumerate(line):
					try:
						word.decode('ascii')
						words.append(word)
					except UnicodeDecodeError:
						del line[i]

		return ' '.join(words)

	def tokenize(self, text):
		"""Split a block of text into sentences, and further into words"""
		sentences = []
		for s in sent_tokenize(text):
			sentences.append(word_tokenize(s))
		return sentences

	def get_word_vecs(self, sent):
		vecs = []
		#punctuation and stopwords may add too much noise to vectors
		#s = [w for w in sent if w not in self.punctuation and w not in self.stopwords]

		for i, w in enumerate(sent):
			#if w not in self.punctuation and w not in self.stopwords:
			if w in self.words and w not in self.stopwords:
				#instiantiate vector as the length of our feature set
				word_vec = [0]*len(self.vocab)
				window_words = []
				#handle the exception of the word being less than window_size
				#away from the beginning/end of the sentence
				for i in range(1,self.window_size+1) + range(-self.window_size,0):
					try:
						if sent[i] in self.vocab:
							window_words.append(sent[i])
					except (IndexError): pass

				for w in window_words:
					word_vec[self.vocab[w]] = 1
				vecs.append(word_vec)
			else:
				vecs.append(None)

		return vecs

	def create_vectors(self, f):
		f = open(f)
		vecs = []
		sents = self.tokenize(self.get_file_text(f))
		for s in sents:
			word_vecs = self.get_word_vecs(s)
			vecs.append(zip(s, word_vecs))

		return vecs

	def collect_word_vecs(self, word_vecs):
		for s in word_vecs:
			for word, vec in s:
				if vec is not None:
					self.word_vectors[word].append(vec)

	"""
	# Following functions needed before I preprocessed to get vocabulary
	def pad_vecs(self):
		#pad vectors so they have an index for each feature for clustering
			for word in self.word_vectors:
				for i, vec in enumerate(self.word_vectors[word]):
					self.word_vectors[word][i] = self.pad(vec, len(self.features), 0)

	def pad(self, l, size, padding):
		return l + [padding] * abs((len(l)-size))
	"""

	def create(self, filename):
		vecs = self.create_vectors(filename)
		self.collect_word_vecs(vecs)



"""
Hyperparameters:
	Should I remove stopwords and/or punctuation in get_word_vecs()?
	Size of window (self.window_size)
"""





