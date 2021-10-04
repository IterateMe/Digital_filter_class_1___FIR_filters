import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy import signal
import math

def averager(ones, k): #passe bas h(k) coeffficients egaux
    signal_x = np.array([i for i in range(k)])
    signal_y = np.array([1 if i<=ones else 0 for i in range(k)]) * (1/ones)
    signal_freq = np.fft.fft(signal_y)
    return signal_x, signal_y, signal_freq

def passe_bas(N, mc):
    K = (2*mc) + 1
    h_0_ = K/N
    h_n_ = np.array([ math.sin( math.pi*n*K/N )/math.sin( math.pi*n/N )for n in range(1, N) ]) * 1/N
    h_n_ = np.insert( h_n_, 0, h_0_)
    return h_n_

def coupe_bande():
    pass

if __name__ == '__main__':
    matplotlib.use('TkAgg')
    x,y,f = averager(882, 44100)
    plt.plot(np.log10(np.abs(f))*20)
    plt.show()