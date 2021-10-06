from signal_data import Signal_data as SD
import numpy as np
from scipy.io import wavfile as wf

source_guit = "signals\\note_guitare_LAd.wav"
source_basson = "signals\\note_basson_plus_sinus_1000_Hz.wav"


def basson():
    basson = SD("Basson", source_basson)
    basson.nettoyer_signal()
    # basson.generate_enveloppe()
    # basson.show_enveloppe_temp()
    #
    # basson.generate_fft(47545, 49823)
    # basson.show_freq_amp()
    #
    # basson.extract_main_sin(2)
    # basson.generate_Do_in_wav_for_validation("Basson Test pour valid")
    #
    # basson.generate_all_notes()
    # basson.generate_bethoven()

    # Genere le fichier .wav du signal
    wf.write("..\\{}.wav".format("Thats the good stuff"), 44100, np.int16(basson.time_y))
    print("fichier généré")

def guit():
    guit = SD("Guitarre", source_guit)
    guit.generate_enveloppe()
    # guit.show_enveloppe_temp()

    guit.generate_fft(8481, 8860)
    # guit. show_freq_amp()

    guit.extract_main_sin(5)
    guit.generate_LaD_in_wav_for_validation("Guit test pour la validation")
    #
    # guit.generate_all_notes()
    # guit.generate_bethoven()


if __name__ == '__main__':
    print("Starting program . . .\n")
    basson()
    guit()


