import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy import signal

from multipledispatch import dispatch

matplotlib.use('TkAgg')

@dispatch(str, np.ndarray, str, np.ndarray, str)
def show(title,
         x_array, x_label,
         y_array, y_label):
    plt.plot(x_array, y_array)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

@dispatch(str, np.ndarray, str, np.ndarray, str, np.ndarray, str)
def show(title,
         x_array, x_label,
         y_array, y_label,
         y_array2, y_label2):
    fig, axs = plt.subplots(2)

    axs[0].stem(x_array, y_array)
    axs[0].set_xlabel(x_label)
    axs[0].set_ylabel(y_label)

    axs[1].stem(x_array, y_array2)
    axs[1].set_xlabel(x_label)
    axs[1].set_ylabel(y_label2)

    fig.suptitle(title)
    plt.show()

@dispatch(str, np.ndarray, str, np.ndarray, str, np.ndarray, str, np.ndarray, str)
def show(title,
         x_array, x_label,
         y_array, y_label,
         x_array2, x_label2,
         y_array2, y_label2):
    fig, axs = plt.subplots(2)

    axs[0].stem(x_array, y_array)
    axs[0].set_xlabel(x_label)
    axs[0].set_ylabel(y_label)
    axs[1].stem(x_array2, y_array2)
    axs[1].set_xlabel(x_label2)
    axs[1].set_ylabel(y_label2)

    fig.suptitle(title)
    plt.show()
