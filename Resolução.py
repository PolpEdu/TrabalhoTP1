import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.io import wavfile
import math

data = np.random.randint(0, 10, size=20)


def criarhist(data, alfabeto):
    print("fjlsnka")
    # ocorrencias = [i.count for x in data for i in alfabeto]
    # print(ocorrencias)

    # for x in data:
    #    plt.xtics()
    #    plt.bar()
    # plt.show()


def lerficheiro(nome):
    ext = nome.split(".")[1]
    PATH = "./data/" + nome

    if ext == "txt":
        # Caracteres ASCII, existe 127 caracteres ASCII
        alfabeto = [x for x in range(0, 127 + 1)]
        with open(PATH, "r", encoding='ASCII') as f:
            data = f.read()

    elif ext == "bmp":
        # bmp os valores usados (preto a branco) vão de 0 a 255
        alfabeto = [x for x in range(0, 255 + 1)]
        datasquare = mpimg.imread(PATH) 
        data = datasquare.flatten()

    elif ext == "wav":

        [fs, info] = wavfile.read(PATH)

        # como o dtype é sempre int*BITS*
        # vou e tiro o numero de bits por cada amostra para conseguir o maior valor
        print(str(info.dtype).split("int")[1])
        max = math.pow(2, int(str(info.dtype).split("int")[1]))

        # Wav normalizado vai de 0 a max+1.
        alfabeto = [x for x in range(0, int(max + 1))]

        data = [fs, info]

    print(f"Alfabeto:{alfabeto}\n"
          f"Data:{data}")
    return alfabeto, data


# def entropia(data):


if __name__ == "__main__":
    [alfabeto, data] = lerficheiro("english.txt")
    criarhist(data, alfabeto)
