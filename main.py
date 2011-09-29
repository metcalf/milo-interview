'''
Created on May 2, 2010

@author: Andrew Metcalf
'''
import sys

print sys.argv[0]
sys.path.append(sys.argv[0])

from milo_imperative import product_matcher as imperative_matcher
from milo_functional import product_matcher as functional_matcher

def print_help():
    print "python main.py [mode] <customer_file> <products_file>"
    print ""
    print "Modes (defaults to imperative):"
    print "    functional    Run using the functional version of the program"
    print "    imperative    Run using the imperative version of the program"
    print ""
    print "Example: python main.py imperative cust prod"

def run_imperative(customer_names, product_names):
    matcher = imperative_matcher.ProductMatcher(customer_names, product_names)
    pairs = matcher.match_products()
    suitability = matcher.match_suitability(pairs)
    
    return [pairs, suitability]
    
def run_functional(customer_names, product_names):
    return functional_matcher.matched_solution(customer_names, product_names)

def print_result(pairs, suitability,customer_names, product_names):
    for cust, prod in enumerate(pairs):
        if(prod != -1):
            print customer_names[cust] + " => " + product_names[prod]
        else:
            print customer_names[cust] + " does not receive an offer"
    
    print ""
    print "Total suitability: " + str(suitability)

def main(args):
    if(len(args) < 3 or args[1] in ["--help", "-h", "help"]):
        print_help()
    else:
        try:
            product_names  = open(args.pop()).read().replace("\r","").split('\n')
            customer_names = open(args.pop()).read().replace("\r","").split('\n')
            
        except:
            print_help()
            return 0
        
        if(len(args) < 2 or args[1] == "imperative"):
            result = run_imperative(customer_names, product_names)
        else:
            result = run_functional(customer_names, product_names)

        print_result(result[0], result[1],customer_names, product_names)

if __name__ == "__main__":
    main(sys.argv)
