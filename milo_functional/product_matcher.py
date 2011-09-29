#!/usr/bin/env python2.6

'''Implements product-customer matching functionally

For a list of customer names and product names, ProductMatcher
computes the maximum suitability assignment of customers to products
based on the suitabilty algorithm defined by the Customer object.

It uses the Hungarian/Munkres algorithm to solve the assignment problem.
Implementation of the Hungarian algorithm based on:
http://en.wikipedia.org/wiki/Hungarian_algorithm
http://github.com/bmc/munkres/blob/master/munkres.py

Usage: Call matched_solution with a list of customer_names and product_names

Note on structure: To make the functional implementation clearer, helper functions
that are only called by one other function are grouped under that function.
Helpers that are called by multiple functions are at the bottom of the file

Created on May 2, 2010
@author: Andrew Metcalf
'''

import names #@UnresolvedImport
import matrix_functions #@UnresolvedImport
from sys import maxint
     
###############################################
# PUBLIC INSTANCE METHODS
###############################################

count = 0

def matched_solution(customer_names,product_names):
    """Finds and returns the optimal assignment and total match suitability
    
    Returns is of the form [assignment, suitability] where assignment is a 
    list of length equal to the number of customers in which:
        -1 represents a customer that is not matched with any products
        Any other element represents the index of the matched product
    """
    return build_solution(suitability_matrix(customer_names,product_names))
    
def build_solution(suitability):
    return solution_with_suitability(match_products(suitability),suitability)

def solution_with_suitability(solution,suitability):
    return [solution, match_suitability(solution,suitability)]

def match_suitability(result, suitability):
    """Determines the total suitability of a given matching"""
    return sum(map(\
            lambda index, row: (index > -1 and row[index]) or 0,\
            result,suitability))

def run_matcher(suitability):
    """Run the hungarian algorithm on the given suitability matrix"""
    return next_iteration(cover_columns(setup_matrix(suitability)))

def next_iteration(result):
    return (len(result) == 1 and result[0]) or \
            next_iteration(prime_zeroes(*result))

def match_products(suitability):
    """Determine the optimal matching of customer to products given a suitability matrix
    Return is in the form specified for matched_solution
    """
    return read_result(run_matcher(suitability),len(suitability),len(suitability[0]))
    
def read_result(matrix,height,width):
    """Determine the optimal matching of customer to products given a completed hungarian matrix
    Return is in the form specified for matched_solution
    """
    return map(lambda index: find_row_result(matrix[index],width),range(height))
    
def find_row_result(row,width):
    try:
        return row[:width].index([0,1])
    except:
        return -1

def setup_matrix(suitability):
    """
    1. Computes the suitability matrix, 
    2. Converts it to an n x n minimum assignment problem
    3. Starts the Hungarian algorith by subtracting the smallest value from each row 
    and starring zeros 
    """
    return star_zeroes( \
                matrix_functions.subtract_row_min( \
                    matrix_functions.min_matrix( \
                        matrix_functions.augment_matrix( \
                            suitability))))

def suitability_matrix(customer_names, product_names):
    """Returns a matrix of suitability scores between customers and products"""
    return map(lambda customer_name: suitability_row(customer_name, product_names), \
               customer_names)


def suitability_row(customer_name, product_names):
    return map(lambda product_name: names.get_suitability(customer_name,product_name), \
               product_names)

###############################################
# HUNGARIAN ALGORITHM STEPS
###############################################

############## STAR ZEROES FUNCTIONS ##############
def star_zeroes(matrix):
    """
    Traverse the matrix and star any zero that does not have a starred zero in its row or column
    Returns the new matrix
    """
    return star_row_zeroes(iter(matrix))
    
def star_row_zeroes(row_iter, input = [[],[]]):
    try:
        return star_row_zeroes(row_iter, star_curr_row(row_iter.next(), input))
    except StopIteration:
        return input[1]

