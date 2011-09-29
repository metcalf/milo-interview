#!/usr/bin/env python2.6
'''Provides a series of static functions to operate on matrices (2d lists)

IMPORTANT NOTE: All functions perform matrix operations IN PLACE wherever possible

Created on May 4, 2010
@author: Andrew Metcalf
'''

def subtract_row_min(matrix):
    """Subtracts the minimum value of each row of a matrix from that row"""
    for row in matrix:
        low = min(row)
        for i, value in enumerate(row):
            row[i] = value-low
    
    return matrix
    
def augment_matrix(matrix):
    """Augments the given matrix with zero-filled rows or columns to make it square"""
    cols = len(matrix[0])
    rows = len(matrix)
    
    if(rows == cols):
        return matrix
    elif(cols > rows): 
        # Augemnt with new rows
        for i in range(0,cols-rows):
            matrix.append(create_row(cols))
    else:
        # Augment with columns
        for row in matrix:
            for i in range(0,rows-cols):
                row.append(0)
    
    return matrix
 
def create_row(length,value=0):     
    return [value for i in range(length)]

def min_matrix(matrix):
    """Replaces each element in the matrix with max(matrix)-element"""
    high = max(max(matrix))
    
    for row in matrix:
        for i, value in enumerate(row):
            row[i] = high-value
    
    return matrix