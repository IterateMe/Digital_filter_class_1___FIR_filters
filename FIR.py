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

def coupe_bande(p):
    fe = 44100
    fc0 = 1000
    fc1 = 40

    mc = fc1 / fe * p
    k = mc * 2 + 1

    omega0 = 2 * math.pi * fc0 / fe

    dirac = [ 1 if n == 0 else 0 for n in range(-p//2, p//2) ]
    hlp = [ k/p if n == 0 else (1 / p) * (math.sin(math.pi * n * k / p)) / (math.sin(math.pi * n / p)) for n in range(-p//2, p//2) ]
    hbs = [ dirac[n] - 2 * hlp[n] * math.cos(n * omega0) for n in range(-p//2, p//2) ]

    return hbs

if __name__ == '__main__':
    matplotlib.use('TkAgg')
    # x,y,f = averager(882, 44100)
    # plt.plot(np.log10(np.abs(f))*20)
    # plt.show()

    filtre = coupe_bande(6000)
    plt.plot(20*np.log10(np.abs(np.fft.fft(filtre))))
    plt.show()