#!/usr/bin/env python2.6
'''Functions for determining the suitability of a product for a customer
Created on May 2, 2010

@author: Andrew Metcalf
'''

from fractions import gcd

VOWELS = ['a','e','i','o','u']
CONSONANTS = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
    
def get_suitability(customer, product):
    """Determines the suitability of a product for the customer
        
    * If the length of the product name is even, the base suitability score (SS)
     is the number of vowels in the customer's name multiplied by 1.5.   
    * If the length of the product name is odd, the base SS is the number of 
    consonants in the customer's name multiplied by 1.   
    * If the length of the product name shares any common factors (besides 1) with the 
    length of the customer's name, the SS is increased by 50% above the base SS.  
    
    Args: A customer name and a product name
    
    Returns: A suitability score (float)
    """
    return ((len(product) % 2 == 0 and 1.5*count_letters(customer, VOWELS)) \
            or (len(product) % 2 != 0 and count_letters(customer,CONSONANTS))) * \
            (((has_common_factor(len(customer), len(product)) and 1.5)) or 1)


def count_letters(word,letters): 
    return reduce(lambda curr,letter: curr + word.lower().count(letter), \
                  letters, 0)

def has_common_factor(num1, num2):
    return gcd(num1, num2) > 1