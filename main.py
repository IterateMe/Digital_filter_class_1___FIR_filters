import numpy as np
from scipy import signal



from signal_data import Signal_data as SD

SOURCE_FILE = "signals\\note_basson_plus_sinus_1000_Hz.wav"



if __name__ == '__main__':
    LaD = SD("LaD", SOURCE_FILE)
    LaD.show_enveloppe_temp()
    pass
