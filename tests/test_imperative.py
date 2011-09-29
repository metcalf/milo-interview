#!/usr/bin/env python2.6
'''Tests the imperative implementations of product_matcher and names

Created on May 2, 2010

@author: Andrew Metcalf
'''

from milo_imperative import product_matcher #@UnresolvedImport
from milo_imperative import names #@UnresolvedImport
from milo_imperative import logger #@UnresolvedImport

import unittest


CASE_PATH= "./cases/"
LOG_PATH = "./logs/" 

class ProductMatcherSteps(unittest.TestCase):
    
    def test_match_products(self):
        cases = (
                 [1, 0],
                 [1],
                 [0],
                 [0,2,1,3],
                 [2,0,3],
                 [2,0,3],
                 [-1,0,-1]
                 )
        
        log = logger.Logger(LOG_PATH)
        
        for i, expected in enumerate(cases):
            matcher = self._get_matcher(i,log)
            self.assertEqual(expected, matcher.match_products())
        
        log.write()
    
    def test_match_suitability(self):
        cases = ( 11.5, 7, 4.5, 17.5, 20.25, 19.75, 4.5 )
        
        for i, expected in enumerate(cases):
            matcher = self._get_matcher(i)
            pairs = matcher.match_products()
            self.assertEqual(expected, matcher.match_suitability(pairs))
    
    def test_suitability_matrix(self):
        cases = (
                 [[4.5,7],[4.5,4]],
                 [[4.5,7]],
                 [[4.5]],
                 [[4.5,3,3,3],[1.5,3,4.5,3],[4.5,4,4,4],[1.5,3,3,4.5]],
                 [[3,3,4.5,4.5],[11.25,4,6,4],[3,3,4.5,4.5]],
                 [[11,11,11,11.25],[2,2,2,4.5],[3,3,3,6.75]],
                 [[2.25],[4.5],[3]]
                 )
        
        for i, expected in enumerate(cases):
            matcher = self._get_matcher(i)            
            self.assertEqual(expected,matcher.suitability_matrix())
            
    def _get_matcher(self, index,log = None):
        customer_names = open(CASE_PATH+'customers-'+str(index)+'.txt').read().replace("\r","").split('\n')
        product_names  = open(CASE_PATH+'products-' +str(index)+'.txt').read().replace("\r","").split('\n')
        
        # My files from excel have an extra new lines...
        customer_names.pop()
        product_names.pop()
        return product_matcher.ProductMatcher(customer_names, product_names, log)

class NameClasses(unittest.TestCase):
    
    def test_get_factors(self):
        cases = {
                 "test this name" : set([2,7,14]),
                 "prime number!" : set([13]),
                 "b" : set(),
                 "oddNumber" : set([3,9]),
                 "test" : set([2,4])
                 }
        
        for name, factors in cases.iteritems():
            self.assertEqual(factors, names.Name(name).get_factors())
    
    def test_has_common_factors(self):
        cases = (
                 (["test this name","anotherAB"],False),
                 (["test this name","test"],True)
                 
                 )
        
        for input in cases:
            other_factors = names.Name(input[0][1]).get_factors()
            self.assertEqual(input[1],names.Name(input[0][0]).has_common_factor(other_factors))

    def test_is_even(self):
        cases = {
                 "test" : True,
                 "other" : False
                 }
        
        for name, expected in cases.iteritems():
            self.assertEqual(expected, names.Product(name).is_even())
    
    def test_get_suitability(self): 
        cases = (
                 (["Henry James","Widget"],4.5),
                 (["Andrew","Widget"],4.5),
                 (["Henry James","BlahB"],7),
                 (["Andrew","BlahB"],4)
                 )
        
        for input in cases:
            product = names.Product(input[0][1])
            self.assertEqual(input[1],names.Customer(input[0][0]).get_suitability(product))

if __name__ == '__main__':
    unittest.main()
