#!/usr/bin/env python2.6
'''Logs the state of the imperative hungarian algorithm for use in test cases

Usage: 
Instantiate with the directory where the log files should be stored
Call log to record the matcher state
Call write to output all logged values to file

Created on May 8, 2010
@author: Andrew Metcalf
'''

import pickle
import copy

class Logger(object):
    
    def __init__(self,log_path):
        self._inputs = {}
        self._outputs = {}
        self._log_path = log_path
    
    def log(self,input,function_name,matcher):
        """Record the matcher state
        
        Args:
            input: boolean specifying whether this is the input or output of a function
            function_name: name of the calling function 
            matcher: the matcher object
        """
        
        if input:
            record = self._inputs
        else:
            record = self._outputs
        
        if not record.has_key(function_name):
            record[function_name] = []
        
        record[function_name].append(self._get_state(matcher))
    
    def write(self):
        for name,data in self._inputs.iteritems():
            pickle.dump(data, self._get_file(True,name))
            
        for name,data in self._outputs.iteritems():
            pickle.dump(data, self._get_file(False,name))    
    
    def _get_file(self,input, function_name):
        if input:
            mod = "input"
        else:
            mod = "output"
            
        return open(self._log_path+mod+"_"+function_name+".log","w")
            
    
    def _get_state(self, matcher):
        new_matrix = []
        
        for row,star_row,prime_row in zip(matcher.get_matrix(),matcher._starred,matcher._primed):
            new_row = []
            for item,star,prime in zip(row,star_row,prime_row):
                if(star):
                    mark = 1
                elif(prime):
                    mark = 2
                else:
                    mark = 0
                new_row.append([item,mark])
                
            new_matrix.append(new_row)   
        
        return [new_matrix,copy.deepcopy(matcher._row_covered), copy.deepcopy(matcher._col_covered),[matcher._z_row, matcher._z_col],[matcher._products,matcher._customers]]