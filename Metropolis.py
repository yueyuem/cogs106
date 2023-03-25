#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 06:32:09 2023

@author: uumin
"""
import scipy.stats
import math
import random
import numpy as np
from SignalDetection import SignalDetection
class Metropolis:
    
    
    def __init__(self,logTarget: callable, initialState : int):
        
        self.logTarget = logTarget
        self.initialState = initialState
        self.currentState = initialState
        self.samples = []
       
        
    def __str__(self):
        return f'current state: {self.currentState}'
        
    def r_rate(self, proposal):
        p_current = max(1e-15, self.logTarget(self.currentState))
        log_p_current = np.log(p_current)
        p_proposal = max(1e-15, self.logTarget(proposal))
        log_p_proposal = np.log(p_proposal)
        #p_proposal = self.logTarget(proposal)
        #log_p_proposal = np.log(p_proposal)
        
        log_p_acceptance = min(0, log_p_proposal - log_p_current)
 
        return log_p_acceptance
        
    def _accept(self, proposal : int):
        
        p_acceptance = self.r_rate(proposal)
        
        if random.uniform(0, 1) < math.exp(p_acceptance):
            self.currentState = proposal
            self.samples.append(proposal)
            return True
        else:
            return False

    def adapt(self, blockLengths : list) : 
        block_n = len(blockLengths)
        r_target = 0.4
        stepSize = 1
        accept_num = 0
        total_num = 0
        
        for i in range(block_n):
            
            for j in range(blockLengths[i]):
                proposal = np.random.normal(self.currentState, stepSize)
                total_num += 1
                p_acceptance = self.r_rate(proposal)
                if random.uniform(0, 1) < math.exp(p_acceptance):
                    accept_num +=1
                
                accept_rate = accept_num / total_num
                
                stepSize = stepSize * math.pow(( accept_rate / r_target), 1.1)
            
        
        self.stepSize = stepSize 
        return self
    
    def sample(self, nSamples: int):
        for i in range(nSamples):
            proposal = np.random.normal(self.currentState, self.stepSize)
            self._accept(proposal)
        
        return self
    
    def summary(self):
        result = dict()
        result['mean'] =  np.mean(self.samples)
        result['c025'] = np.percentile(self.samples, 2.5)
        result['c975'] = np.percentile(self.samples, 97.5)
        print(result)
        return result
