#!/usr/bin/env python

import sys, os, lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher, TermQuery
from org.apache.lucene.index import IndexReader

from string import Template

class CustomTemplate(Template):
    delimiter = '#'
    
def index_request(format, dir, record_name, query):
  indexDir = '/Users/lizazim/Documents/index/' + dir
  template = CustomTemplate(format)
  fsDir = SimpleFSDirectory(Paths.get(indexDir))
  reader = DirectoryReader.open(fsDir)
  searcher = IndexSearcher(reader)
  query = TermQuery(Term(record_name, query))
  scoreDocs = searcher.search(query, 10000000000).scoreDocs
  results = []
  for scoreDoc in scoreDocs:
    doc = searcher.doc(scoreDoc.doc)
    table = dict((field.name(), field.stringValue())
                   for field in doc.getFields())
    results.append(template.substitute(table).encode('utf-8'))
  reader.close()
  return results

first_sixth = ["a", "b", "c"]
second_sixth = ["d", "e", "f", "g"]
third_sixth = ["h", "i", "j", "k"]
fourth_sixth = ["l", "m", "n", "o", "p"]
fifth_sixth = ["q", "r", "s", "t"]

#lucene.initVM(vmargs=['-Djava.awt.headless=true'])
#print index_request("#value", "disambiguations", "subject", "Piano_(disambiguation)")