def star_curr_row(row, input, pos = 0):
    return (pos >= len(row) and [input[0], input[1]+[create_unstared_row(row)]]) or \
            ((pos in input[0] or row[pos] != 0) and star_curr_row(row, input, pos+1)) or \
            [input[0]+[pos], input[1]+[create_stared_row(row, pos)]]            

def create_unstared_row(row):
    return map(lambda item: [item, 0], row)

def create_stared_row(row, pos):
    return map(lambda item: [item, 0], \
               row[:pos])+[[row[pos],1]]+map(lambda item: [item, 0], row[pos+1:])

############## COVER COLUMNS FUNCTIONS ##############
def cover_columns(matrix):
    """Cover any column that contains a starred zero"""
    return check_done(matrix,\
            reduce(lambda prev, curr: map(lambda x,y: x or y,prev, curr),\
            get_marks(matrix, 1)))
 
def check_done(matrix, covered_columns):
    """Determine whether a solution has been found,
    If so, return [matrix] otherwise, return [matrix,covered)rows,covered_cols]
    """
    return (covered_columns.count(True) == len(matrix) and [matrix]) or \
            [matrix,get_false_row(len(matrix)),covered_columns]
   
def get_marks(matrix, mark):
    return map(lambda row: get_row_marks(row,mark), matrix)

def get_false_row(elements):
    return matrix_functions.create_row((elements),False) 

############## PRIME ZEROES FUNCTIONS ##############
def prime_zeroes(matrix, covered_rows, covered_cols):
    """Finds the minimum number of lines required to cover all zeroes
    or identifies a potential for an alternative starring
    
    1. Prime an uncovered zero
    2. If no uncovered zero is found, construct_path
    3. If there is a starred zero in the row of the primed zero,
       cover this row, uncover this column otherwise, adjust matrix
    4. Repeat
    
    """
    return prime_uncovered(matrix,covered_rows, covered_cols, \
                         uncovered_zero(matrix,covered_rows,covered_cols))
    
def prime_uncovered(matrix, covered_rows, covered_cols, uncovered):
    return (uncovered == (-1,-1) and adjust_matrix(matrix, covered_rows, covered_cols)) or \
             get_starred(set_mark(matrix,uncovered[0],uncovered[1],2),\
                         covered_rows, covered_cols, uncovered)
   

def get_starred(matrix, covered_rows, covered_cols, uncovered):
    return cover_star(matrix, covered_rows, covered_cols, \
                      (uncovered[0],starred_position(matrix[uncovered[0]])),uncovered)
        
def cover_star(matrix, covered_rows, covered_cols, starred, uncovered):
    return (starred[1] != -1 and \
        prime_zeroes(matrix, set_value(covered_rows, starred[0],True),\
                     set_value(covered_cols, starred[1], False))) or \
        construct_path(matrix,uncovered)

def set_value(items, index, value):
    return map(lambda item, i: (i == index and value) or (item and i != index), \
               items,range(len(items)))

def uncovered_zero(matrix, covered_rows, covered_cols, row = 0):
    """Find the first uncovered zero in the matrix"""
    return (not covered_rows[row] and uncovered_zero_row(matrix[row], covered_cols, row)) or \
            (row+1 < len(matrix) and uncovered_zero(matrix,covered_rows, covered_cols, row+1)) or \
            (-1,-1)
    
def uncovered_zero_row(row, covered_cols, row_num, col = 0):
    return (not covered_cols[col] and row[col][0] == 0 and (row_num, col)) or \
            (col+1 < len(row) and uncovered_zero_row(row,covered_cols,row_num, col+1))

############## CONSTRUCT PATH FUNCTIONS ##############
def construct_path(matrix, primed):
    """ Find and operate on a series of alternating primed and starred zeros
    
    1. Find the series
        A. Start with the uncovered primed zero from prime_zeroes
        B. Add any starred zero in the column of zero from step 1
        C. Add the primed zero in the row of the zero from step 2 (always will exist)
        D. Repeat until no zero is found in step 2
    2. Unstar each primed zero, prime each starred zero within the series
    3. Erase all primes and uncover the matrix
    4. Return to cover_columns
    
    """    
    return cover_columns(unprime_all(apply_path(*add_primed(matrix,primed,[]))))

