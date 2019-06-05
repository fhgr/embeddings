#!/usr/bin/env python3

from embedded.datasource.wikidata import WikipediaReferencesIterator
from embedded.retrieval.cached import CachedTextRetrieval

PERSON_QUERY="""PREFIX wd:<http://www.wikidata.org/entity/>
PREFIX wdt:<http://www.wikidata.org/prop/direct/>

SELECT * FROM <http://wikidata.org> WHERE {
  ?s wdt:P31 wd:Q5.
}
"""

# the next is simple :)
w = WikipediaReferencesIterator(server_url='http://localhost:8890/sparql/', base_query=PERSON_QUERY, language='en')
c = CachedTextRetrieval()

for url in w:
    c.get_url(url)
    print(url)
