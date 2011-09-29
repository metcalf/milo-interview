#!/usr/bin/env python2.6
'''Classes that represent customers and products for product matcher

Defines a set of classes representing customers and products for 
use in the product matcher.  Classes define the functions necessary
to compute a suitability score between a product and a customer.

Created on May 2, 2010
@author: Andrew Metcalf

'''

class Name(object):
    """Base classs for product and customer names
    
    Defines logic for determining greatest common factors
    """
    
    def __init__(self, name):
        self._name = name
        self._factors = self._find_factors(len(name))
        
    def _find_factors(self, number):
        factors = set()
        for i in range(2,number+1):
            if(number % i == 0):
                factors.add(i)
        
        return factors
    
    def get_factors(self):
        return self._factors
    
    def has_common_factor(self,factors):
        return not set(factors).isdisjoint(self._factors)

class Product(Name): 
    """Represents a product name"""   
    def is_even(self):
        return (len(self._name) % 2) == 0

class Customer(Name):
    """Represents a customer name
    
    Provides functions for determining the suitability of a product for the customer
    """
    
    VOWELS = ['a','e','i','o','u']
    CONSONANTS = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
    

    def __init__(self, name):
        Name.__init__(self,name)
        
        self._vowels = self._count_letters(name, self.VOWELS)
        self._consonants = self._count_letters(name, self.CONSONANTS)

    def get_suitability(self, product):
        """Determines the suitability of a product for the customer
        
        * If the length of the product name is even, the base suitability score (SS)
         is the number of vowels in the customer's name multiplied by 1.5.   
        * If the length of the product name is odd, the base SS is the number of 
        consonants in the customer's name multiplied by 1.   
        * If the length of the product name shares any common factors (besides 1) with the 
        length of the customer's name, the SS is increased by 50% above the base SS.  
        
        Args: A Product object
        
        Returns: A suitability score (float)
        """
        
        if product.is_even():
            score = self._vowels * 1.5
        else:
            score = self._consonants
        
        if self.has_common_factor(product.get_factors()):
            score *= 1.5 
        
        return score

    def _count_letters(self,name, letters):
        low_name = name.lower()
        count = 0
        
        for letter in letters:
            count = count + low_name.count(letter)
        
        return count
