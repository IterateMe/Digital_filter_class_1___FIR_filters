import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def show(title, x_array, x_label, y_array, y_label):
    plt.plot(x_array, y_array)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

def show(title, x_array, x_label, y_array, y_label,  y_array2, y_label2):
    fig, axs = plt.subplots(2)

    axs[0].plot(x_array, y_array)
    axs[0].xlabel(x_label)
    axs[0].ylabel(y_label)

    axs[1].plot(x_array, y_array2)
    axs[1].xlabel(x_label)
    axs[1].ylabel(y_label2)

    fig.title(title)
    plt.show()




def show(title,
         x_array, x_label,
         y_array, y_label,
         x_array2, x_label2,
         y_array2, y_label2):
    print(title)
    print(x_array)
    fig, axs = plt.subplots(2)

    axs[0].plot(x_array, y_array)
    axs[0].xlabel(x_label)
    axs[0].ylabel(y_label)
    axs[1].plot(x_array2, y_array2)
    axs[1].xlabel(x_label2)
    axs[1].ylabel(y_label2)

    fig.title(title)
    plt.show()
