import numpy as np
import math
from scipy import signal
from scipy.io import wavfile as wf
import visualise as vis
import FIR

class Signal_data():
    def __init__(self, name, source_file, fft_window):
        print("Generating all the data for {} . . .".format(name))

        self.fft_win = fft_window
        # Definir le nom du signal
        self.name = name

        # Importer les donnees du fichier .wav et en faire un array numpy
        self.wav = wf.read(source_file)
        self.datarate = self.wav[0]
        self.time_y = np.array(self.wav[1], dtype=float)

        #
        self.x = np.array([i for i in range(len(self.time_y))]) # Index des valeurs du fichier
        self.freq = np.fft.fft(self.time_y[fft_window[0]:fft_window[1]])
        self.freqDb = np.log10(self.freq)*20
        self.freq_norm = np.array([2*math.pi*i/len(self.time_y) for i in range(len(self.time_y))])


    def show_freq_amp(self):
        title = "Transformée de fourier du signal {}".format(self.name)
        N = (self.fft_win[1] - self.fft_win[0])
        vis.show(title,
                 self.x, "Temps (s)",
                 self.time_y, "Amplitude",
                 self.x[0:N//2]*self.datarate/N, "Freq (Hz)",
                 np.abs(self.freqDb[0:N//2]), "Amplitude") # N'affiche que la première moitiée car la deuxième n'est qu'un reflet de la première

    def show_freq_angle(self):
        title = "Déphasage du signal {}".format(self.name)
        vis.show(title,
                 self.x, "Temps (s)",
                 self.time_y, "Amplitude",
                 self.x, "m",
                 np.angle(self.freq), "Déphasage (rad)")

    def show_freq_normalized(self):
        vis.show("Valeurs de la fréquence normalisée de {} en fonction de son index".format(self.name),
                 self.x, "Index",
                 self.freq_norm, "Valeur (rad)")

    def show_enveloppe_temp(self):
        freq_redressed = abs(self.time_y)
        filtre = FIR.passe_bas(20000, 10)

        vis.show("Enveloppe du signal {}".format(self.name),
                 np.array([i for i in range(len(filtre))]), "Temps (s)",
                 filtre, "Amplitude")

        enveloppe = np.convolve( filtre, freq_redressed)
        vis.show("Enveloppe du signal {}".format(self.name),
                 np.array([i for i in range(len(enveloppe))]), "Temps (s)",
                 enveloppe, "Amplitude",
                 self.x, "Temps (s)",
                 self.time_y, "Amplitude")
