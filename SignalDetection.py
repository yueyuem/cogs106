
import numpy as np
from scipy.stats import norm



class SignalDetection:
    
    def __init__(self, hits, misses, falaseAlarms, correctRejections):
        self.hits = hits
        self.misses = misses
        self.fa = falaseAlarms
        self.cr = correctRejections
        
        #calculating H-hit rate
        self.h_rate = self.hits / (self.hits + self.misses)
        
        #calculating FA false alarm rate
        self.f_rate = self.fa / (self.fa + self.cr)
        
    def get_hrate(self):
        return
        
    def d_prime(self):
        z_h = norm.ppf(self.h_rate)
        z_fa = norm.ppf(self.f_rate)
        d_p = z_h - z_fa
        return d_p
    
    def criterion(self):
        z_h = norm.ppf(self.h_rate)
        z_fa = norm.ppf(self.f_rate)
        #calculating base on C = -0.5 * (Z(H) + Z(FA))
        criterion = -0.5 * (z_h  + z_fa)
        
        return criterion
    
    def __add__(self, other):
        if isinstance(other, SignalDetection): 
            total_hits = self.hits + other.hits
            #print(total_hits)
            total_misses = self.misses + other.misses
            total_fa = self.fa + other.fa
            total_cr = self.cr + other.cr
            #print(total_hits,total_misses,total_fa,total_cr)
            new_signal = SignalDetection(total_hits,total_misses,total_fa,total_cr)
            return new_signal 
        else:
            raise TypeError("Only SignalDetection class is Allowed")

    
    def __mul__(self, other):
        if type(other) == int:
            new_signal = SignalDetection(self.hits * other ,self.misses  * other, self.fa * other, self.cr * other)
            return new_signal 
        else:
           raise TypeError('Only int are allowed')
    
    def __rmul__(self, other):
        if type(other) == int:
            new_signal = SignalDetection(self.hits * other ,self.misses  * other, self.fa * other, self.cr * other)
            return new_signal 
        else:
           raise TypeError('Only int are allowed')
    
    def plot_roc(self):
        return
    
    def plot_std(self):
        return
signal_a = SignalDetection(5,5,5,5)
signal_b = SignalDetection(6,10,5,5)
signal_c = 2 * signal_b 
print(signal_c.hits)
    
        
        
setter function
    
    

        

