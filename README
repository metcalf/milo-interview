# Milo Interview

Written: May 2010

This package provides two implementations (functional and imperative) of a program 
for assigngin a list of products to a list of customers to maximize the suitability 
of the products for the customers.

Suitability is computed as follows:
	* If the length of the product name is even, the base suitability score (SS)
	 is the number of vowels in the customer's name multiplied by 1.5.   
	* If the length of the product name is odd, the base SS is the number of 
	consonants in the customer's name multiplied by 1.   
	* If the length of the product name shares any common factors (besides 1) with the 
	length of the customer's name, the SS is increased by 50% above the base SS.  
        
The Hungarian/Munkres algorithm is used to solve the assignment problem.
Implementation of the Hungarian algorithm based on:
http://en.wikipedia.org/wiki/Hungarian_algorithm
http://github.com/bmc/munkres/blob/master/munkres.py

USAGE:
python main.py [mode] <customer_file> <products_file>

Modes (defaults to imperative):
    functional    Run using the functional version of the program
    imperative    Run using the imperative version of the program
	
Example: python main.py imperative cust.dat prod.dat