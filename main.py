from signal_data import Signal_data as SD
import numpy as np
source_guit = "signals\\note_guitare_LAd.wav"
source_basson = "signals\\note_basson_plus_sinus_1000_Hz.wav"


if __name__ == '__main__':
    print("Starting program . . .\n")
    #guit = SD("LaD a la Guitare", source_guit, (8481, 8860), 5)
    #guit.show_freq_amp()
    #guit.show_enveloppe_temp()
    basson = SD("Basson", source_basson, True)

