from signal_data import Signal_data as SD
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile as wf

source_guit = "signals\\note_guitare_LAd.wav"
source_basson = "signals\\note_basson_plus_sinus_1000_Hz.wav"
source_sin = "signals\\sin_1000Hz.wav"

def basson():
    start = 0
    end =  44100*3
    diff = end - start
    print(diff)
    basson = SD("Basson", source_basson)
    basson.generate_fft(start, end)
    phase_avant = basson.angle
    Db_avant = basson.freqDb

    basson.nettoyer_signal()
    basson.generate_fft(start, end)
    phase_apres = basson.angle
    Db_apres = basson.freqDb

    x_values = np.array( [ i * (44100/diff) for i in range(diff//20) ] )

    fig, axs = plt.subplots(2)
    axs[0].plot(x_values, Db_avant[0:diff//20])
    axs[0].set_xlabel("Fréquence (Hz)")
    axs[0].set_ylabel("Amplitude (Db)")

    axs[1].plot(x_values, Db_apres[0:diff//20])
    axs[1].set_xlabel("Fréquence (Hz)")
    axs[1].set_ylabel("Amplitude (Db)")

    fig.suptitle("Réponse fréquencielle avant et après le filtrage du basson")
    plt.show()

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
    # wf.write("..\\{}.wav".format("Thats the good stuff"), 44100, np.int16(basson.time_y))
    # print("fichier généré")

def guit():
    guit = SD("Guitarre", source_guit)
    ##guit.generate_enveloppe()
    # guit.show_enveloppe_temp()

    guit.generate_fft(8481, 8860)
    guit. show_freq_amp()

    # guit.extract_main_sin(5)
    # guit.generate_LaD_in_wav_for_validation("Guit test pour la validation")
    #
    # guit.generate_all_notes()
    # guit.generate_bethoven()

def sin():
    sin = SD("Sin 1000Hz", source_sin)
    temps_avant = sin.time_y
    initial_length = len(temps_avant)
    sin.generate_fft(0, 44100)
    fft_avant = sin.freqDb

    sin.nettoyer_signal()
    temps_apres = sin.time_y
    sin.generate_fft(0, 44100)
    fft_apres = sin.freqDb

    time_x = np.array([i / 44100 for i in range(initial_length)])

    fig, axs = plt.subplots(2)

    axs[0].plot(time_x, temps_avant)
    axs[0].set_xlabel("Temps (s)")
    axs[0].set_ylabel("Amplitude")

    axs[1].plot(time_x, temps_apres)
    axs[1].set_xlabel("Temps (s)")
    axs[1].set_ylabel("Amplitude")

    fig.suptitle("Spectre")
    plt.show()


if __name__ == '__main__':
    print("Starting program . . .\n")
    #basson()
    #$guit()
    #sin()

