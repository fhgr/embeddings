'''
Created on May 27, 2019

@author: Albert Weichselbraun

see also: https://rare-technologies.com/word2vec-tutorial/
'''

import gensim
import os
from gzip import GzipFile
from builtins import staticmethod

class Train(object):
    '''
    Trains an embedding based on an iterator
    '''

    @staticmethod
    def train_model(model_name, sentence_iterator, size):
        ''' number of dimensions to include in the model '''
        model = gensim.models.Word2Vec(sentence_iterator, size=size, workers=os.cpu_count())
        model.save(GzipFile(model_name + ".gz", "w"))
