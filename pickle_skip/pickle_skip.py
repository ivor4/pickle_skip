# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 18:33:49 2023

@author: Jaime Bonache < http://www.github.com/ivor4/pickle_skip > < jaime.bonache.iv4@gmail.com >
"""

import numpy as np


class PickleSkipper:
    def __init__(self, target: object, max_recurs: int = 64, verbose:bool = True, trace:bool = False, max_array_size: int = 64)->None:
        self.target = target
        self.max_recurs = max_recurs
        self.verbose = verbose
        self.trace = trace
        self.max_array_size = max_array_size
        
    @classmethod
    def _get_value_dict(cls, target:object, prop:str)->object:
        return target[prop]
    
    @classmethod
    def _get_value_inst(cls, target:object, prop:str)->object:
        return target.__dict__[prop]
    
    def GetGetterFunction(self, target)->(callable,enumerate):
        getFunc = None
        getEnumerate = None
        isInstance = False
        isDict = False
        
        try:
            if(isinstance(target,dict)):
                getEnumerate = target.keys()
                getFunc = PickleSkipper._get_value_dict
                isDict = True
        except:
            pass


        try:
            getEnumerate = target.__dict__.keys()
            getFunc = PickleSkipper._get_value_inst
            isInstance = True
        except:
            pass
        
        if(not isInstance and not isDict):
            #Treated as a final value
            pass
            
        return getFunc,getEnumerate
    
    
    
    def _recursive_trial_and_error(self, target:object, concat_attr:str, n_iter:int)->object:
        if(self.trace):
            print(concat_attr)
            
        if(n_iter >= self.max_recurs):
            #setattr(retVal, 'value', 'PICKLE-SKIP-RECURS-MAX')
            retVal = 'PICKLE-SKIP-RECURS-MAX'
        else:
            getfunc, getEnumerate = self.GetGetterFunction(target)

            
            #If object has attributes, it will need to be iterated again
            if(getfunc != None):
                retVal = {}
                for next_prop in getEnumerate:
                    if(not isinstance(next_prop, str)):
                        if(self.verbose):
                            print('Cannot understand property: '+concat_attr+'.'+str(next_prop))
                        continue
                    elif(next_prop.startswith('__')):
                        #Avoid inner attributes as they may loop into themselves
                        retVal[next_prop] = str(target)
                        continue
                    
                    try:
                        next_target = getfunc(target, next_prop)
                    except:
                        if(self.verbose):
                            print('Error reading attr: '+concat_attr+'.'+next_prop)
                        retVal[next_prop] = str(target)
                        continue
                    
                    if(next_target is self):
                        #Avoid self, if it was included in target object, this would lead into an endless loop
                        #until max_recurs
                        continue
                    innerRetVal = self._recursive_trial_and_error(next_target,concat_attr+'.'+next_prop, n_iter+1)
                    retVal[next_prop] = innerRetVal

                        
            #If value has no attributes, then is a final value, if it is known type, get directly, otehrwise, string
            else:
                if(isinstance(target, list) or (isinstance(target, tuple))):
                    if(len(target) <= self.max_array_size):
                        retVal = []
                        for i in range(len(target)):
                            retVal.append(self._recursive_trial_and_error(target[i],concat_attr+'['+str(i)+']', n_iter+1))
                    else:
                        retVal = str(target)
                elif(isinstance(target, np.ndarray)):
                    excess_array = False
                    shape = target.shape
                    for i in shape:
                        if(i > self.max_array_size):
                            excess_array = True
                            break
                    if(excess_array):
                        retVal = str(target)
                    else:
                        retVal = target
                elif(isinstance(target, bool)):
                    retVal = target
                elif(isinstance(target, int)):
                    retVal = target
                elif(isinstance(target, float)):
                    retVal = target
                elif(target is None):
                    retVal = target
                else:
                    retVal = str(target)
        return retVal
            
        
    
    def Update(self)->dict:
        #Start from iteration 0
        retVal = self._recursive_trial_and_error(self.target, '',0) 
        return retVal

