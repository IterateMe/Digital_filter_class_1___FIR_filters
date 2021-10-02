import numpy as np
import math
from scipy import signal
from scipy.io import wavfile as wf
import visualise as vis

class Signal_data():
    def __init__(self, name, source_file):
        print("Generating all the data for {}".format(name))
        self.name = name

        self.wav = wf.read(source_file)
        self.datarate = self.wav[0]
        self.time_y = np.array(self.wav[1], dtype=float)
        print("Data Rate = {}".format(self.datarate))

        self.x = np.array([i for i in range(len(self.time_y))])

        self.freq = np.fft.fft(self.time_y)
        self.freqDb = np.log10(np.fft.fft(self.time_y))*20
        print(self.freqDb)
        self.freq_norm = np.array([2*math.pi*i/len(self.time_y) for i in range(len(self.time_y))])
        self.freq_redressed = np.abs(self.time_y)


    def show_freq_amp(self):
        title = "Transformée de fourier du signal {}".format(self.name)

        vis.show(title,
                 self.x, "Temps (s)",
                 self.time_y, "Amplitude",
                 self.x[0:len(self.x)//2], "m",
                 np.abs(self.freqDb[0:len(self.x)//2]), "Freq (rad)")

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
        vis.show("Enveloppe du signal {}".format(self.name),
                 self.x, "Temps (s)",
                 self.freq_norm, "Amplitude")



