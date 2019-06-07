#!/usr/bin/env python3

from sys import stdin

from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:8890/sparql/")
sparql.setQuery(stdin.read())
sparql.setReturnFormat(JSON)

for result in sparql.query().convert()['results']['bindings']:
    print("\t".join(result[binding]['value'] for binding in sorted(result.keys())))
