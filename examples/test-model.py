#!/usr/bin/env python3

from gensim.models import KeyedVectors, Word2Vec
from gensim.test.utils import datapath

wv = Word2Vec.load('wikipedia-bigram.model.gz')
wv.wv.save_word2vec_format('/tmp/wikipedia-bigram.model.bin', binary=True)

print("the", wv.most_similar('the'))
print("environment", wv.most_similar('environment'))
print("greenpeace", wv.most_similar('greenpeace'))
print("transparency international", wv.most_similar("transparency_international"))
print("amnesty international", wv.most_similar('amnesty_international'))
print("siemens", wv.most_similar('siemens'))

## organizations
print("environment : human rights", wv.most_similar(positive=["greenpeace", "human_rights"], negative=["environmental"]))
print("corruption : integrity", wv.most_similar(positive=["transparency_international", "integrity"], negative=["corruption"]))

## corrupt entities
print ("transparency_international : siemens", wv.most_similar(positive=["transparency_international", "greenpeace"], negative=["siemens"]))



