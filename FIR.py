import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import math


def passe_bas(N, mc):
    K = (2*mc) + 1
    h_0_ = K/N
    h_n_ = np.array([ math.sin( math.pi*n*K/N )/math.sin( math.pi*n/N )for n in range(1, N) ]) * 1/N
    h_n_ = np.insert( h_n_, 0, h_0_)
    return h_n_

def coupe_bande():
    pass
