'''
Created on May 29, 2019

@author: albert
'''
import unittest

from embedded.retrieval.cached import CachedTextRetrieval
from time import time


class Test(unittest.TestCase):

    def testCachedRetrieval(self):
        r = CachedTextRetrieval()
        r.clear_cache()
        
        content = r.get_url("https://weichselbraun.net/publications/")
        assert 'Albert' in content
        
        t = time()
        content = r.get_url("https://weichselbraun.net/")
        assert time() - t >= 1.5
        
        t = time()
        content = r.get_url("https://weichselbraun.net/")
        assert time() - t <= 0.2
        
if __name__ == "__main__":
    unittest.main()