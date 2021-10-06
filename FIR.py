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
    # to_plot = np.log10(np.abs(f))*20
    #
    # fig, axs = plt.subplots(2)
    # axs[0].plot(to_plot[0:22050])
    # axs[0].set_xlabel("Fréquence (Hz)")
    # axs[0].set_ylabel("Amplitude (Db)")
    #
    # axs[1].plot(np.array([20,21,22,23,24,25]),to_plot[20:26])
    # axs[1].set_xlabel("Fréquence (Hz)")
    # axs[1].set_ylabel("Amplitude (Db)")
    #
    # fig.suptitle("Réponse fréquencielle du filtre passe bas moyenneur")
    # plt.show()

    filtre = coupe_bande(6000)
    #fig, axs = plt.subplots(2)

    time_x = np.array([i/44.1 for i in range(6000)])
    plt.plot(time_x, filtre)
    plt.xlabel("Temps (ms)")
    plt.ylabel("Amplitude")
    plt.title("Réponse temporelle du filtre pour Fe de 44100 Hz")

    # start = 110
    # stop = 160
    # x_values = np.array([i + start + 1 for i in range(stop-start)])
    # to_plot_1 = 20*np.log10(np.abs(np.fft.fft(filtre)))
    # to_plot_2 = np.angle(np.fft.fft(filtre))
    #
    # axs[0].plot(x_values, to_plot_1[start:stop])
    # axs[0].set_xlabel("Index m")
    # axs[0].set_ylabel("Amplitude (Db)")
    # axs[1].plot(x_values, to_plot_2[start:stop])
    # axs[1].set_xlabel("Index m")
    # axs[1].set_ylabel("Dephasage (rad)")
    #
    # fig.suptitle("Réponse du filtre coupe bande")
    plt.show()