def find_starred(matrix,last,path):
    return add_starred(matrix,[starred_position(extract_col(matrix,last[1])),last[1]],path)

def extract_col(matrix, col):
    """Return a list representing all of the elements in the given column"""
    return map(lambda row: row[col],matrix)

def add_starred(matrix,starred,path):
    return (starred[0] == -1 and [matrix,path]) or \
            find_primed(matrix,starred,path+[starred])

def find_primed(matrix,last,path):
    return add_primed(matrix,[last[0],primed_position(matrix[last[0]])],path)

def add_primed(matrix,primed,path):
    return find_starred(matrix,primed,path+[primed])

def apply_path(matrix, path):
    return reduce(lambda mat,item: (mat[item[0]][item[1]][1] == 1  and \
                                    set_mark(mat,item[0],item[1],0)) or \
                  set_mark(mat,item[0],item[1],1),path,matrix)

def unprime_all(matrix):
    return map(unprime_row,matrix)

def unprime_row(row):
    return map(lambda item: item[1] == 2 and [item[0],0] or item,row)  

############## ADJUST MATRIX FUNCTIONS ##############
def adjust_matrix(matrix, covered_rows, covered_cols):
    """Adjust the matrix to find the second minimum cost among conflicting rows
        
        1. Find the smallest uncovered value in the matrix
        2. Add the smallest value to each covered row
        3. Subtract the smallest value from each uncovered column  
        4. Prime zeroes
        """
    return prime_zeroes( \
            do_adjust_matrix(matrix, covered_rows, covered_cols,\
                             min_uncovered(matrix, covered_rows, covered_cols)),\
                        covered_rows, covered_cols)
    
def do_adjust_matrix(matrix,covered_rows, covered_cols, min_val):
    return map(lambda row, index: do_adjust_row(\
                ((covered_rows[index] and map(lambda item: [item[0] + min_val,item[1]], row)) or row),\
                covered_cols,min_val),\
                matrix,range(len(matrix)))
    
def do_adjust_row(row,covered_cols,min_val):
    return map(lambda item, index: (covered_cols[index] and item) or \
               [item[0]-min_val,item[1]],row, range(len(row)))

def min_uncovered(matrix, covered_rows, covered_cols):
    """Find the minimum uncovered element 
    (create a matrix with all covered rows set to maxint and find the minimum value)
    """
    return min(map(row_min,set_covered(matrix, covered_rows, covered_cols, maxint)))

def row_min(row):
    return min(map(lambda item: item[0],row))

def set_covered(matrix, covered_rows, covered_cols, value):
    """
    Return a matrix with all covered elements set to value
    NOTE: This new element is always unstarred
    """
    return map(lambda row, index: (covered_rows[index] and matrix_functions.create_row(len(row),[value,0]))\
               or row_set_covered(row, covered_cols, value)\
               ,matrix,range(len(matrix)))
    
def row_set_covered(row, covered_cols, value):
    return map(lambda item, index: (covered_cols[index] and [value,0]) or \
               item,row, range(len(row)))


###############################################
# HELPER METHODS
###############################################

def set_mark(matrix,row,col,mark):
    """Return a new matrix with the mark in row, col set to mark"""
    return map(lambda list,index: (index == row and set_row_mark(list,col,mark)) or list \
               ,matrix,range(len(matrix)))

def set_row_mark(list,col,mark):
    return map(lambda item, index: (index == col and [item[0],mark]) or \
                                    (index != col and item),\
               list,range(len(list)))

def starred_position(list):
    """Find the index of any starred zero in the list"""
    return marked_positions(list, 1)

def primed_position(list):
    """Find the index of any primed zero in the list"""
    return marked_positions(list, 2)

def marked_positions(list, mark):
    """Find the index of any elements in the list with the specified mark"""
    try:
        return get_row_marks(list, mark).index(True)
    except:
        return -1
    
def get_row_marks(row, mark):
    """Return a list representing the mark elements from the row"""
    return map(lambda item: item[1] == mark,row)