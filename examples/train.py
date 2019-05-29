#!/usr/bin/python3

import gzip
from csv import reader
from embedded.train import Train

with gzip.open("wikidata.csv.gz", "rt") as f:
    src = reader(f)
    Train.train_model('wikidata.model.gz', src)
