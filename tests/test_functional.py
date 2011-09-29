#!/usr/bin/env python2.6
'''Tests the functional implementations of product_matcher and names

Created on May 2, 2010

@author: Andrew Metcalf
'''
from milo_functional import names #@UnresolvedImport
from milo_functional import product_matcher #@UnresolvedImport

import unittest
import pickle

CASE_PATH= "./cases/"
LOG_PATH = "./logs/"

class ProductMatcherSteps(unittest.TestCase):
    
    def test_hungarian_matrix(self):
        pass
    
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
            (customer_names, product_names) = self._get_matcher(i)            
            self.assertEqual(expected,product_matcher.suitability_matrix(customer_names, product_names))
            
     
    def test_uncovered_zero(self):
        matrices = (
                    [[[1, 0], [2, 0]], [[3, 0], [4, 0]]],
                    [[[0, 0], [1, 0]], [[1, 0], [0, 0]]],
                    [[[2, 0], [5, 0], [1, 0]], [[5, 0], [0, 0], [3, 0]], [[0, 0], [2, 0], [0, 0]]]
                    )
        
        covers = (
                  [[False,False,False],[False,False,False]],
                  [[False,False,False],[True,False,False]],
                  [[False,True,False],[True,False,False]]
                  )
        
        expected = (
                   [(-1,-1),(-1,-1),(-1,-1)],
                   [(0,0),(1,1),(-1,-1)],
                   [(1,1),(1,1),(2,2)]
                   )
        # Runs each combination of matrices and covers
        for i,matrix in enumerate(matrices):
            for j,cover in enumerate(covers):
                self.assertEqual(expected[i][j],product_matcher.uncovered_zero(matrix, cover[0], cover[1]))

    def test_run_matcher(self):
        (start, expected) = self._get_log_data("run_matcher")
        
        for input,result in zip(start,expected):
            product_names = [product._name for product in input[4][0]]
            customer_names = [customer._name for customer in input[4][1]]
            suitability = product_matcher.suitability_matrix(customer_names, product_names)
            self.assertEqual(result[0],product_matcher.run_matcher(suitability))
    
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

        for i, expected in enumerate(cases):
            suitability = product_matcher.suitability_matrix(*self._get_matcher(i))
            self.assertEqual(expected, product_matcher.match_products(suitability)) 
            
    def test_matched_solution(self):
        cases = ( 11.5, 7, 4.5, 17.5, 20.25, 19.75, 4.5 )
        
        for i, expected in enumerate(cases):
            self.assertEqual(expected, product_matcher.matched_solution(*self._get_matcher(i))[1]) 
    
    def _get_matcher(self, index):
        customer_names = open(CASE_PATH+'customers-'+str(index)+'.txt').read().replace("\r","").split('\n')
        product_names  = open(CASE_PATH+'products-' +str(index)+'.txt').read().replace("\r","").split('\n')
        
        # My files from excel have extra new lines...
        customer_names.pop()
        product_names.pop()
        return (customer_names, product_names)
    
    def _get_log_data(self, function_name):
        return (pickle.load(open(LOG_PATH+"input_"+function_name+".log")), \
                pickle.load(open(LOG_PATH+"output_"+function_name+".log")))
                
"""
    These tests check each of the main hungarian algorithm functions against logged output
    from the equivalent functions in the imperative solution.  To use them, each function must
    be modified to return the end state in the form [matrix, covered_rows, covered_cols] rather
    than calling the next function in the chain.

    def test_cover_columns(self):
        (start, expected) = self._get_log_data("cover_columns")
        
        for input,result in zip(start,expected):
            self.assertEqual(result[2],product_matcher.cover_columns(input[0]))

    def test_adjust_matrix(self):
        (start, expected) = self._get_log_data("adjust_matrix")
        
        for input,result in zip(start,expected):
            self.assertEqual(result[0],product_matcher.adjust_matrix(*input[:3]))
            
    def test_prime_zeroes(self):
        # Does not test what gets called next and passing of z_row, z_col
        (start, expected) = self._get_log_data("prime_zeroes")
        
        for input,result in zip(start,expected):
            self.assertEqual(result[:3],product_matcher.prime_zeroes(*input[:3]))
            
    def test_construct_path(self):
        # Does not test what gets called next and passing of z_row, z_col
        (start, expected) = self._get_log_data("construct_path")
        
        for input,result in zip(start,expected):
            self.assertEqual(result[0],product_matcher.construct_path(input[0],input[3]))
"""

class NameClasses(unittest.TestCase):
    
    def test_has_common_factors(self):
        cases = (
                 (["test this name","anotherAB"],False),
                 (["test this name","test"],True)
                 
                 )
        
        for input in cases:
            self.assertEqual(input[1],names.has_common_factor(len(input[0][0]), len(input[0][1])))
    
    def test_get_suitability(self): 
        cases = (
                 (["Henry James","Widget"],4.5),
                 (["Andrew","Widget"],4.5),
                 (["Henry James","BlahB"],7),
                 (["Andrew","BlahB"],4),
                 (["ft","WDNKSb"],0)
                 )
        
        for input in cases:
            self.assertEqual(input[1],names.get_suitability(input[0][0],input[0][1]))

    def test_count_letters(self):
        cases = {
                 "blah" : [1,3],
                 "A n o" : [2, 1]
                 
                 }
        
        for input, expected in cases.iteritems():
            self.assertEqual(expected[0], names.count_letters(input, names.VOWELS))
            self.assertEqual(expected[1], names.count_letters(input, names.CONSONANTS))
        
        
               
if __name__ == '__main__':
    unittest.main()