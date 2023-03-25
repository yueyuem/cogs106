import unittest
from scipy.stats import norm
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np
import random

class SignalDetection: 
    def __init__ (self, hits = 0, misses = 0, falseAlarms = 0, correctRejections = 0):
        self.hits = hits
        self.misses = misses 
        self.falseAlarms = falseAlarms
        self.correctRejections = correctRejections 
        
    def hitrate(self):
        
        return self.hits/(self.hits + self.misses)
    
    def farate(self):
        
        return self.falseAlarms/(self.falseAlarms+self.correctRejections)
    
    def d_prime(self):
        
        return norm.ppf(self.hitrate()) - norm.ppf(self.farate())
    
    def criterion(self):
        
        return  -0.5 * (norm.ppf(self.hitrate()) + norm.ppf(self.farate()))
    
    def __str__(self):
        return f'Signal Detection:\n hits : {self.hits} \n misses : {self.misses}\n falsealarm: {self.falseAlarms}\n cr: {self.correctRejections}'
    
    # overload + and *
    def __add__(self, o):
        hits = self.hits + o.hits
        misses = self.misses + o.misses
        falseAlarms = self.falseAlarms + o.falseAlarms
        correctRejections = self.correctRejections + o.correctRejections
        return SignalDetection(hits, misses, falseAlarms, correctRejections)

    def __mul__(self, o):
        hits = self.hits * o
        misses = self.misses * o
        falseAlarms = self.falseAlarms * o
        correctRejections = self.correctRejections * o
        return SignalDetection(hits, misses, falseAlarms, correctRejections)

    # generates a plot of the Receiver Operating Characteristic (ROC) 
    # for one hit rate and false alarm rate
    @staticmethod
    def plot_roc1(*signals):
        for signal in signals[0]:
            #print('signal', signal)
            #print(type(signal))
            plt.plot(signal.farate(),signal.hitrate(),color = 'black', marker = 'o')
            
        plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--', label ="Chance Line")
        plt.xlabel('False Alarm Rate')
        plt.ylabel('Hit Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend()
        plt.show()
        return
    #a method that only plot a roc curve for a single SignalDetection
    def plot_roc_single(self):
        # Plot the ROC curve using matplotlib
        plt.plot([0, self.farate(), 1], [0, self.hitrate(), 1], color ='red', marker ='o', markersize = 10, label ='ROC')
        plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--', label ="Chance Line")
        plt.xlabel('False Alarm Rate')
        plt.ylabel('Hit Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend()
        plt.show()
        
    def plot_sdt(self):
        # Create response distribution arrays
        signal_mean = self.d_prime() / 2
        noise_mean = -self.d_prime() / 2
        response_std = 1
        self.signal_response = norm(signal_mean, response_std).pdf
        self.noise_response = norm(noise_mean, response_std).pdf
        
        fig, ax = plt.subplots()
        
        # Plot signal and noise response distributions
        x = np.linspace(-4, 4, num=1000)
        ax.plot(x, self.signal_response(x), label='Signal', linewidth=2)
        ax.plot(x, self.noise_response(x), label='Noise', linewidth=2)
        
        # Plot criterion line
        ax.axvline(self.criterion(), color='green', linestyle='--', linewidth=2)
        
        # Plot decision bound line dprime
        
        #ax.axhline(self.signal_response(signal_mean),xmin = -signal_mean,xmax =noise_mean  ,color='black', linestyle='--', linewidth=2)
        ax.plot([noise_mean, signal_mean], [self.signal_response(signal_mean), self.noise_response(noise_mean)], color='black', linestyle='--', linewidth=2)
        
        # Add labels and legend
        ax.set_xlabel('Response')
        ax.set_ylabel('Probability Density')
        ax.set_title('Signal Detection Theory Plot')
        ax.legend()
        
        
        # Show plot
        plt.show()

    """@staticmethod
    def simulate1(dprime, criteriaList, signalCount, noiseCount):
        sdtList = []
        k = len(criteriaList)
        for i in range(k):
            criteria = criteriaList[i]
            signal = random.sample(range(signalCount), signalCount)
            noise = random.sample(range(noiseCount), noiseCount)
            signalDist = norm(loc=dprime/2, scale=1)
            noiseDist = norm(loc=-dprime/2, scale=1)
            signalHits = sum(signalDist.pdf(signal) >= criteria)
            signalMisses = signalCount - signalHits
            noiseFalseAlarms = sum(noiseDist.pdf(signal) >= criteria)
            noiseCorrectRejections = noiseCount - noiseFalseAlarms
            #print(signalHits,signalMisses,noiseFalseAlarms,noiseCorrectRejections)
            sdt = SignalDetection(signalHits, signalMisses, noiseFalseAlarms, noiseCorrectRejections)
            sdtList.append(sdt)
            
        return sdtList"""
        
    
    @staticmethod
    def simulate(dprime, criteriaList, signalCount, noiseCount):
        sdtList = []
        for i in range(len(criteriaList)):
            k = criteriaList[i] + (dprime / 2)
            hr = 1 - norm.cdf(k - dprime)
            fa = 1 - norm.cdf(k)
            hits = np.random.binomial(signalCount, norm.cdf(dprime / 2 + criteriaList[i]))
            misses = signalCount - hits
            false_alarms = np.random.binomial(noiseCount, norm.cdf(dprime / 2 - criteriaList[i]))
            criteria = noiseCount - false_alarms
            #print(hits, misses, false_alarms, criteria)
            new_sig = SignalDetection(hits, misses, false_alarms, criteria)
            sdtList.append(new_sig)
        return sdtList
    
    
    def nLogLikelihood(self,hitRate, falseAlarmRate):
        h = self.hits
        m = self.misses
        f = self.falseAlarms
        r = self.correctRejections
        return -h * np.log(hitRate)-m*np.log(1-hitRate)-f*np.log(falseAlarmRate)-r*np.log(1-falseAlarmRate)
    
    
    @staticmethod
    #hitRate = rocCurve(falseAlarmRate, a)
    def rocCurve(falseAlarmRate, a):
        
        
        return norm.cdf(a + norm.ppf(falseAlarmRate))
    
    
    @staticmethod
    def plot_roc(sdtList):
        plt.figure()
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.xlabel("False Alarm Rate")
        plt.ylabel("Hit Rate")
        plt.title("Receiver Operating Characteristic Curve")
        if isinstance(sdtList, list):
            for i in range(len(sdtList)):
                sdt = sdtList[i]
                plt.plot(sdt.farate(), sdt.hitrate(), 'o', color='black')
        x, y = np.linspace(0, 1, 100), np.linspace(0, 1, 100)
        plt.plot(x, y, '--', color='black')
        plt.grid()
        
        
    @staticmethod
    def rocLoss(a, sdtList):
        l = 0
        for sdt in sdtList:
            fa = sdt.farate()
            pred_h = sdt.rocCurve(fa, a)
            
            l += sdt.nLogLikelihood(pred_h, fa)
        return l
       
    """ @staticmethod
    def fit_roc1(sdtList):
        ahat = 0
        #[hit rate, false alarm rate] pairs.
        hfa = [[sdt.hitrate(), sdt.farate()]for sdt in sdtList]
        fa_list = [ sdt.farate()for sdt in sdtList]
        a = 1
        result =minimize(SignalDetection.rocCurve, x0=[1,1,1], args= (falseAlarmRate, a))for fa in fa_list 
        a = result.x[0]
        # Generate the ROC curve with markers
        x = np.linspace(0, 1, 100)
        y = SignalDetection.rocCurve(x, a)
        plt.plot(x, y)
        for hit_rate, false_alarm_rate in hfa:
            plt.plot(false_alarm_rate, hit_rate, 'o')
        plt.xlabel('False alarm rate')
        plt.ylabel('Hit rate')
        plt.show()
        
       # minimize(self.rocCurve, x0)
        return """
    
    @staticmethod
    def fit_roc(sdtList):
        SignalDetection.plot_roc(sdtList)
        a = 1
        result =minimize(SignalDetection.rocLoss,x0 = 1.0, args= (sdtList,) ,method='BFGS')
        #print(result)
        aHat = result.x[0]
        """plot the predict hit rate curve"""
        loss = []
        for i in range(0, 100, 1):
            loss.append((SignalDetection.rocCurve(i / 100, float(aHat))))
        plt.plot(np.linspace(0, 1, 100), loss, '-', color='r')
        
        return float(aHat)

def main():
    
    dPrime       = 1.5
    criteriaList = [-0.5,0,0.5]
    signalCount  = 1000
    noiseCount   = 1000
    
    sdtList      = SignalDetection.simulate(dPrime, criteriaList, signalCount, noiseCount)
        
    test_sig = SignalDetection(375,625,350,650)
    #print(test_sig)
    #print(test_sig.criterion())
    
    list_signals = []
    for i in range(5):
        param = [random.randrange(1,20)  for j in range(4) ]
        print(param)
        new_sig = SignalDetection(param[0],param[1],param[2],param[3])
        list_signals.append(new_sig)
    SignalDetection.plot_roc(list_signals)
    #print(new_sig )
    
    SignalDetection.plot_roc(list_signals)
    
def testroccurve():
    dPrime  = 0
    sdtList = SignalDetection.simulate(dPrime, [0,1,-1,0.7,-0.8,0.5,0.1], 1e7, 1e7)
    aHat    = SignalDetection.fit_roc(sdtList)
    #print('ahat:',aHat)
    
if "__name__" == '__main__':
    main()
    
        
        
        

        
        
        
        
        
