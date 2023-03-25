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

        log_p_current = np.log(self.logTarget(self.currentState))
        
        log_p_proposal = np.log(self.logTarget(proposal))
        #p_proposal = self.logTarget(proposal)
        #log_p_proposal = np.log(p_proposal)
        
        log_p_acceptance = min(0, np.log(log_p_proposal )- np.log(log_p_current))
 
        return log_p_acceptance
    
        
    def _accept(self, proposal : int):
        
        p_acceptance = self.r_rate(proposal)
        
        if random.uniform(0, 1) < math.exp(p_acceptance):
            self.currentState = proposal
            self.samples.append(proposal)
            return True
        else:
            return False

    def adapt1(self, blockLengths : list) : 
        block_n = len(blockLengths)
        r_target = 0.4
        stepSize = 1
        accept_num = 0
        total_num = 0
        
        for i in range(block_n):
            block_acceptance = []
            for j in range(blockLengths[i]):
                proposal = np.random.normal(self.currentState, stepSize)
                print('proposal', proposal)
                total_num += 1
                p_acceptance = self.r_rate(proposal)
                if random.uniform(0, 1) < math.exp(p_acceptance):
                    accept_num +=1
                    
                    accept_rate = accept_num / total_num
                    print("accept! ",accept_num )
                    print('acceptrate rate: ', accept_rate)
                    stepSize = stepSize * (( accept_rate / r_target)** 1.1)
                else:
                    print('not accept here')
                print(stepSize)
                break
        
        self.stepSize = stepSize 
        return self
    def adapt(self, blockLengths):
        """
        Performs the adaptation phase of the Metropolis algorithm to adjust the step size.
    
        Parameters:
            blockLengths (list): A list of integers specifying the number of iterations in each adaptation block.
    
        Returns:
            self: The Metropolis object with the updated step size.
        """
        kblocks = len(blockLengths)
        target_rate = 0.4
        step_size = 1
        x = 0
        
        TEST = False
        for i in range(kblocks):
            step_size_k = []
            accept_count = 0
            proposal_count = 0
            for j in range(blockLengths[i]):
              
                x+=1
                proposal = np.random.normal(self.currentState, step_size)
                p_acceptance = self.r_rate(proposal)
                u = random.uniform(0, 1)
                if u < math.exp(p_acceptance):
                    self.currentState = proposal
                    accept_count += 1
                    print("accept! ",accept_count )
                proposal_count += 1
                
                    
                acceptance_rate = accept_count / proposal_count
                step_size = step_size * np.power((acceptance_rate / target_rate), 1.1)
                step_size_k.append(step_size)
                if TEST and x < 10:

                    print('p acceptance: ', math.exp(p_acceptance))
                    print('step_size: ', step_size)
                    print('proposal: ', proposal)
                    print('acceptance rate: ', acceptance_rate)
                    print()
                elif TEST:
                    break
                else:
                    pass
            
        self.stepSize = np.mean(step_size_k)
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
