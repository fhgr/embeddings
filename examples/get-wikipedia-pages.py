#!/usr/bin/env python3

from embedded.datasource.wikidata import WikipediaReferencesIterator
from embedded.retrieval.cached import CachedTextRetrieval

# the next is simple :)
w = WikipediaReferencesIterator(server_url='http://localhost:8890/sparql/', language='en')
c = CachedTextRetrieval()

for url in w:
    c.get_url(url)
    print(url)
