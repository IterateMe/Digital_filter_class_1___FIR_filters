import numpy as np
import math
from scipy import signal
from scipy.io import wavfile as wf
import visualise as vis
import FIR

class Signal_data():
    def __init__(self, name, source_file, inspect):
        print("Generating basic data for {} . . .".format(name))
        # Definir le nom du signal
        self.name = name

        # Importer les donnees du fichier .wav et en faire un array numpy
        self.wav = wf.read(source_file)
        self.datarate = self.wav[0]
        self.time_y = np.array(self.wav[1], dtype=float)
        self.time_x = np.array([i for i in range(len(self.time_y))])  # Index des valeurs du fichier

        # Creer les array necessaires au traitement de signal
        self.freq = None
        self.freqDb = None
        self.freq_norm = np.array([2*math.pi*i/self.datarate for i in range(self.datarate)])
        self.main_sin = None

        if inspect is True:
            self.generate_fft(0,len(self.time_x))
            self.show_freq_amp()


    def generate_fft(self, start, end):
        print ("Generating fft for {} . . .".format(self.name))
        self.freq = np.fft.fft(self.time_y[start:end])
        self.freqDb = np.log10(np.abs(self.freq)) * 20

    def extract_main_sin(self, amp_diff):
        print("Extracting main sin for {} . . .".format(self.name))
        if self.freq == None:
            print("fft must be defined in order to extract main sin")
        N = (self.fft_win[1] - self.fft_win[0])
        ref_freq = self.time_x[0:N // 2] * self.datarate / N
        main_sin_index = []
        main_sin_freq = []
        main_sin_amp = []
        for i in range(1, len(self.freqDb)//2 - 1):
            if (self.freqDb[i] > self.freqDb[i-1] + amp_diff) and ( self.freqDb[i] > self.freqDb[i+1] + amp_diff ):
                main_sin_index.append(i)
                main_sin_freq.append(ref_freq[i])
                main_sin_amp.append(self.freqDb[i])
        print("\n{} sin have been extracted for {}:".format(len(main_sin_amp), self.name))
        print("\t\tFREQ\t\t:\t\tAMP")
        for i in range(len(main_sin_freq)):
            print("\t{} : {}".format(main_sin_freq[i], main_sin_amp[i]))

        self.main_sin = (main_sin_index, main_sin_amp)


    def show_freq_amp(self):
        title = "Transformée de fourier du signal {}".format(self.name)
        N = len(self.time_x)
        vis.show(title,
                 self.time_x, "Temps (s)",
                 self.time_y, "Amplitude",
                 self.time_x[0:N // 2] * self.datarate / N, "Freq (Hz)",
                 np.abs(self.freqDb[0:N//2]), "Amplitude") # N'affiche que la première moitiée car la deuxième n'est qu'un reflet de la première

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
        freq_redressed = abs(self.time_y)
        filtre = FIR.passe_bas(self.datarate, 22)
        # filtre = np.log10(filtre) * 20
        #
        # vis.show("Filtre pour enveloppe du {}".format(self.name),
        #          np.array([i for i in range(len(filtre))]), "Temps (s)",
        #          filtre, "Amplitude")

        enveloppe = np.convolve( filtre, freq_redressed)
        vis.show("Enveloppe du signal {}".format(self.name),
                 np.array([i for i in range(len(enveloppe))]), "Temps (s)",
                 enveloppe, "Amplitude",
                 self.time_x, "Temps (s)",
                 self.time_y, "Amplitude")
