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
        self.time_array = np.array(self.wav[1], dtype=float)
        self.datarate = self.wav[0]
        print("Data Rate = {}".format(self.datarate))

        self.x = np.array( [i for i in range(len(self.time_array))] )
        self.y = np.array(self.time_array)

        self.freq= np.fft.fft(self.y)
        self.freq_length = len(self.freq)

        self.freq_norm = np.array([i for i in range(0, 2, len(self.time_array))])
        self.freq_redressed = np.abs(self.time_array)


    def show_freq_amp(self):
        title = "Transformée de fourier de {}".format(self.name)
        vis.show(title,
                 self.x, "Temps (s)",
                 self.y, "Amplitude",
                 self.x, "m",
                 np.abs(self.freq), "Freq (rad)")

    def show_freq_angle(self):
        pass

    def show_freq_normalized(self):
        pass

    def show_enveloppe_temp(self):
        # vis.show("Signal redressé de {}".format(self.name),
        #          self.x, "Temps (s)",
        #          self.freq_redressed, "Amplitude")
        print(len(self.freq_redressed))
        print([i for i in range(0, 2, len(self.time_array))])


