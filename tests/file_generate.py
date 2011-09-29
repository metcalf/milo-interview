#!/usr/bin/env python2.6
'''Generates test files for the product matchers

Usage: Call write files
    

Created on May 4, 2010

@author: Andrew Metcalf
'''

import random
import string

def write_files(products, customers, append,case_path):
    """Generates random test files
    
    Args:
        products: number of products
        customers: number of customers
        append: descriptive string to append to the file name
        case_path: directory where the file should be created
    """
    
    MAX_LENGTH = 25
    
    customer_file  = open(case_path+'customers-'+append+'.txt', 'w')
    product_file   = open(case_path+'products-'+append+'.txt', 'w')
    
    lines = []
    for i in range(customers):
        lines.append(gen_random_string(MAX_LENGTH))
        
    customer_file.write("\n".join(lines)) 
    
    lines = []    
    for i in range(products):
        lines.append(gen_random_string(MAX_LENGTH))
        
    product_file.write("\n".join(lines))   
        
    customer_file.close()
    product_file.close() 

def gen_random_string(max_length):
    line = ""
    chars = string.letters + string.digits + ' -'
    for i in range(int(random.uniform(1, max_length))):
        line = line + str(random.sample(chars,1)[0])
        
    return line
  
#write_files(150,150,"large","./cases/")