import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.io import wavfile as wf
from fourier import time_to_fft as T

SOURCE_FILE = "C:\\Users\\viann\Desktop\\note_guitare_LAd.wav"

a = wf.read(SOURCE_FILE)

audio_array = np.array(a[1], dtype=float)

if __name__ == '__main__':
    test = T("test", audio_array)
    test.show_freq_amp()
    pass
