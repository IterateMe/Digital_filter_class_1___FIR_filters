from signal_data import Signal_data as SD

SOURCE_FILE = "signals\\note_basson_plus_sinus_1000_Hz.wav"


if __name__ == '__main__':
    print("Starting program . . .")
    LaD = SD("LaD", SOURCE_FILE, (47545, 49823))
    #LaD.show_freq_amp()
    LaD.show_enveloppe_temp()

