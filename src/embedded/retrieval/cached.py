'''
Created on May 29, 2019

@author: Albert Weichselbraun
'''

import gzip
import os.path
import requests
import shutil
from urllib.parse import quote_plus
from time import time, sleep
from inscriptis import get_text

# the time to wait between accesses
SLEEP_TIME = 1.5

class CachedTextRetrieval(object):
    '''
    Retrieves the text version of the given URL from the Web and
    stores it content in a cache. 
    '''


    def __init__(self):
        self.cache_base = ".cached-retrieval"
        if (not os.path.exists(self.cache_base)):
            os.mkdir(self.cache_base)
        self.last_access = time()
        
    def get_url(self, url, cached=True):
        '''
        Returns the cached version of the given URL, if available.
        '''
        cache_file = os.path.join(self.cache_base, quote_plus(url)) + ".gz"
        if os.path.exists(cache_file) and cached:
            with gzip.open(cache_file, 'rt') as f:
                return f.read()
            
        # guard for politeness    
        while (time() - self.last_access) <= SLEEP_TIME:
            sleep(0.5)
             
        html_content = requests.get(url).text
        text_content = get_text(html_content, display_images=False,
                                deduplicate_captions=False,
                                display_links=False)
        self.last_access = time()
        
        # let's cache again
        with gzip.open(cache_file, 'wt') as f:
            f.write(text_content)
            
        return text_content
        
    def clear_cache(self):
        if (os.path.exists(self.cache_base)):
            shutil.rmtree(self.cache_base)
            os.mkdir(self.cache_base)