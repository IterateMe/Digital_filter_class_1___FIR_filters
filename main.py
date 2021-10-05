from signal_data import Signal_data as SD
import numpy as np
from scipy.io import wavfile as wf

source_guit = "signals\\note_guitare_LAd.wav"
source_basson = "signals\\note_basson_plus_sinus_1000_Hz.wav"


if __name__ == '__main__':
    print("Starting program . . .\n")
    #guit = SD("LaD a la Guitare", source_guit)
    #guit.generate_fft(8481, 8860)
    #guit.show_synth_signal()
    #guit.generate_notes()
    #guit.generate_wave_file()
    #guit.show_freq_amp()
    #guit.show_enveloppe_temp()

    basson = SD("Basson", source_basson)
    basson.nettoyer_signal()
    wf.write("{}.wav".format("Basson"), 44100, np.int16(basson.time_y))
    print("fichier généré")

