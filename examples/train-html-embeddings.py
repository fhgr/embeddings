#!/usr/bin/env python3

import lzma
import tarfile
import logging
import re

from json import load
from lxml import etree

from embedded.train import Train

RE_FILTER_XML_HEADER = re.compile("<\?xml version=\".*? encoding=.*?\?>")
CORPUS_FILE = '../corpus/forum.tar.lzma'

TEXT_BLACKLIST = ('script', 'style')

class HtmlArchiveReader(object):

    def __init__(self, corpus_file):
        self.corpus_file = corpus_file
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    def __iter__(self):
        ''' iterates over the HTML archive and extracts all
            relevant word embeddings
        '''
        with lzma.open(self.corpus_file) as f:
            with tarfile.open(fileobj=f) as src:
                for fname in src.getmembers():
                    if not fname.isfile or not fname.name.endswith('.json'):
                        continue
                    self.logger.info("Processing file '%s'." % fname.name)
                    fobj = load(src.extractfile(fname))
                    yield from list(self.extract_features(fobj['html']))


    @staticmethod
    def normalize_text(txt):
        '''
        Normalizes text based on its length
        '''
        txt = txt.strip()
        if not txt:
            return ""
        elif len(txt) <= 5:
            return "*"
        elif len(txt) <= 10:
            return "**"
        elif len(txt) <= 20:
            return "***"
        elif len(txt) <= 40:
            return "****"
        return "*****"


    @staticmethod
    def extract_features(html):
        '''
        Extracts all relevant features from the given html file
        '''
        try:
            html = RE_FILTER_XML_HEADER.sub("", html)
            dom = etree.HTML(html)
        except ValueError as e:
            print(html[:240])
            print(e)
            import sys
            sys.exit(-1)
        for element in dom.iter():
            xpath = dom.getroottree().getpath(element)
            # filter comments
            if not isinstance(element.tag, str):
                continue

            element_list = [element.split("[")[0] for element in xpath.split("/")]
            element_text = element.text.strip() if element.text else ""
            if not element.tag in TEXT_BLACKLIST and element_text:
                element_list.append(HtmlArchiveReader.normalize_text(element_text))
            yield element_list

Train.train_model('html.model', HtmlArchiveReader(CORPUS_FILE), size=50)

