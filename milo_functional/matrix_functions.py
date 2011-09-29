#!/usr/bin/env python2.6
'''Provides a series of static functions to operate on matrices (2d lists)

Created on May 4, 2010
@author: Andrew Metcalf
'''

def subtract_row_min(matrix): 
    """Subtracts the minimum value of each row of a matrix from that row"""
    return map(subtract_min_from_row, matrix)
    

def subtract_min_from_row(row): 
    return map(lambda item: item - min(row), row)
    
    
def augment_matrix(matrix): 
    """Augments the given matrix with zero-filled rows or columns to make it square"""
    return (len(matrix[0]) == len(matrix) and matrix) or do_augment(matrix)
 
def do_augment(matrix): 
    return (len(matrix[0]) < len(matrix) and augment_matrix(add_col(matrix)))\
            or augment_matrix(add_row(matrix))
 
def add_row(matrix): 
    return matrix+[create_row(len(matrix[0]))]

def add_col(matrix): 
    return map(lambda row: row+[0], matrix)


def create_row(elements, value = 0, row = []): 
    return(elements == 0 and row) or create_row(elements-1,value, row+[value])
 
 
def min_matrix(matrix): 
    """Replaces each element in the matrix with max(matrix)-element"""
    return map(lambda row: map(lambda item: max(max(matrix))-item,row), matrix)
