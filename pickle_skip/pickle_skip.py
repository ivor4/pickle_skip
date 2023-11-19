# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 18:33:49 2023

@author: Jaime Bonache < http://www.github.com/ivor4/pickle_skip > < jaime.bonache.iv4@gmail.com >
"""

import cloudpickle

class ContainerObject:
    pass

class PickleSkipper:
    def __init__(self, target: object, max_recurs: int = 64)->None:
        self.target = target
        self.max_recurs = max_recurs
        
    @classmethod
    def _get_value_dict(cls, target:object, prop:str)->object:
        return target[prop]
    
    @classmethod
    def _get_value_inst(cls, target:object, prop:str)->object:
        return getattr(target, prop)
    
    def GetGetterFunction(self, target)->(callable,enumerate):
        getfunc = None
        getEnumerate = None
        isInstance = False
        isDict = False
        
        try:
            getEnumerate = target.keys()
            getfunc = PickleSkipper._get_value_dict
            isDict = True
        except Exception:
            pass
        
        if(not isDict):
            try:
                getEnumerate = vars(target).keys()
                getfunc = PickleSkipper._get_value_inst
                isInstance = True
            except Exception:
                pass
        
        if(not isInstance and not isDict):
            #Treated as a final value
            pass
            
        return getfunc,getEnumerate
    
    
    
    def _recursive_trial_and_error(self, target:object, n_iter:int)->ContainerObject:
        retVal = ContainerObject()
        print(n_iter)
        print(target)
        
        if(n_iter >= self.max_recurs):
            setattr(retVal, 'value', 'PICKLE-SKIP-RECURS-MAX')
        else:
            getfunc, getEnumerate = self.GetGetterFunction(target)
            
            #If object has attributes, it will need to be iterated again
            if(getfunc != None):
                for next_prop in getEnumerate:
                    print(next_prop)
                    next_target = getfunc(target, next_prop)
                    
                    fail = False
                    try:
                        _ = cloudpickle.dumps(next_target, protocol = cloudpickle.DEFAULT_PROTOCOL)
                    except:
                        fail = True
                    
                    if(fail):
                        innerRetVal = self._recursive_trial_and_error(next_target, n_iter+1)
                        setattr(retVal, next_prop, innerRetVal)
                    else:
                        setattr(retVal, next_prop, next_target)
                        
            #If value has no attributes, then is a final value, if it is observable by pickle, go on, otherwise give err value
            else:
                fail = False
                try:
                    _ = cloudpickle.dumps(target, protocol = cloudpickle.DEFAULT_PROTOCOL)
                except:
                    fail = True
                
                if(fail):
                    retVal = 'PICKLE-SKIP-VALUE-UNREADABLE'
                else:
                    retVal = target
        return retVal
            
        
    
    def Update(self)->ContainerObject:
        #Start from iteration 0
        retVal = self._recursive_trial_and_error(self.target, 0) 
        return retVal

