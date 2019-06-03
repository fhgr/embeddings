#!/usr/bin/python3

import gzip
import string
from csv import reader
from glob import glob
from embedded.train import Train

TRANSLATE = str.maketrans('', '', string.punctuation)

class CacheReader():

    def __init__(self, path):
        self.files = glob(path)

    def __iter__(self):
        for fname in self.files:
            with gzip.open(fname, 'rt') as f:
                for word in f.read().split():
                    word = word.translate(TRANSLATE).lower()
                    if word:
                        yield word


Train.train_model('wikipedia.model.gz', CacheReader(".cached-retrieval/*.gz"))

