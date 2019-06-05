#!/usr/bin/python3

import gzip
import string
from csv import reader
from glob import glob
from embedded.train import Train
from sentence_splitter import SentenceSplitter

from gensim.models.phrases import Phrases, Phraser

TRANSLATE = str.maketrans('', '', string.punctuation)

class CacheReader():
    ''' Returns an iterator over sentences'''

    def __init__(self, path):
        self.files = glob(path)
        self.splitter = SentenceSplitter(language='en')

    def __iter__(self):
        for fname in self.files:
            with gzip.open(fname, 'rt') as f:
                for sentence in self.splitter.split(f.read()):
                    if sentence:
                        yield [word.translate(TRANSLATE).lower() for word in sentence.split()]

# detect multi-word expressions and train with them
sentences = CacheReader(".cached-retrieval/*.gz")
phrases = Phraser(Phrases(sentences, min_count=1, threshold=1, delimiter=b' '))  # train model

#trigram  = Phrases(bigram[sentence_stream], min_count=1, delimiter=b' ')

sentences = CacheReader(".cached-retrieval/*.gz")
Train.train_model('wikipedia.model', phrases[sentences])

