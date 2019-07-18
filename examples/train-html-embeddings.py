#!/usr/bin/env python3

import lzma
import tarfile

from json import load
from lxml import etree

CORPUS_FILE = '../corpus/forum.tar.lzma'

TEXT_BLACKLIST = ('script', 'style')

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


def extract_features(html):
    '''
    Extracts all relevant features from the given html file
    '''
    dom = etree.HTML(html)
    for element in dom.iter():
        xpath = dom.getroottree().getpath(element)
        # filter comments
        if not isinstance(element.tag, str):
            continue

        element_list = [element.split("[")[0] for element in xpath.split("/")]
        element_text = element.text.strip() if element.text else ""
        if not element.tag in TEXT_BLACKLIST and element_text:
            element_list.append(normalize_text(element_text))
        print(element_list)


with lzma.open(CORPUS_FILE) as f:
    with tarfile.open(fileobj=f) as src:
        for fname in src.getmembers():
            if not fname.isfile or not fname.name.endswith('.json'):
                continue
            fobj = load(src.extractfile(fname))
            extract_features(fobj['html'])
            break

