#!/usr/bin/env python2.6
'''Common test class for testing matrix functions

Change the import statement to change whether the
functional or imperative implementation is tested

Created on May 5, 2010
@author: Andrew Metcalf
'''
from milo_functional import matrix_functions #@UnresolvedImport
import unittest

class MatrixFunctions(unittest.TestCase):
    
    def test_zero_row(self):
        self.assertEqual([0,0], matrix_functions.create_row(2))
    
    def test_augment_matrix(self):
        cases = (
             ([[1,2,3],[2,3,4]] , [[1,2,3],[2,3,4],[0,0,0]]), # More columns
             ([[1],[2]] , [[1,0],[2,0]]), # One col
             ([[1,2],[2,6],[3,6]] , [[1,2,0],[2,6,0],[3,6,0]]), # More rows
             ([[1,2,3],[2,3,4],[0,0,0]] , [[1,2,3],[2,3,4],[0,0,0]]), # Square
             ([[1]] , [[1]]), # One element
             ([[1,2,3,5],[2,3,4,5]] , [[1,2,3,5],[2,3,4,5],[0,0,0,0],[0,0,0,0]])
             )
        
        for input in cases:
            self.assertEqual(input[1], matrix_functions.augment_matrix(input[0]))
    
    def test_min_matrix(self):
        cases = (
                 ([[1,2],[3,4]], [[3,2],[1,0]]),
                 ([[0,0,0],[0,0,0]], [[0,0,0],[0,0,0]]),
                 ([[4,4,4],[4,4,4]], [[0,0,0],[0,0,0]]),
                 ([[4,4,4],[1,1,1]], [[0,0,0],[3,3,3]]),
                 )

        for input in cases:
            self.assertEqual(input[1], matrix_functions.min_matrix(input[0]))
        
    def test_subtract_row_min(self):
        cases = (
                 ([[1,2],[3,4]], [[0,1],[0,1]]),
                 ([[4,6],[9,2]], [[0,2],[7,0]]),
                 ([[1]],[[0]])
                ) 
        
        for input in cases:
            self.assertEqual(input[1], matrix_functions.subtract_row_min(input[0]))
            
if __name__ == '__main__':
    unittest.main()