import numpy as np
from scipy import signal

import visualise as plot

class time_to_fft():
    def __init__(self, name, time_array1):
        self.name = name
        self.x = [i for i in range(len(time_array1))]
        self.y = np.array(time_array1)

        self.freq_array1 = np.fft.fft(self.y)
        self.freq_array1_length = len(self.freq_array1)


    def show_freq_amp(self):
        title = "Transformée de fourier de {}".format(self.name)
        plot.show(title, self.x, "Temps (s)", self.y, "Y", self.x, "m", self.freq_array1, "Freq (rad)")

        pass

    def show_freq_angle(self):
        pass

    def show_freq_normalized(self):
        pass


