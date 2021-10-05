import numpy as np
import math
from scipy import signal
from scipy.io import wavfile as wf
import matplotlib.pyplot as plt
import matplotlib
import visualise as vis
import FIR

class Signal_data():
    def __init__(self, name, source_file):
        print("Generating basic data for {} . . .".format(name))
        # Definir le nom du signal
        self.name = name


        # Importer les donnees du fichier .wav et en faire un array numpy
        self.wav = wf.read(source_file)
        self.datarate = self.wav[0]
        self.time_y = np.array(self.wav[1], dtype=float)
        self.time_x = np.array([i for i in range(len(self.time_y))])  # Index des valeurs du fichier

        # Creer les array necessaires au traitement de signal
        self.fft_win = None     #Fenetre du signal temporel analyser pour generer la fft
        self.freq = None        #will contain imaginary part
        self.angle = None
        self.freqDb = None
        self.freq_norm = np.array([2*math.pi*i/self.datarate for i in range(self.datarate)])
        self.enveloppe = None
        self.main_sin = None

        self.notes_dict = None


    def generate_fft(self, start, end):
        print ("Generating fft for {} . . .".format(self.name))
        self.fft_win = (start, end)
        self.freq = np.fft.fft(self.time_y[start:end])
        self.angle = np.angle(self.freq)
        self.freqDb = np.log10(np.abs(self.freq)) * 20

        self.extract_main_sin(5)
        self.generate_enveloppe()

    def extract_main_sin(self, amp_diff):
        print("Extracting main sin for {} . . .".format(self.name))

        N = (self.fft_win[1] - self.fft_win[0])
        ref_freq = self.time_x[0:N // 2] * self.datarate / N
        main_sin_index  = []
        main_sin_freq   = []
        main_sin_amp    = []
        for i in range(1, len(self.freqDb)//2 - 1):
            if (self.freqDb[i] > self.freqDb[i-1] + amp_diff) and ( self.freqDb[i] > self.freqDb[i+1] + amp_diff ):
                main_sin_index.append(i)
                main_sin_freq.append(ref_freq[i])
                main_sin_amp.append(self.freqDb[i])
        print("\n{} sin have been extracted for {}:".format(len(main_sin_amp), self.name))
        print("\t\tFREQ (Hz)\t:\tAMP (Db)")
        for i in range(len(main_sin_freq)):
            print("\t{} : {}".format(main_sin_freq[i], main_sin_amp[i]))

        self.main_sin = (main_sin_index, main_sin_freq, main_sin_amp)

    def generate_enveloppe(self):
        print("Generating enveloppe")
        freq_redressed = abs(self.time_y)
        x, filtre, f = FIR.averager(882, 44100)
        enveloppe = np.convolve(filtre, freq_redressed)
        enveloppe = enveloppe[0:-self.datarate + 1]

        self.enveloppe = enveloppe * 2

    def nettoyer_signal(self):
        repeat = 5
        filtre = FIR.coupe_bande(6000)
        signal = self.time_y
        for i in range(repeat):
            signal = np.convolve(signal, filtre)
        self.time_y = signal

    def synthetize_signal(self, factor):
        # generate the sin wave for the duration of the original sample
        # print("enveloppe: ", self.enveloppe)
        #
        # print("Enveloppe : {}".format(len(self.enveloppe)))
        # print("time_x: {}".format(len(self.time_x)))
        # print("diff = {}".format( len(self.enveloppe) - len(self.time_x)))

        synth_signal = [0 for i in self.time_x]
        for n in self.time_x:
            for i in range(len(self.main_sin[0])):
                amp = np.abs(self.freq[self.main_sin[0][i]])
                t = n/self.datarate
                f = (self.main_sin[1][i])*factor
                dephasage = np.angle(self.freq[self.main_sin[0][i]])
                synth_signal[n] += amp * math.sin(2*math.pi*t*f + dephasage)

        # normaliser l amplitude sur une valeur max de 1
        biggest = max(synth_signal)

        # multiply by the values of the enveloppe
        print("Multiply with enveloppe . . .")
        synth_signal = np.multiply(synth_signal, self.enveloppe)
        return synth_signal / biggest

    def generate_wave_file(self):
        # generate wav file
        print("\n\nGenerating WAV file . . .\n\n")
        for note in self.notes_dict.keys():
            print("Generation de {}".format(note))
            wf.write("{}.wav".format(note), 44100, np.int16(self.notes_dict[note]))

    def generate_notes(self):
        print("\n\nGenerating notes . . .")
        notes = {}
        nom = ["Do", "DoD", "Re", "ReD", "Mi", "Fa", "FaD", "Sol", "SolD", "La", "LaD", "Si"]
        facteur = [2**(k/12) for k in range(-9, 2+1)]
        for i in range(len(nom)):
            print("Synthetising {}".format(nom[i]))
            notes[nom[i]] = self.synthetize_signal(facteur[i])
        self.notes_dict = notes


    def show_synth_signal(self):
        plt.plot(self.synth_signal_source)
        plt.show()

    def show_freq_amp(self):
        title = "Transformée de fourier du signal {}".format(self.name)
        x_label_time = "Temps (s)"
        y_label_time = "Amplitude"
        x_label_freq = "Freq (Hz)"
        y_label_freq = "Amplitude (Db)"

        N = len(self.freqDb)

        freq_array = np.array([i*self.datarate/N for i in range(N//2)])

        fig, axs = plt.subplots(2)
        axs[0].stem(self.time_y)
        axs[0].set_xlabel(x_label_time)
        axs[0].set_ylabel(y_label_time)
        axs[1].stem(freq_array, self.freqDb[0:N//2])
        axs[1].set_xlabel(x_label_freq)
        axs[1].set_ylabel(y_label_freq)

        fig.suptitle(title)
        plt.show()

    def show_freq_angle(self):
        title = "Déphasage du signal {}".format(self.name)
        vis.show(title,
                 self.time_x, "Temps (s)",
                 self.time_y, "Amplitude",
                 self.time_x, "m",
                 np.angle(self.freq), "Déphasage (rad)")

    def show_freq_normalized(self):
        vis.show("Valeurs de la fréquence normalisée de {} en fonction de son index".format(self.name),
                 self.time_x, "Index",
                 self.freq_norm, "Valeur (rad)")

    def show_enveloppe_temp(self):

        vis.show("Enveloppe du signal {}".format(self.name),
                 np.array([i for i in range(len(self.enveloppe))]), "Temps (s)",
                 self.enveloppe, "Amplitude",
                 self.time_x, "Temps (s)",
                 self.time_y, "Amplitude")
