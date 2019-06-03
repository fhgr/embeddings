'''
Created on May 27, 2019

@author: Albert Weichselbraun

TODO: 
- consider 'Also known as' in the sentences :)
  compare: https://www.wikidata.org/wiki/Q61933318
  
Note:
- wikidata prefixes: https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format#Prefixes_used
'''

import logging
from SPARQLWrapper import SPARQLWrapper, JSON
from builtins import staticmethod
from DistUpgrade import DistUpgradeFetcherSelf

# select all non-profit organizations
# + subclass of npo
# + subclass of subclasses of npo
DEFAULT_BASE_QUERY = """
PREFIX wd:<http://www.wikidata.org/entity/>
PREFIX wdt:<http://www.wikidata.org/prop/direct/>

SELECT * WHERE {
    {?s wdt:P31 wd:Q163740. } 
    UNION
    {
     ?sc wdt:P279 wd:Q163740. 
     ?s  wdt:P31 ?sc.
    }
    UNION 
    { 
     ?scc wdt:P279 wd:Q163740. 
     ?sc  wdt:P279 ?scc.
     ?s   wdt:P31 ?sc.
    }
}
"""

"""
PREFIX wd:<http://www.wikidata.org/entity/>
PREFIX wdt:<http://www.wikidata.org/prop/direct/>

SELECT * FROM <http://wikidata.org> WHERE {
  <http://www.wikidata.org/entity/Q55672> ?pp ?oo.
  {?oo rdfs:label ?o.}
  UNION
  {?oo rdfs:description ?o.}
  UNION
  {?oo skos:altLabel ?o.}
  UNION
  {  <http://www.wikidata.org/entity/Q55672> skos:altLabel ?o.}
  filter(lang(?o)="en")
 }
LIMIT 200
"""

# select all relevant data for a given entitiy.
class WikidataIterator(object):
    '''
    Creates artificial sentences based on a WikiData base query
    '''
    def __init__(self, server_url, base_query=DEFAULT_BASE_QUERY, language="en"):
        '''
        Constructor
        base_query - a query that returns all relevant entities in the 'o' binding.
        '''
        self.sparql = SPARQLWrapper(server_url)
        self.sparql.setQuery(base_query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        
        self.language = language;
        self.entities = [r['s']['value'] for r in results['results']['bindings']]
        print("Obtained {} entities to be queries for background information.".format(len(self.entities)))
        
    def __iter__(self):
        return self 


class LodWikidataIterator(WikidataIterator):
    ''' Iterates over Wikidata values
    '''
        
    @staticmethod
    def get_key(resource_url):
        '''
        returns the resource's identifier
        '''
        return resource_url.split("/")[-1]
        
    def __iter__(self):
        for entity in self.entities:
            logging.info("Querying statements for entity <{}>".format(entity))
            query = """SELECT * WHERE {{
                <{}> ?p ?o.
                FILTER(!isLiteral(?o) || lang(?o)="{}")
            self.sparql.setQuery(query)
            }}""".format(entity, self.language)
            self.sparql.setQuery(query)
            results = self.sparql.query().convert()
            for r in results['results']['bindings']:
                yield self.get_key(entity), r['p']['value'], self.get_key(r['o']['value'])

class WikipediaReferencesIterator(WikidataIterator):
    
    def __iter__(self):
        for entity in self.entities:
            query = """PREFIX wd:<http://www.wikidata.org/entity/>
            PREFIX wdt:<http://www.wikidata.org/prop/direct/>
            PREFIX schema: <http://schema.org/>
            
            SELECT * FROM <http://wikidata.org> WHERE {{
              ?url schema:about <{}> .
            }}
            """.format(entity)
            self.sparql.setQuery(query)
            while True:
                try:
                    results = self.sparql.query().convert()
                    break
                except Exception as e:
                    print(e)
                    pass

            for r in results['results']['bindings']:
                url = r['url']['value']
                if self.language + ".wikipedia.org" in url:
                    yield url
    
