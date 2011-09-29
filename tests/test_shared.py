#!/usr/bin/env python2.6
'''Tests the main module of the product matcher

NOTE: These tests can generate large files the take a long time to complete
      They probably should not be included in a regular test run

Created on May 9, 2010
@author: Andrew Metcalf
'''
import unittest
from time import clock
import main #@UnresolvedImport
import random
from tests import file_generate

CASE_PATH= "./cases/"

class TestShared(unittest.TestCase):

    def test_large_file(self):
        names = self._get_names("large")
        
        start = clock()
        print "Starting long file test... "
        
        resultI = main.run_imperative(*names)
        
        print "imperative run time(s): " + str(clock()-start)
        start = clock()
        
        resultF = main.run_functional(*names)
        self.assertEqual(resultI,resultF)
        print "functional run time(s): " + str(clock()-start)
        
    def test_many_files(self):
        NUM_TESTS = 100
        TEST_LENGTH = 20
        total_time = 0
        for i in range(NUM_TESTS):
            num_customers = int(random.uniform(TEST_LENGTH/2,TEST_LENGTH+1))
            num_products = int(random.uniform(TEST_LENGTH/2,TEST_LENGTH+1))
            file_generate.write_files(num_customers, num_products, "multi",CASE_PATH)
            
            names = self._get_names("multi")
            
            start = clock()
            print "Starting long file test (multi)... "
            #print len(customer_names)
            #print len(product_names)
            
            resultI = main.run_imperative(*names)
            
            print "imperative run time(s): " + str(clock()-start)
            total_time += (clock()-start)
            start = clock()
            
            resultF = main.run_functional(*names)
            self.assertEqual(resultI,resultF)
            total_time += (clock()-start)
            print "functional run time(s): " + str(clock()-start)
            
            
            start = clock()
        
        print "average time: " + str(total_time/NUM_TESTS)
        
        
    def _get_names(self,append):
        customer_file = open(CASE_PATH+'customers-'+append+'.txt')
        product_file  = open(CASE_PATH+'products-'+append+'.txt')
        
        customer_names = customer_file.read().replace('\r',"").split('\n')
        product_names  = product_file.read().replace('\r',"").split('\n')
        
        customer_file.close()
        product_file.close() 
        
        return (customer_names, product_names)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()