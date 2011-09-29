#!/usr/bin/env python2.6
'''Implements product-customer matching 

For a list of customer names and product names, ProductMatcher
computes the maximum suitability assignment of customers to products
based on the suitabilty algorithm defined by the Customer object.

It uses the Hungarian/Munkres algorithm to solve the assignment problem.
Implementation of the Hungarian algorithm based on:
http://en.wikipedia.org/wiki/Hungarian_algorithm
http://github.com/bmc/munkres/blob/master/munkres.py

Usage: 
1. Initialize a new ProductMatcher with a list of customer names and 
   a list of product names
2. Call match_products to return a list with the product index assigned 
   to each customer in order
3. Call match_suitability with the list of assignments to return the 
   suitability of the match

Created on May 2, 2010
@author: Andrew Metcalf
'''

import names #@UnresolvedImport
import matrix_functions #@UnresolvedImport
from sys import maxint
import copy

class ProductMatcher():
    
    def __init__(self, customer_names, product_names, logger = None):        
        self._products = [names.Product(name) for name in product_names]
        self._customers = [names.Customer(name) for name in customer_names]
        
        self._size = max(len(customer_names),len(product_names))
        
        self._row_covered = [False for i in range(self._size)]
        self._col_covered = [False for i in range(self._size)]
        self._starred     = [[False for j in range(self._size)] for i in range(self._size)]
        self._primed      = [[False for j in range(self._size)] for i in range(self._size)]

        self._z_row       = -1
        self._z_col       = -1
        self._logger = logger
        
        
    ###############################################
    # PUBLIC INSTANCE METHODS
    ###############################################
    
    def match_products(self):
        """Computes the most suitable product matching
        
        Returns the matching as a list of length equal to the number of customers
        -1 represents a customer that is not matched with any products
        Any other element represents the index of the matched product
        
        For example, [0,-1,1] means the first customer is matched with the first 
        product, the second customer is not matched, the third customer is matched
        with the second product
        """
        
        self._setup_matcher()
        
        # Run the algorithm until a solution is found
        self._log(True,"run_matcher")
        # cover controls whether "_cover_columns" is called during each iteration
        cover = True 
        done = False
        while not done:                            
            if cover and self._cover_columns():
                done = True
            else:
                if(self._prime_zeroes()):
                    self._adjust_matrix()
                    cover = False
                else:
                    self._construct_path()
                    cover = True
         
        self._log(False,"run_matcher")
        
        # Read the solution from the matrix           
        results = []
        
        for row in self._starred[:self._height]:
            try:
                results.append(row[:self._width].index(True))
            except ValueError:
                results.append(-1)
        
        return results
    
    def match_suitability(self, matches):
        """Determines the total suitability of a given matching"""
        
        if not hasattr(self, "_suitability"):
            self._setup_matcher()
        
        total = 0
        for row, col in enumerate(matches):
            if(col != -1):
                total += self._suitability[row][col]
            
        return total
    
    def suitability_matrix(self):
        """Returns a matrix of suitability scores between customers and products"""
        matrix = []
        for customer in self._customers:
            row = []
            for product in self._products:
                row.append(customer.get_suitability(product))
            matrix.append(row)
            
        return matrix

    def get_matrix(self):
        return self._matrix
    
    
    ###############################################
    # HUNGARIAN ALGORITHM STEPS
    ###############################################
    
    def _setup_matcher(self):
        """
        1. Computes the suitability matrix, 
        2. Converts it to an n x n minimum assignment problem
        3. Starts the Hungarian algorith by subtracting the smallest value from each row 
        and starring zeros 
        """
        
        self._suitability = self.suitability_matrix()
        self._height = len(self._suitability)
        self._width = len(self._suitability[0])
        
        # Store the original suitability matrix for computing match suitability later
        self._matrix = copy.deepcopy(self._suitability)
        
        matrix_functions.augment_matrix(self._matrix)   
        matrix_functions.min_matrix(self._matrix)   
        matrix_functions.subtract_row_min(self._matrix)
        #matrix_functions.subtract_col_min(suitability)
        
        self._star_zeroes()
    
    def _star_zeroes(self):
        """
        Traverse the matrix and star any zero that does
        not have a starred zero in its row or column
        """
        for i in range(self._size):
            for j in range(self._size):
                if(self._matrix[i][j] == 0 and not self._covered(i,j)):
                    self._starred[i][j]  = True
                    self._col_covered[j] = True
                    self._row_covered[i] = True
                
        self._uncover_all()
    
    def _cover_columns(self):
        """Cover any column that contains a starred zero"""
        self._log(True,"cover_columns")
        for i in range(self._size):
            for j in range(self._size):
                if(self._starred[i][j]):
                    self._col_covered[j] = True
                 
        # If we have _covered every column, a solution has been found
        if sum(self._col_covered) >= self._size:
            self._log(False,"cover_columns")
            return True 
        else:
            self._log(False,"cover_columns")
            return False
     
    
    def _prime_zeroes(self):
        """Finds the minimum number of lines required to cover all zeroes
        or identifies a potential for an alternative starring
        
        1. Prime an uncovered zero
        2. If no uncovered zero is found, break and construct_path (return True)
        3. If there is a starred zero in the row of the primed zero,
           cover this row, uncover this column otherwise, break and adjust matrix (return False)
        4. Repeat
        
        """
        
        self._log(True,"prime_zeroes")
        while True: # Loop is broken by function returns
            (z_row, z_col) = self._uncovered_zero()
            
            if(z_row < 0):
                self._log(False,"prime_zeroes")
                return True
            else:
                self._primed[z_row][z_col] = True
                       
                star_col = self._starred_column(z_row)
                
                if star_col > -1:
                    self._row_covered[z_row] = True
                    self._col_covered[star_col] = False
                else:
                    self._z_row = z_row
                    self._z_col = z_col
                    self._log(False,"prime_zeroes")
                    return False
        
    
    def _construct_path(self): 
        """ Find and operate on a series of alternating primed and starred zeros
        
        1. Find the series
            A. Start with the uncovered primed zero from prime_zeroes
            B. Add any starred zero in the column of zero from step 1
            C. Add the primed zero in the row of the zero from step 2 (always will exist)
            D. Repeat until no zero is found in step 2
        2. Unstar each primed zero, prime each starred zero within the series
        3. Erase all primes and uncover the matrix
        
        """
          
        self._log(True,"construct_path")
        
        count = 0
        path = []
        path.append([self._z_row, self._z_col])
        
        done = False
        while not done:
            # Find a starred zero in the column of the last element in the path
            row = self._starred_row(path[count][1])
            
            if row >= 0:
                # Store the starred zero
                path.append([row, path[count][1]])
                count += 1
                
                # Find and store a primed zero
                col = self._primed_column(row)
                path.append([row, col])
                count += 1
                
            else:
                done = True
        
        # Unstar each starred and star each primed zero
        for item in path:
            if self._starred[item[0]][item[1]]:
                self._starred[item[0]][item[1]] = False
            else:
                self._starred[item[0]][item[1]] = True
                self._primed[item[0]][item[1]] = False
        
        self._uncover_all()
        self._unprime_all()
        
        self._log(False,"construct_path")
        
    
    def _adjust_matrix(self):
        """Adjust the matrix to find the second minimum cost among conflicting rows
        
        1. Find the smallest uncovered value in the matrix
        2. Add the smallest value to each covered row
        3. Subtract the smallest value from each uncovered column  
        
        """
        
        self._log(True,"adjust_matrix")
        
        min_v = maxint
        
        for i in range(self._size):
            if(not self._row_covered[i]):
                for j,covered in enumerate(self._col_covered):
                    if(not covered):
                        min_v = min(min_v,self._matrix[i][j])   
        
                
        for i in range(self._size):
            for j in range(self._size):
                if self._row_covered[i]:
                    self._matrix[i][j] += min_v
                if not self._col_covered[j]:
                    self._matrix[i][j] -= min_v 
                    
        self._log(False,"adjust_matrix")
        
    ###############################################
    # HELPER METHODS
    ###############################################
       
    def _starred_column(self,row):
        """Find the column of any starred zero in the row"""
        for j in range(0,self._size):
            if(self._starred[row][j]):
                return j
        return -1

    def _starred_row(self,col):
        """Find the row of any starred zero in the column"""
        for i in range(0,self._size):
            if(self._starred[i][col]):
                return i
            
        return -1
    
    def _primed_column(self, row):
        """Find the column of any primed zero in the row"""
        for j in range(0,self._size):
            if(self._primed[row][j]):
                return j
        return -1
    
    def _uncovered_zero(self):
        """Find the first uncovered zero in the matrix"""
        for i in range(0,self._size):
            for j in range(0,self._size):
                if(self._matrix[i][j] == 0 and not self._covered(i,j)):
                    return (i,j)
        
        return (-1, -1)
    
    
    def _uncover_all(self):
        for i in range(self._size):
            self._row_covered[i] = False
            self._col_covered[i] = False
            
    def _unprime_all(self):
        for i in range(0,self._size):
            for j in range(0,self._size):
                self._primed[i][j] = False
        
    def _covered(self, row, col):
        return self._row_covered[row] or self._col_covered[col]
    
    def _log(self, input, function_name):
        if(self._logger != None):
            self._logger.log(input,function_name,self)