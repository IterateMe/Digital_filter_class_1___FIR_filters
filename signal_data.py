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

    def extract_main_sin(self, amp_diff):
        print("Extracting main sin for {} . . .".format(self.name))
        # amp_diff est la valeur de discrimination permettant de sélectionner les sinusoïdes ayant les plus forts maximums locaux

        N = (self.fft_win[1] - self.fft_win[0])
        ref_freq = self.time_x[0:N // 2] * self.datarate / N
        main_sin_index  = [] # Contient la valeur de la m ieme frequence dans l'analyse de fourier
        main_sin_freq   = [] # Contient les valeurs de fréquences réelles
        main_sin_amp    = [] # Contient les valeurs d'amplitude correspondantes
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
        print("Generating enveloppe . . .")
        freq_redressed = abs(self.time_y)
        x, filtre, f = FIR.averager(884, self.datarate+1)
        enveloppe = np.convolve(filtre, freq_redressed)
        enveloppe = enveloppe[0:-self.datarate + 1]

        self.enveloppe = enveloppe * 2

    def nettoyer_signal(self):
        repeat = 5
        filtre = FIR.coupe_bande(6000)
        signal = self.time_y
        original_length = len(signal)
        for i in range(repeat):
            signal = np.convolve(signal, filtre)
        self.time_y = signal[0:original_length]

    def synthetize_signal(self, factor):

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
        length = min(len(synth_signal), len(self.enveloppe))     #afin d'éviter les problèmes d'array incompatibles
        synth_signal = np.multiply(synth_signal[0:length], self.enveloppe[0:length])
        return synth_signal / biggest

    def generate_single_note_wave_file(self, note):
        # generate wav file
        print("\n\nGenerating WAV file . . .\n\n")
        print("Generation de {}".format(note))
        wf.write("..\\{}_{}.wav".format(self.name, note), 44100, np.int16(self.notes_dict[note]))

    def generate_bethoven(self, guit=False):
        start = 20000
        end = 44100 + start
        if guit:
            start = 8000
            end = 44100 + start

        Sol = self.notes_dict["Sol"][start:end]
        MiB = self.notes_dict["ReD"][start:end]
        Fa  = self.notes_dict["Fa"][start:end]
        Re  = self.notes_dict["Re"][start:end]
        silence = np.array([0 for i in range(end-start)])

        result = np.concatenate( (Sol, Sol) )
        result = np.concatenate((result, Sol))
        result = np.concatenate((result, MiB))
        result = np.concatenate((result, silence))
        result = np.concatenate((result, Fa))
        result = np.concatenate((result, Fa))
        result = np.concatenate((result, Fa))
        result = np.concatenate((result, Re))

        wf.write("..\\Beth.wav", 44100, np.int16(result))
        print("Bethoven generated\n")

    def generate_all_notes(self):
        print("\n\nGenerating notes . . .")
        notes = {}
        nom = ["Do", "DoD", "Re", "ReD", "Mi", "Fa", "FaD", "Sol", "SolD", "La", "LaD", "Si"]
        facteur = [2**(k/12) for k in range(-9, 2+1)]
        for i in range(len(nom)):
            print("Synthetising {}".format(nom[i]))
            notes[nom[i]] = self.synthetize_signal(facteur[i])
        self.notes_dict = notes

    def generate_Do_in_wav_for_validation(self, filename):  # faster than generating all notes
        facteur = 2**(-9/12)
        print("\nSynthetising {} (Validation). . .".format("Do"))
        signal = self.synthetize_signal(facteur)
        print("Generating WAV file . . .")
        wf.write("..\\{}.wav".format(filename), 44100, np.int16(signal))
        print("WAV file generated\n")

        matplotlib.use('TkAgg')
        plt.plot(signal)
        plt.show()

        # print("Generating Bethoven . . .\n")
        # offset = np.array([0 for i in range(11025)])
        # note1 = signal
        # note2 = np.concatenate((np.array([0 for i in range(11025*1)]), signal))
        # note3 = np.concatenate((np.array([0 for i in range(11025*2)]), signal))
        # note4 = np.concatenate((np.array([0 for i in range(11025*3)]), signal))
        # signal_length = len(note4)
        # note1 = np.concatenate( ( note1, np.array( [0 for i in range(signal_length-len(note1))] ) ) )
        # note2 = np.concatenate( ( note2, np.array( [0 for i in range(signal_length-len(note2))] ) ) )
        # note3 = np.concatenate( ( note3, np.array( [0 for i in range(signal_length-len(note3))] ) ) )
        # note4 = np.concatenate( ( note4, np.array( [0 for i in range(signal_length-len(note4))] ) ) )
        #
        #
        # result = np.add(note1,note2)
        # result = np.add(result,note3)
        # result = np.add(result,note4)
        # result = result / 4
        #
        # wf.write("..\\Beth.wav".format(filename), 44100, np.int16(result))
        # print("Bethoven generated\n")


    def show_freq_amp(self):
        title = "{} : Transformée de fourier du La dièze".format(self.name)
        x_label_time = "Temps (s)"
        y_label_time = "Amplitude"
        x_label_freq = "Freq (Hz)"
        y_label_freq = "Amplitude (Db)"

        N = len(self.freqDb)

        freq_array = np.array([i*self.datarate/N for i in range(N//2)])
        time_array = np.array([i/self.datarate for i in range(len(self.time_y))])

        fig, axs = plt.subplots(2)
        axs[0].plot(time_array, self.time_y)
        axs[0].set_xlabel(x_label_time)
        axs[0].set_ylabel(y_label_time)
        axs[1].stem(freq_array, self.freqDb[0:N//2])
        axs[1].set_xlabel(x_label_freq)
        axs[1].set_ylabel(y_label_freq)

        fig.suptitle(title)
        plt.show()

    def show_freq_angle(self):
        title = "{} : Déphasage du La dièze".format(self.name)
        vis.show(title,
                 self.time_x, "Temps (s)",
                 self.time_y, "Amplitude",
                 self.time_x, "m",
                 np.angle(self.freq), "Déphasage (rad)")

    def show_enveloppe_temp(self):
        vis.show("{} : Enveloppe du La dièze".format(self.name),
                 np.array([i for i in range(len(self.enveloppe))]) / self.datarate, "Temps (s)",
                 self.enveloppe, "Amplitude",
                 self.time_x / self.datarate, "Temps (s)",
                 self.time_y, "Amplitude")
